from django.shortcuts import render

from watched.models import Watched
from .serializers import RatingSerializers,Rating
from rest_framework import viewsets
from rest_framework import permissions
from users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import Http404
# Create your views here.

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializers
    http_method_names = ['post',]
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie')
        user_id = request.data.get('user')
        try:
            watched = Watched.objects.get(movie_id = movie_id, user_id = user_id)
        except Watched.DoesNotExist: 
            Watched.objects.create(movie_id = movie_id, user_id = user_id)
            
        return super().create(request, *args, **kwargs)
    
class RatingDeleteAPIVIew(APIView):
    serializer_class = RatingSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                description='ID user',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
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
    def delete(self, request, user_id, movie_id, *args, **kwargs):

        try:
            watched_obj = Rating.objects.get(user_id=user_id, movie_id=movie_id)

            watched_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Watched.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class RatingUpdateAPIView(APIView):
    
    serializer_class = RatingSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            raise Http404
        
    def put(self,request,pk, *args, **kwargs):
        rating = self.get_object(pk)
        serializer = RatingSerializers(rating,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)