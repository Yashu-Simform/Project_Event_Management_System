from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from ems.emsmodels import *
from rest_framework import status


# User Serializers
class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


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
        if value - timedelta(hours=1) <= timezone.now():
            raise serializers.ValidationError('Event time must be of after 5 minutes of the time of creation of event.')
        
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


# Invite Module
class InviteBaseSerializer(serializers.ModelSerializer):
    create_timestamp = serializers.DateTimeField(format="%B %d %Y %I:%M %p")

    class Meta:
        model = Invite
        fields = "__all__"


class CreateInviteSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Invite
        fields = [
            "invite_from",
            "invite_to",
            "status",
            "create_timestamp",
            "event",
            "receiver_email",
            "event_id",
        ]
        # fields.append('email')

    def validate(self, attrs):
        try:
            print("attrs", attrs)
            event_obj = Event.objects.get(event_id=attrs["event_id"])
            if event_obj.event_time - timedelta(minutes=10) <= timezone.now():
                raise serializers.ValidationError(
                    "Invite must be sent at least 10 minutes before the event!"
                )

            return attrs
        except Event.DoesNotExist as e:
            raise serializers.ValidationError(f"Event not found! Exception: {e}")
        except Exception as e:
            raise e

    def create(self, validated_data):
        try:
            validated_data["event"] = Event.objects.get(
                event_id=validated_data["event_id"]
            )

            instance = Invite.objects.create(**validated_data)
            return instance
        except Exception as e:
            raise e

    def invite_sent_validation(event: Event):
        event = Event.objects.get(event.event_id)

        if event.event_time - timedelta(minutes=10) <= timezone.now():
            serializers.ValidationError(
                "Invite must be sent at least 10 minutes before the event!"
            )


class EventListSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


# class InvitedListSerializer(serializers.ModelSerializer):
#     # event = serializers.StringRelatedField()
#     event = serializers.SerializerMethodField(source="event_invites")

#     class Meta:
#         model = Invite
#         fields = ['event', 'receiver_email', 'status']


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_id', 'title', 'venue', 'event_time']
 
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
 
class InvitedListSerializer(serializers.ModelSerializer):
    event = EventSerializer()   # Nested serializer simply JOINS the relations
 
    class Meta:
        model = Invite
        fields = ['event', 'receiver_email', 'status']
 
 