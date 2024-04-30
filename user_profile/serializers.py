from rest_framework import serializers
from users.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','email','gender','bio','profile_pic']
        extra_kwargs = {'id': {'read_only': True},'password': {'write_only': True}}
    