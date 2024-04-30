from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet

router = DefaultRouter()
router.register(r'',GenreViewSet,basename='genres')

urlpatterns = [
    path('', include(router.urls)),
]