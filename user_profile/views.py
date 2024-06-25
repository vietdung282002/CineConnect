from rest_framework import permissions
from rest_framework import viewsets,mixins,status
from rest_framework.response import Response
from users.models import CustomUser
from .serializers import UserProfileSerializer,UserListSerializer,UserProfileUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class UserProfileViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_permissions(self):
        
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'search':
            return UserListSerializer
        elif self.action == 'update':
            return UserProfileUpdateSerializer  
        else:
            return UserProfileSerializer
        
    def update(self, request, *args, **kwargs):
        username = request.data['username']
        id = request.user.id
        if CustomUser.objects.filter(Q(username=username) & ~Q(id=id)).exists():
            
            data = {
                "detail":"A user with that username already exists."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            return super().update(request, *args, **kwargs)
        
        
    
    @action(detail=False, methods=['get'],serializer_class=UserListSerializer)  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            if self.request.user.id != None:
                self.queryset = CustomUser.objects.filter(Q(username__icontains=query) & ~Q(id=self.request.user.id) & ~Q(is_superuser=True))
            else:
                self.queryset = CustomUser.objects.filter(Q(username__icontains=query) &  ~Q(is_superuser=True))
        else:
            self.queryset = []
        
        return super().list(request, *args, **kwargs)
    
    
            