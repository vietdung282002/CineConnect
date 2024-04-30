from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_profile.views import UserProflieViewSet

router = DefaultRouter()
router.register(r'',UserProflieViewSet,basename='users')

urlpatterns = [
    path('', include(router.urls)),
]