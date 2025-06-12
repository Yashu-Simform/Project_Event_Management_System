from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from src.apps.events.models import Event
from src.apps.invitations.models import Invite
from src.apps.events.serializers import EventSerializer

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
            "sent_from",
            "sent_to",
            "status",
            "create_timestamp",
            "event",
            "receiver_email",
            "event_id",
            'req_type'
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

class InvitedListSerializer(serializers.ModelSerializer):
    event = EventSerializer()   # Nested serializer simply JOINS the relations
 
    class Meta:
        model = Invite
        fields = ['event', 'receiver_email', 'status']
 


# class InvitedListSerializer(serializers.ModelSerializer):
#     # event = serializers.StringRelatedField()
#     event = serializers.SerializerMethodField(source="event_invites")

#     class Meta:
#         model = Invite
#         fields = ['event', 'receiver_email', 'status']