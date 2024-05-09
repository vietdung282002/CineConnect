from django.shortcuts import render
from .models import Movie
from genres.models import Genre
from .serializers import MovieCreateSerializer, MovieDetailDisplaySerializer, MovieListDisplaySerializers
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailDisplaySerializer
        elif self.action == 'list':
            return MovieListDisplaySerializers
        else:
            return MovieCreateSerializer

    http_method_names = ['get']
