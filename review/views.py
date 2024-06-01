# Create your views here.
import logging
from rest_framework import viewsets, mixins,status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from watched.models import Watched
from .models import Review,Comment,Reaction
from .serializers import ReviewSerializers, ReviewDetailSerializer, ReviewListSerializers, CommentSerializer, CommentListSerializer, ReactionSerializer, ReactionDetailSerializer
from .permissions import IsOwnerOrReadOnly
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
        query = request.query_params.get('movie', None)
        if query:
            query_set = Review.objects.filter(movie_id=query)
            self.queryset = query_set
        else: 
            self.queryset =[]
        return super().list(request, *args, **kwargs)
    
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    http_method_names = ['get','post','patch','delete']
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
        
    @action(detail=True, methods=['get'],
            serializer_class=CommentListSerializer)  
    def comment_list(self, request, pk):
        instance = Comment.objects.filter(review_id=pk)
        comment = [CommentListSerializer(comment).data for comment in instance]
        response = {
            "id": pk,
            "review": comment
        }

        return Response(response, status=status.HTTP_200_OK)
    
class ReactionViewSet(viewsets.GenericViewSet):
    queryset = Reaction.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = ReactionSerializer
    
    @action(detail=False, methods=['post'],serializer_class=ReactionSerializer)  
    def like(self,request, *args, **kwargs):
        try:
            review = Review.objects.get(id = request.data.get('review'))
        except Review.DoesNotExist:
            data = {
                "status": "error",
                "message": "Objects not found"
            }
            return Response(data= data,status=status.HTTP_404_NOT_FOUND)
        
        try:
            reaction = Reaction.objects.get(review = review,user_id = request.user.id)
            logger.warning(reaction.like)
        except Reaction.DoesNotExist:
            reaction = Reaction.objects.create(review = review,user_id = request.user.id)
            
        data = None
        if reaction.like == False:
            reaction.like = True
            reaction.dislike = False
            reaction.save()
            data = {
                "status": "success",
                "message": {
                    "review":review.id,
                    "like": True,
                    "dislike":False
                }
            }
        else: 
            reaction.like = False
            reaction.save()
            reaction.delete()
            data = {
                "status": "success",
                "message": {
                    "review":review.id,
                    "like": False,
                    "dislike":False
                }
            }
        return Response(data, status=status.HTTP_201_CREATED)
        
    @action(detail=False, methods=['post'],
            serializer_class=ReactionSerializer)  
    def dislike(self,request, *args, **kwargs):
        try:
            review = Review.objects.get(id = request.data.get('review'))
        except Review.DoesNotExist:
            data = {
                "status": "error",
                "message": "Objects not found"
            }
            return Response(data= data,status=status.HTTP_404_NOT_FOUND)
        
        try:
            reaction = Reaction.objects.get(review_id = review.id,user_id = request.user.id)
        except Reaction.DoesNotExist:
            reaction = Reaction.objects.create(review = review,user_id = request.user.id)
        
        data = None
        if reaction.dislike == False:
            reaction.dislike = True
            reaction.like = False
            reaction.save()
            data = {
                "status": "success",
                "message": {
                    "review":review.id,
                    "like": False,
                    "dislike":True
                }
            }
        else: 
            reaction.dislike = False
            reaction.save()
            reaction.delete()
            data = {
                "status": "success",
                "message": {
                    "review":review.id,
                    "like": False,
                    "dislike":False
                }
            }
            
        
        return Response(data, status=status.HTTP_201_CREATED)