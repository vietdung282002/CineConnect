from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from .serializers import Activity,ActivitySerializers
# Create your views here.
class ActivityViewsets(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context
    
    def list(self, request, *args, **kwargs):
        user_query = request.query_params.get('user', None)
        if user_query:
            query_set = Activity.objects.filter(user_id = user_query)
            self.queryset = query_set
        else: 
            self.queryset = []
        return super().list(request, *args, **kwargs)