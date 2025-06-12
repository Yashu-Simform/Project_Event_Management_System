from src.apps.events.models import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.events.serializers import *
from rest_framework import status
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import time


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


class EventChoiceData(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventChoicesSerializer

    def get_queryset(self):
        # print(dir(self.request))
        print(type(self.request.user))

        qs = Event.objects.all()
        return qs
