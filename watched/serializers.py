from rest_framework import serializers
from watched.models import Watched
from movies.models import Movie
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field
from movies.serializers import MovieListSerializers
import logging

logger = logging.getLogger(__name__)


class WatchedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = ['movie', 'user']
        extra_kwargs = {'user':{'read_only':True}}

class WatchedDetailSerializers(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = Watched
        fields = [ 'movie']
        # extra_kwargs = {'user':{'write_only':True}}

    @extend_schema_field(serializers.ListField)
    def get_movie(self, watched_instance):
        movie = watched_instance.movie

        return MovieListSerializers(movie).data 
