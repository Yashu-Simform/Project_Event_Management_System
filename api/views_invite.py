from django.shortcuts import render
from ems import emsmodels
from django.db import connection
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status as status_code
from .utils import send_invite_mail
from datetime import datetime


class CreateInvite(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite_data = request.data
        # print(invite_data)
        # event_id = invite_data['event_id'] if 'event_id' in invite_data else None

        # if not event_id:
        #     return Response({'status': status_code.HTTP_400_BAD_REQUEST, 'message': 'Event ID is required!'})

        # invite_data.pop('event_id')

        serializer = CreateInviteSerializer(data=invite_data)

        if serializer.is_valid():
            #   Get event from db.
            # try:
            #     event = Event.objects.get(event_id = event_id)
            # except:
            #     return Response({'status': status_code.HTTP_404_NOT_FOUND, 'message': 'Event not found!'})

            #   Check participant exist in user db.
            try:
                invite_to = User.objects.get(
                    email=serializer.validated_data["receiver_email"]
                )
            except:
                #   Reference to an anonymous user.
                invite_to = User.objects.get(id=0)
            instance = serializer.save(
                invite_from=self.request.user, invite_to=invite_to
            )

            return Response(
                {
                    "status": status_code.HTTP_200_OK,
                    "message": "Invite Sent Successfully!",
                }
            )
        else:
            print(serializer.errors)

        return Response(
            {"status": status_code.HTTP_400_BAD_REQUEST, "message": "Invalid Data!"}
        )


class ResponseToInvitation(APIView):
    def get(self, req, invite_id, status):
        invite = Invite.objects.get(invite_id=invite_id) if invite_id else None
        if not invite:
            return Response(
                {
                    "status": status_code.HTTP_404_NOT_FOUND,
                    "message": "Invite not found!",
                }
            )

        if status == "Accepted":
            invite.status = "Accepted"
            invite.save()
            return Response(
                {"status": status_code.HTTP_200_OK, "message": "Invite Accepted!"}
            )
        elif status == "Declined":
            invite.status = "Declined"
            invite.save()
            return Response(
                {"status": status_code.HTTP_200_OK, "message": "Invite Declined!"}
            )

        return Response(
            {
                "status": status_code.HTTP_400_BAD_REQUEST,
                "message": "Invalid query params!",
            }
        )

class InvitedListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Invite.objects.all()
    serializer_class = InvitedListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Invite.objects.filter(invite_from=user.id)
        # qs = Invite.objects.select_related('event').filter(invite_from=user.id)

        # qs = user.invite_from.all()
        # print([e.event.title for e in qs])
        return qs
    

class UserInviteListView(generics.ListAPIView):
    serializer_class = InvitedListSerializer
 
    def get_queryset(self):
        user = self.request.user
        qs = Invite.objects.filter(invite_from=user.id).select_related('event')
        return qs