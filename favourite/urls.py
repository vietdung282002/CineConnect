from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FavouriteViewSet, FavouriteDeleteAPIVIew

router = DefaultRouter()
router.register(r'', FavouriteViewSet, basename="favourite")
urlpatterns = [
    path('', include(router.urls)),
    path('delete/<int:user_id>/<int:movie_id>/', FavouriteDeleteAPIVIew.as_view(), name='delete')
]
