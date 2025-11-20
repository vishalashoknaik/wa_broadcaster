# SPAMURAI - Complete Windows Setup Guide

**Everything you need to go from zero to sending your first WhatsApp broadcast.**

---

## 📋 What You'll Need

- Windows 10 or 11
- Internet connection
- A WhatsApp account
- Google account (for Google Sheets)
- 30-45 minutes for complete first-time setup

---

## Table of Contents

1. [Install System Requirements](#step-1-install-system-requirements)
2. [Download & Extract SPAMURAI](#step-2-download--extract-spamurai)
3. [Setup Firebase Credentials](#step-3-setup-firebase-credentials-mandatory)
4. [Create Google Sheets](#step-4-create-google-sheets)
5. [Configure SPAMURAI](#step-5-configure-spamurai)
6. [Launch SPAMURAI](#step-6-launch-spamurai)
7. [Connect WhatsApp](#step-7-connect-whatsapp)
8. [Send Your First Broadcast](#step-8-send-your-first-broadcast)

---

## Step 1: Install System Requirements

### 1A. Install Python

1. Go to: **https://www.python.org/downloads/**
2. Click "Download Python" (latest version)
3. Run the installer
4. ⚠️ **CRITICAL**: Check ✅ **"Add Python to PATH"** at the bottom
5. Click "Install Now"
6. Wait for installation to complete
7. Click "Close"

**Verify Installation:**
```
1. Press Windows + R
2. Type: cmd
3. Press Enter
4. Type: python --version
5. You should see: Python 3.x.x
```

### 1B. Install Google Chrome

1. Go to: **https://www.google.com/chrome/**
2. Download and install Chrome
3. Launch Chrome once to verify it works

---

## Step 2: Download & Extract SPAMURAI

1. Download the SPAMURAI package (ZIP file)
2. Extract to a simple location like: **`C:\SPAMURAI\`**
3. Verify the folder contains:
   ```
   C:\SPAMURAI\
   ├── src/
   ├── config/
   ├── launchers/
   ├── setup_firebase.bat
   ├── diagnose_windows.bat
   └── requirements.txt
   ```

---

## Step 3: Setup Firebase Credentials (MANDATORY)

You'll receive a file named **`firebase_spamurai.json`** - this is required for SPAMURAI to work.

### Option A: Automatic Setup (Recommended)

1. Place `firebase_spamurai.json` in the `C:\SPAMURAI\` folder
2. Open **Command Prompt** (search "cmd" in Start menu)
3. Type:
   ```
   cd C:\SPAMURAI
   setup_firebase.bat firebase_spamurai.json
   ```
4. Press Enter
5. Wait for:
   ```
   [OK] Valid Firebase credentials file found
   [OK] FIREBASE_CREDENTIALS environment variable set
   Setup complete!
   ```
6. **Important**: Close Command Prompt completely

### Option B: Manual Setup

1. Copy `firebase_spamurai.json` to: `C:\SPAMURAI\config\`
2. Rename it to: **`firebase-credentials.json`**
3. Done!

**Verify Firebase Setup:**
```
1. Open new Command Prompt
2. Type: echo %FIREBASE_CREDENTIALS%
3. Should show JSON data (if using Option A) or nothing (if using Option B - that's OK)
```

---

## Step 4: Create Google Sheets

SPAMURAI uses two Google Sheets: one for contacts and one for messages.

### 4A. Create Contacts Sheet

1. Go to: **https://sheets.google.com**
2. Click **+ Blank** to create new spreadsheet
3. Name it: **"SPAMURAI Contacts"**
4. Create these columns in Row 1:

   | A (Name) | B (WhatsApp Number) | C (nick_name) |
   |----------|---------------------|---------------|
   | John Doe | 919876543210 | John |
   | Jane Smith | 918765432109 | Jane |
   | Bob Wilson | 917654321098 | Bob |

5. **Important Column Details:**
   - **Name**: Full name of contact
   - **WhatsApp Number**: Phone with country code (no +, no spaces, no dashes)
     - Example: `919876543210` (India)
     - Example: `14155552671` (USA)
   - **nick_name**: Short name used in messages (optional)

6. Fill in your contacts (Row 2 onwards)

7. **Share the sheet:**
   - Click **Share** button (top right)
   - Under "General access" → Change to **"Anyone with the link"**
   - Set permission to **"Viewer"**
   - Click **Done**

8. **Copy the sheet URL:**
   - Copy the entire URL from your browser
   - Example: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
   - Save this URL - you'll need it later

### 4B. Create Messages Sheet

1. Create another new spreadsheet
2. Name it: **"SPAMURAI Messages"**
3. Create this structure:

   | First Messages | Followup Messages |
   |----------------|-------------------|
   | Hey <nick_name>! 👋 How are you? | Let me know! |
   | Hello <nick_name>! Hope you're doing great! | Would love to hear from you. |
   | Hi <nick_name>, long time no see! | Reply when you can. |
   | What's up <nick_name>? 🙂 | Thanks! |

4. **Important Notes:**
   - Row 1 is header (will be skipped)
   - **Column A**: First messages (one will be randomly selected per contact)
   - **Column B**: Follow-up messages (optional, sent 3 seconds after first message)
   - Use `<nick_name>` placeholder - it will be replaced with the name from your Contacts sheet
   - You can use emojis, multiple lines (Alt+Enter), and special characters

5. **Share the sheet** (same as Contacts sheet):
   - Click **Share** → "Anyone with the link" → "Viewer" → **Done**

6. **Copy the sheet URL** and save it

---

## Step 5: Configure SPAMURAI

### 5A. Create Your Config File

1. Navigate to: `C:\SPAMURAI\config\`
2. Find the file: `config.example.json`
3. Right-click → **Copy**
4. Paste in the same folder
5. Rename the copy to: **`config.json`**

### 5B. Edit Config File

1. Right-click `config.json` → **Open with** → **Notepad**
2. Update these sections:

**User Profile:**
```json
"user_profile": {
  "name": "Your Name",
  "phone_number": "919876543210"
},
```
*Replace with your actual name and WhatsApp number*

**Google Sheets URLs:**
```json
"google_sheets_config": {
  "messages": {
    "sheet_url": "PASTE_YOUR_MESSAGES_GOOGLE_SHEET_URL_HERE",
    "tab_name": "Sheet1"
  },
  "contacts": {
    "sheet_url": "PASTE_YOUR_CONTACTS_GOOGLE_SHEET_URL_HERE",
    "tab_name": "Sheet1"
  }
},
```
*Paste the full URLs you copied in Step 4*

**Firebase Config:**
```json
"firebase_config": {
  "enabled": true,
  "credentials_path": "config/firebase-credentials.json",
  "collection_name": "message_events"
}
```
*Should already be `"enabled": true"` - leave it as is*

**Message Settings (Optional):**
```json
"default_delay": 60,
"timeouts": {
  "100": 30,
  "300": 30
}
```
- `default_delay`: Seconds between each message (60 = 1 minute)
- `timeouts`: Pause intervals to avoid WhatsApp blocking
  - `"100": 30` = Pause 30 minutes after 100 messages
  - `"300": 30` = Pause 30 minutes after 300 messages

3. **Save** the file (Ctrl+S)
4. Close Notepad

---

## Step 6: Launch SPAMURAI

### 6A. First Launch

1. Navigate to: `C:\SPAMURAI\launchers\`
2. **Double-click**: `SPAMURAI.bat`
3. A Command Prompt window will open showing:
   ```
   =========================================
     SPAMURAI - WhatsApp Broadcast Ninja
     Strike fast. Strike precise.
   =========================================

   [Step 1/6] Checking Python installation...
   [OK] Python 3.x.x detected

   [Step 2/6] Setting up virtual environment...
   [OK] Virtual environment created

   [Step 3/6] Activating virtual environment...
   [OK] Virtual environment activated

   [Step 4/6] Checking dependencies...
   Streamlit not found. Installing dependencies...
   This may take a few minutes...
   ```

4. **First run takes 2-5 minutes** to install all packages
5. Wait for:
   ```
   [Step 5/6] Checking Firebase credentials...
   [OK] Firebase credentials found

   [Step 6/6] Launching SPAMURAI GUI...
   =========================================
     GUI will open in your browser
     URL: http://localhost:8501
   =========================================
   ```

6. Your browser will automatically open to: **http://localhost:8501**
7. **Success!** You'll see the SPAMURAI interface

### 6B. Subsequent Launches

After first-time setup:
- Double-click `SPAMURAI.bat`
- Takes only 5-10 seconds
- Browser opens automatically

**To stop SPAMURAI:**
- Press `Ctrl+C` in the Command Prompt window
- Or close the Command Prompt window

---

## Step 7: Connect WhatsApp

### 7A. Initial WhatsApp Setup

When you first use SPAMURAI:

1. Click **"Start Campaign"** button in the GUI
2. Chrome will open with WhatsApp Web
3. You'll see a **QR code**
4. On your phone:
   - Open **WhatsApp**
   - Tap **Menu** (⋮) or **Settings**
   - Tap **"Linked Devices"**
   - Tap **"Link a Device"**
   - **Scan the QR code** on your computer screen
5. WhatsApp Web will load your chats
6. ✅ **WhatsApp is now connected!**

### 7B. Staying Logged In

SPAMURAI keeps you logged in using a Chrome profile:
- You only need to scan the QR code **once**
- Subsequent runs will already be logged in
- If you ever need to log in again, just repeat Step 7A

---

## Step 8: Send Your First Broadcast

### 8A. Load Your Data

1. In the SPAMURAI GUI, you'll see the main interface
2. Your Google Sheets URLs should already be loaded (from config.json)
3. Click **"Load Contacts"** button
4. You'll see your contacts appear in the table
5. Click **"Load Messages"** button
6. You'll see your message variants appear

### 8B. Test Message (Recommended)

Before sending to everyone, send a test to yourself:

1. Find yourself in the contacts list
2. Check the checkbox next to your name
3. Click **"Start Campaign"**
4. SPAMURAI will:
   - Open WhatsApp Web (if not already open)
   - Find your chat
   - Send the message
   - Log the event to Firebase
5. Check your phone - you should receive the message!

### 8C. Send Bulk Broadcast

1. **Select recipients:**
   - Check boxes next to contacts you want to message
   - Or use **"Select All"** to message everyone

2. **Review settings:**
   - Delay between messages: Set in config (default 60 seconds)
   - Follow-up enabled: Check config.json

3. **Start campaign:**
   - Click **"Start Campaign"**
   - SPAMURAI will:
     - Send messages one by one
     - Wait the configured delay between each
     - Pause at timeout intervals (100, 300 messages)
     - Log all events to Firebase
     - Show progress in real-time

4. **Monitor progress:**
   - Watch the GUI for status updates
   - Check `config\whatsapp.log` for detailed logs
   - Check `config\sent_numbers.log` for successfully sent messages
   - Check `config\failed_numbers.log` for any failures

### 8D. Resume Capability

If SPAMURAI stops (crash, power outage, etc.):
- Simply restart and click "Start Campaign" again
- It will automatically skip numbers already in `sent_numbers.log`
- It will continue from where it left off

---

## 📊 Understanding SPAMURAI Files

### Config Folder Files

```
config/
├── config.json              → Your settings (YOU EDIT THIS)
├── firebase-credentials.json → Firebase credentials (auto-placed)
├── contacts.xlsx            → Downloaded from Google Sheets (auto-generated)
├── messages.xlsx            → Downloaded from Google Sheets (auto-generated)
├── whatsapp.log             → Detailed operation logs
├── sent_numbers.log         → Successfully sent numbers
├── failed_numbers.log       → Failed numbers with reasons
├── message_sent_log.json    → Message tracking
└── exclude.txt              → Numbers to skip (optional)
```

**To exclude numbers from campaigns:**
1. Open `config\exclude.txt` (create if doesn't exist)
2. Add phone numbers, one per line:
   ```
   919876543210
   918765432109
   ```
3. Save the file
4. These numbers will be skipped in all campaigns

---

## ⚙️ Advanced Settings

### Changing Message Delay

Edit `config.json`:
```json
"default_delay": 60
```
- `30` = 30 seconds between messages
- `60` = 1 minute (recommended)
- `120` = 2 minutes (safer)

### Adjusting Timeout Pauses

Edit `config.json`:
```json
"timeouts": {
  "50": 10,    ← Pause 10 min after 50 messages
  "100": 30,   ← Pause 30 min after 100 messages
  "300": 60    ← Pause 60 min after 300 messages
}
```

### Enabling Follow-up Messages

Edit `config.json`:
```json
"followup_config": {
  "enabled": true,
  "delay_seconds": 3
}
```
- SPAMURAI will send Column B message 3 seconds after Column A

### Sending Images/Media

Edit `config.json`:
```json
"send_as_media": true,
"media_file": "config/media/sample.jpeg"
```
1. Place your image in `config\media\` folder
2. Update `media_file` path
3. Message will be sent as caption with the image

---

## 🔧 Troubleshooting

### Problem: "Python not found"

**Solution:**
1. Uninstall Python completely
2. Download from python.org again
3. ⚠️ **CHECK "Add Python to PATH"** during installation
4. Restart your computer
5. Try again

### Problem: "Firebase credentials not configured"

**Solution:**
1. Check that `firebase_spamurai.json` exists
2. Run setup again:
   ```
   cd C:\SPAMURAI
   setup_firebase.bat firebase_spamurai.json
   ```
3. Or manually copy to `config\firebase-credentials.json`
4. Restart SPAMURAI

### Problem: "Failed to load contacts from Google Sheets"

**Solution:**
1. Verify sheet URL is correct in `config.json`
2. Make sure sheet is shared: "Anyone with the link" + "Viewer"
3. Check sheet has correct columns: Name, WhatsApp Number, nick_name
4. Check internet connection

### Problem: "WhatsApp Web not loading" or "QR code not appearing"

**Solution:**
1. Make sure Chrome is installed
2. Go to https://web.whatsapp.com manually in Chrome - does it work?
3. Clear Chrome cache/cookies
4. Try logging out of WhatsApp Web manually and restart SPAMURAI

### Problem: Messages sending too fast / account blocked

**Solution:**
1. Increase `default_delay` in config.json (try 120 seconds = 2 minutes)
2. Add more timeout pauses:
   ```json
   "timeouts": {
     "50": 15,
     "100": 30,
     "150": 30,
     "200": 60
   }
   ```
3. Don't send more than 200-300 messages per day initially
4. Build up slowly over days/weeks

### Problem: GUI doesn't open in browser

**Solution:**
1. Check Command Prompt for errors
2. Manually open browser and go to: http://localhost:8501
3. Check if port 8501 is already in use (close other instances)

### Problem: Need to check system

**Solution:**
Run the diagnostic tool:
```
cd C:\SPAMURAI
diagnose_windows.bat
```
It will check:
- ✅ Python installation
- ✅ Chrome installation
- ✅ Firebase credentials
- ✅ All required packages
- ✅ Network connectivity

Fix any issues it reports, then try again.

---

## 📈 Best Practices

### For WhatsApp Account Safety

1. **Start slow**: Send 50-100 messages first day, gradually increase
2. **Use delays**: Keep `default_delay` at 60 seconds minimum
3. **Add pauses**: Use timeout intervals every 50-100 messages
4. **Personalize**: Use `<nick_name>` placeholders for personalization
5. **Vary messages**: Use multiple message variants in your Google Sheet
6. **Don't spam**: Only message people who know you / expect your message
7. **Monitor**: Check for any warnings from WhatsApp

### For Firebase Costs (Free Tier)

Firebase free tier:
- **50,000 reads/day** - Free
- **20,000 writes/day** - Free
- **1 GB storage** - Free

For 300 messages/day, you'll use ~300-600 writes (well within free tier).

### For Data Management

1. **Backup your config.json** regularly
2. **Update Google Sheets** instead of editing Excel files locally
3. **Monitor logs**: Check `whatsapp.log` for issues
4. **Archive campaigns**: Save `sent_numbers.log` after each campaign
5. **Clean up**: Clear old logs periodically

---

## 🔐 Security & Privacy

### Keep These Files Secure

- ✅ `firebase_spamurai.json` - Contains Firebase access credentials
- ✅ `config/firebase-credentials.json` - Same credentials
- ✅ `config/config.json` - Contains your Google Sheets URLs and phone numbers

**Never:**
- Share these files publicly
- Commit them to public Git repositories
- Email them unencrypted
- Post them in forums/chat

### WhatsApp Data

- SPAMURAI only accesses WhatsApp Web through Chrome
- No passwords are stored
- No message content is sent to external servers (except Firebase logging)
- Your WhatsApp session stays on your computer

---

## 📚 Additional Resources

**Documentation Files:**
- `FIREBASE_SETUP.md` - Detailed Firebase information
- `GOOGLE_SHEETS_SETUP.md` - Advanced Google Sheets features
- `TROUBLESHOOTING.md` - Common issues and solutions
- `DIAGNOSTIC_TOOLS.md` - Using diagnostic tools

**Tools:**
- `launchers\SPAMURAI.bat` - Main launcher
- `diagnose_windows.bat` - System diagnostics
- `setup_firebase.bat` - Firebase setup tool

**Logs:**
- `config\whatsapp.log` - Detailed operation logs
- `config\sent_numbers.log` - Successfully sent messages
- `config\failed_numbers.log` - Failed messages

---

## 🎯 Quick Command Reference

```bash
# Launch SPAMURAI
launchers\SPAMURAI.bat

# Run diagnostics
diagnose_windows.bat

# Setup Firebase
setup_firebase.bat firebase_spamurai.json

# Check Firebase configured
echo %FIREBASE_CREDENTIALS%

# View logs
type config\whatsapp.log
type config\sent_numbers.log
type config\failed_numbers.log

# Edit config
notepad config\config.json
```

---

## ✅ Installation Checklist

Before your first broadcast, verify:

- [ ] Python installed with PATH
- [ ] Chrome installed
- [ ] SPAMURAI extracted to C:\SPAMURAI\
- [ ] Firebase credentials configured (either method)
- [ ] Contacts Google Sheet created and shared
- [ ] Messages Google Sheet created and shared
- [ ] config.json created and edited with:
  - [ ] Your name and phone number
  - [ ] Contacts sheet URL
  - [ ] Messages sheet URL
  - [ ] Firebase enabled
- [ ] SPAMURAI launches successfully
- [ ] GUI opens in browser
- [ ] WhatsApp Web connected
- [ ] Test message sent to yourself
- [ ] Ready for bulk broadcast! 🚀

---

## 🆘 Need Help?

1. **Run diagnostics**: `diagnose_windows.bat`
2. **Check logs**: `config\whatsapp.log`
3. **Review troubleshooting section** above
4. **Check detailed docs**: See Additional Resources section
5. **Verify configuration**: Make sure all URLs and settings are correct

---

**Congratulations! You're ready to use SPAMURAI! 🥷⚡**

**Remember:** Start with a test message to yourself, then gradually scale up your broadcasts.
