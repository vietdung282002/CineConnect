# Create your views here.
import logging
from rest_framework import viewsets, mixins,status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from watched.models import Watched
from .models import Review,Comment,Reaction
from .serializers import ReviewSerializers, ReviewDetailSerializer, ReviewListSerializers, CommentSerializer, CommentListSerializer, ReactionSerializer, ReactionListSerializer
from .permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from activity.models import Activity
from django.db.models import Q
from favourite.models import Favourite
from follow.models import Follow
from movies.models import Movie
from recommendation_system.models import MovieRecommend
from rating.models import Rating
from favourite.models import Favourite
from users.models import CustomUser
logger = logging.getLogger(__name__)


class ReviewViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ReviewSerializers
        elif self.action == 'list':
            return ReviewListSerializers
        else:
            return ReviewDetailSerializer
        
    http_method_names =['get','post','put','delete']
        

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        movie = Movie.objects.get(id = movie_id)
        content = data.get('content')

        user = CustomUser.objects.get(id = request.user.id)
        
        if Review.objects.filter(user = user,movie = movie).exists():
            review = Review.objects.create(movie=movie, user=user,content = content,again= True)
            Activity.objects.create(movie=movie,user=user,type=1,review=review)
            
            data = data = {
                "status": "success",
                "message": ReviewSerializers(review).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        try:
            watched = Watched.objects.get(movie=movie, user=user)
        except Watched.DoesNotExist:
            Watched.objects.create(movie=movie, user=user)
            Activity.objects.create(movie=movie,user=user,type=3)
            
        try:
            review = Review.objects.create(movie=movie, user=user,content = content)
            Activity.objects.create(movie=movie,user=user,type=1,review=review)
            data = data = {
                "status": "success",
                "message": ReviewSerializers(review).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        movie_query = request.query_params.get('movie', None)
        user_query = request.query_params.get('user', None)
        if movie_query:
            query_set = Review.objects.filter(movie_id=movie_query)
            self.queryset = query_set
        elif user_query:
            query_set = Review.objects.filter(user_id = user_query)
            self.queryset = query_set
        else: 
            self.queryset = Review.objects.all()
            
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def calculatePopular(self,request,*args, **kwargs):
        queryset = Review.objects.all()
        for review in queryset:
            review.update_popular()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])  
    def newsfeed(self, request, *args, **kwargs):
        user_id = request.user.id
        if user_id:
            followed_users = Follow.objects.filter(follower_id=user_id).values_list('followee_id', flat=True)
            favourite_movies = Favourite.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
        
            query_set = Review.objects.filter(
                Q(user_id__in=followed_users) | Q(movie_id__in=favourite_movies)
            ).exclude(user_id=user_id)
        else: 
            query_set = Review.objects.none()
    
        self.queryset = query_set
            
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def recommend(self, request, *args, **kwargs):
        user_id = request.user.id
        if user_id:
            recommended_movies = MovieRecommend.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
            query_set = Review.objects.filter(
                Q(movie_id__in=recommended_movies)).exclude(user_id=user_id).order_by('popular')
            
        else: 
            query_set = Review.objects.none()
    
        self.queryset = query_set
            
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            self.queryset = Review.objects.filter(content__icontains=query)
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
    
    
    
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    http_method_names = ['get','post','put','delete']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentListSerializer
        else:
            return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        review = request.data.get('review')
        comment = request.data.get('comment')
        try: 
            comment = Comment.objects.create(review_id = review,comment = comment,user_id = request.user.id)
            Activity.objects.create(user_id=request.user.id,type=7,review_id=review)
            data = {
                "status": "success",
                "message": "comment success"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        query = request.query_params.get('review', None)
        if query:
            query_set = Comment.objects.filter(review_id=query)
            self.queryset = query_set
        else:
            self.queryset = Comment.objects.all()
        return super().list(request, *args, **kwargs)
    
class ReactionViewSet(mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Reaction.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReactionListSerializer
        else:
            return ReactionSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def list(self, request, *args, **kwargs):
        query = request.query_params.get('review', None)
        if query:
            query_set = Reaction.objects.filter(review_id=query)
            self.queryset = query_set
        else:
            self.queryset = []
        return super().list(request, *args, **kwargs)
    
    
    @csrf_exempt
    @action(detail=False, methods=['post'],serializer_class=ReactionSerializer)  
    def like(self,request, *args, **kwargs):
        query = request.query_params.get('review', None)
        try:
            review = Review.objects.get(id = query)
        except Review.DoesNotExist:
            data = {
                "status": "error",
                "result": "Objects not found"
            }
            return Response(data= data,status=status.HTTP_404_NOT_FOUND)
        
        try:
            reaction = Reaction.objects.get(review = review,user_id = request.user.id)
        except Reaction.DoesNotExist:
            reaction = Reaction.objects.create(review = review,user_id = request.user.id)
            
        data = None
        if reaction.like == False:
            reaction.like = True
            reaction.save()
            review = reaction.review
            movie = review.movie
            data = {
                "status": "success",
                "result": {
                    "review":review.id,
                    "like": True,
                }
            }
            Activity.objects.create(user_id=request.user.id,type=4,review=review)
        else: 
            reaction.like = False
            reaction.save()
            reaction.delete()
            data = {
                "status": "success",
                "result": {
                    "review":review.id,
                    "like": False,
                }
            }
            
        count = Reaction.objects.filter(review= review)
        count = len(count)
        data['result']['number_of_like'] = count
        return Response(data, status=status.HTTP_201_CREATED)
        
    