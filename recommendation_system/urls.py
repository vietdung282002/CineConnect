from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import add,cal_cosine_simulator


urlpatterns = [
    path('add/',add, name="recommend"), 
    path('calCosineSimulator/',cal_cosine_simulator, name="get"), 
]
