from rest_framework import serializers
from watched.models import Watched
from movies.models import Movie
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field
from movies.serializers import MovieListSerializers


class WatchedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = ['movie', 'user']

class WatchedDetailSerializers(serializers.ModelSerializer):
    watched = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'watched']
        # extra_kwargs = {'user':{'write_only':True}}

    @extend_schema_field(serializers.ListField)
    def get_watched(self, user_instance):
        user_query_data = CustomUser.objects.get(id=user_instance.id)
        query_data = []
        for movie in user_query_data.watched_list.all():
            query_data.append(movie)

        return [MovieListSerializers(watched).data for watched in query_data]
