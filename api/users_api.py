from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('newtoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshed-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='verify_token'),
    path('events-list/', UserEventsList.as_view(), name='user_event_list'),
]