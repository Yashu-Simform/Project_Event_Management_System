from django.shortcuts import render
from ems import emsmodels
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status
from rest_framework import status


class CreateInvite(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, *args, **kwargs):
        invite_data = request.data

        serializer = CreateInviteSerializer(data=invite_data)

        if serializer.is_valid():
            #   Get event from db.
            try:
                event = Event.objects.get(event_id = event_id)
                print(event.title)
            except:
                return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Event not found!'})

            #   Check participant exist in user db.
            try:
                invite_to = User.objects.get(email=serializer.validated_data['email'])
            except:
                #   Reference to an anonymous user.
                invite_to = User.objects.get(id=0)

            serializer.validated_data.pop('email')

            serializer.save(invite_from = self.request.user, invite_to = invite_to, event = event)

            return Response({'status': status.HTTP_200_OK, 'message': 'Invite Sent Successfully!'})
        else:
            print(serializer.errors)
        
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Data!'})
