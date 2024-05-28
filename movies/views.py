
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie
from genres.models import Genre
from .serializers import MovieCreateSerializer, MovieDetailDisplaySerializer, MovieListDisplaySerializers
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
        if self.action == 'list' or self.action == 'search' or self.action == 'genre':
            return MovieListDisplaySerializers
        elif self.action == 'retrieve':
            return MovieDetailDisplaySerializer
        else:
            return MovieCreateSerializer
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # if not self.request.user.is_anonymous:
        context['user_id'] = self.request.user.id

        return context

    @action(detail=False, methods=['get'],serializer_class=MovieListDisplaySerializers)  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            self.queryset = Movie.objects.filter(title__icontains=query)
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'],serializer_class=MovieListDisplaySerializers)  
    def genre(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        response = None
        if query:
            genre_obj = Genre.objects.get(id = query)
            self.queryset = Movie.objects.filter(genres = genre_obj)
            response = super().list(request, *args, **kwargs)
            logger.warning(response.data)
            response.data['genre_name'] = genre_obj.name
        else:
            self.queryset = []
            response = super().list(request, *args, **kwargs)
            response.data['genre_name'] = genre_obj.name
        return response
            