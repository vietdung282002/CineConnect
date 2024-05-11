from rest_framework import serializers
from favourite.models import Favourite
from movies.models import Movie
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field
from movies.serializers import MovieListSerializers


class FavouriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['movie', 'user']
        extra_kwargs = {'user':{'read_only':True}}

class FavouriteDetailSerializers(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    class Meta:
        model = Favourite
        fields = [ 'movie']
        # extra_kwargs = {'user':{'write_only':True}}

    @extend_schema_field(serializers.ListField)
    def get_movie(self, favourite_instance):
        movie = favourite_instance.movie

        return MovieListSerializers(movie).data 