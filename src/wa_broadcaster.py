import sys
import os
import pandas as pd
from messenger import WhatsAppMessenger
from tracker import WhatsAppTracker
import time
import json
import argparse
import random

from lib import random_sleep, normalize_phone
from google_sheets_client import GoogleSheetsClient
import message_parser

__version__ = "1.7.0"

class WhatsAppOrchestrator:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.tracker = WhatsAppTracker(self.config)
        self.messenger = WhatsAppMessenger(self.config['chrome_user_data'])
        self.message_pools = self._load_messages()
        self.combination_usage = {}  # Track combination usage for summary

    def _load_config(self, path):
        with open(path) as f:
            return json.load(f)

    def _load_messages(self):
        """Load message pools from Google Sheets"""
        try:
            gs_config = self.config.get('google_sheets_config', {})

            if not gs_config.get('enabled'):
                raise Exception("Google Sheets is not enabled in config")

            # Download from Google Sheets
            sheets_client = GoogleSheetsClient(self.tracker.logger)
            rows = sheets_client.fetch_messages(
                gs_config['spreadsheet_id'],
                gs_config.get('sheet_gid', 0)
            )

            # Parse into MessagePools (separate first/followup pools)
            pools = message_parser.parse_from_google_sheets(rows)

            self.tracker.logger.info(
                f"✅ Loaded {len(pools.first_messages)} first messages, "
                f"{len(pools.followup_messages)} followup messages from Google Sheets"
            )
            return pools

        except Exception as e:
            raise Exception(f"Failed to load messages from Google Sheets: {str(e)}")

    def _get_random_message_combination(self, nick_name):
        """Select random first message and random followup message independently

        Returns:
            Tuple of (first_msg, followup_msg, first_idx, followup_idx, total_first, total_followup)
        """
        # Select random first message
        first_idx = random.randint(0, len(self.message_pools.first_messages) - 1)
        first = self.message_pools.first_messages[first_idx].replace("<nick_name>", nick_name)
        total_first = len(self.message_pools.first_messages)

        # Select random followup message (if pool exists)
        followup = None
        followup_idx = None
        total_followup = len(self.message_pools.followup_messages)

        if self.message_pools.followup_messages:
            followup_idx = random.randint(0, len(self.message_pools.followup_messages) - 1)
            followup = self.message_pools.followup_messages[followup_idx].replace("<nick_name>", nick_name)

        # Return 1-indexed for human readability
        return (
            first,
            followup,
            first_idx + 1,
            followup_idx + 1 if followup_idx is not None else None,
            total_first,
            total_followup
        )

    def _get_contacts(self):
        df = pd.read_excel(self.config['excel_path'])
        contacts = []
        for _, row in df.iterrows():
            if pd.notna(row['WhatsApp Number']):
                raw_num = str(row['WhatsApp Number']).strip().replace('.0', '')
                name = str(row['Name'])
                nick_name = str(row['nick_name']) if pd.notna(row.get('nick_name')) else " "
                contacts.append((name, raw_num, nick_name))
        return contacts

    def _track_combination_usage(self, first_idx, followup_idx):
        """Track which message combinations were used"""
        if followup_idx is not None:
            key = f"First {first_idx} + Followup {followup_idx}"
        else:
            key = f"First {first_idx} (no followup)"
        self.combination_usage[key] = self.combination_usage.get(key, 0) + 1

    def _print_summary(self):
        """Print campaign summary with combination usage statistics"""
        print("\n" + "="*70)
        print("📊 CAMPAIGN SUMMARY")
        print("="*70)

        # Overall stats
        print(f"\n✅ Total messages sent: {self.tracker.sent_count}")
        print(f"📋 First message pool: {len(self.message_pools.first_messages)} variants")
        print(f"📋 Followup message pool: {len(self.message_pools.followup_messages)} variants")

        total_possible = len(self.message_pools.first_messages) * max(1, len(self.message_pools.followup_messages))
        if self.message_pools.followup_messages:
            print(f"🔢 Possible combinations: {total_possible}")

        # Combination usage breakdown
        if self.combination_usage:
            print("\n📈 Message Combination Usage:")
            print("-" * 70)

            # Sort combinations for readability
            sorted_usage = sorted(self.combination_usage.items(), key=lambda x: x[0])

            for combo_key, count in sorted_usage:
                percentage = (count / self.tracker.sent_count * 100) if self.tracker.sent_count > 0 else 0
                bar_length = int(percentage / 2)  # Scale to 50 chars max
                bar = "█" * bar_length
                print(f"{combo_key:35} | {count:3} ({percentage:5.1f}%) {bar}")

            print("-" * 70)

            # Individual pool statistics
            print(f"\n📊 Pool Usage Analysis:")

            # First message stats
            first_stats = {}
            for key, count in self.combination_usage.items():
                if key.startswith("First "):
                    first_num = key.split()[1]
                    first_stats[first_num] = first_stats.get(first_num, 0) + count

            if first_stats:
                print(f"\n  First Message Usage:")
                for first_num in sorted(first_stats.keys(), key=lambda x: int(x)):
                    count = first_stats[first_num]
                    pct = (count / self.tracker.sent_count * 100) if self.tracker.sent_count > 0 else 0
                    print(f"    First {first_num}: {count} times ({pct:.1f}%)")

            # Followup message stats
            followup_stats = {}
            for key, count in self.combination_usage.items():
                if "Followup" in key and "no followup" not in key:
                    followup_num = key.split("Followup ")[1]
                    followup_stats[followup_num] = followup_stats.get(followup_num, 0) + count

            if followup_stats:
                print(f"\n  Followup Message Usage:")
                for followup_num in sorted(followup_stats.keys(), key=lambda x: int(x)):
                    count = followup_stats[followup_num]
                    pct = (count / self.tracker.sent_count * 100) if self.tracker.sent_count > 0 else 0
                    print(f"    Followup {followup_num}: {count} times ({pct:.1f}%)")

            # No followup count
            no_followup = sum(count for key, count in self.combination_usage.items() if "no followup" in key)
            if no_followup > 0:
                print(f"\n  No followup sent: {no_followup} messages")

        print("\n" + "="*70 + "\n")

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
            print("", flush=True)
            input("Scan QR Code then press Enter...\n\n")

        contacts = self._get_contacts()
        excluded = self.tracker.get_excluded_numbers()
        sent = self.tracker.get_already_sent()

        print("", flush=True)
        ph_num = input('Enter your phone number to send test message: ')
        nick_name = input('Enter nick_name: ')
        print('Sending test message to', ph_num, flush=True)
        random_sleep(1)

        # Get random combination for test
        first_msg, followup_msg, first_idx, followup_idx, total_first, total_followup = self._get_random_message_combination(nick_name)

        print('\n' + '='*60)
        if followup_idx:
            print(f'TEST MESSAGE PREVIEW [First {first_idx}/{total_first} + Followup {followup_idx}/{total_followup}]')
        else:
            print(f'TEST MESSAGE PREVIEW [First {first_idx}/{total_first}]')
        print('='*60)
        print(f'FIRST MESSAGE (variant {first_idx}):')
        print(first_msg)

        followup_enabled = self.config.get('followup_config', {}).get('enabled', False)
        if followup_enabled and followup_msg:
            delay = self.config['followup_config'].get('delay_seconds', 3)
            print(f'\nFOLLOWUP MESSAGE (variant {followup_idx}) (after {delay}s):')
            print(followup_msg)
        print('='*60 + '\n')

        # Send first message
        result = self.messenger.send_exact_message(ph_num, first_msg)
        if result is not True:
            print(f'❌ Failed to send first message: {result}')
            sys.exit(-1)

        print('✅ First message sent!')

        # Send followup if enabled
        if followup_enabled and followup_msg:
            print(f'Waiting {delay} seconds before sending followup...')
            time.sleep(delay)
            result2 = self.messenger.send_exact_message(ph_num, followup_msg)
            if result2 is not True:
                print(f'❌ Failed to send followup message: {result2}')
                sys.exit(-1)
            print('✅ Followup message sent!')

        print('\nVerify the message(s) sent to your phone number and confirm.')
        print('Also check if your config file is correct.')
        response = input('Input "Yes" if messages are fine, else "No" to cancel: ')
        if response.upper() != 'YES':
            sys.exit(-1)

        for name, number, nick_name in contacts:
            if normalize_phone(number) in excluded:
                self.tracker.logger.info(f"SKIPPED (excluded): {number}")
                continue

            if normalize_phone(number) in sent:
                self.tracker.logger.info(f"SKIPPED (already sent): {number}")
                continue

            try:
                # Get random message combination
                first_msg, followup_msg, first_idx, followup_idx, total_first, total_followup = self._get_random_message_combination(nick_name)

                # Send first message
                result = self.messenger.send_exact_message(number, first_msg)
                if result is not True:
                    self.tracker.record_failure(name, number, f"First message failed: {result}")

                    # Critical: Stop if rate limited to avoid account ban
                    if "RATE LIMIT DETECTED" in str(result):
                        self.tracker.logger.error("⚠️ CRITICAL: Rate limit detected! Stopping to protect account.")
                        self.tracker.logger.error("⚠️ Wait at least 24 hours before resuming.")
                        break
                    continue

                # Send followup if enabled and exists
                followup_enabled = self.config.get('followup_config', {}).get('enabled', False)
                if followup_enabled and followup_msg:
                    delay = self.config['followup_config'].get('delay_seconds', 3)
                    time.sleep(delay)

                    result2 = self.messenger.send_exact_message(number, followup_msg)
                    if result2 is not True:
                        self.tracker.record_failure(name, number, f"Followup failed: {result2}")

                        if "RATE LIMIT DETECTED" in str(result2):
                            self.tracker.logger.error("⚠️ CRITICAL: Rate limit detected! Stopping to protect account.")
                            self.tracker.logger.error("⚠️ Wait at least 24 hours before resuming.")
                            break
                        continue

                # Both succeeded (or only first if no followup)
                if followup_idx:
                    combo_info = f"First {first_idx}/{total_first} + Followup {followup_idx}/{total_followup}"
                else:
                    combo_info = f"First {first_idx}/{total_first}"
                self.tracker.record_success(name, number, combo_info)

                # Track combination usage for summary
                self._track_combination_usage(first_idx, followup_idx)

                self._check_timeout()
                random_sleep(self.config['default_delay'])

            except Exception as e:
                self.tracker.logger.error(f"CRITICAL ERROR: {str(e)}")
                break

        self.messenger.quit()
        self.tracker.logger.info(
            f"COMPLETED. Total messages sent: {self.tracker.sent_count}"
        )

        # Print summary report
        self._print_summary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Automation Orchestrator")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to configuration JSON file (default: config.json)"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit"
    )

    args = parser.parse_args()

    if args.version:
        print(f"WhatsApp Orchestrator version {__version__}")
        sys.exit(0)

    # Change working directory to where config file is located
    config_dir = os.path.dirname(os.path.abspath(args.config))
    if config_dir:
        os.chdir(config_dir)
        print(f"Changed working directory to: {config_dir}")

    print(f"=== Starting script (version {__version__}) ===")
    orchestrator = WhatsAppOrchestrator(os.path.abspath(args.config))
    orchestrator.run()
