from django.shortcuts import render
from ems import emsmodels
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import *

# API's

class PublicEventList(generics.ListAPIView):
    queryset = emsmodels.Event.objects.filter(event_type = 'public')
    serializer_class = PublicEventsListSerializer


class CreateEvent(generics.CreateAPIView):
    queryset = emsmodels.Event.objects.all()
    serializer_class = CreateEventSerializer

class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# class UserLogin(APIView):
#     def post(self, req):
#         if req.data:
#             serializer = UserLoginSerializer(data=req.data)
#             if serializer.is_valid():
#                 return Response()
#         return Response()