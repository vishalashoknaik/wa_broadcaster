import logging
import os
import sys
from pathlib import Path

from lib import normalize_phone
from firebase_logger import FirebaseLogger


class WhatsAppTracker:
    def __init__(self, config):
        self.config = config
        self.sent_count = 0
        self.logger = None
        self.file_handler = None
        self.console_handler = None
        self._setup_logging()
        self._ensure_files_exist()

        # Initialize Firebase logger (won't crash if disabled/misconfigured)
        self.firebase_logger = FirebaseLogger(config)

    def _setup_logging(self):
        """Setup logging with proper handler management"""
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Ensure log file exists
        self._ensure_file_exists(self.config['log_file'])

        # File handler (UTF-8)
        self.file_handler = logging.FileHandler(self.config['log_file'], encoding='utf-8')
        self.file_handler.setFormatter(formatter)

        # Console handler with UTF-8 support (no global sys.stdout modification)
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(formatter)

        self.logger = logging.getLogger('tracker')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def _ensure_file_exists(self, filepath):
        """Safely create file if it doesn't exist"""
        try:
            if not os.path.isfile(filepath):
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
                with open(filepath, 'w', encoding='utf-8'):
                    pass
        except (OSError, IOError) as e:
            # Log to stderr if logger not ready
            print(f"Warning: Could not create file {filepath}: {e}", file=sys.stderr)

    def _ensure_files_exist(self):
        """Ensure all tracking files exist"""
        for filepath in [self.config['sent_numbers_file'],
                         self.config['error_numbers_file']]:
            self._ensure_file_exists(filepath)

    def _read_normalized_numbers(self, filepath):
        """Generic method to read and normalize phone numbers from file

        Args:
            filepath: Path to file containing phone numbers

        Returns:
            Set of normalized phone numbers
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return {normalize_phone(line.strip()) for line in f if line.strip()}
        except FileNotFoundError:
            return set()
        except (OSError, IOError) as e:
            if self.logger:
                self.logger.warning(f"Could not read {filepath}: {e}")
            return set()

    def _write_to_file(self, filepath, content):
        """Safely append content to file

        Args:
            filepath: Path to file
            content: Content to append (without newline)
        """
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(f"{content}\n")
        except (OSError, IOError) as e:
            if self.logger:
                self.logger.error(f"Could not write to {filepath}: {e}")

    def record_success(self, name, number, variant_info=None, message_content=None, tags=None):
        """Record successful message send"""
        self.sent_count += 1
        variant_str = f" [variant: {variant_info}]" if variant_info else ""
        self.logger.info(f"SUCCESS (#{self.sent_count}): {name} ({number}){variant_str}")
        self._write_to_file(self.config['sent_numbers_file'], number)

        # Log to Firebase (if enabled)
        self.firebase_logger.log_success(
            name=name,
            phone=number,
            variant_info=variant_info,
            message_content=message_content,
            tags=tags
        )

    def record_failure(self, name, number, error, variant_info=None, tags=None):
        """Record failed message send"""
        self.logger.error(f"FAILED: {name} ({number}) - {error}")
        self._write_to_file(self.config['error_numbers_file'], f"{number}|{error}")

        # Log to Firebase (if enabled)
        self.firebase_logger.log_failure(
            name=name,
            phone=number,
            error=error,
            variant_info=variant_info,
            tags=tags
        )

    def get_excluded_numbers(self):
        """Get set of excluded phone numbers"""
        return self._read_normalized_numbers(self.config['exclude_file'])

    def get_already_sent(self):
        """Get set of already sent phone numbers"""
        return self._read_normalized_numbers(self.config['sent_numbers_file'])

    def cleanup(self):
        """Clean up resources (remove logging handlers)"""
        if self.logger:
            if self.file_handler:
                self.logger.removeHandler(self.file_handler)
                self.file_handler.close()
                self.file_handler = None
            if self.console_handler:
                self.logger.removeHandler(self.console_handler)
                self.console_handler.close()
                self.console_handler = None

    def __del__(self):
        """Ensure cleanup on object destruction"""
        self.cleanup()
