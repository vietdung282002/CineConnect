from django.shortcuts import render
from rest_framework import viewsets, permissions
from users.models import CustomUser
from rating.models import Rating
from watched.models import Watched
from review.models import Review
from .serializers import WatchedDetailSerializers, WatchedSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

import logging

logger = logging.getLogger(__name__)

# Create your views here.

class WatchedViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    # serializer_class = WatchedDetailSerializers
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return WatchedDetailSerializers
        else:
            return WatchedSerializers

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        if Watched.objects.filter(user_id=request.user.id, movie_id=movie_id).exists():
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        pass


class WatchedDeleteAPIVIew(APIView):
    serializer_class = WatchedSerializers
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='movie_id',
                description='ID of the movie to delete',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
            # Add more parameters if needed
        ],
    )
    def delete(self, request, movie_id, *args, **kwargs):

        try:
            watched_obj = Watched.objects.get(user_id=request.user.id, movie_id=movie_id)
            try:
                rating_obj = Rating.objects.get(user_id=request.user.id, movie_id=movie_id)
                return Response({'error': "You can't not remove from watched because there is activity on it"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Rating.DoesNotExist:
                try: 
                    review_obj =  Review.objects.get(user_id=request.user.id, movie_id=movie_id)
                    return Response({'error': "You can't not remove from watched because there is activity on it"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
                except Review.DoesNotExist:
                    watched_obj.delete() 
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Watched.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
    