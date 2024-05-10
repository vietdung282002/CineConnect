from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ReviewDetailSerializer, Review
# Create your views here.

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    http_method_names = ['get']
    
    
