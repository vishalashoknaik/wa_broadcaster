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

## First Run vs. Subsequent Runs

### First Run
- Takes 2-5 minutes
- Creates virtual environment
- Downloads and installs all dependencies
- You'll see installation progress

### Subsequent Runs
- Takes 5-10 seconds
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
