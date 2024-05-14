from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet,ReactionViewSet

router = DefaultRouter()
router.register(r'comment',CommentViewSet ,basename='comment')
router.register(r'reaction',ReactionViewSet ,basename='reaction')
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
