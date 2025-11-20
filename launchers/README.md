# SPAMURAI Quick Launchers

**Strike fast. Strike precise. Leave no trace. 🥷⚡**

These launchers provide a hassle-free way to run SPAMURAI without typing commands.

---

## 🪟 Windows Users

### Quick Start
1. **Double-click** `SPAMURAI.bat`
2. Wait for dependencies to install (first run only)
3. GUI opens automatically in your browser

### What it does
✅ Checks Python installation
✅ Creates virtual environment
✅ Installs all dependencies
✅ Launches SPAMURAI GUI
✅ Handles errors gracefully

### Requirements
- Python 3.8 or higher ([Download](https://www.python.org/downloads/))
- Check "Add Python to PATH" during installation
- **Firebase credentials configured** (See FIREBASE_SETUP.md)

---

## 🍎 macOS Users

### Quick Start
1. **Double-click** `SPAMURAI.command`
2. Allow Terminal to run the script (if prompted)
3. Wait for dependencies to install (first run only)
4. GUI opens automatically in your browser

### What it does
✅ Checks Python installation
✅ Creates virtual environment
✅ Installs all dependencies
✅ Launches SPAMURAI GUI
✅ Color-coded status messages

### Requirements
- Python 3.8 or higher (usually pre-installed)
- Or install via Homebrew: `brew install python3`
- **Firebase credentials configured** (See FIREBASE_SETUP.md)

---

## 🐧 Linux Users

### Quick Start
Use the original script in the project root:
```bash
./start_spamurai.sh
```

Or run manually:
```bash
cd wa_broadcaster
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m streamlit run src/gui.py
```

---

## First-Time Setup: Firebase Configuration

⚠️ **IMPORTANT:** Before running the launcher for the first time, you MUST configure Firebase credentials.

### Quick Setup (3 steps):

1. **Get Firebase credentials:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a project (or use existing)
   - Project Settings → Service Accounts → Generate New Private Key
   - Download the JSON file

2. **Run the setup script:**
   ```bash
   # Windows
   setup_firebase.bat C:\path\to\your-credentials.json

   # macOS
   ./setup_firebase.sh /path/to/your-credentials.json
   ```

3. **Launch SPAMURAI:**
   - Double-click the launcher
   - It will verify Firebase credentials before starting

For detailed Firebase setup instructions, see [FIREBASE_SETUP.md](../FIREBASE_SETUP.md)

---

## First Run vs. Subsequent Runs

### First Run
- Takes 2-5 minutes
- Creates virtual environment
- Downloads and installs all dependencies
- Verifies Firebase credentials
- You'll see installation progress

### Subsequent Runs
- Takes 5-10 seconds
- Verifies Firebase credentials
- Skips installation (already done)
- Directly launches GUI

---

## Troubleshooting

### "Python not found" error

**Windows:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Restart your computer

**macOS:**
```bash
brew install python3
```

### "Permission denied" on macOS

The `.command` file should already be executable. If not:
```bash
chmod +x SPAMURAI.command
```

### Dependencies fail to install

Check your internet connection and try again. If the problem persists:
```bash
# Manually install
cd wa_broadcaster
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### GUI doesn't open automatically

Manually open your browser and go to:
```
http://localhost:8501
```

### "Firebase credentials not configured" error

The launcher will stop with this error if Firebase is not set up:

**Fix:**
1. Follow the Firebase setup steps above
2. Run the setup script: `setup_firebase.sh` (Mac) or `setup_firebase.bat` (Windows)
3. Restart the launcher

**Verify Firebase is set up:**
```bash
# Mac/Linux
echo $FIREBASE_CREDENTIALS

# Windows
echo %FIREBASE_CREDENTIALS%
```

If the above shows nothing, Firebase environment variable is not set. Re-run the setup script.

---

## Advanced: Creating Desktop Shortcuts

### Windows
1. Right-click `SPAMURAI.bat`
2. Select "Create shortcut"
3. Drag shortcut to Desktop

### macOS
1. Drag `SPAMURAI.command` to Desktop while holding **⌘ + ⌥** (creates alias)

---

## What's Next?

For an even simpler experience, check the **native installers**:
- **Windows:** `SPAMURAI-Setup.exe` (coming soon)
- **macOS:** `SPAMURAI.app` bundle (coming soon)

---

*Made with ⚡ by the SPAMURAI team*
