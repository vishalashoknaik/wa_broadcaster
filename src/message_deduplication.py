"""
Message Deduplication Module for SPAMURAI
Prevents sending the same message content to the same number multiple times.

This module tracks:
1. Message hashes mapped to numbers (with timestamps)
2. Message hashes mapped to actual message content

Files:
- message_sent_log.json: {hash: [{number, sent_at}, ...]}
- message_content_log.json: {hash: "actual message text"}
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path


class MessageDeduplication:
    """Handles message deduplication logic"""

    def __init__(self, sent_log_path, content_log_path):
        """
        Initialize message deduplication tracker

        Args:
            sent_log_path: Path to message_sent_log.json
            content_log_path: Path to message_content_log.json
        """
        self.sent_log_path = Path(sent_log_path)
        self.content_log_path = Path(content_log_path)

        # Load existing logs
        self.sent_log = self._load_json(self.sent_log_path)
        self.content_log = self._load_json(self.content_log_path)

    def _load_json(self, path):
        """Load JSON file, return empty dict if not exists"""
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {path}: {e}")
                return {}
        return {}

    def _save_json(self, path, data):
        """Save data to JSON file"""
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error: Could not save {path}: {e}")

    def compute_message_hash(self, message):
        """
        Compute SHA256 hash of message content

        Args:
            message: Message text to hash

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(message.encode('utf-8')).hexdigest()

    def has_sent_to_number(self, message, number):
        """
        Check if this exact message was already sent to this number

        Args:
            message: Message text
            number: Phone number

        Returns:
            tuple: (bool, datetime_str or None)
                   (True, timestamp) if already sent
                   (False, None) if not sent
        """
        msg_hash = self.compute_message_hash(message)

        # Check if this hash has any entries
        if msg_hash not in self.sent_log:
            return False, None

        # Check if this specific number is in the list
        for entry in self.sent_log[msg_hash]:
            if entry['number'] == number:
                return True, entry['sent_at']

        return False, None

    def record_sent(self, message, number):
        """
        Record that a message was sent to a number

        Args:
            message: Message text
            number: Phone number
        """
        msg_hash = self.compute_message_hash(message)
        timestamp = datetime.now().isoformat()

        # Update sent log
        if msg_hash not in self.sent_log:
            self.sent_log[msg_hash] = []

        # Add entry (number + timestamp)
        self.sent_log[msg_hash].append({
            'number': number,
            'sent_at': timestamp
        })

        # Update content log (only store message once per hash)
        if msg_hash not in self.content_log:
            self.content_log[msg_hash] = message

        # Save both files
        self._save_json(self.sent_log_path, self.sent_log)
        self._save_json(self.content_log_path, self.content_log)

    def get_message_by_hash(self, msg_hash):
        """
        Retrieve message content by hash

        Args:
            msg_hash: Message hash

        Returns:
            Message text or None if not found
        """
        return self.content_log.get(msg_hash)

    def get_sent_count_for_message(self, message):
        """
        Get total number of times this message was sent

        Args:
            message: Message text

        Returns:
            Number of recipients who received this message
        """
        msg_hash = self.compute_message_hash(message)
        if msg_hash not in self.sent_log:
            return 0
        return len(self.sent_log[msg_hash])

    def get_all_numbers_for_message(self, message):
        """
        Get all numbers that received this message

        Args:
            message: Message text

        Returns:
            List of (number, timestamp) tuples
        """
        msg_hash = self.compute_message_hash(message)
        if msg_hash not in self.sent_log:
            return []

        return [(entry['number'], entry['sent_at'])
                for entry in self.sent_log[msg_hash]]

    def get_stats(self):
        """
        Get deduplication statistics

        Returns:
            dict with stats
        """
        total_messages = len(self.content_log)
        total_sends = sum(len(entries) for entries in self.sent_log.values())

        return {
            'unique_messages': total_messages,
            'total_sends': total_sends,
            'avg_sends_per_message': total_sends / total_messages if total_messages > 0 else 0
        }

    def cleanup_old_entries(self, days_threshold=90):
        """
        Remove entries older than specified days (optional maintenance method)

        Args:
            days_threshold: Remove entries older than this many days
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        cleaned_count = 0

        for msg_hash, entries in list(self.sent_log.items()):
            # Filter out old entries
            new_entries = []
            for entry in entries:
                try:
                    entry_date = datetime.fromisoformat(entry['sent_at'])
                    if entry_date >= cutoff_date:
                        new_entries.append(entry)
                    else:
                        cleaned_count += 1
                except Exception:
                    # Keep entry if we can't parse date
                    new_entries.append(entry)

            # Update or remove hash
            if new_entries:
                self.sent_log[msg_hash] = new_entries
            else:
                # Remove hash if no entries left
                del self.sent_log[msg_hash]
                # Also remove from content log
                if msg_hash in self.content_log:
                    del self.content_log[msg_hash]

        # Save updated logs
        self._save_json(self.sent_log_path, self.sent_log)
        self._save_json(self.content_log_path, self.content_log)

        return cleaned_count
