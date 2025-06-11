from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework import status
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.transaction import atomic
import time

from api.utils import success_response, error_response

from api import logger

class UserRegistration(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, req):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            logger.debug(str(refresh))
            logger.debug(str(refresh.access_token))
            
            return success_response(status=status.HTTP_200_OK, message='User Registration Successfull!', data={'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            logger.debug(serializer.errors)
            return error_response(status=status.HTTP_400_BAD_REQUEST, message='Invalid data', error=serializer.errors)

class UserLogout(APIView):
    def get(self, req):
        req.COOKIES.clear()
        return Response({"status": status.HTTP_200_OK, "data": "Logout Successful!"})