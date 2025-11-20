# SPAMURAI - Windows Quick Start Guide

**Get up and running in 30 minutes.**

⚠️ **Note:** For complete first-time setup with detailed explanations, see COMPLETE_WINDOWS_SETUP.md

---

## Installation Checklist

- [ ] Install Python
- [ ] Install Chrome
- [ ] Download SPAMURAI
- [ ] Setup Firebase
- [ ] Create Google Sheets (or have URLs ready)
- [ ] Configure SPAMURAI
- [ ] Launch SPAMURAI

---

## 1. Install Python (5 minutes)

1. Go to: **https://www.python.org/downloads/**
2. Download Python (latest version)
3. Run installer
4. ✅ **CHECK "Add Python to PATH"**
5. Click "Install Now"

---

## 2. Install Chrome (2 minutes)

1. Go to: **https://www.google.com/chrome/**
2. Download and install

---

## 3. Download SPAMURAI (1 minute)

1. Download SPAMURAI folder
2. Extract to: `C:\SPAMURAI\`

---

## 4. Setup Firebase (1 minute)

You'll receive a **`firebase_spamurai.json`** file with SPAMURAI.

### Option A: Automatic Setup (Recommended)

1. Open Command Prompt (search "cmd")
2. Type:
   ```
   cd C:\SPAMURAI
   setup_firebase.bat firebase_spamurai.json
   ```
3. Wait for "Setup complete!"
4. Close Command Prompt

### Option B: Manual Setup

1. Copy `firebase_spamurai.json` to `C:\SPAMURAI\config\`
2. Rename it to `firebase-credentials.json`
3. Done!

---

## 5. Setup Google Sheets (10 minutes)

### Contacts Sheet:
1. Create Google Sheet with columns: **Name | WhatsApp Number | nick_name**
2. Add your contacts (phone with country code, no +)
3. Share: "Anyone with the link" → "Viewer"
4. Copy URL

### Messages Sheet:
1. Create Google Sheet with columns: **First Messages | Followup Messages**
2. Add message variants (use `<nick_name>` placeholder)
3. Share: "Anyone with the link" → "Viewer"
4. Copy URL

**See COMPLETE_WINDOWS_SETUP.md Step 4 for detailed instructions**

---

## 6. Configure SPAMURAI (3 minutes)

1. Copy `config\config.example.json` to `config\config.json`
2. Edit `config.json` in Notepad
3. Update:
   - Your name and phone number
   - Contacts Google Sheet URL
   - Messages Google Sheet URL
   - Firebase should already be enabled
4. Save

---

## 7. Launch SPAMURAI (2 minutes)

1. Go to: `C:\SPAMURAI\launchers\`
2. **Double-click: `SPAMURAI.bat`**
3. First run installs packages (2-5 minutes)
4. Browser opens automatically
5. Done! 🎉

---

## First-Time Usage

1. **Connect WhatsApp:**
   - Click "Start Campaign" in GUI
   - Chrome opens WhatsApp Web
   - Scan QR code with your phone (WhatsApp → Linked Devices)

2. **Send test message:**
   - Select yourself in contacts list
   - Click "Start Campaign"
   - Check your phone for the message

3. **Send bulk broadcast:**
   - Select all contacts (or specific ones)
   - Click "Start Campaign"
   - Monitor progress in GUI

---

## Daily Usage

**To launch SPAMURAI:**
- Double-click: `launchers\SPAMURAI.bat`
- Wait 10 seconds
- GUI opens in browser
- WhatsApp already connected (no QR code needed)
- Start sending!

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Reinstall Python with "Add to PATH" checked |
| "Firebase not configured" | Re-run: `setup_firebase.bat firebase_spamurai.json` |
| Manual Firebase setup | Copy `firebase_spamurai.json` to `config\`, rename to `firebase-credentials.json` |
| GUI doesn't open | Open browser, go to: http://localhost:8501 |
| Need help? | Run: `diagnose_windows.bat` |

---

## Full Documentation

- **Detailed Setup**: `WINDOWS_INSTALLATION.md`
- **Firebase Guide**: `FIREBASE_SETUP.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`

---

**That's it! You're ready to go! 🥷⚡**
