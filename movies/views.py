from django.shortcuts import render
from .models import Movie
from genres.models import Genre
from .serializers import MoviesSerializer
from rest_framework import viewsets,permissions
from rest_framework.response import Response

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
    
