from django.shortcuts import render
from rest_framework import viewsets,mixins
from .serializers import TestSerializers,TestWJob
# Create your views here.
class TestViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = TestWJob.objects.all()
    serializer_class = TestSerializers
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)