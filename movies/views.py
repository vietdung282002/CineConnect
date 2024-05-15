
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieCreateSerializer, MovieDetailDisplaySerializer, MovieListDisplaySerializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema,OpenApiParameter
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    http_method_names = ['get']
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'search':
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
        self.serializer_class = MovieListDisplaySerializers
        logger.warning(self.action)
        return super().list(request, *args, **kwargs)
            