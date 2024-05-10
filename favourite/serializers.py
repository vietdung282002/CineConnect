from rest_framework import serializers
from favourite.models import Favourite
from movies.models import Movie
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field
from movies.serializers import MovieListSerializers


class FavouriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['movie', 'user']

class FavouriteDetailSerializers(serializers.ModelSerializer):
    favourite = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'favourite']
        # extra_kwargs = {'user':{'write_only':True}}

    @extend_schema_field(serializers.ListField)
    def get_favourite(self, user_instance):
        user_query_data = CustomUser.objects.get(id=user_instance.id)
        query_data = []
        for movie in user_query_data.favourite_list.all():
            query_data.append(movie)

        return [MovieListSerializers(watched).data for watched in query_data]
