import random
import string
from django.core.cache import cache
from src.apps.authentication.exceptions import OTPExpired, OTPVerificationError
import uuid
from src.apps.authentication.models import EmsUser
from rest_framework_simplejwt.tokens import RefreshToken

class OTP:
    def generate_otp(self, id, length = 6) -> str:
        otp = ''.join([random.choice(string.digits) for _ in range(length)])
        self.store_otp_to_cache(id, otp)
        return otp
    
    def store_otp_to_cache(self, id, otp, timeout=300) -> None:
        cache.set(f'otp_{id}', otp, timeout)

    def verify_otp(self, id, raw_otp) -> bool:
        otp: str = cache.get(f'otp_{id}')
        
        if not otp:
            raise OTPExpired()
        
        if otp == raw_otp:
            return True

        return False
    

def create_auth_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}