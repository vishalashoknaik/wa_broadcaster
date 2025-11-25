# SPAMURAI Folder Structure

**Clean and organized documentation structure**

---

## 📁 Root Directory

User-facing essentials only:

```
wa_broadcaster/
├── README.md                          ← Main entry point
│
├── windows/                           ← Windows users start here!
│   ├── README.md                     ← Windows entry point
│   ├── COMPLETE_WINDOWS_SETUP.md     ← Full setup guide
│   ├── QUICK_START_WINDOWS.md        ← Quick reference
│   ├── LAUNCH_SPAMURAI.bat           ← Main launcher
│   ├── setup_firebase.bat            ← Firebase setup
│   └── diagnose_windows.bat          ← System diagnostics
│
├── requirements.txt                   ← Python dependencies
├── setup_firebase.sh                  ← Firebase setup (Mac/Linux)
├── diagnose_mac.sh                    ← System diagnostics (Mac)
├── start_spamurai.sh                  ← Launch script (Mac/Linux)
├── firebase_spamurai.json             ← Firebase credentials (user adds)
│
├── src/                               ← Source code
├── config/                            ← Configuration files
├── launchers/                         ← Launch scripts
├── tests/                             ← Test files
└── docs/                              ← Documentation
```

---

## 🪟 windows/ - Windows Users Folder

Everything Windows users need in one place:

```
windows/
├── README.md                          ← Windows entry point
├── COMPLETE_WINDOWS_SETUP.md         ← Full installation guide (30-45 min)
├── QUICK_START_WINDOWS.md            ← Quick setup checklist (30 min)
│
├── LAUNCH_SPAMURAI.bat               ← Main launcher (double-click this!)
├── setup_firebase.bat                ← Firebase credentials setup
└── diagnose_windows.bat              ← System diagnostics
```

**For Windows users:** This is your one-stop folder. Everything you need is here!

---

## 📚 docs/ - User Documentation

Reference guides and help:

```
docs/
├── FIREBASE_SETUP.md                  ← Complete Firebase documentation
├── FIREBASE_CREDENTIALS_README.txt    ← How to install firebase_spamurai.json
├── GOOGLE_SHEETS_SETUP.md             ← Google Sheets advanced features
├── TROUBLESHOOTING.md                 ← Common issues and solutions
├── DIAGNOSTIC_TOOLS.md                ← Using diagnostic tools
├── FOLDER_STRUCTURE.md                ← This file
├── CLEANUP_SUMMARY.md                 ← Record of folder cleanup
│
├── advanced/                          ← Advanced features
│   └── MESSAGE_DEDUPLICATION.md       ← Deduplication system
│
└── developer/                         ← For developers/distributors
    ├── DISTRIBUTION_CHECKLIST.md      ← How to package and distribute
    ├── LAUNCHERS.md                   ← Launcher system documentation
    ├── build/                         ← Build system for executables
    │   ├── BUILD_INSTRUCTIONS.md
    │   ├── build.py
    │   ├── build_windows.py
    │   └── ... (PyInstaller configs)
    └── utils/                         ← Utility scripts
        └── gen_import_contacts_csv.au3
```

---

## 🧪 tests/ - Test Files

Test scripts and utilities:

```
tests/
├── test_firebase.py                   ← Firebase connection test
└── test_deduplication.py              ← Message deduplication test
```

---

## 🗂️ config/ - Configuration & Data

User configuration and generated files:

```
config/
├── config.example.json                ← Template (DO NOT EDIT)
├── config.json                        ← User config (create from example)
├── firebase-credentials.json          ← Firebase credentials (auto-placed)
│
├── contacts.xlsx                      ← Downloaded from Google Sheets
├── messages.xlsx                      ← Downloaded from Google Sheets
│
├── whatsapp.log                       ← Detailed operation logs
├── sent_numbers.log                   ← Successfully sent numbers
├── failed_numbers.log                 ← Failed numbers with reasons
├── message_sent_log.json              ← Message tracking
├── message_content_log.json           ← Content tracking
├── exclude.txt                        ← Numbers to skip (optional)
│
└── media/                             ← Media files for broadcasts
    └── sample.jpeg                    ← Example media file
```

