from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from .serializers import Activity,ActivitySerializers
# Create your views here.
class ActivityViewsets(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers