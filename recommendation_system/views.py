from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from users.models import CustomUser
from movies.models import Movie
from rest_framework.response import Response
from rest_framework import viewsets, mixins,status, permissions

# Create your views here.


from .recommendation_engine import content_recommendations,cal_cosine_simulator,createCountVectorizer

@csrf_exempt        
@api_view(['POST'])
def add(request):
    user_id = request.user.id
    movie_id = request.data['movie']
    try:
        user = CustomUser.objects.get(id = user_id)
        try:
            movie = Movie.objects.get(id= movie_id)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    try:
        content_recommendations(movie,user)
    except Exception as e:
        return Response( status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)

@csrf_exempt        
@api_view(['GET'])
def get(request):
    cal_cosine_simulator()
    return Response(status=status.HTTP_200_OK)
