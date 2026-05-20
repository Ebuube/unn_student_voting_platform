import secrets

def generate_otp(length=6) -> str:
     "Generates random OTP code of specified length."
     otp = secrets.randbelow(10 ** length)

     return str(otp).zfill(length)
