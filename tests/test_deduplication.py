#!/usr/bin/env python3
"""
Test script for message deduplication functionality
"""

import sys
import os
from message_deduplication import MessageDeduplication
import json
from pathlib import Path

def test_deduplication():
    """Test message deduplication logic"""

    print("=" * 60)
    print("MESSAGE DEDUPLICATION TEST")
    print("=" * 60)

    # Use test log files
    test_sent_log = "/tmp/test_message_sent_log.json"
    test_content_log = "/tmp/test_message_content_log.json"

    # Clean up any existing test files
    for file in [test_sent_log, test_content_log]:
        if Path(file).exists():
            os.remove(file)
            print(f"✓ Cleaned up {file}")

    # Initialize deduplication
    dedup = MessageDeduplication(test_sent_log, test_content_log)
    print(f"\n✓ Initialized MessageDeduplication")
    print(f"  - Sent log: {test_sent_log}")
    print(f"  - Content log: {test_content_log}")

    # Test messages and numbers
    msg1 = "Hi {name}, check out our summer sale!"
    msg2 = "New winter collection has arrived!"
    msg3 = "Hi {name}, check out our summer sale!"  # Same as msg1

    number1 = "9876543210"
    number2 = "9876543211"

    print("\n" + "-" * 60)
    print("TEST 1: First send - should allow")
    print("-" * 60)

    already_sent, sent_time = dedup.has_sent_to_number(msg1, number1)
    print(f"Check: msg1 to {number1} - Already sent: {already_sent}")
    assert not already_sent, "Should not be marked as sent yet"

    dedup.record_sent(msg1, number1)
    print(f"✓ Recorded: msg1 to {number1}")

    print("\n" + "-" * 60)
    print("TEST 2: Duplicate send - should block")
    print("-" * 60)

    already_sent, sent_time = dedup.has_sent_to_number(msg1, number1)
    print(f"Check: msg1 to {number1} - Already sent: {already_sent}, Time: {sent_time}")
    assert already_sent, "Should be marked as already sent"
    print(f"✓ Correctly blocked duplicate send")

    print("\n" + "-" * 60)
    print("TEST 3: Same message, different number - should allow")
    print("-" * 60)

    already_sent, sent_time = dedup.has_sent_to_number(msg1, number2)
    print(f"Check: msg1 to {number2} - Already sent: {already_sent}")
    assert not already_sent, "Should allow same message to different number"

    dedup.record_sent(msg1, number2)
    print(f"✓ Recorded: msg1 to {number2}")

    print("\n" + "-" * 60)
    print("TEST 4: Different message, same number - should allow")
    print("-" * 60)

    already_sent, sent_time = dedup.has_sent_to_number(msg2, number1)
    print(f"Check: msg2 to {number1} - Already sent: {already_sent}")
    assert not already_sent, "Should allow different message to same number"

    dedup.record_sent(msg2, number1)
    print(f"✓ Recorded: msg2 to {number1}")

    print("\n" + "-" * 60)
    print("TEST 5: Verify message hashing")
    print("-" * 60)

    hash1 = dedup.compute_message_hash(msg1)
    hash3 = dedup.compute_message_hash(msg3)
    print(f"Hash of msg1: {hash1[:16]}...")
    print(f"Hash of msg3: {hash3[:16]}...")
    assert hash1 == hash3, "Same messages should have same hash"
    print(f"✓ Hashing works correctly")

    print("\n" + "-" * 60)
    print("TEST 6: Check log files created")
    print("-" * 60)

    assert Path(test_sent_log).exists(), "Sent log file should exist"
    assert Path(test_content_log).exists(), "Content log file should exist"
    print(f"✓ Both log files created")

    # Display log contents
    print(f"\n📄 message_sent_log.json:")
    with open(test_sent_log, 'r') as f:
        sent_data = json.load(f)
        print(json.dumps(sent_data, indent=2))

    print(f"\n📄 message_content_log.json:")
    with open(test_content_log, 'r') as f:
        content_data = json.load(f)
        for hash_val, message in content_data.items():
            print(f"  {hash_val[:16]}... => {message[:50]}...")

    print("\n" + "-" * 60)
    print("TEST 7: Statistics")
    print("-" * 60)

    stats = dedup.get_stats()
    print(f"Unique messages: {stats['unique_messages']}")
    print(f"Total sends: {stats['total_sends']}")
    print(f"Avg sends per message: {stats['avg_sends_per_message']:.2f}")

    assert stats['unique_messages'] == 2, "Should have 2 unique messages"
    assert stats['total_sends'] == 3, "Should have 3 total sends"
    print(f"✓ Statistics correct")

    print("\n" + "-" * 60)
    print("TEST 8: Get numbers for specific message")
    print("-" * 60)

    recipients = dedup.get_all_numbers_for_message(msg1)
    print(f"Recipients of msg1: {len(recipients)}")
    for num, time in recipients:
        print(f"  - {num} at {time}")

    assert len(recipients) == 2, "msg1 should have been sent to 2 numbers"
    print(f"✓ Recipient tracking works")

    # Cleanup
    for file in [test_sent_log, test_content_log]:
        if Path(file).exists():
            os.remove(file)

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nMessage deduplication is working correctly!")
    print("\nHow it works:")
    print("  1. Each message gets a unique SHA256 hash")
    print("  2. System tracks (hash + number) combinations")
    print("  3. Before sending, checks if this exact message")
    print("     was already sent to this number")
    print("  4. Allows same message to different numbers")
    print("  5. Allows different messages to same number")
    print("  6. Blocks only duplicate (same message, same number)")

if __name__ == "__main__":
    try:
        test_deduplication()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
