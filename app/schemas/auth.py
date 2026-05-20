from pydantic import BaseModel


class OTPRequest(BaseModel):
    reg_number: str


class OTPVerify(BaseModel):
    reg_number: str
    otp_code: str
