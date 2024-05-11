from django.shortcuts import render
from .models import Movie
from genres.models import Genre
from .serializers import MovieCreateSerializer, MovieDetailDisplaySerializer, MovieListDisplaySerializers
from rest_framework import viewsets
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailDisplaySerializer
        # elif self.action == 'retrieve' and not self.request.user.is_anonymous:
        #     return LoggedMovieDetailDisplaySerializer
        elif self.action == 'list':
            return MovieListDisplaySerializers
        else:
            return MovieCreateSerializer

    http_method_names = ['get']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # if not self.request.user.is_anonymous:
        context['user_id'] = self.request.user.id
        
        return context