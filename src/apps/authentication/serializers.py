from rest_framework import serializers
from src.apps.authentication.models import EmsUser
from core.validators import user_model_validations
from django.core.validators import validate_email
from src.apps.authentication.utils import OTP


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = EmsUser
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"email": {"validators": [validate_email]}}

    def validate(self, data: dict):
        email: str = data.get("email", "")
        data["username"] = email.strip().split("@")[0]
        return data

    def validate_password(self, value):
        try:
            return user_model_validations.validate_password(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        user = EmsUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = EmsUser
        fields = ["email", "password"]

class OTPVerify(serializers.Serializer):
    id = serializers.IntegerField()
    raw_otp = serializers.CharField(max_length=6)

    def validate_raw_otp(self, value:str):
        if not value.isdigit():
            serializers.ValidationError("TypeError: Not a valid OTP!")
        return value
