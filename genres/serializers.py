from rest_framework import serializers
from .models import Genre

class GenresSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']
        
    def create(self,validated_data):
        
        instance, _ = Genre.objects.get_or_create(**validated_data)
        return instance
    
