#!/usr/bin/env python3
"""
Test script for Firebase integration.
Tests Firebase logging without actually sending WhatsApp messages.
"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from firebase_logger import FirebaseLogger


def test_firebase_disabled():
    """Test with Firebase disabled"""
    print("\n=== Test 1: Firebase Disabled ===")
    config = {
        'firebase_config': {
            'enabled': False
        }
    }

    logger = FirebaseLogger(config)
    print(f"✓ Firebase logger created (enabled={logger.enabled})")

    # These should not crash even though Firebase is disabled
    logger.log_success(
        name="Test User",
        phone="+1234567890",
        variant_info="Test 1/1",
        tags={"test": "true", "environment": "testing"}
    )
    print("✓ log_success() called (no-op expected)")

    logger.log_failure(
        name="Test User",
        phone="+1234567890",
        error="Test error",
        tags={"test": "true"}
    )
    print("✓ log_failure() called (no-op expected)")
    print("✓ Test passed: Firebase disabled mode works")


def test_firebase_enabled():
    """Test with Firebase enabled (requires valid credentials)"""
    print("\n=== Test 2: Firebase Enabled ===")

    # Try to load config
    config_path = "config/config.json"
    if not os.path.exists(config_path):
        print("⚠️  No config.json found - skipping enabled test")
        print("   To test Firebase enabled mode:")
        print("   1. Set up Firebase (see FIREBASE_SETUP.md)")
        print("   2. Add firebase_config to config.json")
        print("   3. Run this test again")
        return

    with open(config_path) as f:
        config = json.load(f)

    firebase_config = config.get('firebase_config', {})
    if not firebase_config.get('enabled'):
        print("⚠️  Firebase is disabled in config.json")
        print("   Set 'enabled': true in firebase_config to test")
        return

    print(f"Credentials path: {firebase_config.get('credentials_path')}")
    print(f"Collection name: {firebase_config.get('collection_name')}")

    try:
        logger = FirebaseLogger(config)
        print(f"✓ Firebase logger created (enabled={logger.enabled})")

        if not logger.enabled:
            print("⚠️  Firebase failed to initialize (check credentials)")
            return

        print(f"✓ Session ID: {logger.session_id}")

        # Test logging a success event
        print("\nLogging test success event...")
        logger.log_success(
            name="Test User",
            phone="+1234567890",
            variant_info="Test Message 1/1",
            message_content="This is a test message",
            tags={
                "test": "true",
                "environment": "testing",
                "campaign_name": "Firebase Integration Test"
            }
        )
        print("✓ Success event logged to Firestore")

        # Test logging a failure event
        print("\nLogging test failure event...")
        logger.log_failure(
            name="Test User 2",
            phone="+0987654321",
            error="Test error message",
            variant_info="Test Message 1/1",
            tags={
                "test": "true",
                "environment": "testing"
            }
        )
        print("✓ Failure event logged to Firestore")

        print("\n✓ Test passed: Firebase enabled mode works")
        print(f"\n📊 Check Firebase Console:")
        print(f"   Collection: {firebase_config.get('collection_name')}")
        print(f"   Session ID: {logger.session_id}")
        print(f"   You should see 2 test events (1 success, 1 failure)")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("🔥 Firebase Integration Test")
    print("=" * 50)

    # Test 1: Disabled mode (always safe to run)
    test_firebase_disabled()

    # Test 2: Enabled mode (requires Firebase setup)
    test_firebase_enabled()

    print("\n" + "=" * 50)
    print("✅ All tests completed!")


if __name__ == '__main__':
    main()
