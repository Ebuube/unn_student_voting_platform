"""
Model for Registry Upload
"""
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String, ForeignKey

from app.models.base import Base


class RegistryUploadStatus(str, PyEnum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class RegistryUpload(Base):
    __tablename__ = "registry_uploads"

    id = Column(Integer, primary_key=True, index=True)

    election_id = Column(
        Integer,
        ForeignKey("elections.id"),
        nullable=False,
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    file_name = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)

    total_rows = Column(Integer, default=0)
    invalid_rows = Column(Integer, default=0)

    status = Column(
        Enum(RegistryUploadStatus),
        nullable=False,
        default=RegistryUploadStatus.PROCESSING,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
