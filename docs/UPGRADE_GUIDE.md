# SPAMURAI Upgrade Guide

## Upgrading to Latest Version

This guide helps existing SPAMURAI users upgrade to the latest version with new features like user profile tracking and enhanced Firebase integration.

---

## Quick Upgrade Steps

### For All Users:

1. **Pull the latest code**
   ```bash
   git pull origin master
   ```

2. **Update dependencies** (automatic in most cases)
   - If using the launcher scripts (`LAUNCH_SPAMURAI.bat` or `SPAMURAI.command`), dependencies will auto-install
   - Or manually run: `pip install -r requirements.txt`

3. **Update your config.json**
   - Add the new `user_profile` section (see below)

4. **Launch SPAMURAI**
   - Use the launcher scripts as usual
   - First run will auto-install `firebase-admin` if needed

---

## What's New

### 1. User Profile Tracking
Your name and phone number are now tracked with every message sent to Firebase.

### 2. Firebase Admin Auto-Install
The `firebase-admin` package will automatically install on first run if missing.

### 3. Firebase Credentials Naming
Preferred filename is now `config/firebase.json` (backward compatible with old naming).

### 4. Project Reorganization
- Documentation moved to `docs/`
- Windows files moved to `windows/`
- Better folder structure

---

## Required Config Changes

### Add User Profile Section

Open your `config/config.json` and add this at the top:

```json
{
  "user_profile": {
    "name": "Your Full Name",
    "phone_number": "9876543210"
  },
  ... (rest of your existing config)
}
```

**Note:** Phone number should be 10 digits (without country code or special characters).

### Example Updated Config:

```json
{
  "user_profile": {
    "name": "John Doe",
    "phone_number": "9876543210"
  },
  "google_sheets_config": {
    "messages": {
      "sheet_url": "https://docs.google.com/spreadsheets/d/...",
      "tab_name": "Sheet1"
    },
    "contacts": {
      "sheet_url": "https://docs.google.com/spreadsheets/d/...",
      "tab_name": "Sheet1"
    }
  },
  "firebase_config": {
    "enabled": true,
    "credentials_path": "config/firebase.json",
    "collection_name": "message_events"
  },
  ... (other settings)
}
```

---

## Firebase Credentials Update (Optional)

### Old Naming (Still Works):
```
config/firebase-credentials.json
```

### New Naming (Recommended):
```
config/firebase.json
```

**To update:**
1. Rename your credentials file: `firebase-credentials.json` → `firebase.json`
2. Update `config.json`:
   ```json
   "firebase_config": {
     "credentials_path": "config/firebase.json"
   }
   ```

The launcher will show a notice if you're using the old naming, but it will still work.

---

## Dependency Installation

### Automatic (Recommended)

Just launch SPAMURAI using the launcher scripts:
- **Windows**: `LAUNCH_SPAMURAI.bat` or `windows/LAUNCH_SPAMURAI.bat`
- **Mac**: `launchers/SPAMURAI.command`

The launcher will:
1. Check for `firebase-admin` package
2. Auto-install if missing
3. Verify Firebase credentials exist

### Manual Installation

If you prefer to install manually:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or just install firebase-admin
pip install firebase-admin>=6.0.0
```

---

## Troubleshooting Upgrades

### Issue: "firebase-admin not found"

**Solution:**
- Run the launcher script (auto-installs)
- Or manually: `pip install firebase-admin`

### Issue: "User profile not configured"

**Solution:**
- Add `user_profile` section to your `config.json` (see above)
- GUI will show validation errors if fields are missing

### Issue: "Firebase credentials not found"

**Solution:**
- Make sure your `config/firebase.json` or `config/firebase-credentials.json` exists
- Contact your POC if you don't have the file
- Check `firebase_config.credentials_path` in your config.json

### Issue: Virtual environment issues

**Solution:**
- Delete the `venv/` folder
- Run the launcher again (it will recreate the venv)

### Issue: Import errors after upgrade

**Solution:**
```bash
# Clear old packages and reinstall
rm -rf venv/
pip install -r requirements.txt
```

---

## Verification Steps

After upgrading, verify everything works:

1. **Launch SPAMURAI**
   ```bash
   # Windows
   LAUNCH_SPAMURAI.bat

   # Mac
   ./launchers/SPAMURAI.command
   ```

2. **Check the GUI**
   - You should see the "User Profile" section at the top
   - Enter your name and phone number
   - Save configuration

3. **Send a test message**
   - Use a small contact list
   - Verify Firebase logs include sender information

4. **Check Firebase Console**
   - Go to your Firestore collection
   - Recent message events should include:
     ```json
     {
       "sender": {
         "name": "Your Name",
         "phone": "9876543210"
       }
     }
     ```

---

## Rolling Back (If Needed)

If you encounter issues and need to roll back:

```bash
# 1. Check out previous version
git log --oneline
git checkout <previous-commit-hash>

# 2. Reinstall old dependencies
pip install -r requirements.txt

# 3. Revert config changes
# Remove user_profile section from config.json
```

---

## Getting Help

If you run into issues:

1. **Check logs**
   - `config/whatsapp.log` - Main application log
   - Check terminal output for error messages

2. **Run diagnostics**
   - **Windows**: `windows/diagnose_windows.bat`
   - **Mac**: `./diagnose_mac.sh`

3. **Contact Support**
   - Create an issue on GitHub
   - Contact your POC for Firebase-related issues

---

## Summary Checklist

After upgrading, make sure you have:

- [ ] Pulled latest code (`git pull`)
- [ ] Added `user_profile` to `config.json`
- [ ] Run the launcher (auto-installs dependencies)
- [ ] Firebase credentials in place (`config/firebase.json`)
- [ ] Tested with a small campaign
- [ ] Verified sender info appears in Firebase logs

---

**Version:** Updated for SPAMURAI v1.10.2+

**Last Updated:** 2024-11-20
