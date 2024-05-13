from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserRegisterViewSet, UserLoginViewSet, UserLogoutViewSet

router = DefaultRouter()
# router.register(r'profiles',UserProflieViewSet,basename='users')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'logout', UserLogoutViewSet, basename='logout')
router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