---

## 💻 src/ - Source Code

Application source code:

```
src/
├── gui.py                             ← Streamlit GUI (main interface)
├── wa_broadcaster.py                  ← Main orchestrator
├── messenger.py                       ← WhatsApp Web automation
├── tracker.py                         ← Logging and state tracking
├── firebase_logger.py                 ← Firebase integration
├── lib.py                             ← Utility functions
│
└── (other source files)
```

---

## 🚀 launchers/ - Launch Scripts

One-click launchers:

```
launchers/
├── SPAMURAI.bat                       ← Windows launcher
├── SPAMURAI.command                   ← Mac launcher
├── SPAMURAI_DEBUG.bat                 ← Windows debug launcher
├── SPAMURAI_DEBUG.command             ← Mac debug launcher
└── README.md                          ← Launcher documentation
```

---

## 📋 Documentation Hierarchy

### For End Users:

1. **Start Here:**
   - `README.md` → Overview and quick links
   - `COMPLETE_WINDOWS_SETUP.md` → Full setup guide

2. **Quick Reference:**
   - `QUICK_START_WINDOWS.md` → Fast setup
   - `GETTING_STARTED.txt` → One-page printable

3. **Configuration Help:**
   - `docs/FIREBASE_SETUP.md`
   - `docs/FIREBASE_CREDENTIALS_README.txt`
   - `docs/GOOGLE_SHEETS_SETUP.md`

4. **Troubleshooting:**
   - `docs/TROUBLESHOOTING.md`
   - `docs/DIAGNOSTIC_TOOLS.md`

### For Advanced Users:

5. **Advanced Features:**
   - `docs/advanced/MESSAGE_DEDUPLICATION.md`

### For Developers/Distributors:

6. **Development:**
   - `docs/developer/DISTRIBUTION_CHECKLIST.md`
   - `docs/developer/LAUNCHERS.md`
   - `CLAUDE.md` (project architecture)

---

## 🗑️ Deleted Files (Redundant)

Removed to clean up the project:

- ❌ `WINDOWS_INSTALLATION.md` - Replaced by `COMPLETE_WINDOWS_SETUP.md`
- ❌ `SETUP_INSTRUCTIONS.txt` - Replaced by `COMPLETE_WINDOWS_SETUP.md`
- ❌ `README_INSTALLATION.md` - Replaced by `README.md`
- ❌ `COMBINATION_SUMMARY_EXAMPLE.md` - Technical doc, not needed

---

## 📦 Distribution Package

When sharing SPAMURAI with users, include:

```
SPAMURAI-v1.0.zip
│
├── wa_broadcaster/                    ← Entire folder
│   ├── README.md                     ← Points to setup guide
│   ├── COMPLETE_WINDOWS_SETUP.md
│   ├── QUICK_START_WINDOWS.md
│   ├── GETTING_STARTED.txt
│   ├── src/
│   ├── config/
│   ├── launchers/
│   ├── docs/
│   └── ... (all files)
│
├── firebase_spamurai.json             ← Your credentials file
└── START_HERE.txt                     ← Points to README.md
```

---

## 🎯 Finding Documentation

| What You Need | Where to Look |
|---------------|---------------|
| Getting started | `README.md` |
| **Windows setup** | **`windows/`** folder |
| Complete installation (Windows) | `windows/COMPLETE_WINDOWS_SETUP.md` |
| Quick setup (Windows) | `windows/QUICK_START_WINDOWS.md` |
| Firebase help | `docs/FIREBASE_SETUP.md` |
| Google Sheets help | `docs/GOOGLE_SHEETS_SETUP.md` |
| Troubleshooting | `docs/TROUBLESHOOTING.md` |
| System diagnostics | `docs/DIAGNOSTIC_TOOLS.md` |
| Advanced features | `docs/advanced/` |
| Distribution guide | `docs/developer/DISTRIBUTION_CHECKLIST.md` |
| Build system | `docs/developer/build/` |
| Test files | `tests/` |

---

**Clean. Organized. Easy to navigate. 🥷⚡**
