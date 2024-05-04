from rest_framework import serializers
from .models import Movie,Cast,Director
from genres.models import Genre
from genres.serializers import GenresSerializers
from people.models import Person
from people.serializers import PersonSerializers
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class CastCharactorSerializer(serializers.ModelSerializer):
    cast = PersonSerializers(read_only= True)
    cast_id = serializers.PrimaryKeyRelatedField(write_only= True,source= 'person', queryset= Person.objects.all())
    class Meta:
        model = Cast
        fields = ['cast','charactor','cast_id','order']    
    
class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(),slug_field='id'
    )
    casts = CastCharactorSerializer(many = True)
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres','casts']
        
    def create(self, validated_data):
        
        genres_data = validated_data.pop('genres', []) 
        
        cast_data = validated_data.pop('cast', []) 
        movie = Movie.objects.create(**validated_data)
        for cast in cast_data:
            Cast.objects.create(movie_id = movie.id,**cast)
        genresInstances = []
        for genre in genres_data:
            genresInstances.append(genre)
        
        movie.genres.set(genresInstances)
        return movie
    
class CastMovieSerializer(serializers.ModelSerializer):
    cast = PersonSerializers()
    class Meta:
        model = Cast
        fields = ['cast','charactor','cast_id','order']
        
class MovieListDisplaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres']

class MovieDetailDisplaySerializer(serializers.ModelSerializer):
    casts = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres','casts']

    def get_casts(self,movie_instance):
        query_data = Cast.objects.filter(movie = movie_instance)
        # logger.warning(query_data)

        return [CastMovieSerializer(person).data for person in query_data]
    
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
                'original_name': cast['cast']['name'],  # Bạn có thể sử dụng thông tin khác nếu cần
                'profile_path': cast['cast']['profile_path'],
                'character': cast['charactor'],
                'order': cast['order']
            }
            cast_data.append(cast_info)
        data['casts'] = cast_data
        return data
