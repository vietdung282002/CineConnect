from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet

router = DefaultRouter()
router.register(r'', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
]
