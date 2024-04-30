from django.shortcuts import render
from users.models import CustomUser
from .serializers import UserProfileSerializer
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.
class UserProflieViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch','delete']
    