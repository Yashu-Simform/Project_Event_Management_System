from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ems.emsmodels import *

#User Serializers
class UserBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


# Event Serializers
class EventBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Event
        fields = '__all__'

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'host', 'description', 'event_type', 'venue', 'event_time'] 

        read_only_fields = ['host']


class PublicEventsListSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Event
        fields = ['event_id', 'title', 'host', 'event_time', 'venue', 'total_participants']


# Invite Module
class InviteBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'

class CreateInviteSerializer(InviteBaseSerializer):
    pass