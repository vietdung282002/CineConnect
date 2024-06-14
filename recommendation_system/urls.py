from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import add


urlpatterns = [
    path('add/',add, name="recommend"), 
]
