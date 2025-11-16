# Message Combination Summary - Example Output

This document shows example output from the campaign summary report with combination tracking.

## Google Sheet Setup Example

Your Google Sheet has **independent pools**:

| First Messages | Followup Messages |
|----------------|-------------------|
| Hey <nick_name>! 👋 | Let me know! |
| Hello <nick_name>! | Would love to hear back. |
| Hi <nick_name>, | Thanks! |
| What's up <nick_name>? |  |

- **4 first messages** in Column A
- **3 followup messages** in Column B
- **Possible combinations**: 4 × 3 = **12 combinations**

## Example Campaign Summary Output

After sending to 100 contacts with followup enabled:

```
======================================================================
📊 CAMPAIGN SUMMARY
======================================================================

✅ Total messages sent: 100
📋 First message pool: 4 variants
📋 Followup message pool: 3 variants
🔢 Possible combinations: 12

📈 Message Combination Usage:
----------------------------------------------------------------------
First 1 + Followup 1            |   9 (  9.0%) ████
First 1 + Followup 2            |   7 (  7.0%) ███
First 1 + Followup 3            |  10 ( 10.0%) █████
First 2 + Followup 1            |   8 (  8.0%) ████
First 2 + Followup 2            |   9 (  9.0%) ████
First 2 + Followup 3            |   7 (  7.0%) ███
First 3 + Followup 1            |  10 ( 10.0%) █████
First 3 + Followup 2            |   8 (  8.0%) ████
First 3 + Followup 3            |   9 (  9.0%) ████
First 4 + Followup 1            |   8 (  8.0%) ████
First 4 + Followup 2            |   9 (  9.0%) ████
First 4 + Followup 3            |   6 (  6.0%) ███
----------------------------------------------------------------------

📊 Pool Usage Analysis:

  First Message Usage:
    First 1: 26 times (26.0%)
    First 2: 24 times (24.0%)
    First 3: 27 times (27.0%)
    First 4: 23 times (23.0%)

  Followup Message Usage:
    Followup 1: 35 times (35.0%)
    Followup 2: 33 times (33.0%)
    Followup 3: 32 times (32.0%)

======================================================================
```

## What This Tells You

### Combination Tracking (Most Important!)
```
First 1 + Followup 1: 9 times
First 1 + Followup 2: 7 times
First 1 + Followup 3: 10 times
```

This shows **exactly which message pairs** were sent together:
- 9 contacts received "Hey <nick_name>! 👋" + "Let me know!"
- 7 contacts received "Hey <nick_name>! 👋" + "Would love to hear back."
- 10 contacts received "Hey <nick_name>! 👋" + "Thanks!"

### Individual Pool Usage
Shows how often each individual message was used across all combinations:
- **First 1** was used 26 times total (combined with different followups)
- **Followup 1** was used 35 times total (combined with different first messages)

### Distribution Verification
All combinations are roughly equal (~8%), confirming random selection is working correctly.

## Debugging Example

**User reports**: "I got a confusing message combination"

**Check logs:**
```
2025-01-08 10:30:15 - INFO - SUCCESS (#45): John Doe (1234567890) [First 2/4 + Followup 3/3]
```

**Now you know:**
- They got **First Message 2**: "Hello <nick_name>!"
- They got **Followup Message 3**: "Thanks!"
- Look up Row 3 and Row 4 in your Google Sheet to see exact content

## A/B Testing Use Case

After the campaign, analyze response rates:

```
Combinations with Followup 1: 35 sends → 20 responses (57% response rate)
Combinations with Followup 2: 33 sends → 15 responses (45% response rate)
Combinations with Followup 3: 32 sends → 25 responses (78% response rate) ⭐
```

**Action**: Update Google Sheet to use more variants like Followup 3!

## Example with Followup Disabled

If you set `followup_config.enabled = false`:

```
======================================================================
📊 CAMPAIGN SUMMARY
======================================================================

✅ Total messages sent: 95
📋 First message pool: 4 variants
📋 Followup message pool: 3 variants

📈 Message Combination Usage:
----------------------------------------------------------------------
First 1 (no followup)           |  25 ( 26.3%) █████████████
First 2 (no followup)           |  23 ( 24.2%) ████████████
First 3 (no followup)           |  24 ( 25.3%) ████████████
First 4 (no followup)           |  23 ( 24.2%) ████████████
----------------------------------------------------------------------

📊 Pool Usage Analysis:

  First Message Usage:
    First 1: 25 times (26.3%)
    First 2: 23 times (24.2%)
    First 3: 24 times (25.3%)
    First 4: 23 times (24.2%)

  No followup sent: 95 messages

======================================================================
```

## Example with Unequal Pools

Google Sheet with 5 first messages but only 2 followup messages:

| First Messages | Followup Messages |
|----------------|-------------------|
| Message A      | Followup X        |
| Message B      | Followup Y        |
| Message C      |                   |
| Message D      |                   |
| Message E      |                   |

**Result**: 5 × 2 = **10 combinations**

```
First 1 + Followup 1: 9 times
First 1 + Followup 2: 11 times
First 2 + Followup 1: 10 times
First 2 + Followup 2: 9 times
First 3 + Followup 1: 11 times
First 3 + Followup 2: 10 times
First 4 + Followup 1: 9 times
First 4 + Followup 2: 10 times
First 5 + Followup 1: 11 times
First 5 + Followup 2: 10 times
```

Each first message gets paired randomly with one of the two followup messages.

## Log File Example

During execution, each send is logged with combination info:

```
2025-01-08 10:30:15 - INFO - SUCCESS (#1): John Doe (1234567890) [First 2/4 + Followup 1/3]
2025-01-08 10:30:45 - INFO - SUCCESS (#2): Jane Smith (0987654321) [First 1/4 + Followup 3/3]
2025-01-08 10:31:10 - INFO - SUCCESS (#3): Bob Wilson (5556667777) [First 4/4 + Followup 2/3]
2025-01-08 10:31:35 - INFO - SUCCESS (#4): Alice Brown (1112223333) [First 3/4 + Followup 1/3]
```

This gives you complete traceability of which exact combination each contact received!

## Benefits Summary

✅ **Combination Tracking** - See which pairs were sent together
✅ **Individual Pool Stats** - Verify each message is being used
✅ **Distribution Verification** - Confirm randomization is working
✅ **Debugging Power** - Look up exact messages sent to any contact
✅ **A/B Testing** - Compare performance of different combinations
✅ **Full Traceability** - Every send logged with complete info
