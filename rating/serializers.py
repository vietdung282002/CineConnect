from rest_framework import serializers

from .models import Rating


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['movie', 'user', 'rate']
        extra_kwargs = {'user': {'read_only': True}}


class RatingUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate']
