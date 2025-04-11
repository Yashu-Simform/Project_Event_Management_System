from django.urls import path, include
from .views import *

urlpatterns = [
    path('<event_id>/save/', CreateInvite.as_view(), name='create_invite'),
]