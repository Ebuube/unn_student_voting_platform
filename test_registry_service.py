"""
Test if Registry Service works
"""
from pprint import pprint

from app.db import SessionLocal
from app.services.registry import ingest_registry


def load_csv_file():
    with open("sample_registry_upload.csv", "r") as f:
        return f.read()

def run_test():
    file_content = load_csv_file()

    with SessionLocal() as session:
        result = ingest_registry(
            session=session,
            election_id=1,
            uploaded_by=1,
            file_name="sample_registry_upload.csv",
            file_content=file_content,
        )

        print("\n===== REGISTRY UPLOAD RESULT =====")
        pprint(result)

if __name__ == "__main__":
    run_test()
