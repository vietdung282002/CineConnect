from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowViewSet

router = DefaultRouter()
router.register(r'',FollowViewSet,basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
