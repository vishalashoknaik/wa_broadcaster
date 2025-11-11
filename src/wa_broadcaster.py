import sys
import os
import pandas as pd
from messenger import WhatsAppMessenger
from tracker import WhatsAppTracker
from message_deduplication import MessageDeduplication
import time
import json
import argparse
import random

from lib import random_sleep, normalize_phone
from google_sheets_client import GoogleSheetsClient
import message_parser
from table_display import print_table

__version__ = "1.9.0"

class WhatsAppOrchestrator:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.tracker = WhatsAppTracker(self.config)
        self.messenger = WhatsAppMessenger(self.config['chrome_user_data'])
        self.message_pools = self._load_messages()
        self.combination_usage = {}  # Track combination usage for summary

        # Initialize message deduplication
        sent_log_path = self.config.get('message_sent_log', 'config/message_sent_log.json')
        content_log_path = self.config.get('message_content_log', 'config/message_content_log.json')
        self.deduplication = MessageDeduplication(sent_log_path, content_log_path)

    def _load_config(self, path):
        with open(path) as f:
            return json.load(f)

    def _fetch_from_google_sheets(self, config_key, config_name):
        """Generic method to fetch data from Google Sheets

        Args:
            config_key: Key in google_sheets_config (e.g., 'messages', 'contacts')
            config_name: Display name for error messages

        Returns:
            Tuple of (rows, sheet_url, tab_name, available_sheets)
        """
        try:
            gs_config = self.config.get('google_sheets_config', {})
            sheet_config = gs_config.get(config_key, {})

            sheets_client = GoogleSheetsClient(self.tracker.logger)

            sheet_url = sheet_config.get('sheet_url')
            tab_name = sheet_config.get('tab_name')

            if not sheet_url or not tab_name:
                raise Exception(f"{config_name} config must have 'sheet_url' and 'tab_name'")

            rows, available_sheets = sheets_client.fetch_messages_by_tab_name(sheet_url, tab_name)

            return rows, sheet_url, tab_name, available_sheets

        except Exception as e:
            raise Exception(f"Failed to fetch {config_name}: {str(e)}")

    def _store_preview_data(self, attr_name, sheet_url, tab_name, available_sheets, rows, headers):
        """Store preview data for a sheet

        Args:
            attr_name: Attribute name to store data (e.g., 'messages_preview_data')
            sheet_url: Google Sheets URL
            tab_name: Tab name
            available_sheets: List of available sheet names
            rows: Data rows
            headers: Column headers for display
        """
        setattr(self, attr_name, {
            'sheet_url': sheet_url,
            'tab_name': tab_name,
            'available_sheets': available_sheets,
            'rows': rows[:2],  # First 2 rows for preview
            'headers': headers
        })

    def _load_messages(self):
        """Load message pools from Google Sheets"""
        rows, sheet_url, tab_name, available_sheets = self._fetch_from_google_sheets('messages', 'Messages')

        # Parse into MessagePools (separate first/followup pools)
        pools = message_parser.parse_from_google_sheets(rows)

        # Store for preview
        self._store_preview_data(
            'messages_preview_data',
            sheet_url, tab_name, available_sheets, rows,
            ['First Messages', 'Followup Messages']
        )

        self.tracker.logger.info(
            f"✅ Loaded {len(pools.first_messages)} first messages, "
            f"{len(pools.followup_messages)} followup messages from Google Sheets"
        )
        return pools

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
        """Load contacts from Google Sheets"""
        rows, sheet_url, tab_name, available_sheets = self._fetch_from_google_sheets('contacts', 'Contacts')

        # Store for preview
        self._store_preview_data(
            'contacts_preview_data',
            sheet_url, tab_name, available_sheets, rows,
            ['Name', 'WhatsApp Number', 'nick_name']
        )

        # Parse contacts
        contacts = []
        for row in rows:
            if len(row) >= 2:  # At minimum need name and number
                name = row[0] if len(row) > 0 else ""
                number = row[1] if len(row) > 1 else ""
                nick_name = row[2] if len(row) > 2 else " "
                if name and number:
                    # Normalize number
                    number = str(number).strip().replace('.0', '')
                    contacts.append((name, number, nick_name))

        self.tracker.logger.info(
            f"✅ Loaded {len(contacts)} contacts from Google Sheets"
        )
        return contacts

    def _track_combination_usage(self, first_idx, followup_idx):
        """Track which message combinations were used"""
        if followup_idx is not None:
            key = f"First {first_idx} + Followup {followup_idx}"
        else:
            key = f"First {first_idx} (no followup)"
        self.combination_usage[key] = self.combination_usage.get(key, 0) + 1

    def _print_pool_stats(self, pool_name, key_prefix, key_filter):
        """Generic method to print usage statistics for a message pool

        Args:
            pool_name: Display name (e.g., "First Message", "Followup Message")
            key_prefix: Prefix to extract number from key (e.g., "First ", "Followup ")
            key_filter: Function to filter relevant keys
        """
        stats = {}
        for key, count in self.combination_usage.items():
            if key_filter(key):
                # Extract number from key
                if key_prefix in key:
                    parts = key.split(key_prefix)
                    if len(parts) > 1:
                        num = parts[1].split()[0]  # Get first word after prefix
                        stats[num] = stats.get(num, 0) + count

        if stats:
            print(f"\n  {pool_name} Usage:")
            for num in sorted(stats.keys(), key=lambda x: int(x)):
                count = stats[num]
                pct = (count / self.tracker.sent_count * 100) if self.tracker.sent_count > 0 else 0
                print(f"    {pool_name} {num}: {count} times ({pct:.1f}%)")

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
            self._print_pool_stats(
                "First",
                "First ",
                lambda key: key.startswith("First ")
            )

            # Followup message stats
            self._print_pool_stats(
                "Followup",
                "Followup ",
                lambda key: "Followup" in key and "no followup" not in key
            )

            # No followup count
            no_followup = sum(count for key, count in self.combination_usage.items() if "no followup" in key)
            if no_followup > 0:
                print(f"\n  No followup sent: {no_followup} messages")

        print("\n" + "="*70 + "\n")

    def _print_sheet_preview(self, title, emoji, preview_data_attr):
        """Print preview of a single Google Sheet

        Args:
            title: Display title (e.g., "MESSAGES SHEET")
            emoji: Emoji prefix (e.g., "📋", "👥")
            preview_data_attr: Attribute name containing preview data
        """
        if hasattr(self, preview_data_attr):
            preview_data = getattr(self, preview_data_attr)
            print(f"\n{emoji} {title}:")
            print(f"URL: {preview_data['sheet_url']}")
            print(f"Tab: {preview_data['tab_name']}")
            print(f"Available tabs: {', '.join(preview_data['available_sheets'])}")
            print(f"\nShowing first 2 rows:")
            print_table(
                preview_data['headers'],
                preview_data['rows'],
                max_rows=2
            )

    def _preview_sheets(self):
        """Display preview of messages and contacts sheets for user verification"""
        print("\n" + "="*70)
        print("=== GOOGLE SHEETS PREVIEW ===")
        print("="*70)

        # Messages preview
        self._print_sheet_preview("MESSAGES SHEET", "📋", "messages_preview_data")

        # Contacts preview
        self._print_sheet_preview("CONTACTS SHEET", "👥", "contacts_preview_data")

        print("\n" + "="*70)
        print("⚠️  PLEASE VERIFY THE DATA ABOVE MATCHES YOUR GOOGLE SHEETS")
        print("="*70 + "\n")

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

    def _handle_rate_limit(self, result):
        """Check for rate limiting and handle appropriately

        Args:
            result: Result from send_exact_message

        Returns:
            True if rate limited (should stop), False otherwise
        """
        if "RATE LIMIT DETECTED" in str(result):
            self.tracker.logger.error("⚠️ CRITICAL: Rate limit detected! Stopping to protect account.")
            self.tracker.logger.error("⚠️ Wait at least 24 hours before resuming.")
            return True
        return False

    def _cleanup(self):
        """Clean up all resources (WebDriver, logging handlers)"""
        try:
            if hasattr(self, 'messenger'):
                self.messenger.quit()
        except Exception as e:
            print(f"Warning: Error cleaning up messenger: {e}", file=sys.stderr)

        try:
            if hasattr(self, 'tracker'):
                self.tracker.cleanup()
        except Exception as e:
            print(f"Warning: Error cleaning up tracker: {e}", file=sys.stderr)

    def run(self):
        try:
            if not self.messenger.login():
                print("", flush=True)
                input("Scan QR Code then press Enter...\n\n")

            contacts = self._get_contacts()
            excluded = self.tracker.get_excluded_numbers()
            sent = self.tracker.get_already_sent()

            # Show preview of Google Sheets data if available
            if hasattr(self, 'messages_preview_data') or hasattr(self, 'contacts_preview_data'):
                self._preview_sheets()
                response = input('Do the sheets above look correct? Type "YES" to continue or "NO" to cancel: ')
                if response.upper() != 'YES':
                    print("Campaign cancelled by user.")
                    self._cleanup()
                    sys.exit(0)

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
                self._cleanup()
                sys.exit(-1)

            print('✅ First message sent!')

            # Send followup if enabled
            if followup_enabled and followup_msg:
                print(f'Waiting {delay} seconds before sending followup...')
                time.sleep(delay)
                result2 = self.messenger.send_exact_message(ph_num, followup_msg)
                if result2 is not True:
                    print(f'❌ Failed to send followup message: {result2}')
                    self._cleanup()
                    sys.exit(-1)
                print('✅ Followup message sent!')

            print('\nVerify the message(s) sent to your phone number and confirm.')
            print('Also check if your config file is correct.')
            response = input('Input "Yes" if messages are fine, else "No" to cancel: ')
            if response.upper() != 'YES':
                self._cleanup()
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

                    # Check deduplication for first message
                    already_sent, sent_time = self.deduplication.has_sent_to_number(first_msg, normalize_phone(number))
                    if already_sent:
                        self.tracker.logger.info(f"SKIPPED (duplicate message): {number} - Same message already sent on {sent_time}")
                        continue

                    # Check deduplication for followup message if enabled
                    followup_enabled = self.config.get('followup_config', {}).get('enabled', False)
                    if followup_enabled and followup_msg:
                        followup_already_sent, followup_sent_time = self.deduplication.has_sent_to_number(followup_msg, normalize_phone(number))
                        if followup_already_sent:
                            self.tracker.logger.info(f"SKIPPED (duplicate followup): {number} - Same followup message already sent on {followup_sent_time}")
                            continue

                    # Send first message
                    result = self.messenger.send_exact_message(number, first_msg)
                    if result is not True:
                        self.tracker.record_failure(name, number, f"First message failed: {result}")

                        # Critical: Stop if rate limited to avoid account ban
                        if self._handle_rate_limit(result):
                            break
                        continue

                    # Record first message in deduplication log
                    self.deduplication.record_sent(first_msg, normalize_phone(number))

                    # Send followup if enabled and exists
                    followup_enabled = self.config.get('followup_config', {}).get('enabled', False)
                    if followup_enabled and followup_msg:
                        delay = self.config['followup_config'].get('delay_seconds', 3)
                        time.sleep(delay)

                        result2 = self.messenger.send_exact_message(number, followup_msg)
                        if result2 is not True:
                            self.tracker.record_failure(name, number, f"Followup failed: {result2}")

                            if self._handle_rate_limit(result2):
                                break
                            continue

                        # Record followup message in deduplication log
                        self.deduplication.record_sent(followup_msg, normalize_phone(number))

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

            self.tracker.logger.info(
                f"COMPLETED. Total messages sent: {self.tracker.sent_count}"
            )

            # Print summary report
            self._print_summary()

        finally:
            # Always cleanup resources regardless of how we exit
            self._cleanup()


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
