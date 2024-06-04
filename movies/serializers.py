from django.db.models import Avg
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from genres.models import Genre
from genres.serializers import GenresSerializers
from people.models import Person
from people.serializers import PersonSerializers
from rating.models import Rating
from review.models import Review
from .models import Movie, Cast, Director
from favourite.models import Favourite
from django.db.models.functions import Round
import logging

logger = logging.getLogger(__name__)


class CastCharacterSerializer(serializers.ModelSerializer):
    cast = PersonSerializers(read_only=True)
    cast_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='person', queryset=Person.objects.all())

    class Meta:
        model = Cast
        fields = ['cast', 'character', 'cast_id', 'order']


class DirectorSerializer(serializers.ModelSerializer):
    director = PersonSerializers(read_only=True)
    director_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='person', queryset=Person.objects.all())

    class Meta:
        model = Director
        fields = ['director', 'director_id']


class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='id'
    )
    casts = CastCharacterSerializer(many=True)
    director = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title',
                  'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title',
                  'genres', 'casts', 'director']

    def create(self, validated_data):

        genres_data = validated_data.pop('genres', [])

        cast_data = validated_data.pop('cast', [])

        director_data = validated_data.pop('director', [])
        movie = Movie.objects.create(**validated_data)
        for cast in cast_data:
            Cast.objects.create(**cast)

        for director in director_data:
            Director.objects.create(**director)

        genres_instances = []
        for genre in genres_data:
            genres_instances.append(genre)

        movie.genres.set(genres_instances)
        return movie


class CastMovieSerializer(serializers.ModelSerializer):
    cast = PersonSerializers()

    class Meta:
        model = Cast
        fields = ['cast', 'character', 'cast_id', 'order']


class DirectorMovieSerializer(serializers.ModelSerializer):
    director = PersonSerializers()

    class Meta:
        model = Director
        fields = ['director', 'director_id']


class MovieListDisplaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path' ]
        
class MovieSearchListDisplaySerializers(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path','release_date', 'directors']
        
    @extend_schema_field(serializers.ListField)
    def get_directors(self, movie_instance):
        query_data = Director.objects.filter(movie=movie_instance)

        return [DirectorMovieSerializer(person).data for person in query_data]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        director_data = []
        for director in data['directors']:
            director_info = {
                'id': director['director']['id'],
                'name': director['director']['name'],
            }
            director_data.append(director_info)
        data['directors'] = director_data
    
        return data


class RatingDisplaySerializers(serializers.ModelSerializer):
    avr = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['avr', 'total', 'rating']

    def get_avr(self, rating_instance):
        avr = Rating.objects.filter(
            movie=rating_instance.movie).aggregate(avg_rate=Round(Avg('rate'), 1))

        return avr

    def get_total(self, rating_instance):
        total = Rating.objects.filter(movie=rating_instance.movie).count()

        return total

    @extend_schema_field(serializers.ListField)
    def get_rating(self, rating_instance):
        rating = {}
        for rate in range(5, 51, 5):
            rate /= 10
            rating[rate] = Rating.objects.filter(
                movie=rating_instance.movie, rate=rate).count()

        return rating


class MovieDetailDisplaySerializer(serializers.ModelSerializer):
    casts = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    genres = GenresSerializers(many=True)
    favourite_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title',
                  'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title',
                  'genres', 'casts', 'directors', 'rating', 'review_count','favourite_count']

    @extend_schema_field(serializers.ListField)
    def get_casts(self, movie_instance):
        query_data = Cast.objects.filter(movie=movie_instance)

        return [CastMovieSerializer(person).data for person in query_data]
    
    @extend_schema_field(serializers.ListField)
    def get_favourite_count(self, movie_instance):
        query_data = Favourite.objects.filter(movie=movie_instance)

        return len(query_data)

    @extend_schema_field(serializers.ListField)
    def get_rating(self, movie_instance):
        try:
            rating = Rating.objects.filter(movie=movie_instance)
            if not rating.exists():
                logger.warning("No ratings found for the movie")
                return [
                {
                    "avr": {
                        "rate__avg": 0
                    },
                    "total": 0,
                    "rating": {
                        "0.5": 0,
                        "1.0": 0,
                        "1.5": 0,
                        "2.0": 0,
                        "2.5": 0,
                        "3.0": 0,
                        "3.5": 0,
                        "4.0": 0,
                        "4.5": 0,
                        "5.0": 0
                    }
                }
                ]
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
    # Handle the exception if needed, maybe return a default value or raise an error

# if ratings exist, process the first rating in the list
        return [RatingDisplaySerializers(rating[0]).data]

    @extend_schema_field(serializers.ListField)
    def get_directors(self, movie_instance):
        query_data = Director.objects.filter(movie=movie_instance)

        return [DirectorMovieSerializer(person).data for person in query_data]

    @extend_schema_field(serializers.ListField)
    def get_review_count(self, movie_instance):
        review = Review.objects.filter(movie=movie_instance)
        return len(review)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        cast_data = []
        for cast in data['casts']:
            cast_info = {
                'adult': cast['cast']['adult'],
                'gender': cast['cast']['gender'],
                'id': cast['cast']['id'],
                'known_for_department': cast['cast']['known_for_department'],
                'name': cast['cast']['name'],
                'original_name': cast['cast']['name'],
                'profile_path': cast['cast']['profile_path'],
                'character': cast['character'],
                'order': cast['order']
            }
            cast_data.append(cast_info)
        data['casts'] = cast_data

        director_data = []
        for director in data['directors']:
            director_info = {
                'id': director['director']['id'],
                'name': director['director']['name'],
            }
            director_data.append(director_info)
        data['directors'] = director_data
        if self.context['user_id'] is not None:
            try:
                rating = Rating.objects.get(
                    movie=instance, user_id=self.context['user_id'])
            except Rating.DoesNotExist:
                data['rating'][0]['user_rating'] = 0

            data['rating'][0]['user_rating'] = rating.rate
        return data


class MovieListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path', 'title', 'backdrop_path']
