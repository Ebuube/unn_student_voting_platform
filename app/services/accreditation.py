"""
Service Module for Accreditation
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.accreditation import Accreditation
from app.models.election_voter_registry import ElectionVoterRegistry


def accredit_user_for_election(
    db: Session,
    *,
    election_id: int,
    user: User,
) -> Accreditation:
    """
    Accredit a user for an election.

    Accreditation is successful only if:
    - user exists in election voter registry
    - user is not already accredited for the election
    """
    # Check existing accreditation
    existing_accreditation = db.scalar(
        select(Accreditation).where(
            Accreditation.election_id == election_id,
            Accreditation.user_id == user.id,
        ),
    )

    if existing_accreditation:
        return existing_accreditation

    # Match user against election voter registry
    registry_row = db.scalar(
        select(ElectionVoterRegistry).where(
            ElectionVoterRegistry.election_id == election_id,
            ElectionVoterRegistry.reg_number == user.reg_number,
        ),
    )

    if not registry_row:
        raise ValueError("User is not eligible for this election")

    accrediatation = Accreditation(
        election_id=election_id,
        user_id=user.id,
        registry_row_id=registry_row.id,
    )

    db.add(accrediatation)
    db.commit()
    db.refresh(accrediatation)

    return accrediatation
