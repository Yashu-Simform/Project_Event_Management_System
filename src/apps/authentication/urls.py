from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from src.apps.authentication.views import *

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="user_registration"),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('otp-verify/', OTPVerification.as_view(), name='otp_verify'),
    path("newtoken/", TokenObtainPairView.as_view(), name="token_obtain_pair"), #TODO: Need to implement custom login view
    path("refreshed-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verifytoken/", TokenVerifyView.as_view(), name="verify_token"),
]