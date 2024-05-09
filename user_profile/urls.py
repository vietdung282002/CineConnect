from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_profile.views import UserProfileViewSet

router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]