from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotAuthenticated
from core.utils import success_response, error_response
from src.apps.authentication.utils import create_auth_token_pair
from src.apps.authentication.celery_tasks import send_otp_email
from core.settings import logging
from src.apps.authentication.exceptions import OTPExpired
from src.apps.authentication.services import get_user

class UserRegistration(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, req):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            # logger.debug(str(refresh))
            # logger.debug(str(refresh.access_token))

            return success_response(
                status=status.HTTP_200_OK,
                message="User Registration Successfull!",
                data={"refresh": str(refresh), "access": str(refresh.access_token)},
            )
        else:
            # logger.debug(serializer.errors)
            return error_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                error=serializer.errors,
            )


class UserLogout(APIView):
    def get(self, req):
        req.COOKIES.clear()
        return Response({"status": status.HTTP_200_OK, "data": "Logout Successful!"})


class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, req, *args):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            user = authenticate(
                req,
                email=serializer.validated_data.get("email", None),
                password=serializer.validated_data.get("password", None),
            )

            if not user:
                return error_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Invalid Credentials",
                    error=[],
                )
            
            # TODO: OTP Verification
            otpgen = OTP()
            send_otp_email(otp_as_context = otpgen.generate_otp(user.id), recipient_list=[user.email])

            return success_response(
                status=status.HTTP_200_OK,
                message="User Credentials Verified!",
                data={"id": user.id}
            )
        else:
            print(serializer.errors)
            return error_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                error=serializer.errors,
            )

class OTPVerification(APIView):
    serializr_class = OTPVerify

    def post(self, req, *args):
        serializer = self.serializr_class(data=req.data)
        
        if serializer.is_valid():
            try:
                otpgen = OTP()
                if otpgen.verify_otp(serializer.validated_data.get('id'), serializer.validated_data.get('raw_otp')):
                    logging.debug('OTP Verified!')
                    
                    user = get_user(serializer.validated_data.get('id'))
                    token_pair = create_auth_token_pair(user)

                    return success_response(
                        status=status.HTTP_200_OK,
                        message="Login Successfull!",
                        data=token_pair
                    )
                
                return error_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="OTP not verified!",
                    error={}
                )
                
            except OTPExpired as e:
                return error_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=str(e),
                    error={}
                )
            except Exception as e:
                return error_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=str(e),
                    error={}
                )
        else:
            logging.debug(serializer.errors)
            return error_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                error=serializer.errors,
            )
