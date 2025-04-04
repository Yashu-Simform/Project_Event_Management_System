from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class EventBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Event
        fields = '__all__'

class InviteBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'