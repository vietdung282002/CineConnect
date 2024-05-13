# Create your views here.
import logging
from rest_framework import viewsets, mixins,status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from watched.models import Watched
from .serializers import ReviewSerializers,ReviewDetailSerializer, Review, ReviewListSerializers
from .permissions import IsOwnerOrReadOnly
logger = logging.getLogger(__name__)


class ReviewViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ReviewSerializers
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
        
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['get'],
            serializer_class=ReviewListSerializers)  # decorator để định nghĩa hành động tùy chỉnh, `detail=True` để chỉ áp dụng cho một đối tượng cụ thể
    def review_list(self, request, pk):
        instance = Review.objects.filter(movie_id=pk)
        review = [ReviewListSerializers(review).data for review in instance]
        response = {
            "id": pk,
            "review": review
        }
        logger.warning(response)

        return Response(response, status=status.HTTP_200_OK)
