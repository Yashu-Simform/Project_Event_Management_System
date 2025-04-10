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

    def post(self, request, *args, **kwargs):
        invite_data = request.data
        invite_data.pop('csrfmiddlewaretoken')

        serializer = CreateInviteSerializer(**invite_data)

        if serializer.is_valid():
            serializer.save(invite_from = self.request.user)
            pass
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': ''})