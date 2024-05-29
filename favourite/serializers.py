from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from favourite.models import Favourite
from movies.serializers import MovieListSerializers
from user_profile.serializers import UserListSerializer
from rating.models import Rating


class FavouriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['movie', 'user']
        extra_kwargs = {'user': {'read_only': True}}


class FavouriteDetailSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    class Meta:
        model = Favourite
        fields = ['user','rate']
        # extra_kwargs = {'user':{'write_only':True}}

    @extend_schema_field(serializers.ListField)
    def get_user(self, favourite_instance):
        user = favourite_instance.user

        return UserListSerializer(user).data
    
    @extend_schema_field(serializers.ListField)
    def get_rate(self, favourite_instance):
        user = favourite_instance.user
        movie = favourite_instance.movie
        try: 
            rating = Rating.objects.get(user = user, movie= movie)      
        except Rating.DoesNotExist:
            return None
        return rating.rate
    

