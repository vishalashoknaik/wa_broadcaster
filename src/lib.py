import random
import re
import time

import unicodedata


def random_sleep(n):
    """Sleep for a random duration between 0.5n and 1.5n seconds."""
    duration = random.uniform(0.5 * n, 1.5 * n)
    time.sleep(duration)


def normalize_phone(phone: str) -> str:
    phone = str(phone).replace(".0", "") if phone else ""

    if not phone:
        return ""


    # Normalize weird unicode characters
    phone = unicodedata.normalize("NFKC", phone)

    # Keep only digits
    digits = re.sub(r"\D", "", phone)

    # Remove leading country code or '0'
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]

    # Ensure it is 10-digit
    if len(digits) == 10:
        return digits
    else:
        # If invalid, return as-is (or could return "")
        return digits