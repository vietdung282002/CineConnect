from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from favourite.models import Favourite
from movies.serializers import Movie, MovieListSerializers
from rating.models import Rating
from watched.models import Watched
from user_profile.serializers import UserProfileSerializer, CustomUser,UserListSerializer
from .models import Review, Reaction, Comment

import logging

logger = logging.getLogger(__name__)
class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['movie','content']

class ReviewListSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    favourite = serializers.SerializerMethodField()
    movie = serializers.SerializerMethodField()


    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'rating',
            'favourite',
            'content',
            'movie'
        ]
    @extend_schema_field(serializers.ListField)
    def get_movie(self, review_instance):
        movie = Movie.objects.get(id=review_instance.movie.id)

        return MovieListSerializers(movie).data
    
    @extend_schema_field(serializers.ListField)
    def get_user(self, review_instance):
        user = CustomUser.objects.get(id=review_instance.user.id)
        context = self.context
        return UserListSerializer(user).data

    @extend_schema_field(serializers.ListField)
    def get_rating(self, review_instance):
        try:
            rating = Rating.objects.get(
                movie=review_instance.movie, user=review_instance.user)
        except Rating.DoesNotExist:
            return 0

        return rating.rate

    @extend_schema_field(serializers.ListField)
    def get_favourite(self, review_instance):
        try:
            favourite = Favourite.objects.get(
                movie=review_instance.movie, user=review_instance.user)
        except Favourite.DoesNotExist:
            return False

        return True


class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    favourite = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    watched_day = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'movie',
            'user',
            'content',
            'rating',
            'favourite',
            'likes_count',
            'dislikes_count',
            'comment_count',
            'is_liked',
            'is_disliked',
            'watched_day'
        ]

    @extend_schema_field(serializers.ListField)
    def get_movie(self, review_instance):
        movie = Movie.objects.get(id=review_instance.movie.id)
        return MovieListSerializers(movie).data

    @extend_schema_field(serializers.ListField)
    def get_user(self, review_instance):
        user = CustomUser.objects.get(id=review_instance.user.id)
        context = self.context
        return UserListSerializer(user).data
    
    @extend_schema_field(serializers.ListField)
    def get_watched_day(self, review_instance):
        user = CustomUser.objects.get(id=review_instance.user.id)
        movie = Movie.objects.get(id=review_instance.movie.id)
        try:
            watched = Watched.objects.get(movie=movie,user=user)
        except Watched.DoesNotExist:
            return None
        return watched.time_stamp

    @extend_schema_field(serializers.ListField)
    def get_rating(self, review_instance):
        try:
            rating = Rating.objects.get(
                movie=review_instance.movie, user=review_instance.user)
        except Rating.DoesNotExist:
            return 0

        return rating.rate

    @extend_schema_field(serializers.ListField)
    def get_favourite(self, review_instance):
        try:
            favourite = Favourite.objects.get(
                movie=review_instance.movie, user=review_instance.user)
        except Favourite.DoesNotExist:
            return False

        return True

    @extend_schema_field(serializers.ListField)
    def get_likes_count(self, review_instance):
        reaction = Reaction.objects.filter(
            review=review_instance).filter(like=True)
        return len(reaction)

    @extend_schema_field(serializers.ListField)
    def get_dislikes_count(self, review_instance):
        reaction = Reaction.objects.filter(
            review=review_instance).filter(dislike=True)
        return len(reaction)

    @extend_schema_field(serializers.ListField)
    def get_comment_count(self, review_instance):
        comment = Comment.objects.filter(review=review_instance)
        return len(comment)

    @extend_schema_field(serializers.ListField)
    def get_is_liked(self, review_instance):
        if self.context['user_id'] != None:
            try:
                reaction = Reaction.objects.get(
                    review=review_instance, user_id=self.context['user_id'])
            except Reaction.DoesNotExist:
                return False
            return reaction.like

        return False

    @extend_schema_field(serializers.ListField)
    def get_is_disliked(self, review_instance):
        if self.context['user_id'] != None:
            try:
                reaction = Reaction.objects.get(
                    review=review_instance, user_id=self.context['user_id'])
            except Reaction.DoesNotExist:
                return False
            return reaction.dislike

        return False

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['review','comment']

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','user','comment','time_stamp']
        
        
class ReactionSerializer(serializers.ModelSerializer):
    is_reaction = serializers.SerializerMethodField()
    class Meta:
        model = Reaction
        fields = ['review','is_reaction']
        
    @extend_schema_field(serializers.ListField)
    def get_is_reaction(self, reaction_instance):
        try:
            reaction = Reaction.objects.get(reaction=reaction_instance)
            if reaction.like == True:
                return "Liked"
            else:
                return "Disliked"
        except Reaction.DoesNotExist:
            return "None"
        
class ReactionDetailSerializer(serializers.ModelSerializer):
    is_reaction = serializers.SerializerMethodField()
    class Meta:
        model = Reaction
        fields = ['review','user','is_reaction']
        
    @extend_schema_field(serializers.ListField)
    def get_is_reaction(self, reaction_instance):
        try:
            reaction = Reaction.objects.get(reaction=reaction_instance)
            if reaction.like == True:
                return "Liked"
            else:
                return "Disliked"
        except Reaction.DoesNotExist:
            return "None"
            
        
