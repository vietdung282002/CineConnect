# Create your views here.
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer



class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, **kwargs):
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

    def create(self, request, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:

            try:
                user = CustomUser.objects.get(email=username)
                username = user.username
            except CustomUser.DoesNotExist:
                return Response({'error': 'Such user was not found'},
                                status=status.HTTP_404_NOT_FOUND)

        # check to see if username with that password exist
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "status": "success",
                "data": {
                    "token": token.key,
                    'id': user.id
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

    def create(self, request, **kwargs):

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
