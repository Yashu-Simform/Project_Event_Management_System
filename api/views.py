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

from .views_invite import *
from .views_event import *

# API's


class PublicEventList(generics.ListAPIView):
    queryset = Event.objects.filter(event_type="public")
    serializer_class = PublicEventsListSerializer

    @method_decorator(cache_page(60 * 3 * 1, key_prefix="public_events_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        time.sleep(3)
        return super().get_queryset()


class CreateEvent(APIView):

    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "create_event"

    def post(self, request, *args, **kwargs):
        print(self.request.user.id)

        if not self.request.user.is_authenticated:
            print("User is not authenticated!")
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "data": "Unauthorized Request!",
                }
            )

        eventdata = request.data
        eventdata.pop("csrfmiddlewaretoken")
        print(eventdata)
        # eventdata['host'] = self.request.user
        serializer = CreateEventSerializer(data=eventdata)
        if not serializer.is_valid():
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "data": f"Invalid Data! Error: {serializer.errors}"}
            )

        serializer.save(host=self.request.user)

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "data": "Event created successfully!",
            }
        )


class EventRetrive(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventBaseSerializer
    lookup_field = "event_id"


class EventUpdate(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer
    lookup_field = "event_id"


class EventDelete(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventBaseSerializer
    lookup_field = "event_id"


class UserEventsList(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventBaseSerializer

    def get_queryset(self):
        print(self.request.user)
        user_id = self.request.user.id
        qs = Event.objects.filter(host=user_id)
        return qs


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


# class UserLogin(APIView):
#     def post(self, req):
#         if req.data:
#             serializer = UserLoginSerializer(data=req.data)
#             if serializer.is_valid():
#                 return Response()
#         return Response()
