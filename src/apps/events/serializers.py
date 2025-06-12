from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from src.apps.events.models import Event

# Event Serializers
class EventBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "host", "description", "event_type", "venue", "event_time"]

        read_only_fields = ["host"]

    def validate_event_time(self, value):
        if (value - timedelta(hours=1)) <= timezone.now():
            raise serializers.ValidationError('Event time must be of after 1 hour of the time of creation of event.')
        
        return value


class PublicEventsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "event_id",
            "title",
            "host",
            "event_time",
            "venue",
            "total_participants",
        ]


class EventChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["event_id", "title"]

        read_only_fields = ["event_id", "title"]


class EventListSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_id', 'title', 'venue', 'event_time']
 
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'