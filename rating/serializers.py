from rest_framework import serializers
from movies.models import Movie
from users.models import CustomUser
from .models import Rating
from drf_spectacular.utils import extend_schema_field
from movies.serializers import MovieListSerializers

class RatingSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Rating
        fields = ['movie','user','rate']

        
class RatingDetailSerializers(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['rate',]

   
        
    