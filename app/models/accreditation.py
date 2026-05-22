"""
Module for Election Accreditations
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)

from app.models.base import Base


class Accreditation(Base):
    """
    Model for Election Accreditations
    """
    __tablename__ = "accreditations"

    __table_args__ = (
        UniqueConstraint(
            "election_id",
            "user_id",
            name="uq_election_user_accreditation",
        ),
    )

    id = Column(Integer, primary_key=True)

    election_id = Column(
        Integer,
        ForeignKey("elections.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    registry_row_id = Column(
        Integer,
        ForeignKey("election_voter_registry.id", ondelete="CASCADE"),
        nullable=False,
    )

    accredited_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
