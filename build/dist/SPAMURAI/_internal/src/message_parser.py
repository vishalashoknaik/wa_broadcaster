class MessagePools:
    """Represents separate pools of first messages and followup messages"""

    def __init__(self, first_messages, followup_messages):
        self.first_messages = first_messages  # List of first message strings
        self.followup_messages = followup_messages  # List of followup message strings


def parse_from_google_sheets(rows):
    """
    Parse Google Sheets rows into separate message pools for independent random selection

    Expected Google Sheet format:
    Row 1: Headers (First Messages | Followup Messages)
    Row 2+: Data rows with messages in each column (independent pools)

    Example:
    | First Messages      | Followup Messages        |
    |---------------------|--------------------------|
    | Hey <nick_name>! 👋 | Let me know!             |
    | Hello <nick_name>!  | Would love to hear back. |
    | Hi <nick_name>,     | Thanks!                  |
    |                     | Reply when you can.      |

    Args:
        rows: List of rows from CSV

    Returns:
        MessagePools object with separate first and followup message lists

    Raises:
        ValueError: If no valid messages found
    """
    first_messages = []
    followup_messages = []

    for i, row in enumerate(rows):
        if not row:  # Skip completely empty rows
            continue

        # Extract first message from column A
        if len(row) > 0 and row[0].strip():
            first_messages.append(row[0].strip())

        # Extract followup message from column B
        if len(row) > 1 and row[1].strip():
            followup_messages.append(row[1].strip())

    if not first_messages:
        raise ValueError("No valid first messages found in Google Sheet (Column A)")

    # Followup messages are optional
    if not followup_messages:
        followup_messages = []

    return MessagePools(first_messages, followup_messages)
