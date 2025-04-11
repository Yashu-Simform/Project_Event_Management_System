from django.urls import path
from .views import *

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome_page'),
    path('user/register/', UserRegistration.as_view(), name='user_registration_page'),
    path('user/login/', UserLogin.as_view(), name='user_login_page'),
    path('user/logout/', UserLogout.as_view(), name='user_logout_page'),
    path('event/create/page/', CreateEvent.as_view(), name='event_create_page'),
    path('user/dashboard/', UserDashboard.as_view(), name='user_dashboard'),
    path('user/dashboard/myevents/', MyEventsView.as_view(), name='user_dashboard_myevents_page'),
    path('user/dashboard/invitations/', InvitationsView.as_view(), name='user_dashboard_invitations_page'),
    path('event/<int:event_id>/retrive/', EventDetail.as_view(), name='event_details'),
    path('event/<int:event_id>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/update/', EventUpdateView.as_view(), name='event_update_page'),
]
    