# Message Deduplication Feature

## Overview

The message deduplication feature prevents sending the same message content to the same phone number multiple times. This works independently of the existing `sent_numbers.txt` file, providing message-level tracking instead of just number-level tracking.

## How It Works

### Key Concepts

1. **Message Hashing**: Each message gets a unique SHA256 hash based on its content
2. **Tracking Pair**: System tracks (message_hash + phone_number) combinations
3. **Separate Logging**: Maintains separate logs from the existing sent_numbers system
4. **Timestamp Recording**: Records when each message was sent

### What Gets Blocked

```
✅ ALLOWED: Same message to different numbers
✅ ALLOWED: Different messages to same number
❌ BLOCKED: Same message to same number (duplicate)
```

## Example Scenarios

### Scenario 1: Campaign Re-runs

```
Campaign 1: "Hi, check our summer sale!" → 9876543210 ✅ Sent
Campaign 2: "Hi, check our summer sale!" → 9876543210 ❌ Blocked (duplicate)
Campaign 3: "New winter collection!" → 9876543210 ✅ Sent (different message)
```

### Scenario 2: Multiple Recipients

```
Message: "Hi, check our summer sale!"
  → 9876543210 ✅ Sent
  → 9876543211 ✅ Sent (different number)
  → 9876543212 ✅ Sent (different number)
  → 9876543210 ❌ Blocked (already sent to this number)
```

## Files Created

### 1. `message_sent_log.json`

Tracks which messages were sent to which numbers:

```json
{
  "abc123hash...": [
    {
      "number": "9876543210",
      "sent_at": "2025-11-11T18:30:00"
    },
    {
      "number": "9876543211",
      "sent_at": "2025-11-11T18:31:00"
    }
  ],
  "def456hash...": [
    {
      "number": "9876543212",
      "sent_at": "2025-11-11T18:32:00"
    }
  ]
}
```

### 2. `message_content_log.json`

Maps hashes to actual message content:

```json
{
  "abc123hash...": "Hi {name}, check out our summer sale!",
  "def456hash...": "New winter collection has arrived!"
}
```

## Configuration

Add these fields to your `config.json`:

```json
{
  "message_sent_log": "config/message_sent_log.json",
  "message_content_log": "config/message_content_log.json",

  ... (other config fields)
}
```

**Note:** If these fields are not present, the system uses default paths:
- `config/message_sent_log.json`
- `config/message_content_log.json`

## Log Messages

When deduplication blocks a message, you'll see in the logs:

```
SKIPPED (duplicate message): 9876543210 - Same message already sent on 2025-11-11T18:30:00
SKIPPED (duplicate followup): 9876543210 - Same followup message already sent on 2025-11-11T18:31:00
```

## Relationship with sent_numbers.txt

The deduplication system works **alongside** the existing `sent_numbers.txt` file:

| Feature | sent_numbers.txt | Message Deduplication |
|---------|------------------|----------------------|
| Tracks | Phone numbers only | Message + Phone number pairs |
| Blocks | Any message to number | Same message to same number |
| Granularity | Number-level | Message-level |
| Use Case | "Never send again" | "Don't send duplicate messages" |

### Example Flow:

```
1. Check sent_numbers.txt → Number not in list? Proceed
2. Check message deduplication → Message+Number combo not sent? Proceed
3. Send message
4. Add to sent_numbers.txt
5. Add to message deduplication logs
```

## Testing

Run the test script to verify functionality:

```bash
cd src
python3 test_deduplication.py
```

Expected output:
```
============================================================
MESSAGE DEDUPLICATION TEST
============================================================
...
✅ ALL TESTS PASSED!
```

## Benefits

### 1. **Flexible Campaign Re-runs**

You can re-run campaigns to the same contacts with different messages:

```bash
# Day 1: Summer sale campaign
# Day 7: Winter collection campaign (same contacts, different message)
# Day 14: Clearance sale campaign (same contacts, different message)
```

### 2. **Prevents Accidental Duplicates**

If you accidentally run the same campaign twice, deduplication prevents duplicate sends:

```bash
# Run campaign
python wa_broadcaster.py --config config.json

# Accidentally run again (maybe thinking it didn't work)
python wa_broadcaster.py --config config.json
# → All messages blocked as duplicates
```

### 3. **Message-Level Tracking**

See exactly which messages were sent to which contacts and when:

```python
from message_deduplication import MessageDeduplication

dedup = MessageDeduplication('config/message_sent_log.json', 'config/message_content_log.json')

# Get all recipients of a specific message
message = "Hi, check our summer sale!"
recipients = dedup.get_all_numbers_for_message(message)
for number, timestamp in recipients:
    print(f"{number} received message at {timestamp}")
```

