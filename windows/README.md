# SPAMURAI for Windows

**Everything Windows users need in one place 🥷⚡**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Setup
Double-click: **`setup_firebase.bat`**
- Configures Firebase credentials
- Takes 1 minute

### Step 2: Launch
Double-click: **`LAUNCH_SPAMURAI.bat`**
- Installs dependencies (first time: 2-5 min)
- Opens GUI in browser
- Ready to use!

### Step 3: Start Broadcasting
- Follow the GUI instructions
- Connect WhatsApp
- Send messages!

---

## 📚 Documentation

### Installation Guides

**📖 [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md)** ← **START HERE**
- Complete first-time setup (30-45 minutes)
- Covers everything from Python installation to first broadcast
- Includes Google Sheets setup, configuration, troubleshooting

**📖 [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)**
- Quick setup checklist (30 minutes)
- For users who want concise instructions

---

## 🛠️ Tools & Scripts

### Main Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| `LAUNCH_SPAMURAI.bat` | Launch SPAMURAI | Every time you want to use the app |
| `setup_firebase.bat` | Setup Firebase credentials | One-time setup (or when updating credentials) |
| `diagnose_windows.bat` | System diagnostics | When troubleshooting issues |

### How to Use

**First Time Setup:**
```
1. Double-click: setup_firebase.bat
2. Provide path to firebase_spamurai.json
3. Double-click: LAUNCH_SPAMURAI.bat
4. Wait for installation (2-5 minutes)
5. GUI opens in browser
```

**Daily Usage:**
```
1. Double-click: LAUNCH_SPAMURAI.bat
2. Wait 10 seconds
3. GUI opens in browser
4. Start broadcasting!
```

---

## 📋 Prerequisites

Before using SPAMURAI, make sure you have:

- ✅ **Windows 10 or 11**
- ✅ **Python 3.8+** ([Download](https://www.python.org/downloads/))
  - ⚠️ Check "Add Python to PATH" during installation
- ✅ **Google Chrome** ([Download](https://www.google.com/chrome/))
- ✅ **Firebase credentials file** (`firebase_spamurai.json`)
- ✅ **Google Sheets** (Contacts & Messages)

See [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md) for detailed instructions.

---

## 🔧 Troubleshooting

### Problem: "Python not found"

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. ⚠️ **CHECK "Add Python to PATH"** during installation
3. Restart computer
4. Try again

### Problem: "Firebase credentials not configured"

**Solution:**
1. Make sure you have `firebase_spamurai.json` file
2. Run: `setup_firebase.bat firebase_spamurai.json`
3. Follow the prompts
4. Restart LAUNCH_SPAMURAI.bat

### Problem: GUI doesn't open

**Solution:**
1. Manually open browser
2. Go to: `http://localhost:8501`

### Problem: Need full diagnostics

**Solution:**
1. Run: `diagnose_windows.bat`
2. Review the diagnostic report
3. Fix any issues shown
4. Try launching again

---

## 📁 Files in This Folder

```
windows/
├── README.md                      ← You are here
│
├── COMPLETE_WINDOWS_SETUP.md     ← Full installation guide
├── QUICK_START_WINDOWS.md        ← Quick setup guide
│
├── LAUNCH_SPAMURAI.bat           ← Main launcher (use this!)
├── setup_firebase.bat            ← Firebase setup
└── diagnose_windows.bat          ← System diagnostics
```

---

## 🎯 Typical Workflow

### First Time (30-45 minutes)

1. **Read:** [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md)
2. **Install:** Python & Chrome
3. **Setup Firebase:** Run `setup_firebase.bat`
4. **Create Google Sheets:** Contacts & Messages
5. **Configure:** Edit `../config/config.json`
6. **Launch:** Run `LAUNCH_SPAMURAI.bat`
7. **Connect:** WhatsApp Web
8. **Test:** Send to yourself
9. **Broadcast:** Send to everyone!

### Daily Usage (1 minute)

1. **Launch:** Double-click `LAUNCH_SPAMURAI.bat`
2. **Wait:** 10 seconds
3. **Use:** GUI opens in browser
4. **Broadcast:** Start sending!

---

## 📖 Additional Resources

### In This Folder
- [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md) - Full setup guide
- [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md) - Quick reference

### In Main Project
- `../README.md` - Main project README
- `../docs/FIREBASE_SETUP.md` - Detailed Firebase info
- `../docs/GOOGLE_SHEETS_SETUP.md` - Google Sheets advanced features
- `../docs/TROUBLESHOOTING.md` - Common issues
- `../config/config.example.json` - Configuration template

---

## 🆘 Need Help?

1. **Run diagnostics:** `diagnose_windows.bat`
2. **Read full guide:** [COMPLETE_WINDOWS_SETUP.md](COMPLETE_WINDOWS_SETUP.md)
3. **Check troubleshooting:** `../docs/TROUBLESHOOTING.md`
4. **Review logs:** `../config/whatsapp.log`

---

## ✅ Quick Checklist

Before your first broadcast:

- [ ] Python 3.8+ installed (with PATH)
- [ ] Chrome installed
- [ ] Firebase setup completed (`setup_firebase.bat`)
- [ ] Google Sheets created (Contacts & Messages)
- [ ] `config.json` configured
- [ ] Test message sent to yourself
- [ ] Ready to broadcast!

---

**Windows users: You're all set! Everything you need is in this folder! 🚀**

**Quick Start: Double-click `LAUNCH_SPAMURAI.bat` to begin!**
