# Google Sheets Setup Guide

This guide explains how to set up Google Sheets for managing your WhatsApp broadcast messages.

## Features

✅ **Multiple Random Messages** - Define multiple message variants, one is randomly selected per contact
✅ **Immediate Follow-up** - Send a second message immediately after the first (3 seconds delay)
✅ **Central Management** - Update messages in Google Sheets, no code changes needed
✅ **Simple Setup** - No authentication required, just publish and go

## Step 1: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Add the following structure with **separate pools**:

| First Messages | Followup Messages |
|----------------|-------------------|
| Hey <nick_name>! 👋 | Let me know! |
| Hello <nick_name>! | Would love to hear from you. |
| Hi <nick_name>, | Reply when you can. |
| What's up <nick_name>? | Thanks! |
|  | Looking forward to it! |

**Important Notes:**
- Row 1 is the header (will be skipped automatically)
- **Column A**: Pool of first messages (required)
- **Column B**: Pool of followup messages (optional)
- Empty cells are skipped (you can have different counts in each column)
- Use `<nick_name>` placeholder where you want the name from Excel to appear
- **Messages are selected INDEPENDENTLY** - one random first + one random followup = unique combinations
- Example: "First Message 2" can be paired with "Followup Message 4"

## Step 2: Share Your Sheet

1. In your Google Sheet, click the **Share** button (top right)
2. Under "General access":
   - Change to **"Anyone with the link"**
   - Set permission to **"Viewer"**
3. Click **"Done"**

**Note:** No publishing needed! Just sharing with "Anyone with the link" is enough. The app downloads the sheet as Excel format, which preserves all formatting, emojis, and newlines perfectly.

## Step 3: Get Your Spreadsheet ID

1. Look at your Google Sheet URL:
   ```
   https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
   ```

2. Copy the part between `/d/` and `/edit`:
   ```
   1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
   ```

3. This is your **spreadsheet_id**

## Step 4: Get Your Sheet GID (Optional)

If you have multiple sheets in your spreadsheet:

1. Click on the sheet tab you want to use
2. Look at the URL, you'll see something like:
   ```
   https://docs.google.com/spreadsheets/d/1BxiMVs.../edit#gid=123456789
   ```

3. The number after `gid=` is your **sheet_gid**
4. If you don't see `#gid=...`, it's the first sheet and the GID is **0** (default)

## Step 5: Update config.json

1. Open `config.json`
2. Update the Google Sheets configuration:

```json
{
  "google_sheets_config": {
    "enabled": true,
    "spreadsheet_id": "YOUR_SPREADSHEET_ID_HERE",
    "sheet_gid": 0
  },
  "followup_config": {
    "enabled": false,
    "delay_seconds": 3
  }
}
```

**Replace** `YOUR_SPREADSHEET_ID_HERE` with your actual spreadsheet ID from Step 3.

## Step 6: Enable Follow-up Messages (Optional)

If you want to send the second message immediately after the first:

```json
{
  "followup_config": {
    "enabled": true,
    "delay_seconds": 3
  }
}
```

- Set `enabled` to `true`
- `delay_seconds` is the wait time between first and second message (default: 3 seconds)

## Usage

### Running the Application

```bash
cd wa_broadcaster/src
python3 wa_broadcaster.py --config ../config.json
```

### What Happens:

1. **Downloads messages** from Google Sheets
2. **Shows test preview** with randomly selected variant
3. **Sends test message** to your number
4. **Waits for confirmation** before bulk send
5. **Sends to all contacts** with random variants

### Updating Messages:

1. Edit your Google Sheet
2. **No need to republish** - changes are automatic
3. Run the application again
4. It downloads the latest messages automatically

## Example Message Variants

### Simple Messages (No Followup)

| First Message | Followup Message |
|---------------|------------------|
| Hey <nick_name>! 👋 | |
| Hello <nick_name>! | |

Leave followup column empty if you don't want a second message.

### With Followup

| First Message | Followup Message |
|---------------|------------------|
| Hey <nick_name>! 👋 Check out our new product | Let me know if you want more details! |
| Hi <nick_name>! Quick update for you | Reply when you get a chance. |

### Multi-line Messages

You can add line breaks in Google Sheets cells (Alt+Enter on Windows, Option+Enter on Mac):

| First Message | Followup Message |
|---------------|------------------|
| Hey <nick_name>! 👋<br>Hope you're doing well!<br>Check this out... | Let me know!<br>Thanks! |

## Troubleshooting

### "Google Sheet not found or not published"
- Make sure you published the sheet to web (Step 2)
- Check that you copied the correct spreadsheet ID

### "Access denied"
- The sheet must be published with "Anyone with the link can view"
- Re-publish the sheet following Step 2

### "No valid message variants found"
- Check that Column A (First Message) has content
- Make sure you have at least one data row (besides the header)

### "Failed to load messages from Google Sheets"
- Check your internet connection
- Verify the spreadsheet ID is correct
- Make sure the sheet is published

## Security Note

⚠️ **Important:** Publishing your sheet makes it publicly accessible via the URL. Anyone with the spreadsheet ID can read your messages.

**Best Practices:**
- Don't include sensitive information in messages
- Use placeholders like `<nick_name>` instead of actual names
- You can unpublish anytime: File → Share → Publish to web → Stop publishing

## Configuration Reference

```json
{
  "google_sheets_config": {
    "enabled": true,              // Enable/disable Google Sheets
    "spreadsheet_id": "...",      // Your spreadsheet ID
    "sheet_gid": 0                // Sheet GID (0 for first sheet)
  },
  "followup_config": {
    "enabled": false,             // Enable immediate followup
    "delay_seconds": 3            // Wait time between messages
  }
}
```

## Need Help?

- Check that your Google Sheet follows the exact format above
- Make sure the sheet is published to web
- Verify your spreadsheet ID is correct
- Check your internet connection
