import logging

from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response

from rating.models import Rating
from review.models import Review
from watched.models import Watched
from .serializers import WatchedDetailSerializers, WatchedSerializers

logger = logging.getLogger(__name__)
from activity.models import Activity

# Create your views here.

class WatchedViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Watched.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # serializer_class = WatchedDetailSerializers
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return WatchedDetailSerializers
        else:
            return WatchedSerializers

    def list(self, request, *args, **kwargs):
        try:
            query_set = Watched.objects.filter(user_id=request.user.id)
            movie = [WatchedDetailSerializers(watched).data['movie'] for watched in query_set]
            data = {
                "status": "success",
                "message": {
                    "id": request.user.id,
                    'watched': movie}
            }
            return super().list(request, *args, **kwargs)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    
    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        if Watched.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            watched = Watched.objects.create(movie_id=movie_id, user_id=request.user.id)
            Activity.objects.create(movie_id=movie_id,user_id=request.user.id,type=3)
            data = data = {
                "status": "success",
                "message": WatchedSerializers(watched).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            watched_obj = Watched.objects.get(user_id=request.user.id, movie_id=pk)
            try:
                rating_obj = Rating.objects.get(user_id=request.user.id, movie_id=pk)
                return Response({'error': "You can't not remove from watched because there is activity on it"},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Rating.DoesNotExist:
                try:
                    review_obj = Review.objects.get(user_id=request.user.id, movie_id=pk)
                    return Response({'error': "You can't not remove from watched because there is activity on it"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
                except Review.DoesNotExist:
                    watched_obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Watched.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
