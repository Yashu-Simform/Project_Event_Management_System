from django.urls import path, include
from .views import *

urlpatterns = [
    path('save/', CreateInvite.as_view(), name='create_invite'),
]