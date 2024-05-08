from rest_framework import serializers
from users.models import Watched
from movies.models import Movie
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field


class WatchedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = ['movie','user']
        
    
class WatchedDetailSerializers(serializers.ModelSerializer):
    watched = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','watched']
        # extra_kwargs = {'user':{'write_only':True}}
        
    @extend_schema_field(serializers.ListField)
    def get_watched(self,user_instance):
        user_query_data = CustomUser.objects.get(id=user_instance.id) 
        query_data = []
        for movie in user_query_data.watched.all():
            query_data.append(movie)            
        
        return[MovieListSerializers(watched).data for watched in query_data]
        
class MovieListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [ 'id','original_title', 'poster_path', 'title',]