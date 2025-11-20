# SPAMURAI - WhatsApp Broadcast Tool

**Strike fast. Strike precise. Leave no trace. 🥷⚡**

Professional WhatsApp broadcast automation tool with Google Sheets integration and Firebase logging.

---

## 🚀 Quick Start

### For Windows Users

**Option 1: Quick Launch (if already set up)**
- Double-click: **`LAUNCH_SPAMURAI.bat`** in root folder

**Option 2: Full Setup & Documentation**
- 📁 Go to **[windows/](windows/)** folder for complete guides

**What's in the Windows folder:**
- ✅ Complete setup guide
- ✅ Quick start guide
- ✅ Firebase setup script
- ✅ Diagnostics tool

### For Mac/Linux Users

Use the launcher script:
```bash
./start_spamurai.sh
```

Or see the full documentation in `docs/`

---

## ✨ Features

- ✅ **Google Sheets Integration** - Manage contacts and messages in spreadsheets
- ✅ **Multiple Message Variants** - Randomly select from message pool
- ✅ **Follow-up Messages** - Send immediate follow-up (3-second delay)
- ✅ **Personalization** - Use `<nick_name>` placeholders
- ✅ **Firebase Logging** - Cloud-based event logging and analytics
- ✅ **Smart Delays** - Configurable delays and automatic pauses
- ✅ **Resume Capability** - Continue from where you left off
- ✅ **Exclude List** - Skip specific numbers
- ✅ **Media Support** - Send images with captions
- ✅ **Rate Limiting Protection** - Built-in WhatsApp safety features

---

## 📋 Requirements

- **Windows 10/11** (or macOS/Linux)
- **Python 3.8+**
- **Google Chrome**
- **WhatsApp Account**
- **Google Account** (for Google Sheets)
- **Firebase Credentials** (provided as `firebase_spamurai.json`)

---

## 📦 Installation Overview

**For Windows Users:**
1. Go to `windows/` folder
2. Follow `README.md` or `COMPLETE_WINDOWS_SETUP.md`
3. Run `setup_firebase.bat`
4. Double-click `LAUNCH_SPAMURAI.bat`

**For Mac/Linux Users:**
1. Run `./start_spamurai.sh`
2. Follow on-screen instructions

---

## 🎯 Daily Usage

Once installed:

1. **Launch:**
   ```
   Double-click: launchers\SPAMURAI.bat
   ```

