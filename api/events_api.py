from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', CreateEvent.as_view(), name='create_event'),
    path('public-event-list/', PublicEventList.as_view(), name='public_event_list'),
    path('<int:event_id>/retrive/', EventRetrive.as_view(), name='event_retrive'),
    path('<int:event_id>/update/', EventUpdate.as_view(), name='event_update'),
    path('<int:event_id>/delete/', EventDelete.as_view(), name='event_delete'),
    path('event-choices/', EventChoiceData.as_view(), name='event_choice_data')
]
