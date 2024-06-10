from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Activity
from user_profile.serializers import CustomUser,UserListSerializer
from movies.serializers import Movie,MovieListSerializers

class ActivitySerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    movie = serializers.SerializerMethodField()
    user_follow = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = ['id','type','movie','user','user_follow','time_stamp']
        
    @extend_schema_field(serializers.ListField)
    def get_user(self, activity_instance):
        user = CustomUser.objects.get(id=activity_instance.user.id)
        context = self.context
        return UserListSerializer(user,context=context).data
    
    @extend_schema_field(serializers.ListField)
    def get_user_follow(self, activity_instance):
        if(activity_instance.user_follow != None):
            user = CustomUser.objects.get(id=activity_instance.user.id)
            context = self.context
            return UserListSerializer(user,context=context).data
        else:
            return None
    
    @extend_schema_field(serializers.ListField)
    def get_movie(self, review_instance):
        movie = Movie.objects.get(id=review_instance.movie.id)

        return MovieListSerializers(movie).data
    
        