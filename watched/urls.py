from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchedViewSet,WatchedDeleteAPIVIew

router = DefaultRouter()
router.register(r'',WatchedViewSet,basename="watched")
urlpatterns = [
    path('',include(router.urls)),
    path('delete/<int:user_id>/<int:movie_id>/',WatchedDeleteAPIVIew.as_view(),name='delete')
]
