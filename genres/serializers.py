from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from movies.models import Movie
from .models import Genre


class MoviePaticipateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path', 'title', ]


class GenresSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
    

class GenreDetailSerializers(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'movies']

    @extend_schema_field(serializers.ListField)
    def get_movies(self, genre_instance):
        query_data = Movie.objects.filter(genres=genre_instance)
        return [MoviePaticipateSerializers(movie).data for movie in query_data]
