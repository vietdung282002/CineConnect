from django.shortcuts import render
from rest_framework import viewsets, mixins,status, permissions
from .serializers import TestSerializers,TestWJ

# Create your views here.
class TestViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = TestWJ.objects.all()
    serializer_class = TestSerializers
    
    def list(self, request, *args, **kwargs):
        test = TestWJ.objects.create()
        return super().list(request, *args, **kwargs)