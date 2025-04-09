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

# API's

class PublicEventList(generics.ListAPIView):
    queryset = emsmodels.Event.objects.filter(event_type = 'public')
    serializer_class = PublicEventsListSerializer


class CreateEvent(APIView):

    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.user.id)

        if not self.request.user.is_authenticated:
            print('User is not authenticated!')
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'message': 'Unauthorized Request!'})
        
        eventdata = request.data
        eventdata.pop('csrfmiddlewaretoken')
        print(eventdata)
        # eventdata['host'] = self.request.user
        serializer = CreateEventSerializer(data=eventdata)
        if not serializer.is_valid():
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Data!'})
        
        serializer.save(host=self.request.user)

        return Response({'status': status.HTTP_201_CREATED, 'message': 'Event created successfully!'})
    

class UserEventsList(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventBaseSerializer

    def get_queryset(self):
        print(self.request.user)
        user_id = self.request.user.id
        qs = Event.objects.filter(host=user_id)
        return qs


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserLogout(APIView):
    def get(self, req):
        req.COOKIES.clear()
        return Response({'status': status.HTTP_200_OK, 'message': 'Logout Successful!'})

# class UserLogin(APIView):
#     def post(self, req):
#         if req.data:
#             serializer = UserLoginSerializer(data=req.data)
#             if serializer.is_valid():
#                 return Response()
#         return Response()