from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ActivityViewsets

router = DefaultRouter()
router.register(r'', ActivityViewsets, basename="favourite")
urlpatterns = [
    path('', include(router.urls)),
]
