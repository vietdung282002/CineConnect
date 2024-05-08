from django.shortcuts import render
from rest_framework import viewsets,permissions
from users.models import Watched,CustomUser
from .serializers import WatchedDetailSerializers,WatchedSerializers
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class WatchedViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = WatchedDetailSerializers
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return WatchedDetailSerializers
        else:
            return WatchedSerializers
    
    def create(self, request, *args, **kwargs):
        # Lấy dữ liệu từ request data
        data = request.data

        user_id = data.get('user')
        movie_id = data.get('movie')
        if Watched.objects.filter(user_id=user_id, movie_id=movie_id).exists():
            return Response({'message': 'Đối tượng đã tồn tại.'}, status=status.HTTP_400_BAD_REQUEST)

        # Nếu đối tượng chưa tồn tại, tiếp tục quá trình tạo mới
        return super().create(request, *args, **kwargs)
    
