from rest_framework import serializers

from .models import CustomUser


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
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', ]
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []
