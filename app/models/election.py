"""
Election Model
"""
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

import enum

from app.models.base import Base


class ElectionStatus(str, enum.Enum):
    """Enumeration for election status"""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
    ARCHIVED = "ARCHIVED"


class Election(Base):
    """Model representing an election"""
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(Enum(ElectionStatus), default=ElectionStatus.DRAFT,
                    nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)

    is_anonymous = Column(Boolean, default=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relatptionships
    registry_uploads = relationship(
        "RegistryUpload",
        back_populates="election",
    )
    voters = relationship("ElectionVoterRegistry", back_populates="election")
