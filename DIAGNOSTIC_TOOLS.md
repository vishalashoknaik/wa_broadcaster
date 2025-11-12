# SPAMURAI Diagnostic and Debug Tools

Quick reference for troubleshooting SPAMURAI setup issues.

## 🎯 Quick Start

### Having Setup Issues?

**Run this FIRST:**

**Windows:**
```cmd
diagnose_windows.bat
```

**macOS:**
```bash
./diagnose_mac.sh
```

**What it does:**
- ✅ Checks your entire system automatically
- ✅ Identifies missing components
- ✅ Provides specific fix instructions
- ✅ Creates detailed log file
- ✅ Takes 30-60 seconds to complete

---

## 📋 Available Tools

### 1. System Diagnostic Scripts

#### `diagnose_windows.bat` (Windows)
**Purpose:** Complete system check
**Checks:**
- Operating system version
- Python installation (version 3.8+)
- pip package manager
- Required Python packages
- Chrome browser
- ChromeDriver status
- Environment variables
- File permissions
- Network connectivity

**Output:** Creates log at `%TEMP%\spamurai_diagnostics.log`

#### `diagnose_mac.sh` (macOS)
**Purpose:** Complete system check (same as Windows)
**Output:** Creates log at `/tmp/spamurai_diagnostics.log`

### 2. Debug Launchers

#### `launchers/SPAMURAI_DEBUG.bat` (Windows)
**Purpose:** Launch with verbose logging
**Features:**
- Step-by-step startup validation
- Real-time error detection
- Offers to auto-install missing packages
- Shows detailed error messages
- Logs all output

#### `launchers/SPAMURAI_DEBUG.command` (macOS)
**Purpose:** Launch with verbose logging (same as Windows)

---

## 🔍 When to Use Each Tool

### Use Diagnostic Script When:
- ❌ First time setup
- ❌ "Python not found" errors
- ❌ "Module not found" errors
- ❌ Not sure what's wrong
- ❌ Nothing works

### Use Debug Launcher When:
- ⚠️ App crashes on startup
- ⚠️ Need to see detailed logs
- ⚠️ Want to auto-install missing packages
- ⚠️ Troubleshooting specific errors

### Use Regular Launcher When:
- ✅ Everything works
- ✅ All packages installed
- ✅ Previous runs successful

---

## 📊 Understanding Diagnostic Output

### Success Indicators

```
[OK] Python installed
[OK] pip installed
[OK] All packages installed
[OK] Chrome installed
[OK] Can write to directories
[OK] Internet connection is working

[SUCCESS] Your system is ready for SPAMURAI!
```

### Warning Indicators

```
[WARNING] 'python' command not found
[WARNING] pip has an update available
[WARNING] Chrome not found
[WARNING] Cannot reach web.whatsapp.com
```

**Action:** Review warnings, may need fixes

### Error Indicators

```
[ERROR] Python NOT installed
[ERROR] pip NOT installed
[ERROR] Missing Python packages
[ERROR] Chrome NOT installed
[ERROR] Cannot write to directory

[ISSUES FOUND] X issue(s) need to be fixed
```

**Action:** Fix all errors before proceeding

---

## 🛠️ Common Diagnostic Results

### Scenario 1: Python Not Found

**Output:**
```
[ERROR] Python is NOT installed or not in PATH
```

**Fix:**
- Windows: Download from python.org, CHECK "Add to PATH"
- macOS: `brew install python3`

### Scenario 2: Missing Packages

**Output:**
```
[MISSING] streamlit is NOT installed
[MISSING] selenium is NOT installed

[ERROR] Missing packages: streamlit selenium
```

**Fix:**
```bash
pip install streamlit selenium
# Or
pip install -r requirements.txt
```

### Scenario 3: Chrome Not Found

**Output:**
```
[ERROR] Google Chrome is NOT installed
```

**Fix:**
- Download from: https://www.google.com/chrome/

### Scenario 4: All Good!

**Output:**
```
[OK] Python installed
[OK] pip installed
[OK] All packages installed
[OK] Chrome installed

[SUCCESS] Your system is ready for SPAMURAI!
```

**Next:** Run SPAMURAI normally

---

## 💡 Pro Tips

### Tip 1: Run Diagnostic After Installing Python

```bash
# Install Python
# Then immediately run:
diagnose_windows.bat  # or diagnose_mac.sh
```

### Tip 2: Use Debug Launcher for First Run

```bash
# Instead of regular launcher, use:
launchers/SPAMURAI_DEBUG.bat
# or
launchers/SPAMURAI_DEBUG.command
```

Gets you better error messages if something goes wrong.

### Tip 3: Check Log Files

Diagnostic creates detailed logs:
- **Windows:** `%TEMP%\spamurai_diagnostics.log`
- **macOS:** `/tmp/spamurai_diagnostics.log`

View with:
```bash
# Windows
type %TEMP%\spamurai_diagnostics.log

# macOS
cat /tmp/spamurai_diagnostics.log
```

### Tip 4: Run Diagnostic After Updates

After updating Python or installing packages, re-run diagnostic to verify.

---

## 🔄 Typical Workflow

### New User Setup

```
1. Run diagnostic script
   ↓
2. Fix any issues found
   ↓
3. Re-run diagnostic
   ↓
4. Use debug launcher for first run
   ↓
5. Switch to regular launcher
```

### Troubleshooting Issues

```
1. Issue occurs
   ↓
2. Run diagnostic script
   ↓
3. Review output and logs
   ↓
4. Fix identified issues
   ↓
5. Use debug launcher to verify
```

---

## 📖 Full Documentation

- **Complete troubleshooting:** See `TROUBLESHOOTING.md`
- **Setup guides:** See `README.md`
- **Build instructions:** See `build/BUILD_INSTRUCTIONS.md`

---

## 🆘 Still Having Issues?

1. ✅ Run diagnostic
2. ✅ Check TROUBLESHOOTING.md
3. ✅ Review logs
4. ✅ Search GitHub issues
5. ❓ Create new issue with:
   - Diagnostic log
   - Full error message
   - Steps to reproduce

**GitHub:** https://github.com/fawkess/wa_broadcaster/issues

---

## 📝 Quick Command Reference

### Windows
```cmd
REM Diagnostic
diagnose_windows.bat

REM Debug launch
launchers\SPAMURAI_DEBUG.bat

REM Normal launch
launchers\SPAMURAI.bat

REM Check Python
python --version
where python

REM Check packages
pip list

REM Install packages
pip install -r requirements.txt

REM View log
type %TEMP%\spamurai_diagnostics.log
```

### macOS
```bash
# Diagnostic
./diagnose_mac.sh

# Debug launch
./launchers/SPAMURAI_DEBUG.command

# Normal launch
./launchers/SPAMURAI.command

# Check Python
python3 --version
which python3

# Check packages
pip3 list

# Install packages
pip3 install -r requirements.txt

# View log
cat /tmp/spamurai_diagnostics.log
```

---

**Remember:** When in doubt, run the diagnostic! It will tell you exactly what's wrong.
