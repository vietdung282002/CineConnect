from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TestViewset,schedule_task

router = DefaultRouter()
router.register(r'', TestViewset, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path("schedule", schedule_task, name="schedule")
]
