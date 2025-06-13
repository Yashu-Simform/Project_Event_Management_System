from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)  # Get user by email
        except User.DoesNotExist:
            return None

        if user and user.check_password(password):  # Verify password
            return user
        return None
