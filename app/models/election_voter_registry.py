"""
Election Voter Registry Model Module
"""
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from app.models.base import Base


class ElectionVoterRegistry(Base):
    """Model representing a voter registry entry for an election"""
    __tablename__ = "election_voter_registry"

    __table_args__ = (
        UniqueConstraint(
            "election_id",
            "reg_number",
            name="uq_election_reg_number",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    election_id = Column(
        Integer,
        ForeignKey("elections.id"),
        nullable=False,
    )

    upload_id = Column(
        Integer,
        ForeignKey("registry_uploads.id"),
        nullable=False,
    )

    reg_number = Column(String, nullable=False)

    full_name = Column(String, nullable=False)

    email = Column(String, nullable=True)

    phone_number = Column(String, nullable=False)

    department_code = Column(String, nullable=False)

    level = Column(String, nullable=False)

    year_of_graduation = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
