from rest_framework import viewsets,status
from .models import Genre
from movies import models,serializers
from .serializers import GenresSerializers, GenreDetailSerializers
from rest_framework.response import Response


# Create your views here.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return GenresSerializers
        else:
            return GenreDetailSerializers
        
    
