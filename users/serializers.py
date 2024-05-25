from rest_framework import serializers

from .models import CustomUser
from drf_spectacular.utils import extend_schema_field



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', ]
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username_or_email = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username_or_email', 'password', ]
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}
    
    @extend_schema_field(serializers.ListField)
    def get_username_or_email(self, obj):
        return obj.username or obj.email


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []
