class OTPExpired(Exception):
    def __init__(self, msg = "OTP has been expired!"):
        self.msg = msg
    
    def __str__(self):
        return self.msg
    
class OTPVerificationError(Exception):
    def __init__(self, msg = "OTP verification failed!"):
        self.msg = msg

    def __str__(self):
        return self.msg