from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OTP(Base):
    __tablename__ = "otp"

    id: Mapped[int] = mapped_column(primary_key=True)

    reg_number: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    otp_code: Mapped[str] = mapped_column(
        String(6),
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
