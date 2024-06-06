from rest_framework import serializers
from .models import TestWJ

class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestWJ
        fields = '__all__'