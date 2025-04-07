from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', CreateEvent.as_view(), name='create_event'),
    path('public-event-list/', PublicEventList.as_view(), name='public_event_list'),
]
