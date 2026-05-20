from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.auth.jwt import create_access_token
from app.auth.otp import generate_otp
from app.db import SessionLocal
from app.models.otp import OTP
from app.models.user import User
from app.schemas.auth import OTPRequest, OTPVerify


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/request-otp")
def request_otp(payload: OTPRequest):
    with SessionLocal() as db:

        user = db.scalar(
            select(User).where(
                User.reg_number == payload.reg_number,
            )
        )

        if not user:
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Disallow same user from having multiple otps active
        existing_otps = db.scalars(
            select(OTP).where(
                OTP.reg_number == payload.reg_number,
            )
        ).all()

        for otp in existing_otps:
            db.delete(otp)

        # Create New OTP
        otp = generate_otp()
        otp_entry = OTP(
            reg_number=payload.reg_number,
            otp_code=otp,
            expires_at=datetime.now(UTC) + timedelta(minutes=5),
        )

        db.add(otp_entry)
        db.commit()

        # Here you would send the OTP to the user's email
        print(f"OTP for {payload.reg_number}: {otp}")

    return {
        "message": "OTP generated",
        "otp": otp,
    }

@router.post("/verify-otp")
def verify_otp(payload: OTPVerify):
    with SessionLocal() as db:
        otp_entry = db.scalar(
            select(OTP).where(
                OTP.reg_number == payload.reg_number,
                OTP.otp_code == payload.otp_code,
            )
        )

        if not otp_entry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        if otp_entry.expires_at < datetime.now(UTC):
            # Delete expired otp from database
            db.delete(otp_entry)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        user = db.scalar(
            select(User).where(
                User.reg_number == payload.reg_number,
            )
        )

        token = create_access_token(data={
            "sub": user.reg_number,
            "user_id": user.id,
        })

        # Optionally, you can delete the OTP entry after successful verification
        db.delete(otp_entry)
        db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
    }
