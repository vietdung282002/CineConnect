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
        
    http_method_names =['get','post','patch','delete']
        

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        content = data.get('content')
        if Review.objects.filter(user_id = request.user.id,movie_id = movie_id):
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            watched = Watched.objects.get(movie_id=movie_id, user_id=request.user.id)
        except Watched.DoesNotExist:
            Watched.objects.create(movie_id=movie_id, user_id=request.user.id)
        try:
            review = Review.objects.create(movie_id=movie_id, user_id=request.user.id,content = content)
            data = data = {
                "status": "success",
                "message": ReviewListSerializers(review).data
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
            self.queryset = []
            
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
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        else:
            return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        review = request.data.get('review')
        comment = request.data.get('comment')
        try: 
            comment = Comment.objects.create(review_id = review,comment = comment,user_id = request.user.id)
            data = {
                "status": "success",
                "message": CommentSerializer(comment).data
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
            self.queryset = []
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
            data = {
                "status": "success",
                "result": {
                    "review":review.id,
                    "like": True,
                }
            }
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
        
    