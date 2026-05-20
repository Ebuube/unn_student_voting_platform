"""
Utility functions for the application.
"""
def normalize_reg_number(reg_number: str) -> str:
    return reg_number.strip().replace(" ", "").upper()
