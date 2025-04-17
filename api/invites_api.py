from django.urls import path, include
from .views import *

urlpatterns = [
    path("save/", CreateInvite.as_view(), name="create_invite"),
    path(
        "invitation-response/<int:invite_id>/<status>/",
        ResponseToInvitation.as_view(),
        name="invitation_response",
    ),
    path(
        "invited-list/",
        UserInviteListView.as_view(),
        name="invited_list"
    )
]