2. **GUI opens** in browser (http://localhost:8501)

3. **Start broadcasting:**
   - Click "Load Contacts"
   - Click "Load Messages"
   - Select recipients
   - Click "Start Campaign"

---

## 📚 Documentation

### For Windows Users
- 📁 **[Windows Folder](windows/)** - Everything Windows users need
  - Complete setup guide
  - Quick start guide
  - Launch scripts
  - Diagnostics tools

### Configuration & Setup
- 📖 **[Firebase Setup](docs/FIREBASE_SETUP.md)** - Detailed Firebase information
- 📖 **[Firebase Credentials](docs/FIREBASE_CREDENTIALS_README.txt)** - How to install credentials
- 📖 **[Google Sheets Setup](docs/GOOGLE_SHEETS_SETUP.md)** - Advanced Google Sheets features

### Troubleshooting & Tools
- 📖 **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- 📖 **[Diagnostic Tools](docs/DIAGNOSTIC_TOOLS.md)** - Using system diagnostics

### Advanced Features
- 📖 **[Message Deduplication](docs/advanced/MESSAGE_DEDUPLICATION.md)** - Prevent duplicate campaigns

### For Developers/Distributors
- 📖 **[Distribution Checklist](docs/developer/DISTRIBUTION_CHECKLIST.md)** - How to package and distribute
- 📖 **[Launcher System](docs/developer/LAUNCHERS.md)** - Understanding launchers

---

## 🛠️ Tools & Scripts

### Launchers
```bash
# Windows
launchers\SPAMURAI.bat

# Mac/Linux
./start_spamurai.sh
```

### Diagnostics
```bash
# Windows
diagnose_windows.bat

# Mac/Linux
./diagnose_mac.sh
```

### Firebase Setup
```bash
# Windows
setup_firebase.bat firebase_spamurai.json

# Mac/Linux
./setup_firebase.sh firebase_spamurai.json
```

---

## 📁 Project Structure

```
wa_broadcaster/
├── README.md                          ← You are here
│
├── windows/                           ← Windows users start here!
│   ├── README.md                     ← Windows entry point
│   ├── COMPLETE_WINDOWS_SETUP.md     ← Full setup guide
│   ├── QUICK_START_WINDOWS.md        ← Quick reference
│   ├── LAUNCH_SPAMURAI.bat           ← Main launcher
│   ├── setup_firebase.bat            ← Firebase setup
│   └── diagnose_windows.bat          ← System diagnostics
│
├── src/                               ← Source code
│   ├── gui.py                        ← Streamlit GUI
│   ├── wa_broadcaster.py             ← Main orchestrator
│   ├── messenger.py                  ← WhatsApp automation
│   ├── tracker.py                    ← Logging
│   └── firebase_logger.py            ← Firebase integration
│
├── config/                            ← Configuration & data
│   ├── config.example.json           ← Example config (copy to config.json)
│   ├── config.json                   ← Your config (create from example)
│   └── firebase-credentials.json     ← Firebase credentials
│
├── launchers/                         ← Launch scripts
│   ├── SPAMURAI.bat                  ← Windows launcher
│   └── SPAMURAI.command              ← Mac launcher
│
├── docs/                              ← Documentation
│   ├── FIREBASE_SETUP.md
│   ├── FIREBASE_CREDENTIALS_README.txt
│   ├── GOOGLE_SHEETS_SETUP.md
│   ├── TROUBLESHOOTING.md
│   ├── DIAGNOSTIC_TOOLS.md
│   ├── advanced/
│   │   └── MESSAGE_DEDUPLICATION.md
│   └── developer/
│       ├── DISTRIBUTION_CHECKLIST.md
│       ├── LAUNCHERS.md
│       ├── build/                    ← Build system
│       └── utils/                    ← Utility scripts
│
├── tests/                             ← Test files
│   ├── test_firebase.py
│   └── test_deduplication.py
│
├── setup_firebase.sh                  ← Firebase setup (Mac/Linux)
├── diagnose_mac.sh                    ← System diagnostics (Mac)
├── start_spamurai.sh                  ← Quick launcher (Mac/Linux)
├── requirements.txt                   ← Python dependencies
└── firebase_spamurai.json             ← Firebase credentials (you add this)
```

---

## ⚙️ Configuration

### Google Sheets Setup

**Contacts Sheet:**
| Name | WhatsApp Number | nick_name |
|------|-----------------|-----------|
| John Doe | 919876543210 | John |
| Jane Smith | 918765432109 | Jane |

**Messages Sheet:**
| First Messages | Followup Messages |
|----------------|-------------------|
| Hey <nick_name>! 👋 | Let me know! |
| Hello <nick_name>! | Would love to hear from you. |

See [Google Sheets Setup Guide](docs/GOOGLE_SHEETS_SETUP.md) for details.

### Config File

Edit `config/config.json`:
```json
{
  "user_profile": {
    "name": "Your Name",
    "phone_number": "919876543210"
  },
  "google_sheets_config": {
    "messages": {
      "sheet_url": "YOUR_MESSAGES_SHEET_URL"
    },
    "contacts": {
      "sheet_url": "YOUR_CONTACTS_SHEET_URL"
    }
  },
  "firebase_config": {
    "enabled": true
  },
  "default_delay": 60,
  "timeouts": {
    "100": 30,
    "300": 30
  }
}
```

---

## 🔧 Troubleshooting

### Quick Diagnostics
```bash
# Windows
diagnose_windows.bat

# Mac/Linux
./diagnose_mac.sh
```

### Common Issues

**"Python not found"**
- Install Python from python.org
- Check "Add Python to PATH" during installation

**"Firebase credentials not configured"**
- Run: `setup_firebase.bat firebase_spamurai.json`
- Or manually copy to `config/firebase-credentials.json`

**"Failed to load contacts"**
- Check Google Sheet URL in config.json
- Make sure sheet is shared: "Anyone with the link" → "Viewer"

**"WhatsApp Web not loading"**
- Install/update Chrome
- Clear Chrome cache
- Try logging out of WhatsApp Web manually

See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for more solutions.

---

## 📊 Logs & Output

### Log Files
```
config/
├── whatsapp.log              ← Detailed operation logs
├── sent_numbers.log          ← Successfully sent numbers
├── failed_numbers.log        ← Failed numbers with reasons
├── message_sent_log.json     ← Message tracking
└── message_content_log.json  ← Message content tracking
```

### Firebase Logging

All message events are logged to Firebase Firestore:
- Message sent/failed events
- Recipient information
- Message content hashes
- Timestamps and session IDs
- Custom tags

View logs in Firebase Console: https://console.firebase.google.com/

---

## 🔐 Security & Privacy

### Keep These Secure
- ✅ `firebase_spamurai.json` - Contains Firebase credentials
- ✅ `config/config.json` - Contains your Google Sheet URLs
- ✅ `config/firebase-credentials.json` - Firebase credentials

**Never:**
- Share these files publicly
- Commit to public Git repositories
- Email unencrypted
- Post in forums/chat

### WhatsApp Data
- SPAMURAI only accesses WhatsApp Web through Chrome
- No passwords stored
- No message content sent to external servers (except Firebase logging)
- Session stays on your computer

---

## 💰 Costs (Firebase Free Tier)

Firebase Firestore free tier:
- **50,000 reads/day** - Free
- **20,000 writes/day** - Free
- **1 GB storage** - Free

For 300 messages/day: ~300-600 writes/day (well within free tier)

---

## 📈 Best Practices

### WhatsApp Account Safety
1. Start slow: 50-100 messages first day
2. Use delays: 60+ seconds between messages
3. Add pauses: Every 50-100 messages
4. Personalize: Use `<nick_name>` placeholders
5. Vary messages: Multiple variants in Google Sheet
6. Don't spam: Only message people who expect it
7. Monitor: Check for WhatsApp warnings

### Message Quality
- Keep messages conversational
- Use personalization (nick_name)
- Vary message content (multiple variants)
- Test with yourself first
- Respect opt-outs

---

## 🆘 Support

1. **Run diagnostics:** `diagnose_windows.bat` or `diagnose_mac.sh`
2. **Check logs:** `config/whatsapp.log`
3. **Review docs:** See [Documentation](#-documentation) section
4. **Check troubleshooting:** [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

---

## 📝 License & Usage

This tool is for authorized use only. Users are responsible for:
- Complying with WhatsApp Terms of Service
- Respecting recipient privacy
- Following anti-spam regulations
- Obtaining necessary permissions

**Recommended use cases:**
- Small business customer communications
- Community announcements
- Event reminders
- Personal broadcasts to known contacts

**Not recommended for:**
- Mass unsolicited marketing
- Spamming unknown contacts
- Automated bot responses
- Violation of WhatsApp policies

---

## 🎯 Version

**Current Version:** 1.5.1

See `CLAUDE.md` for detailed version information and architecture.

---

## 🙏 Credits

Built with:
- Python & Streamlit
- Selenium WebDriver
- Firebase Firestore
- Google Sheets API
- Chrome DevTools Protocol

---

**Ready to start? 📖 [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md)**

**Questions? 🔧 [Troubleshooting Guide](docs/TROUBLESHOOTING.md)**

**Happy Broadcasting! 🥷⚡**
