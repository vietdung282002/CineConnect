from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer
from .models import CustomUser
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from . permission import IsOwnerOrReadOnly
from rest_framework import permissions

# Create your views here.

class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "data": serializer.data
            }  
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "status": "success",
            "message": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
        
class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    http_method_names = ['post']
    
    
    # @action(detail=False, methods=['post'])
    def update(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if '@' in username:
            try:
                user = authenticate(email=username,password=password)
            except ObjectDoesNotExist:
                pass
        if not user:
            user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "status": "success",
                "data": {
                    "token": token.key
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            "status": "error",
            "message": "Invalid credentials"
        }    
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    
class UserLogoutViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLogoutSerializer
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]
    

    def update(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            data = {
                "status": "success",
                "message": "Successfully logged out."
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    