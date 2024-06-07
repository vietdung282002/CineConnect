from rest_framework import serializers
from .models import TestWJob
class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestWJob
        fields = '__all__'
