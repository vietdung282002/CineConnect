from django.shortcuts import render
from rest_framework import viewsets
from .models import Genre
from .serializers import GenresSerializers, GenreDetailSerializers


# Create your views here.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return GenresSerializers
        else:
            return GenreDetailSerializers
