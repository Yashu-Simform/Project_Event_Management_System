from django.urls import path, include
from .views import *

urlpatterns = [
    path("event/", include("api.events_api")),
    path("user/", include("api.users_api")),
    path("invite/", include("api.invites_api")),
]
