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
from .utils import send_invite_mail


class CreateInvite(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        invite_data = request.data
        print(invite_data)
        event_id = invite_data['event_id'] if 'event_id' in invite_data else None

        if not event_id:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Event ID is required!'})
        
        invite_data.pop('event_id')

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
            receiver_mail = serializer.validated_data['email']
            serializer.validated_data.pop('email')
            instance = serializer.save(invite_from = self.request.user, invite_to = invite_to, event = event)

            try:
                context = {
                    'title': event.title,
                    'description': event.description,
                    'venue': event.venue,
                    'event_time': event.event_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    'invite_id': instance.invite_id,
                }
                send_invite_mail(f"Invitation for event: {event.title}", context, [receiver_mail])
            except Exception as e:
                print(f"Error sending email: {e}")
                return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Unable to send email!'})

            return Response({'status': status.HTTP_200_OK, 'message': 'Invite Sent Successfully!'})
        else:
            print(serializer.errors)
        
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Data!'})


class ResponseToInvitation(APIView):
    def get(self, req, invite_id, status):
        invite = Invite.objects.get(invite_id=invite_id) if invite_id else None
        if not invite:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Invite not found!'})
        
        if status == True:
            invite.status = 'Accepted'
            invite.save()
            return Response({'status': status.HTTP_200_OK, 'message': 'Invite Accepted!'})
        else:
            invite.status = 'Declined'
            invite.save()
            return Response({'status': status.HTTP_200_OK, 'message': 'Invite Declined!'})
        
