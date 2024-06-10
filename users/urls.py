from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserRegisterViewSet, UserLoginViewSet, UserLogoutViewSet,request_password_update,confirm_user_passcode,reset_password

router = DefaultRouter()
# router.register(r'profiles',UserProflieViewSet,basename='users')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'logout', UserLogoutViewSet, basename='logout')
router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('request_password_update',request_password_update, name="request_password_update"), 
    path('confirm_user_passcode', confirm_user_passcode, name="confirm_user_passcode"),
    path('reset_password', reset_password, name="reset_password"),
]
