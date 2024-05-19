# Create your views here.
import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from movies.models import Movie
from watched.models import Watched
from .serializers import RatingSerializers, Rating, RatingUpdateSerializers
from django.db.models import F,Avg

logger = logging.getLogger(__name__)


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RatingSerializers
    queryset = Rating.objects.all()

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return RatingUpdateSerializers
        else:
            return RatingSerializers

    permission_classes = (permissions.IsAuthenticated,)
    
    http_method_names = ['post','put','delete']

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        rate = data.get('rate')
        if Rating.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            watched = Watched.objects.get(movie_id=movie_id, user_id=request.user.id)
        except Watched.DoesNotExist:
            Watched.objects.create(movie_id=movie_id, user_id=request.user.id)

        try:
            rating = Rating.objects.create(movie_id=movie_id, user_id=request.user.id,rate= rate)
            movie = Movie.objects.get(movie_id=movie_id)
            movie.rate_count = F('rate_count') + 1
            movie.rate_avr = Rating.objects.filter(movie_id=movie_id).aggregate(Avg('rate'))

            movie.save()
            
            data = data = {
                "status": "success",
                "message": RatingSerializers(rating).data
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
            rating_obj = Rating.objects.get(user_id=request.user.id, movie_id=pk)

            rating_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Watched.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk, *args, **kwargs):
        try:
            rating_obj = Rating.objects.get(movie_id=pk, user_id=request.user.id)
            serializer = RatingUpdateSerializers(rating_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # def partial_update(self, request, pk, *args, **kwargs):
    #     try:
    #         rating_obj = Rating.objects.get(movie_id=pk, user_id=request.user.id)
    #         serializer = RatingUpdateSerializers(rating_obj, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Rating.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
