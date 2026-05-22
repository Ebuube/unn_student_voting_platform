# test_accreditation_service.py

from pprint import pprint

from sqlalchemy import select

from app.db import SessionLocal
from app.models.user import User
from app.models.election import Election
from app.models.accreditation import (
    Accreditation
)
from app.services.accreditation import (
    accredit_user_for_election
)


def main():
    db = SessionLocal()

    try:
        # replace with existing values in your DB
        election_id = 1
        reg_number = "2021/243067"

        # fetch user
        user = db.scalar(
            select(User).where(
                User.reg_number == reg_number
            )
        )

        if not user:
            print("User not found")
            return

        # fetch election
        election = db.scalar(
            select(Election).where(
                Election.id == election_id
            )
        )

        if not election:
            print("Election not found")
            return

        # run accreditation
        accreditation = accredit_user_for_election(
            db,
            election_id=election_id,
            user=user
        )

        print("\nACCREDITATION CREATED/FETCHED\n")

        pprint({
            "id": accreditation.id,
            "election_id": accreditation.election_id,
            "user_id": accreditation.user_id,
            "registry_row_id": accreditation.registry_row_id,
            "accredited_at": accreditation.accredited_at,
        })

        # verify from DB
        existing = db.scalar(
            select(Accreditation).where(
                Accreditation.election_id == election_id,
                Accreditation.user_id == user.id
            )
        )

        print("\nDB VERIFICATION\n")

        pprint({
            "exists": existing is not None
        })

    except Exception as e:
        print(f"\nERROR: {str(e)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
