from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from users.models import CustomUser
from watched.models import Watched
from favourite.models import Favourite
from review.models import Review
from rating.models import Rating
from follow.models import Follow


class UserProfileSerializer(serializers.ModelSerializer):
    watched_count = serializers.SerializerMethodField()
    favourite_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    rate_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'bio', 'profile_pic','watched_count','favourite_count','review_count','rate_count','is_following']
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    @extend_schema_field(serializers.ListField)
    def get_watched_count(self,user_instance):
        watchlist_count = Watched.objects.filter(user = user_instance).count()
        return watchlist_count
    
    @extend_schema_field(serializers.ListField)
    def get_favourite_count(self,user_instance):
        favourite_count = Favourite.objects.filter(user = user_instance).count()
        return favourite_count
    
    @extend_schema_field(serializers.ListField)
    def get_review_count(self,user_instance):
        review_count = Review.objects.filter(user = user_instance).count()
        return review_count
    
    @extend_schema_field(serializers.ListField)
    def get_rate_count(self,user_instance):
        rate_count = Rating.objects.filter(user = user_instance).count()
        return rate_count
    
    @extend_schema_field(serializers.ListField)
    def get_is_following(self,user_instance):
        if self.context['user_id'] is not None and self.context['user_id'] != user_instance.id:
            try:
                Follow.objects.get(follower_id = self.context['user_id'],followee = user_instance)
                return True
            except Follow.DoesNotExist:
                return False
        return None
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','profile_pic']