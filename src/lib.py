import random
import re
import time

import unicodedata


def random_sleep(n):
    """Sleep for a random duration between 0.5n and 1.5n seconds."""
    duration = random.uniform(0.5 * n, 1.5 * n)
    time.sleep(duration)


def normalize_phone(phone: str) -> str:
    """Normalize phone number to 10-digit format for comparison and storage.

    Args:
        phone: Raw phone number string

    Returns:
        10-digit normalized phone number (without country code)
    """
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


def format_phone_for_whatsapp(phone: str, country_code: str = "91") -> str:
    """Format phone number for WhatsApp Web with country code.

    Normalizes the phone number to 10 digits and prepends the country code.
    Only returns a formatted number if the normalized result is exactly 10 digits.

    Args:
        phone: Raw phone number string
        country_code: Country code to prepend (default: "91" for India)

    Returns:
        Phone number with country code (e.g., "919876543210") if valid,
        empty string if invalid
    """
    # First normalize to get clean 10-digit number
    normalized = normalize_phone(phone)

    # Validate it's exactly 10 digits
    if not normalized or len(normalized) != 10:
        return ""

    # Add country code for WhatsApp Web
    return f"{country_code}{normalized}"