from django.shortcuts import render
from rest_framework import viewsets,status,mixins,permissions
from .models import Follow
from .serializers import FollowerSerializer,FolloweeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from user_profile.serializers import UserListSerializer
from users.models import CustomUser
# Create your views here.
class FollowViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        
        if self.action == 'list_following':
            return FolloweeSerializer
        else:
            return FollowerSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
    
    @csrf_exempt
    @action(detail=False, methods=['post'])  
    def toggle(self,request, *args, **kwargs):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        query = request.query_params.get('user', None)
        user = CustomUser.objects.get(id=query)
        try:
            follow = Follow.objects.get(follower_id= request.user.id, followee_id= query)
            follow.delete()
            data = {
                "status": "success",
                "result": {
                    'user':UserListSerializer(user,context= context).data,
                    'isFollowing':False
                }
            }
            return Response(data=data,status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            try:
                follow = Follow.objects.create(follower_id= request.user.id, followee_id= query)
                data = {
                "status": "success",
                "result": {
                    'user':UserListSerializer(user,context= context).data,
                    'isFollowing':True
                }
            }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                data = {
                    "status": "error",
                    "message": str(e)
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])  
    def list_following(self, request, *args, **kwargs):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        query = request.query_params.get('user', None)
        if query:
            queryset = Follow.objects.filter(follower_id= query)
            self.queryset= queryset
        else:
            self.queryset= []
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])  
    def list_follower(self, request, *args, **kwargs):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        query = request.query_params.get('user', None)
        if query:
            queryset = Follow.objects.filter(followee_id= query)
            self.queryset= queryset
        else:
            self.queryset= []
        return super().list(request, *args, **kwargs)
    