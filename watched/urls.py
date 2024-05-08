from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchedViewSet

router = DefaultRouter()
router.register(r'',WatchedViewSet,basename="watched")
urlpatterns = [
    path('',include(router.urls))
]
