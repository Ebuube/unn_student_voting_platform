"""
Utility functions for the CSV parser for Registry Upload
"""
import csv
import re

from io import StringIO
from typing import Sequence
from email_validator import validate_email, EmailNotValidError


def normalize_reg_number(reg_number: str) -> str:
    return reg_number.strip().replace(" ", "").upper()

def validate_and_clean_contact(email_str: str = "", phone_str: str = "") -> dict[str, str | None]:
    cleaned_email = None
    cleaned_phone = None

    # Validate Email
    if email_str:
        try:
            email_info = validate_email(email_str.strip())
            cleaned_email = email_info.email.lower()
        except EmailNotValidError:
            email_msg = f"Invalid email format: {email_str}"
            raise EmailNotValidError(email_msg)

    # Validate Phone Number
    if phone_str:
        # remove spaces, hyphens, brackets
        cleaned_phone = re.sub(r"[^\d+]", "", phone_str.strip())

        # handle +234 or 234 prefix
        if cleaned_phone.startswith("+234"):
            cleaned_phone = cleaned_phone[4:]
        elif cleaned_phone.startswith("234"):
            cleaned_phone = cleaned_phone[3:]

        # remove leading zero if present
        if cleaned_phone.startswith("0"):
            cleaned_phone = cleaned_phone[1:]

        # Confirm Nigerian phone number is 10 digits after stripping
        if not re.fullmatch(r"\d{10}", cleaned_phone):
            raise ValueError(
                f"Invalid Nigerian phone number format: {phone_str}",
            )

    return {
        "email": cleaned_email,
        "phone": cleaned_phone,
    }


EXPECTED_HEADERS = [
    "reg_number",
    "full_name",
    "email",
    "phone_number",
    "department_code",
    "level",
    "year_of_graduation",
]

def validate_csv_headers(headers: Sequence[str] | None) -> bool:
    if headers is None:
        raise ValueError("CSV file is missing headers")

    headers = list(headers)
    normalized_headers = [header.strip().lower() for header in headers]
    return all(expected in normalized_headers for expected in EXPECTED_HEADERS)

def parse_csv(file_content: str):
    valid_rows = []
    invalid_rows = []

    csv_file = StringIO(file_content)
    reader = csv.DictReader(csv_file)

    if not validate_csv_headers(reader.fieldnames):
        raise ValueError("CSV file is missing required headers")

    seen_reg_numbers = set()

    for row_number, row in enumerate(reader, start=2):

        reg_number = normalize_reg_number(row["reg_number"])
        full_name = row["full_name"].strip().upper()
        email_str = row["email"].strip().lower()
        phone_str = row["phone_number"].strip()

        if not reg_number or not full_name:
            invalid_rows.append({
                "row": row_number,
                "reason": "Missing required fields (reg_number or full_name)",
            })
            continue

        if reg_number in seen_reg_numbers:
            invalid_rows.append({
                "row": row_number,
                "reason": f"Duplicate reg_number: {reg_number}",
            })
            continue

        seen_reg_numbers.add(reg_number)

        if not email_str or not phone_str:
            invalid_rows.append({
                "row": row_number,
                "reason": "Missing contact information (email or phone_number)",
            })
            continue

        # Sanitize contact information
        try:
            contact_info = validate_and_clean_contact(email_str, phone_str)
        except (EmailNotValidError, ValueError) as e:
            invalid_rows.append({
                "row": row_number,
                "reason": str(e),
            })
            continue

        valid_rows.append({
            "reg_number": reg_number,
            "full_name": full_name,
            "email": contact_info["email"],
            "phone_number": contact_info["phone"],
            "department_code": row["department_code"].strip().upper(),
            "level": row["level"].strip().upper(),
            "year_of_graduation": int(row["year_of_graduation"].strip()),
        })

    return {
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "total_rows": len(valid_rows) + len(invalid_rows),
    }
