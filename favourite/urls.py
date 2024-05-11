from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FavouriteViewSet

router = DefaultRouter()
router.register(r'', FavouriteViewSet, basename="favourite")
urlpatterns = [
    path('', include(router.urls)),
]
