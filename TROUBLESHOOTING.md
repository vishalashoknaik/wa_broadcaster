# SPAMURAI Troubleshooting Guide

Complete guide to diagnosing and fixing common setup and runtime issues.

## 🔧 Quick Diagnostic Tools

### Run Diagnostics First!

Before troubleshooting manually, run the diagnostic scripts:

**Windows:**
```cmd
diagnose_windows.bat
```

**macOS:**
```bash
./diagnose_mac.sh
```

**What it checks:**
- ✅ Python installation and version
- ✅ pip package manager
- ✅ Required Python packages
- ✅ Chrome browser
- ✅ ChromeDriver status
- ✅ Environment variables
- ✅ File permissions
- ✅ Network connectivity

The diagnostic will tell you exactly what's missing and how to fix it.

---

## 🐛 Debug Mode Launchers

Use debug launchers for detailed startup logging:

**Windows:**
```cmd
launchers\SPAMURAI_DEBUG.bat
```

**macOS:**
```bash
./launchers/SPAMURAI_DEBUG.command
```

**Benefits:**
- Step-by-step startup validation
- Real-time error detection
- Automatic package installation offer
- Clear error messages

---

## 🔍 Common Issues and Solutions

### Issue 1: "Python is not recognized"

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Cause:** Python not installed or not in PATH

**Solution (Windows):**
1. Download Python from: https://www.python.org/downloads/
2. During installation, **CHECK "Add Python to PATH"**
3. Restart command prompt
4. Verify: `python --version`

**Solution (macOS):**
```bash
# Option 1: Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3

# Option 2: Download from python.org
# Visit: https://www.python.org/downloads/mac-osx/
```

**Verify installation:**
```bash
python3 --version
# Should show: Python 3.8.x or higher
```

---

### Issue 2: "pip is not recognized"

**Symptoms:**
```
'pip' is not recognized as an internal or external command
```

**Cause:** pip not installed or Python installation incomplete

**Solution:**
```bash
# Windows
python -m ensurepip --default-pip
python -m pip install --upgrade pip

# macOS
python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip
```

**Verify:**
```bash
pip --version
# or
pip3 --version
```

---

### Issue 3: "ModuleNotFoundError: No module named 'streamlit'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'selenium'
```

**Cause:** Required Python packages not installed

**Solution:**
```bash
# Install all requirements at once
pip install -r requirements.txt

# Or install individually
pip install streamlit selenium webdriver-manager pandas pyperclip openpyxl requests
```

**Check what's installed:**
```bash
pip list | findstr streamlit    # Windows
pip list | grep streamlit       # macOS
```

---

### Issue 4: "Port 8501 is already in use"

**Symptoms:**
```
ERROR: Could not find an available port
Port 8501 is already in use
```

**Cause:** Another Streamlit instance is running or port is occupied

**Solution (Windows):**
```cmd
# Find process using port 8501
netstat -ano | findstr :8501

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Solution (macOS):**
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process (replace PID with actual number)
kill -9 <PID>
```

**Alternative:** Use a different port
```bash
streamlit run src/gui.py --server.port 8502
```

---

### Issue 5: Chrome/ChromeDriver issues

**Symptoms:**
```
selenium.common.exceptions.SessionNotCreatedException
This version of ChromeDriver only supports Chrome version XX
```

**Cause:** ChromeDriver version mismatch with Chrome browser

**Solution:**

The app uses `webdriver-manager` which auto-downloads the correct ChromeDriver.

If issues persist:

**Windows:**
```cmd
# Clear webdriver cache
rmdir /s /q %USERPROFILE%\.wdm
```

**macOS:**
```bash
# Clear webdriver cache
rm -rf ~/.wdm
```

Then restart SPAMURAI - it will download the correct version.

---

### Issue 6: "Permission denied" errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Cause:** Insufficient permissions to write files

**Solution (Windows):**
1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Navigate to project and run again

**Solution (macOS):**
```bash
# Check directory permissions
ls -la

# Fix if needed
chmod 755 .
chmod 644 *.py
```

---

### Issue 7: "Config file not found"

**Symptoms:**
```
FileNotFoundError: config.json not found
```

**Cause:** Configuration file missing

**Solution:**
```bash
# Copy example config
cp config.example.json config.json

# Edit with your settings
notepad config.json      # Windows
nano config.json         # macOS
```

**Important:** Update these fields in `config.json`:
- `google_sheets_config.messages.sheet_url`
- `google_sheets_config.contacts.sheet_url`
- `chrome_user_data` path

---

### Issue 8: QR Code doesn't appear

**Symptoms:**
- WhatsApp Web loads but no QR code shows
- Chrome window opens but is blank

**Cause:** Chrome user data directory issues

**Solution:**
1. Check `config.json` for `chrome_user_data` path
2. Ensure directory is accessible
3. Try a fresh directory:

```json
{
  "chrome_user_data": "/tmp/WhatsAppSession/Session1"
}
```

**For fresh start:**
```bash
# Windows
rmdir /s /q C:\Temp\WhatsAppSession

# macOS
rm -rf /tmp/WhatsAppSession
```

---

### Issue 9: "Excel file not found"

**Symptoms:**
```
FileNotFoundError: Excel file not found
```

**Cause:** File path incorrect or using Google Sheets

**Solution:**

If using **local Excel file**, ensure:
```json
{
  "excel_path": "contacts.xlsx"
}
```

If using **Google Sheets**, ensure:
```json
{
  "google_sheets_config": {
    "contacts": {
      "sheet_url": "YOUR_SHEET_URL",
      "tab_name": "Sheet1"
    }
  }
}
```

---

### Issue 10: Network/Connection errors

**Symptoms:**
```
ConnectionError: Failed to establish connection
requests.exceptions.ConnectionError
```

**Cause:** Network issues or firewall blocking

**Solution:**
1. Check internet connection: `ping google.com`
2. Check WhatsApp Web: `ping web.whatsapp.com`
3. Disable VPN temporarily
4. Check firewall settings
5. Check proxy settings

**Test network:**
```bash
# Windows
ping google.com
telnet web.whatsapp.com 443

