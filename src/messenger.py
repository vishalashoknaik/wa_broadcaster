import platform
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from lib import random_sleep, format_phone_for_whatsapp

# Define OS-specific paste shortcut
PASTE_SHORTCUT = Keys.COMMAND + 'v' if platform.system() == 'Darwin' else Keys.CONTROL + 'v'

class WhatsAppMessenger:
    # XPath selectors as class constants to avoid duplication
    XPATH_CONTENTEDITABLE = '//div[@contenteditable="true"]'
    XPATH_INPUT_BOX = '//div[@contenteditable="true"][@data-tab="10"]'
    XPATH_INVALID_NUMBER = "//*[contains(text(), 'Phone number shared via url is invalid')]"

    # Rate limit detection keywords
    RATE_LIMIT_KEYWORDS = [
        "too many messages",
        "slow down",
        "you're sending messages too quickly",
        "temporarily banned",
        "account restricted",
        "detected automated",
        "unusual activity"
    ]

    def __init__(self, user_data_dir):
        options = Options()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--start-minimized")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        # Let Chrome choose a random debug port to avoid conflicts
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--log-level=3")

        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self.wait = WebDriverWait(self.driver, 20)
        except Exception as e:
            error_msg = str(e)
            if "Chrome instance exited" in error_msg or "session not created" in error_msg:
                print("\n" + "="*70)
                print("❌ CHROME LAUNCH FAILED")
                print("="*70)
                print(f"\n⚠️  Chrome profile may be corrupted: {user_data_dir}")
                print("\n💡 SOLUTIONS:")
                print(f"   1. Delete the profile directory and restart:")
                print(f"      rm -rf {user_data_dir}")
                print(f"\n   2. Or change 'chrome_user_data' path in config.json")
                print("\n" + "="*70 + "\n")
            raise

    def login(self):
        """Check if already logged in to WhatsApp Web"""
        self.driver.get("https://web.whatsapp.com")
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, self.XPATH_CONTENTEDITABLE)))
            return True
        except TimeoutException:
            return False  # QR scan needed

    def _load_chat(self, formatted_number):
        """Load WhatsApp chat for a given phone number

        Args:
            formatted_number: Phone number with country code

        Returns:
            None (navigates to chat URL)
        """
        chat_url = f"https://web.whatsapp.com/send?phone={formatted_number}"
        self.driver.get(chat_url)

    def _wait_for_input_box(self, timeout=30):
        """Wait for WhatsApp input box to be clickable

        Args:
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found

        Raises:
            TimeoutException if not found within timeout
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, self.XPATH_INPUT_BOX))
        )

    def _find_and_send_keys(self, keys):
        """Find contenteditable input and send keys to it

        Args:
            keys: Keys to send (can be text or Keys constants)
        """
        self.driver.find_element(By.XPATH, self.XPATH_CONTENTEDITABLE).send_keys(keys)

    def _inject_message_via_js(self, message, use_input_event=True):
        """Inject message into WhatsApp input box via JavaScript

        Args:
            message: Message text to inject
            use_input_event: If True, use InputEvent; else use Event
        """
        event_type = "InputEvent" if use_input_event else "Event"
        selector = self.XPATH_INPUT_BOX.replace('//', '').replace('div[@contenteditable="true"][@data-tab="10"]', 'div[contenteditable="true"][data-tab="10"]')

        script = f"""
        var input = document.querySelector('div[contenteditable="true"][data-tab="10"]');
        if (!input) {{
            input = document.querySelector('div[contenteditable="true"]');
        }}
        if (input) {{
            input.innerHTML = `{message}`;
            input.dispatchEvent(new {event_type}('input', {{ bubbles: true }}));
        }}
        """
        self.driver.execute_script(script)

    def _validate_and_format_number(self, number):
        """Validate and format phone number

        Args:
            number: Raw phone number

        Returns:
            Formatted number with country code, or None if invalid
        """
        return format_phone_for_whatsapp(number)

    def _check_for_invalid_number(self):
        """Check if WhatsApp shows invalid number alert

        Returns:
            True if invalid number detected, False otherwise
        """
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH_INVALID_NUMBER))
            )
            return True
        except TimeoutException:
            return False

    def _check_for_rate_limiting(self):
        """Check page source for rate limiting keywords

        Returns:
            Keyword if rate limiting detected, None otherwise
        """
        page_text = self.driver.page_source.lower()
        for keyword in self.RATE_LIMIT_KEYWORDS:
            if keyword in page_text:
                return keyword
        return None

    def _check_for_session_expired(self):
        """Check if WhatsApp session has expired (QR scan needed)

        Returns:
            True if session expired, False otherwise
        """
        page_text = self.driver.page_source.lower()
        return "scan" in page_text or "qr" in page_text

    def send_message(self, number, message):
        """Send message to a WhatsApp number (legacy method)

        Returns:
            True if message sent, False if failed
        """
        try:
            # Validate and format number
            formatted_number = self._validate_and_format_number(number)
            if not formatted_number:
                return False

            # Load chat
            self._load_chat(formatted_number)

            # Wait for input box
            try:
                self._wait_for_input_box(timeout=30)

                # Try DOM injection first
                try:
                    self._inject_message_via_js(message, use_input_event=True)
                    random_sleep(4)
                    self._find_and_send_keys(Keys.ENTER)
                    return True
                except Exception:
                    # Fallback to clipboard
                    pyperclip.copy(message)
                    self._find_and_send_keys(PASTE_SHORTCUT)
                    random_sleep(4)
                    self._find_and_send_keys(Keys.ENTER)
                    return True

            except TimeoutException:
                return False

        except Exception:
            return False

    def send_exact_message(self, number, message):
        """Send message with detailed error reporting

        Returns:
            True on success, error string on failure
        """
        try:
            # Validate and format number
            formatted_number = self._validate_and_format_number(number)
            if not formatted_number:
                return f"Invalid phone number format: {number}"

            # Load chat
            self._load_chat(formatted_number)

            # Check for invalid number alert
            if self._check_for_invalid_number():
                return "Invalid WhatsApp number"

            # Check for rate limiting
            rate_limit_keyword = self._check_for_rate_limiting()
            if rate_limit_keyword:
                return f"RATE LIMIT DETECTED: {rate_limit_keyword}"

            # Wait for input box and send message
            try:
                input_box = self._wait_for_input_box(timeout=30)
            except TimeoutException:
                # Check if session expired
                if self._check_for_session_expired():
                    return "Session expired - QR scan required"
                return "Timeout waiting for chat to load (30s)"

            # Send via clipboard (most reliable method)
            pyperclip.copy(message)
            input_box.send_keys(PASTE_SHORTCUT)
            random_sleep(3)
            input_box.send_keys(Keys.ENTER)

            # Wait for message to be sent
            random_sleep(5)
            return True

        except Exception as e:
            error_msg = str(e)
            if "clipboard" in error_msg.lower():
                return "Clipboard access failed"
            elif "element" in error_msg.lower():
                return "WhatsApp UI element not found"
            elif "timeout" in error_msg.lower():
                return "Page load timeout"
            else:
                return f"Unknown error: {error_msg[:50]}"

    def quit(self):
        """Safely close the WebDriver"""
        try:
            self.driver.quit()
        except Exception:
            pass  # Ignore errors during cleanup
