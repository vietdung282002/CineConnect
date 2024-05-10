from rest_framework import serializers
from .models import Review,Reaction,Comment
from movies.serializers import Movie,MovieListSerializers
from drf_spectacular.utils import extend_schema_field
from user_profile.serializers import UserProfileSerializer, CustomUser
class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'original_title',
            'poster_path',
            'title'
        ]
        
class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    # rating = serializers.SerializerMethodField()
    # favourite = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = [
                'movie',
                'user',
                'content',
                'likes',
                'dislikes',
                # 'comment'
                ]
    
    @extend_schema_field(serializers.ListField)
    def get_movie(self, review_instance):
        movie = Movie.objects.get(id = review_instance.movie.id)

        return MovieListSerializers(movie).data 
    
    @extend_schema_field(serializers.ListField)
    def get_user(self, review_instance):
        user = CustomUser.objects.get(id = review_instance.user.id)

        return UserProfileSerializer(user).data 
    
    # @extend_schema_field(serializers.ListField)
    # def get_rating(self, review_instance):
        