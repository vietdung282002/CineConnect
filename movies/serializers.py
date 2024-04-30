from rest_framework import serializers
from .models import Movie
from genres.models import Genre
from genres.serializers import GenresSerializers

    
class MoviesSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(),slug_field='id'
    )
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres']
        # extra_kwargs = {'id': {'read_only': True}}
        
    