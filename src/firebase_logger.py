import sys
import subprocess

# Auto-install firebase-admin if not present
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("\n" + "="*80)
    print("Installing required dependency: firebase-admin")
    print("="*80)
    print("\nThis is a one-time setup. Please wait...")
    print()

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "firebase-admin>=6.0.0"])
        print("\n✓ firebase-admin installed successfully!")
        print("="*80 + "\n")

        # Import after installation
        import firebase_admin
        from firebase_admin import credentials, firestore
    except subprocess.CalledProcessError as e:
        print("\n" + "="*80)
        print("ERROR: Failed to install firebase-admin!")
        print("="*80)
        print("\nPlease install it manually:")
        print("  pip install firebase-admin")
        print("\nOr install all dependencies:")
        print("  pip install -r requirements.txt")
        print("\n" + "="*80 + "\n")
        raise

from datetime import datetime
import uuid
import hashlib
import os
import json


class FirebaseLogger:
    """
    Logs WhatsApp message events to Google Firestore.

    Events are stored with flexible tagging system for easy filtering and analysis.
    """

    def __init__(self, config):
        """
        Initialize Firebase connection.

        Args:
            config: Dict containing firebase_config with:
                - enabled: bool - Enable/disable Firebase logging
                - credentials_path: str - Path to Firebase service account JSON
                - collection_name: str - Firestore collection name (default: 'message_events')
        """
        self.config = config
        self.enabled = config.get('firebase_config', {}).get('enabled', False)
        self.db = None
        self.session_id = str(uuid.uuid4())

        if self.enabled:
            self._initialize_firebase()

    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK and Firestore client

        Tries credentials in this order:
        1. FIREBASE_CREDENTIALS environment variable (JSON string)
        2. credentials_path from config (file path)
        """
        try:
            firebase_config = self.config.get('firebase_config', {})
            cred = None

            # Option 1: Try environment variable first (recommended)
            credentials_json = os.getenv('FIREBASE_CREDENTIALS')
            if credentials_json:
                try:
                    cred_dict = json.loads(credentials_json)
                    cred = credentials.Certificate(cred_dict)
                    print("✅ Using Firebase credentials from environment variable")
                except json.JSONDecodeError as e:
                    print(f"⚠️ Invalid JSON in FIREBASE_CREDENTIALS: {e}")
                    print("Trying credentials file...")

            # Option 2: Fall back to credentials file
            if not cred:
                credentials_path = firebase_config.get('credentials_path')
                if not credentials_path:
                    print("⚠️ Firebase enabled but no credentials found")
                    print("   Set FIREBASE_CREDENTIALS env var or credentials_path in config")
                    self.enabled = False
                    return

                if not os.path.exists(credentials_path):
                    print(f"⚠️ Firebase credentials file not found: {credentials_path}")
                    self.enabled = False
                    return

                cred = credentials.Certificate(credentials_path)
                print(f"✅ Using Firebase credentials from file: {credentials_path}")

            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)

            self.db = firestore.client()
            self.collection_name = firebase_config.get('collection_name', 'message_events')

            print(f"✅ Firebase initialized - Collection: {self.collection_name}")

        except Exception as e:
            print(f"⚠️ Firebase initialization failed: {e}")
            print("Continuing with local logging only...")
            self.enabled = False

    def _compute_content_hash(self, content):
        """Compute SHA256 hash of message content"""
        if not content:
            return None
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    def log_success(self, name, phone, variant_info=None, message_content=None, tags=None):
        """
        Log successful message send to Firestore.

        Args:
            name: Recipient name
            phone: Recipient phone number
            variant_info: Message variant information (e.g., "First 1/5")
            message_content: Actual message content (optional, will be hashed)
            tags: Dict of custom key-value tags for filtering/categorization
        """
        if not self.enabled:
            return

        try:
            # Get sender info from user profile
            user_profile = self.config.get('user_profile', {})
            sender_name = user_profile.get('name', '')
            sender_phone = user_profile.get('phone_number', '')
            sender_center = user_profile.get('center', '')

            event = {
                'event_type': 'message_sent',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'sender': {
                    'name': sender_name,
                    'phone': sender_phone,
                    'center': sender_center
                },
                'recipient': {
                    'name': name,
                    'phone': phone
                },
                'message': {
                    'variant_info': variant_info,
                    'content_hash': self._compute_content_hash(message_content) if message_content else None,
                    'type': 'text'  # Can be extended for 'media' later
                },
                'tags': tags or {},
                'session_id': self.session_id
            }

            # Add to Firestore
            self.db.collection(self.collection_name).add(event)

        except Exception as e:
            # Don't crash the app if Firebase logging fails
            print(f"⚠️ Firebase logging failed: {e}")

    def log_failure(self, name, phone, error, variant_info=None, tags=None):
        """
        Log failed message send to Firestore.

        Args:
            name: Recipient name
            phone: Recipient phone number
            error: Error message/reason for failure
            variant_info: Message variant information (e.g., "First 1/5")
            tags: Dict of custom key-value tags for filtering/categorization
        """
        if not self.enabled:
            return

        try:
            # Get sender info from user profile
            user_profile = self.config.get('user_profile', {})
            sender_name = user_profile.get('name', '')
            sender_phone = user_profile.get('phone_number', '')
            sender_center = user_profile.get('center', '')

            event = {
                'event_type': 'message_failed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'sender': {
                    'name': sender_name,
                    'phone': sender_phone,
                    'center': sender_center
                },
                'recipient': {
                    'name': name,
                    'phone': phone
                },
                'message': {
                    'variant_info': variant_info,
                    'type': 'text'
                },
                'error': str(error),
                'tags': tags or {},
                'session_id': self.session_id
            }

            # Add to Firestore
            self.db.collection(self.collection_name).add(event)

        except Exception as e:
            # Don't crash the app if Firebase logging fails
            print(f"⚠️ Firebase logging failed: {e}")

    def get_session_id(self):
        """Get current session ID for tagging"""
        return self.session_id
