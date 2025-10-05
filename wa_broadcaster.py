import sys

import pandas as pd
from messenger import WhatsAppMessenger
from tracker import WhatsAppTracker
import time
import json


class WhatsAppOrchestrator:
    def __init__(self):
        self.config = self._load_config()
        self.tracker = WhatsAppTracker(self.config)
        self.messenger = WhatsAppMessenger(self.config['chrome_user_data'])
        self.message = self._load_message()

    def _load_config(self):
        with open('config.json') as f:
            return json.load(f)

    def _load_message(self):
        try:
            with open(self.config['message_file'], 'r', encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise Exception("Message file not found")

    def _get_contacts(self):
        df = pd.read_excel(self.config['excel_path'])
        contacts = []
        for _, row in df.iterrows():
            if pd.notna(row['WhatsApp Number']):
                # Convert numbers like 9964297517.0 to proper format
                raw_num = str(row['WhatsApp Number']).strip().replace('.0', '')
                contacts.append((
                    str(row['Name']),
                    raw_num  # Now gets "9964297517" instead of "9964297517.0"
                ))
        return contacts

    def _check_timeout(self):
        """Check and apply timeouts based on sent count"""
        sent_count = self.tracker.sent_count
        for interval, minutes in self.config['timeouts'].items():
            if sent_count > 0 and sent_count % int(interval) == 0:
                wait_min = minutes
                self.tracker.logger.info(
                    f"⏳ Applying timeout: Waiting {str(wait_min)} mins "
                    f"after {sent_count} messages"
                )
                time.sleep(wait_min * 60)

    def run(self):
        if not self.messenger.login():
            input("Scan QR Code then press Enter...")

        contacts = self._get_contacts()
        excluded = self.tracker.get_excluded_numbers()
        sent = self.tracker.get_already_sent()

        ph_num = input('Enter your phone number to send test message: ')
        print('Sending test message to', ph_num, flush=True)
        time.sleep(1)
        result = self.messenger.send_exact_message(ph_num, self.message)
        print('Verify the message sent to your phone number and confirm.')
        print('Also check if your config file is correct.')
        response = input('Input "Yes" if message is fine, else input "No" to cancel: ')
        if response.upper() != 'YES':
            sys.exit(-1)

        for name, number in contacts:
            if number in excluded:
                self.tracker.logger.info(f"SKIPPED (excluded): {number}")
                continue

            if number in sent:
                self.tracker.logger.info(f"SKIPPED (already sent): {number}")
                continue

            try:
                result = self.messenger.send_exact_message(number, self.message)
                if result is True:
                    self.tracker.record_success(name, number)
                    self._check_timeout()  # Check after each successful send
                else:
                    self.tracker.record_failure(name, number, 'Time out')

                time.sleep(self.config['default_delay'])

            except Exception as e:
                self.tracker.logger.error(f"CRITICAL ERROR: {str(e)}")
                break

        self.messenger.quit()
        self.tracker.logger.info(
            f"COMPLETED. Total messages sent: {self.tracker.sent_count}"
        )

if __name__ == "__main__":
    orchestrator = WhatsAppOrchestrator()
    orchestrator.run()