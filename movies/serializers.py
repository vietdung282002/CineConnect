from rest_framework import serializers
from .models import Movie
from genres.models import Genre
from genres.serializers import GenresSerializers


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id']
        
    def create(self, validated_data):
        instance, _ = Genre.objects.get(**validated_data)
        return instance
    
class MoviesSerializer(serializers.ModelSerializer):
    # genres = GenresSerializers(many= True)
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres']
        # extra_kwargs = {'id': {'read_only': True}}
        
        
    # def create(self, validated_data):
    #     genres_data = validated_data.pop('genres', []) 
        
    #     genresInstances = []
    #     for genre in genres_data:
    #         genresInstances.append(Genre.objects.get(pk = genre['id']))
    #     movie = Movie.objects.create(**validated_data)
    #     movie.genre.set(genresInstances)
    #     return movie
    
    # def get_movies_genres(self, movie):
    #     genres = Genre.objects.filter(movies = movie.id)
    #     serializers = MovieGenreSerializer(genres,many= True)
    #     return serializers.data