# macOS
ping google.com
nc -zv web.whatsapp.com 443
```

---

## 📊 Diagnostic Log Analysis

Both diagnostic scripts create detailed logs:

**Windows:** `%TEMP%\spamurai_diagnostics.log`
**macOS:** `/tmp/spamurai_diagnostics.log`

### Reading the Log

Look for these sections:

```
PYTHON: Python 3.10.0 at C:\Python310\python.exe  ← Python OK
PIP: pip 21.3.1                                    ← pip OK
PACKAGE streamlit: 1.28.0                          ← Package installed
PACKAGE selenium: NOT INSTALLED                     ← Missing package!
CHROME: 120.0.6099.109                             ← Chrome OK
NETWORK: OK                                         ← Internet OK
```

---

## 🔧 Advanced Troubleshooting

### Reset Everything

If nothing works, reset completely:

**Windows:**
```cmd
REM 1. Uninstall Python packages
pip uninstall -y -r requirements.txt

REM 2. Clear caches
rmdir /s /q %USERPROFILE%\.wdm
rmdir /s /q %TEMP%\WhatsAppSession

REM 3. Reinstall
pip install -r requirements.txt

REM 4. Run diagnostic
diagnose_windows.bat
```

**macOS:**
```bash
# 1. Uninstall Python packages
pip3 uninstall -y -r requirements.txt

# 2. Clear caches
rm -rf ~/.wdm
rm -rf /tmp/WhatsAppSession

# 3. Reinstall
pip3 install -r requirements.txt

# 4. Run diagnostic
./diagnose_mac.sh
```

### Check Python Environment

**List installed packages:**
```bash
pip list
pip show streamlit  # Check specific package
```

**Check Python path:**
```bash
# Windows
where python
where pip

# macOS
which python3
which pip3
```

**Check Python version:**
```bash
python --version
python -c "import sys; print(sys.version)"
```

### Virtual Environment (Recommended)

Use virtual environment to avoid conflicts:

**Windows:**
```cmd
REM Create venv
python -m venv venv

REM Activate
venv\Scripts\activate

REM Install packages
pip install -r requirements.txt

REM Run app
streamlit run src/gui.py
```

**macOS:**
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run app
streamlit run src/gui.py
```

---

## 📝 Collecting Debug Information

When asking for help, provide this information:

### System Info

```bash
# Windows
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
python --version
pip --version

# macOS
sw_vers
python3 --version
pip3 --version
```

### Package Versions

```bash
pip list > installed_packages.txt
```

### Error Messages

Copy the full error message, including:
- Error type (e.g., `ModuleNotFoundError`)
- File and line number
- Traceback (full stack trace)

### Diagnostic Results

Run diagnostic and share the log:

**Windows:** `%TEMP%\spamurai_diagnostics.log`
**macOS:** `/tmp/spamurai_diagnostics.log`

---

## 🆘 Getting Help

### Before Asking

1. ✅ Run diagnostic script
2. ✅ Try debug launcher
3. ✅ Check this troubleshooting guide
4. ✅ Search existing GitHub issues

### When Asking

**Provide:**
- Operating system and version
- Python version
- Full error message
- Diagnostic log
- Steps to reproduce

**GitHub Issues:** https://github.com/fawkess/wa_broadcaster/issues

**Format:**
```markdown
## Issue Description
[Clear description of the problem]

## Environment
- OS: Windows 11 / macOS 14.0
- Python: 3.10.0
- SPAMURAI: v1.10.0

## Error Message
```
[Full error message]
```

## Steps to Reproduce
1. Step 1
2. Step 2
3. Error occurs

## Diagnostic Log
[Attach or paste relevant sections]
```

---

## ✅ Verification Checklist

After fixing issues, verify everything works:

- [ ] Diagnostic script passes all checks
- [ ] Debug launcher starts without errors
- [ ] Browser opens to http://localhost:8501
- [ ] Streamlit interface loads
- [ ] Can upload Excel file
- [ ] Can upload message file
- [ ] QR code appears for WhatsApp login
- [ ] Can scan QR code successfully
- [ ] Test message sends successfully

---

## 🔄 Common Workflow Issues

### Issue: Messages not sending

**Check:**
1. WhatsApp Web session active?
2. Phone connected to internet?
3. Numbers in correct format (with country code)?
4. Not in exclude list?
5. Check logs for specific errors

### Issue: Same message sent multiple times

**Cause:** Message deduplication not working

**Solution:**
Check log files exist:
- `config/message_sent_log.json`
- `config/message_content_log.json`

If missing, they'll be auto-created on next send.

### Issue: Can't find contacts in Excel

**Cause:** Column names incorrect

**Solution:**
Excel must have these columns:
- `Name`
- `WhatsApp Number`
- `nick_name` (optional)

---

## 📚 Additional Resources

- **Python Installation:** https://www.python.org/downloads/
- **Streamlit Docs:** https://docs.streamlit.io/
- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **Chrome Download:** https://www.google.com/chrome/
- **Homebrew (macOS):** https://brew.sh/

---

**Last Updated:** November 2025
**Version:** 1.10.0
