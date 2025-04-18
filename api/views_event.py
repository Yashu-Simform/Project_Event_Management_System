from django.shortcuts import render
from ems.emsmodels import *
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status
from rest_framework import status


class EventChoiceData(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventChoicesSerializer

    def get_queryset(self):
        # print(dir(self.request))
        print(type(self.request.user))

        qs = Event.objects.all()
        return qs
