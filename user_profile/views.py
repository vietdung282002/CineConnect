from rest_framework import permissions
from rest_framework import viewsets

from users.models import CustomUser
from .serializers import UserProfileSerializer


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete']
