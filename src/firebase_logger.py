import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid
import hashlib


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
        """Initialize Firebase Admin SDK and Firestore client"""
        try:
            firebase_config = self.config.get('firebase_config', {})
            credentials_path = firebase_config.get('credentials_path')

            if not credentials_path:
                print("Warning: Firebase enabled but no credentials_path provided")
                self.enabled = False
                return

            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(credentials_path)
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
            event = {
                'event_type': 'message_sent',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
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
            event = {
                'event_type': 'message_failed',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
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
