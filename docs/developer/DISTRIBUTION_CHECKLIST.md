# SPAMURAI Distribution Checklist

**What to share with users for easy installation**

---

## Required Files

### 1. Main Application Folder
```
wa_broadcaster/
├── src/
├── config/
├── launchers/
├── requirements.txt
├── setup_firebase.bat
├── setup_firebase.sh
├── diagnose_windows.bat
├── diagnose_mac.sh
└── ... (all other files)
```

### 2. Firebase Credentials File (MANDATORY)
```
firebase_spamurai.json
```

**⚠️ Important:**
- This file is REQUIRED for SPAMURAI to work
- Must be distributed separately or bundled with the app
- Include the `FIREBASE_CREDENTIALS_README.txt` to explain how to install it

### 3. Documentation Files

**Essential:**
- `WINDOWS_INSTALLATION.md` - Full Windows setup guide
- `QUICK_START_WINDOWS.md` - Quick Windows setup
- `FIREBASE_CREDENTIALS_README.txt` - Firebase credentials instructions

**Optional but recommended:**
- `FIREBASE_SETUP.md` - Detailed Firebase information
- `TROUBLESHOOTING.md` - Common issues and solutions
- `DIAGNOSTIC_TOOLS.md` - Using diagnostic tools

---

## Distribution Options

### Option 1: ZIP Package (Recommended)

Create a ZIP file with this structure:

```
SPAMURAI-v1.0.zip
├── wa_broadcaster/          (entire application folder)
├── firebase_spamurai.json   (Firebase credentials)
├── README.txt               (Points to installation guide)
└── FIREBASE_CREDENTIALS_README.txt
```

**README.txt contents:**
```
SPAMURAI - WhatsApp Broadcast Tool

WINDOWS INSTALLATION:
See: wa_broadcaster/WINDOWS_INSTALLATION.md

QUICK START:
See: wa_broadcaster/QUICK_START_WINDOWS.md

FIREBASE SETUP:
See: FIREBASE_CREDENTIALS_README.txt

For issues, run: diagnose_windows.bat
```

### Option 2: Installer (Advanced)

Use the native installer system (see `build/` folder) to create:
- `SPAMURAI-Setup.exe` for Windows
- `SPAMURAI.app` for macOS

Bundle `firebase_spamurai.json` with installer or prompt user to locate it during installation.

### Option 3: GitHub Release

Upload to GitHub Releases:

```
SPAMURAI-v1.0-Windows.zip
├── wa_broadcaster/
├── firebase_spamurai.json
└── FIREBASE_CREDENTIALS_README.txt
```

Include installation instructions in the release notes.

---

## Pre-Distribution Checklist

Before sharing with users:

- [ ] Test installation on clean Windows machine
- [ ] Verify `firebase_spamurai.json` is valid and working
- [ ] Ensure `config.example.json` has Firebase enabled
- [ ] Test both automatic and manual Firebase setup methods
- [ ] Run `diagnose_windows.bat` to verify all checks pass
- [ ] Update version numbers in documentation
- [ ] Include all essential documentation files
- [ ] Test the launcher: `launchers\SPAMURAI.bat`

---

## User Setup Flow (What they'll do)

1. **Extract ZIP** to `C:\SPAMURAI\`
2. **Install Python** (if not installed)
3. **Install Chrome** (if not installed)
4. **Setup Firebase:**
   - Run: `setup_firebase.bat firebase_spamurai.json`
   - OR manually copy to `config\` folder
5. **Launch:** Double-click `launchers\SPAMURAI.bat`
6. **Done!**

Total time: ~10 minutes

---

## Firebase Credentials Security

**Important reminders:**

✅ **DO:**
- Keep `firebase_spamurai.json` secure
- Share only with authorized users
- Use separate Firebase projects for dev/production
- Document which Firebase project is being used
- Rotate credentials periodically

❌ **DON'T:**
- Commit `firebase_spamurai.json` to public Git repos
- Share on public forums or chat
- Email without encryption
- Leave in publicly accessible folders

---

## Support Materials

### What to tell users:

**Subject: SPAMURAI Installation**

"I'm sharing SPAMURAI with you. Here's what to do:

1. Extract the ZIP file to C:\SPAMURAI\
2. Read: WINDOWS_INSTALLATION.md or QUICK_START_WINDOWS.md
3. Follow the installation steps
4. If you have issues, run: diagnose_windows.bat

The firebase_spamurai.json file is required - see FIREBASE_CREDENTIALS_README.txt for setup instructions.

Let me know if you need help!"

---

## Version Tracking

When releasing a new version:

- [ ] Update version in `src/gui.py`
- [ ] Update version in documentation
- [ ] Tag Git release
- [ ] Update changelog
- [ ] Create new ZIP package
- [ ] Upload to distribution location
- [ ] Notify users of update

---

## Files to EXCLUDE from Distribution

Don't include these (user-specific/generated files):

```
config/config.json           (user creates from example)
config/firebase-credentials.json (user adds their own)
config/*.log                 (generated logs)
config/sent_numbers.log      (user-specific)
config/failed_numbers.log    (user-specific)
venv/                        (auto-generated)
__pycache__/                 (auto-generated)
.git/                        (development only)
*.pyc                        (compiled Python)
.DS_Store                    (Mac system files)
```

---

## Testing New Distribution

Before sharing with users, test on a clean system:

1. **Use a VM or fresh Windows install**
2. **Extract your distribution package**
3. **Follow installation guide step-by-step**
4. **Verify everything works**
5. **Note any issues or unclear instructions**
6. **Update documentation if needed**

---

**Ready to distribute!** 🚀
