from rest_framework import permissions
from rest_framework import viewsets,mixins
from users.models import CustomUser
from .serializers import UserProfileSerializer,UserListSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from django.db.models import Q

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'search':
            return UserListSerializer
        else:
            return UserProfileSerializer
    
    @action(detail=False, methods=['get'],serializer_class=UserListSerializer)  
    def search(self,request,*args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            if self.request.user.id != None:
                self.queryset = CustomUser.objects.filter(Q(username__icontains=query) & ~Q(id=self.request.user.id))
            else:
                self.queryset = CustomUser.objects.filter(username__icontains=query)
        else:
            self.queryset = []
        
        return super().list(request, *args, **kwargs)
            