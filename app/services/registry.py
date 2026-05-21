import hashlib

from sqlalchemy.orm import Session

from app.db import get_db
from app.models.registry_upload import RegistryUpload, RegistryUploadStatus
from app.models.election_voter_registry import ElectionVoterRegistry
from utils.csv_parser import parse_csv

def compute_file_hash(file_content: str) -> str:
    return hashlib.sha256(file_content.encode("utf-8")).hexdigest()

def ingest_registry(
    session: Session,
    election_id: int,
    uploaded_by: int,
    file_name: str,
    file_content: str
):
    """
    Ingests a voter registry CSV file for a given election

    Steps:
    1. Compute file hash for deduplication
    2. Create a RegistryUpload record with status PROCESSING
    3. Parse the CSV content
    4. For each valid row, create an ElectionVoterRegistry object
    5. Bulk insert valid rows into the database
    6. Update the RegistryUpload record with total rows, invalid rows, and final status
    7. Commit the transaction
    8. Return a summary of the upload process
    """
    file_hash = compute_file_hash(file_content)

    upload = RegistryUpload(
        election_id=election_id,
        uploaded_by=uploaded_by,
        file_name=file_name,
        file_hash=file_hash,
        status=RegistryUploadStatus.PROCESSING
    )

    session.add(upload)
    session.flush()

    try:
        parsed = parse_csv(file_content)
    except Exception as e:
        upload.status = RegistryUploadStatus.FAILED
        session.commit()
        raise e

    valid_rows = parsed["valid_rows"]
    invalid_rows = parsed["invalid_rows"]

    # Build DB Objects
    db_objects = []

    for row in valid_rows:
        obj = ElectionVoterRegistry(
            election_id=election_id,
            upload_id=upload.id,
            reg_number=row["reg_number"],
            full_name=row["full_name"],
            email=row["email"] or None,
            phone_number=row["phone_number"],
            department_code=row["department_code"],
            level=row["level"],
            year_of_graduation=row["year_of_graduation"],
        )

        db_objects.append(obj)

    # Bulk insert
    session.bulk_save_objects(db_objects)

    # Update Upload Record
    upload.total_rows = parsed["total_rows"]
    upload.invalid_rows = len(parsed["invalid_rows"])

    # Determine final status
    if len(valid_rows) == 0:
        upload.status = RegistryUploadStatus.FAILED
    elif len(invalid_rows) > 0:
        upload.status = RegistryUploadStatus.COMPLETED # Partial success
    else:
        upload.status = RegistryUploadStatus.COMPLETED

    # Commit Transaction
    session.commit()

    return {
        "upload_id": upload.id,
        "total_rows": upload.total_rows,
        "invalid_rows": parsed["invalid_rows"],
        "inserted_rows": len(valid_rows),
        "status": upload.status,
    }
