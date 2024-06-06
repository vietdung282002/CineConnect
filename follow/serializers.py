from rest_framework import serializers
from .models import Follow
from drf_spectacular.utils import extend_schema_field
from user_profile.serializers import CustomUser, UserListSerializer

class FolloweeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['user']
        
    @extend_schema_field(serializers.ListField)
    def get_user(self, follow_instance):
        user = CustomUser.objects.get(id=follow_instance.followee.id)
        context = self.context
        return UserListSerializer(user,context=context).data
    
class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['user']
        
    @extend_schema_field(serializers.ListField)
    def get_user(self, follow_instance):
        user = CustomUser.objects.get(id=follow_instance.follower.id)
        context = self.context
        return UserListSerializer(user,context=context).data