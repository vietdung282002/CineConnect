from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet,RatingDeleteAPIVIew,RatingUpdateAPIView

router = DefaultRouter()
router.register(r'', RatingViewSet, basename='rate')

urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:pk>',RatingUpdateAPIView.as_view(),name='update'),
    path('delete/<int:user_id>/<int:movie_id>/',RatingDeleteAPIVIew.as_view(),name='delete'),
]
