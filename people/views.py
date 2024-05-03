from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PersonSerializers
from .models import Person
# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    