## Advanced Usage

### Get Statistics

```python
from message_deduplication import MessageDeduplication

dedup = MessageDeduplication('config/message_sent_log.json', 'config/message_content_log.json')

stats = dedup.get_stats()
print(f"Unique messages: {stats['unique_messages']}")
print(f"Total sends: {stats['total_sends']}")
print(f"Average sends per message: {stats['avg_sends_per_message']:.2f}")
```

### Check Specific Message

```python
message = "Hi, check our summer sale!"
number = "9876543210"

already_sent, timestamp = dedup.has_sent_to_number(message, number)
if already_sent:
    print(f"Already sent on {timestamp}")
else:
    print("Not sent yet")
```

### Cleanup Old Entries

To remove entries older than 90 days:

```python
cleaned_count = dedup.cleanup_old_entries(days_threshold=90)
print(f"Removed {cleaned_count} old entries")
```

## Technical Details

### Message Hashing

- Algorithm: SHA256
- Encoding: UTF-8
- Hash length: 64 characters (hexadecimal)
- Collision probability: Negligible (2^-256)

### File Format

- Format: JSON
- Encoding: UTF-8 (supports emojis and international characters)
- Auto-created: Files are created automatically on first send

### Performance

- Hash computation: ~0.001 seconds per message
- Lookup: O(1) average case (hash table)
- File I/O: Async write after successful send
- Memory: Loads logs into memory on initialization

## Troubleshooting

### Problem: Log files not created

**Cause:** Directory doesn't exist

**Solution:** The system auto-creates the directory, but ensure parent paths exist:

```bash
mkdir -p config
```

### Problem: All messages being blocked

**Cause:** Same message being sent repeatedly

**Solution:** Check if you're using the same message template. Either:
1. Create different message variants
2. Delete the log files to start fresh:
   ```bash
   rm config/message_sent_log.json config/message_content_log.json
   ```

### Problem: Want to reset deduplication for specific campaign

**Solution:** Backup and clear the log files:

```bash
# Backup
cp config/message_sent_log.json config/message_sent_log.backup.json
cp config/message_content_log.json config/message_content_log.backup.json

# Clear
rm config/message_sent_log.json config/message_content_log.json

# Run campaign

# Restore if needed
mv config/message_sent_log.backup.json config/message_sent_log.json
mv config/message_content_log.backup.json config/message_content_log.json
```

## Migration from Older Versions

If you're upgrading from a version without message deduplication:

1. **Update config.json** (optional, uses defaults if not present):
   ```json
   {
     "message_sent_log": "config/message_sent_log.json",
     "message_content_log": "config/message_content_log.json"
   }
   ```

2. **No data migration needed**: Existing `sent_numbers.txt` continues to work

3. **First run**: Log files will be created automatically

4. **Behavior change**:
   - Previously: Number sent to once = never send again
   - Now: Can send different messages to same number, but not same message

## FAQ

**Q: Will this break my existing campaigns?**

A: No, it works alongside existing systems. `sent_numbers.txt` still prevents any sends to numbers in that file.

**Q: Can I disable this feature?**

A: Currently it's always enabled. However, since it only blocks truly duplicate messages, it shouldn't interfere with normal operations.

**Q: What happens if I delete the log files?**

A: The system starts fresh. All messages will be considered "not sent" and will be sent again (unless blocked by `sent_numbers.txt`).

**Q: Does this work with followup messages?**

A: Yes! Both first messages and followup messages are tracked separately. A followup can be sent even if the first message was already sent (and vice versa).

**Q: How much disk space do the log files use?**

A: Minimal. Each entry is ~150 bytes. For 10,000 messages to 1,000 contacts:
- message_sent_log.json: ~150 KB
- message_content_log.json: ~200 KB

**Q: Can I view message history in the GUI?**

A: Not currently. This is a background logging feature. You can view the JSON files directly or write a custom viewer.

**Q: Does this track when messages were read?**

A: No, it only tracks when messages were sent from SPAMURAI. WhatsApp read receipts are not tracked.

## Future Enhancements

Potential additions (not yet implemented):

- [ ] GUI dashboard showing message history
- [ ] Export deduplication logs to CSV/Excel
- [ ] Message variant analysis (which message performed best)
- [ ] Automatic cleanup of old entries
- [ ] Integration with response tracking
- [ ] Per-campaign deduplication controls

---

**Version:** 1.10.0+
**Last Updated:** November 2025
**Module:** `src/message_deduplication.py`
