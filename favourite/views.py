from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from favourite.models import Favourite
from rating.models import Rating
from review.models import Review
from movies.models import Movie
from users.models import CustomUser
from .serializers import FavouriteSerializers, FavouriteDetailSerializers
import threading
from recommendation_system import recommendation_engine

# Create your views here.
class FavouriteViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Favourite.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # serializer_class = WatchedDetailSerializers
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return FavouriteDetailSerializers
        else:
            return FavouriteSerializers

    def list(self, request, *args, **kwargs):

        try:
            query_set = Favourite.objects.filter(user_id=request.user.id)
            movie = [FavouriteDetailSerializers(watched).data['movie'] for watched in query_set]
            data = {
                "status": "success",
                "message": {
                    "id": request.user.id,
                    'favourite': movie}
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
        movie = Movie.objects.get(id = movie_id)
        user = CustomUser.objects.get(id = request.user.id)
        if Favourite.objects.filter(user=user, movie=movie).exists():
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            favourite = Favourite.objects.create(movie=movie, user=user)
            data = {
                "status": "success",
                "message": FavouriteSerializers(favourite).data
            }
            thread = threading.Thread(target=recommendation_engine.content_recommendations(movie=movie,user=user))
            thread.start()
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            favourite_obj = Favourite.objects.get(user_id=request.user.id, movie_id=pk)
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
                    favourite_obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Favourite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
