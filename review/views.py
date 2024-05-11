from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ReviewDetailSerializer, Review, ReviewListSerializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
import logging
logger = logging.getLogger(__name__)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    http_method_names = ['get']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # if not self.request.user.is_anonymous:
        context['user_id'] = self.request.user.id
        
        return context
    
    def list(self, request, *args, **kwargs):
        pass
    
    @action(detail=True, methods=['get'],serializer_class = ReviewListSerializers)  # decorator để định nghĩa hành động tùy chỉnh, `detail=True` để chỉ áp dụng cho một đối tượng cụ thể
    def review_list(self, request, pk):
        instance = Review.objects.filter(movie_id = pk)
        review = [ReviewListSerializers(review).data for review in instance]
        response = {
            "id": pk,
            "review": review
        }
        logger.warning(response)
        
        return Response(response, status=status.HTTP_200_OK)
    
    
