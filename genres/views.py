from django.shortcuts import render
from rest_framework import viewsets
from .models import Genre
from .serializers import GenresSerializers

# Create your views here.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializers
    http_method_names = ['get']
    