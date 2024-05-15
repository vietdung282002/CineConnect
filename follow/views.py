from django.shortcuts import render
from rest_framework import viewsets,status,mixins
from .models import Follow
from .serializers import FollowSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        followee = data.get('followee')
        if Follow.objects.filter(follower_id=request.user.id, followee_id=followee).exists():
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow = Follow.objects.create(follower_id=request.user.id, followee_id=followee)
            data = {
                "status": "success",
                "message": FollowSerializer(follow).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk, *args, **kwargs):
        try:
            follow_obj = Follow.objects.get(follower_id=request.user.id, followee_id=pk)
            follow_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)