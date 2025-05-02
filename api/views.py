from django.shortcuts import render
from ems.emsmodels import *
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework import status
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.transaction import atomic
import time

# API's
from .views_invite import *
from .views_event import *


class UserRegistration(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    # queryset = EmsUser.objects.all()
    # serializer_class = UserRegistrationSerializer

    @method_decorator(atomic)
    def post(self, req):
        serializer = UserRegistrationSerializer(data=req.data)

        if serializer.is_valid():
            # valid_data = serializer.validated_data
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            print(str(refresh))
            print(str(refresh.access_token))
            
            return Response(data={'refresh': str(refresh), 'access': str(refresh.access_token)},status= status_code.HTTP_201_CREATED)
        else:
            return Response({'status': status_code.HTTP_400_BAD_REQUEST, 'data': f'Invalid data. \n {serializer.error_messages}'})


class UserLogout(APIView):
    def get(self, req):
        req.COOKIES.clear()
        return Response({"status": status.HTTP_200_OK, "data": "Logout Successful!"})