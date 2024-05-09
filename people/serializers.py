from rest_framework import serializers
from .models import Person
from movies.models import Movie
from drf_spectacular.utils import extend_schema_field


class MovieParticipateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path', 'title', ]


class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonDetailSerializers(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            'id',
            'adult',
            'biography',
            'birthday',
            'deathday',
            'gender',
            'homepage',
            'known_for_department',
            'name',
            'place_of_birth',
            'profile_path',
            'movies'
        ]

    @extend_schema_field(serializers.ListField)
    def get_movies(self, person_instance):
        cast_query_data = Movie.objects.filter(casts=person_instance)
        director_query_data = Movie.objects.filter(directors=person_instance)
        query_data = cast_query_data.union(director_query_data)

        return [MovieParticipateSerializers(movie).data for movie in query_data]
