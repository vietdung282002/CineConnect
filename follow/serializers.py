from rest_framework import serializers
from .models import Follow
from drf_spectacular.utils import extend_schema_field
from user_profile.serializers import CustomUser, UserListSerializer

class FolloweeSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # class Meta:
    #     model = Follow
    #     fields = ['user']
        
    # @extend_schema_field(serializers.ListField)
    # def get_user(self, follow_instance):
    #     user = CustomUser.objects.get(id=follow_instance.followee.id)
    #     context = self.context
    #     return UserListSerializer(user,context=context).data

    id = serializers.IntegerField(source='followee.id')
    username = serializers.CharField(source='followee.username')
    profile_pic = serializers.CharField(source='followee.profile_pic')
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'username', 'profile_pic', 'is_following']
    
    @extend_schema_field(serializers.ListField)
    def get_is_following(self, follow_instance):
        if self.context['user_id'] is not None and self.context['user_id'] != follow_instance.followee.id:
            try:
                Follow.objects.get(follower_id = self.context['user_id'],followee_id = follow_instance.followee.id)
                return True
            except Follow.DoesNotExist:
                return False
        return None
        
class FollowerSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # class Meta:
    #     model = Follow
    #     fields = ['user']
        
    # @extend_schema_field(serializers.ListField)
    # def get_user(self, follow_instance):
    #     user = CustomUser.objects.get(id=follow_instance.follower.id)
    #     context = self.context
    #     return UserListSerializer(user,context=context).data
    id = serializers.IntegerField(source='followee.id')
    username = serializers.CharField(source='followee.username')
    profile_pic = serializers.CharField(source='followee.profile_pic')
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'username', 'profile_pic', 'is_following']
    
    @extend_schema_field(serializers.ListField)
    def get_is_following(self, follow_instance):
        if self.context['user_id'] is not None and self.context['user_id'] != follow_instance.followee.id:
            try:
                Follow.objects.get(followee_id = self.context['user_id'],follower_id = follow_instance.followee.id)
                return True
            except Follow.DoesNotExist:
                return False
        return None
        