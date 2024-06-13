# Create your views here.
import logging

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from movies.serializers import Movie,MovieDetailDisplaySerializer
from watched.models import Watched
from users.models import CustomUser
from .serializers import RatingSerializers, Rating, RatingUpdateSerializers
from django.db.models import F,Avg
import threading
from recommendation_system import recommendation_engine
from recommendation_system.models import MovieRecommend
from activity.models import Activity
logger = logging.getLogger(__name__)


class RatingViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RatingSerializers
    queryset = Rating.objects.all()

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return RatingUpdateSerializers
        else:
            return RatingSerializers
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context

    permission_classes = (permissions.IsAuthenticated,)
    
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        rate = data.get('rate')
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        try:
            movie= Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id = request.user.id)
        if Rating.objects.filter(user_id=request.user.id, movie=movie).exists():
            Rating.objects.get(user_id=request.user.id, movie=movie).delete()
        try:
            watched = Watched.objects.get(movie=movie, user_id=request.user.id)
        except Watched.DoesNotExist:
            Watched.objects.create(movie=movie, user_id=request.user.id)
            Activity.objects.create(movie=movie,user=user,type=3)
        try:
            
            if rate > 0:
                rating = Rating.objects.create(movie=movie, user_id=request.user.id,rate= rate)
                Activity.objects.create(movie=movie,user=user,type=5)
                movie.rate_count = F('rate_count') + 1
                movie.rate_avr = Rating.objects.filter(movie=movie).aggregate(Avg('rate')).get('rate__avg')

                movie.save()
                
                data = {
                    "status": "success",
                    "message": {
                        "movie": movie_id,
                        "user": request.user.id,
                        "rate": MovieDetailDisplaySerializer(movie,context=context).data['rating']
                    }
                }
                
            else:
                data = {
                    "status": "success",
                    "message": {
                        "movie": movie_id,
                        "user": request.user.id,
                        "rate": MovieDetailDisplaySerializer(movie,context=context).data['rating']
                    }
                }
                
            if rate >= 4:
                recommendation_engine.content_recommendations(movie,user)
            if rate <2:
                if MovieRecommend.objects.filter(user_id = request.user.id,movie_id= movie_id).exists():
                    MovieRecommend.objects.get(user_id = request.user.id,movie_id= movie_id).delete()
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)