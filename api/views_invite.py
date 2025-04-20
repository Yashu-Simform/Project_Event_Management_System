from django.shortcuts import render
from ems.emsmodels import *
from django.db import connection
from rest_framework.views import APIView
from rest_framework import generics, mixins
# from django.contrib.auth.models import User
from ems.emsmodels import EmsUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status as status_code
from .utils import send_mail_ems
from datetime import datetime


class CreateInvite(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite_data = request.data

        serializer = CreateInviteSerializer(data=invite_data)

        if serializer.is_valid():

            try:
                invite_to = EmsUser.objects.get(
                    email=serializer.validated_data["receiver_email"]
                )
            except:
                #   Reference to an anonymous user.
                invite_to = EmsUser.objects.get(id=0)
            instance = serializer.save(
                invite_from=self.request.user, invite_to=invite_to
            )

            return Response(
                {
                    "status": status_code.HTTP_200_OK,
                    "data": "Invite Sent Successfully!",
                }
            )
        else:
            print(serializer.errors)

        return Response(
            {"status": status_code.HTTP_400_BAD_REQUEST, "data": "Invalid Data!"}
        )


class ResponseToInvitation(APIView):
    def get(self, req, invite_id, status):
        invite = Invite.objects.get(invite_id=invite_id) if invite_id else None
        if not invite:
            return Response(
                {
                    "status": status_code.HTTP_404_NOT_FOUND,
                    "data": "Invite not found!",
                }
            )

        if status == "Accepted":
            invite.status = "Accepted"
            invite.save()
            return Response(
                {"status": status_code.HTTP_200_OK, "data": "Invite Accepted!"}
            )
        elif status == "Declined":
            invite.status = "Declined"
            invite.save()
            return Response(
                {"status": status_code.HTTP_200_OK, "data": "Invite Declined!"}
            )

        return Response(
            {
                "status": status_code.HTTP_400_BAD_REQUEST,
                "data": "Invalid query params!",
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
    
class ParticipateInvite(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, req):
        data = req.data

        serializer = CreateInviteSerializer(data=data)

        if serializer.is_valid():
            try:
                invite_to = EmsUser.objects.get(id=data['host'])
            except:
                return Response({'status': status_code.HTTP_404_NOT_FOUND, 'data': 'User not found!'})
            
            serializer.save(invite_from=self.request.user, invite_to=invite_to, receiver_email=invite_to.email, req_type='participation')
        
            return Response({'status': status_code.HTTP_200_OK, 'data': 'Invite Sent Successfully!'})
        else:
            return Response({'status': status_code.HTTP_400_BAD_REQUEST, 'data': serializer.errors})