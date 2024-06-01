
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie
from genres.models import Genre
from favourite.models import Favourite
from watched.models import Watched
from users.models import CustomUser
from .serializers import MovieCreateSerializer, MovieDetailDisplaySerializer, MovieListDisplaySerializers,MovieSearchListDisplaySerializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema,OpenApiParameter
from recommendation_system.recommendation_engine import create_tfidf_matrix,cal_cosine_simulator,content_recommendations
from asgiref.sync import async_to_sync
import asyncio
import threading
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    http_method_names = ['get','post']
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'genre' or self.action =='favourite' or self.action =='watched':
            return MovieListDisplaySerializers
        elif self.action == 'retrieve':
            return MovieDetailDisplaySerializer
        elif self.action == 'search':
            return MovieSearchListDisplaySerializers
        else:
            return MovieCreateSerializer
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context

    @action(detail=False, methods=['get'])  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            self.queryset = Movie.objects.filter(title__icontains=query)
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def genre(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            genre_obj = Genre.objects.get(id = query)
            self.queryset = Movie.objects.filter(genres = genre_obj)
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def favourite(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            user = CustomUser.objects.get(id=query)
        else:
            self.queryset = []  
            return super().list(request, *args, **kwargs)
        if user:
            favourite_list = Favourite.objects.filter(user_id= user.id)
            movie_list = []
            for favourite in favourite_list:
                movie = favourite.movie
                movie_list.append(movie)
                
            self.queryset = movie_list
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
            
    @action(detail=False, methods=['get'],serializer_class=MovieListDisplaySerializers)  
    def watched(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            user = CustomUser.objects.get(id=query)
        else:
            self.queryset = []  
            return super().list(request, *args, **kwargs)
        if user:
            watched_list = Watched.objects.filter(user_id= user.id)
            movie_list = []
            for watched in watched_list:
                movie = watched.movie
                movie_list.append(movie)
                
            self.queryset = movie_list
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)