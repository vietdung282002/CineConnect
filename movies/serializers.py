from rest_framework import serializers
from .models import Movie,Cast,Director
from genres.models import Genre
from genres.serializers import GenresSerializers
from people.models import Person
from people.serializers import PersonSerializers
import logging
from drf_spectacular.utils import extend_schema_field
logger = logging.getLogger(__name__)

class CastCharactorSerializer(serializers.ModelSerializer):
    cast = PersonSerializers(read_only= True)
    cast_id = serializers.PrimaryKeyRelatedField(write_only= True,source= 'person', queryset= Person.objects.all())
    class Meta:
        model = Cast
        fields = ['cast','charactor','cast_id','order']  
        
class DirectorSerializer(serializers.ModelSerializer):
    director = PersonSerializers(read_only= True)
    director_id = serializers.PrimaryKeyRelatedField(write_only= True,source= 'person', queryset= Person.objects.all())
    class Meta:
        model = Director
        fields = ['director','director_id']     
    
class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(),slug_field='id'
    )
    casts = CastCharactorSerializer(many = True)
    director = DirectorSerializer(many = True)
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres','casts','director']
        
    def create(self, validated_data):
        
        genres_data = validated_data.pop('genres', []) 
        
        cast_data = validated_data.pop('cast', []) 
        
        director_data = validated_data.pop('director',[])
        movie = Movie.objects.create(**validated_data)
        for cast in cast_data:
            Cast.objects.create(movie_id = movie.id,**cast)
        
        for director in director_data:
            Director.objects.create(movie_id = movie.id,**director)
            
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
        
class DirectorMovieSerializer(serializers.ModelSerializer):
    director = PersonSerializers()
    class Meta:
        model = Director
        fields = ['director','director_id']  
        
class MovieListDisplaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres']

class MovieDetailDisplaySerializer(serializers.ModelSerializer):
    casts = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    genres = GenresSerializers(many=True)
    class Meta:
        model = Movie
        fields = [ 'id', 'adult', 'backdrop_path', 'budget', 'homepage', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'revenue', 'runtime', 'status', 'tagline', 'title', 'genres','casts','directors']
    
    @extend_schema_field(serializers.ListField)
    def get_casts(self,movie_instance):
        query_data = Cast.objects.filter(movie = movie_instance)
        
        return [CastMovieSerializer(person).data for person in query_data]
    
    @extend_schema_field(serializers.ListField)
    def get_directors(self,movie_instance):
        query_data = Director.objects.filter(movie = movie_instance)
        
        return [DirectorMovieSerializer(person).data for person in query_data]
    
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
        
        director_data = []
        for director in data['directors']:
            director_info = {
                'adult': director['director']['adult'],
                'gender': director['director']['gender'],
                'id': director['director']['id'],
                'known_for_department': director['director']['known_for_department'],
                'name': director['director']['name'],
                'original_name': director['director']['name'],  # Bạn có thể sử dụng thông tin khác nếu cần
                'profile_path': director['director']['profile_path'],
            }
            director_data.append(director_info)
        data['directors'] = director_data
        return data

class MovieListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [ 'id','original_title', 'poster_path', 'title',]
