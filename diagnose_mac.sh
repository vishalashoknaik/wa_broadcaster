#!/bin/bash
################################################################################
# SPAMURAI System Diagnostics - macOS
# This script checks your system for all requirements and dependencies
################################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log file
LOGFILE="/tmp/spamurai_diagnostics.log"
echo "SPAMURAI Diagnostics - $(date)" > "$LOGFILE"
echo "" >> "$LOGFILE"

# Counter for issues
ISSUES_FOUND=0

echo ""
echo "============================================================================"
echo "                    SPAMURAI SYSTEM DIAGNOSTICS"
echo "                           macOS Edition"
echo "============================================================================"
echo ""
echo "This diagnostic will check:"
echo "  1. Operating System Information"
echo "  2. Python Installation and Version"
echo "  3. pip Package Manager"
echo "  4. Required Python Packages"
echo "  5. Firebase Credentials (MANDATORY)"
echo "  6. Chrome Browser Installation"
echo "  7. ChromeDriver Status"
echo "  8. Environment Variables"
echo "  9. File Permissions"
echo "  10. Network Connectivity"
echo ""
echo "Press Enter to start diagnosis..."
read

echo ""

################################################################################
# STEP 1: Operating System Information
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 1/9] Operating System Information"
echo "============================================================================"
echo ""

echo "Checking macOS version..."
sw_vers
sw_vers >> "$LOGFILE"

echo ""
echo "Checking system architecture..."
uname -m
echo "ARCH: $(uname -m)" >> "$LOGFILE"

echo ""
echo -e "${GREEN}[INFO]${NC} macOS architecture detected"
echo ""

################################################################################
# STEP 2: Python Installation
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 2/9] Python Installation"
echo "============================================================================"
echo ""

PYTHON_FOUND=0
PYTHON_VERSION=""
PYTHON_PATH=""
PYTHON_CMD=""

echo "Checking for Python..."
echo ""

# Check python3 command (preferred on macOS)
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} 'python3' command found"
    PYTHON_VERSION=$(python3 --version 2>&1)
    PYTHON_PATH=$(which python3)
    echo "    Version: $PYTHON_VERSION"
    echo "    Path: $PYTHON_PATH"
    PYTHON_FOUND=1
    PYTHON_CMD="python3"
    echo "PYTHON: $PYTHON_VERSION at $PYTHON_PATH" >> "$LOGFILE"
else
    echo -e "${YELLOW}[WARNING]${NC} 'python3' command not found"
fi

echo ""

# Check python command
if command -v python &> /dev/null; then
    PY_VER=$(python --version 2>&1)
    PY_PATH=$(which python)

    # Check if it's Python 3
    if [[ $PY_VER == *"Python 3"* ]]; then
        echo -e "${GREEN}[OK]${NC} 'python' command found (Python 3)"
        echo "    Version: $PY_VER"
        echo "    Path: $PY_PATH"

        if [ $PYTHON_FOUND -eq 0 ]; then
            PYTHON_VERSION=$PY_VER
            PYTHON_PATH=$PY_PATH
            PYTHON_FOUND=1
            PYTHON_CMD="python"
        fi
    else
        echo -e "${YELLOW}[WARNING]${NC} 'python' command found but it's Python 2"
        echo "    Version: $PY_VER"
        echo "    Use 'python3' instead"
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} 'python' command not found"
fi

echo ""
if [ $PYTHON_FOUND -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Python 3 is NOT installed"
    echo ""
    echo "FIX:"
    echo "  Option 1 (Recommended): Install via Homebrew"
    echo "    1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "    2. Install Python: brew install python3"
    echo ""
    echo "  Option 2: Download from python.org"
    echo "    1. Download from: https://www.python.org/downloads/mac-osx/"
    echo "    2. Run the installer"
    echo ""
    echo "PYTHON: NOT FOUND" >> "$LOGFILE"
    ((ISSUES_FOUND++))
else
    echo -e "${GREEN}[OK]${NC} Python is installed and accessible"

    # Check Python version (need 3.8+)
    echo ""
    echo "Verifying Python version (requires 3.8 or higher)..."

    if $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo -e "${GREEN}[OK]${NC} Python version is 3.8 or higher"
    else
        echo -e "${RED}[ERROR]${NC} Python version is too old (need 3.8+)"
        echo "    Current: $PYTHON_VERSION"
        echo ""
        echo "FIX: Upgrade Python"
        echo "  brew upgrade python3"
        echo "  Or download from: https://www.python.org/downloads/mac-osx/"
        ((ISSUES_FOUND++))
    fi
fi

################################################################################
# STEP 3: pip Package Manager
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 3/9] pip Package Manager"
echo "============================================================================"
echo ""

PIP_FOUND=0
PIP_VERSION=""
PIP_CMD=""

echo "Checking for pip..."
echo ""

# Check pip3 command
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} 'pip3' command found"
    PIP_VERSION=$(pip3 --version 2>&1)
    echo "    $PIP_VERSION"
    PIP_FOUND=1
    PIP_CMD="pip3"
    echo "PIP: $PIP_VERSION" >> "$LOGFILE"
else
    echo -e "${YELLOW}[WARNING]${NC} 'pip3' command not found"
fi

echo ""

# Check pip command
if command -v pip &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} 'pip' command found"
    PIP_V=$(pip --version 2>&1)
    echo "    $PIP_V"

    if [ $PIP_FOUND -eq 0 ]; then
        PIP_VERSION=$PIP_V
        PIP_FOUND=1
        PIP_CMD="pip"
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} 'pip' command not found"
fi

echo ""
if [ $PIP_FOUND -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} pip is NOT installed"
    echo ""
    echo "FIX:"
    echo "  Run: $PYTHON_CMD -m ensurepip --default-pip"
    echo "  Or: $PYTHON_CMD -m pip install --upgrade pip"
    echo ""
    echo "PIP: NOT FOUND" >> "$LOGFILE"
    ((ISSUES_FOUND++))
else
    echo -e "${GREEN}[OK]${NC} pip is installed and accessible"

    # Check pip upgrade
    echo ""
    echo "Checking if pip needs upgrade..."
    if $PIP_CMD list --outdated 2>/dev/null | grep -q "pip"; then
        echo -e "${BLUE}[INFO]${NC} pip has an update available"
        echo "    Run: $PYTHON_CMD -m pip install --upgrade pip"
    fi
fi

################################################################################
# STEP 4: Required Python Packages
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 4/9] Required Python Packages"
echo "============================================================================"
echo ""

if [ $PIP_FOUND -eq 0 ]; then
    echo -e "${YELLOW}[SKIP]${NC} Cannot check packages without pip"
else
    echo "Checking required packages..."
    echo ""

    MISSING_PACKAGES=""

    # List of required packages
    PACKAGES=("selenium" "webdriver-manager" "pandas" "pyperclip" "openpyxl" "requests" "streamlit")

    for pkg in "${PACKAGES[@]}"; do
        echo "Checking: $pkg"
        if $PIP_CMD show "$pkg" &> /dev/null; then
            VERSION=$($PIP_CMD show "$pkg" | grep "Version:" | awk '{print $2}')
            echo -e "    ${GREEN}[OK]${NC} $pkg version $VERSION installed"
            echo "PACKAGE $pkg: $VERSION" >> "$LOGFILE"
        else
            echo -e "    ${RED}[MISSING]${NC} $pkg is NOT installed"
            echo "PACKAGE $pkg: NOT INSTALLED" >> "$LOGFILE"
            MISSING_PACKAGES="$MISSING_PACKAGES $pkg"
        fi
        echo ""
    done

    if [ -n "$MISSING_PACKAGES" ]; then
        echo -e "${RED}[ERROR]${NC} Some required packages are missing:$MISSING_PACKAGES"
        echo ""
        echo "FIX:"
        echo "  Run: $PIP_CMD install$MISSING_PACKAGES"
        echo "  Or: $PIP_CMD install -r requirements.txt"
        echo ""
        ((ISSUES_FOUND++))
    else
        echo -e "${GREEN}[OK]${NC} All required packages are installed"
    fi
fi

################################################################################
# STEP 5: Firebase Credentials (MANDATORY)
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 5/10] Firebase Credentials (MANDATORY)"
echo "============================================================================"
echo ""

FIREBASE_READY=0

echo "Checking Firebase credentials..."
echo ""

# Check environment variable
if [ -n "$FIREBASE_CREDENTIALS" ]; then
    echo -e "${GREEN}[OK]${NC} FIREBASE_CREDENTIALS environment variable is set"

    # Validate JSON
    if echo "$FIREBASE_CREDENTIALS" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
        echo -e "${GREEN}[OK]${NC} Credentials JSON is valid"
        FIREBASE_READY=1
        echo "FIREBASE: Environment variable (valid)" >> "$LOGFILE"
    else
        echo -e "${RED}[ERROR]${NC} FIREBASE_CREDENTIALS contains invalid JSON"
        echo "FIREBASE: Environment variable (INVALID JSON)" >> "$LOGFILE"
        ((ISSUES_FOUND++))
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} FIREBASE_CREDENTIALS environment variable not set"
fi

echo ""

# Check credentials file
if [ -f "$SCRIPT_DIR/config/firebase-credentials.json" ]; then
    echo -e "${GREEN}[OK]${NC} Credentials file found at: config/firebase-credentials.json"

    # Validate JSON
    if python3 -c "import json; json.load(open('$SCRIPT_DIR/config/firebase-credentials.json'))" 2>/dev/null; then
        echo -e "${GREEN}[OK]${NC} Credentials file JSON is valid"
        if [ $FIREBASE_READY -eq 0 ]; then
            FIREBASE_READY=1
            echo "FIREBASE: File-based (valid)" >> "$LOGFILE"
        fi
    else
        echo -e "${RED}[ERROR]${NC} Credentials file contains invalid JSON"
        echo "FIREBASE: File-based (INVALID JSON)" >> "$LOGFILE"
        ((ISSUES_FOUND++))
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} No credentials file at: config/firebase-credentials.json"
fi

echo ""

if [ $FIREBASE_READY -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Firebase credentials NOT configured!"
    echo ""
    echo "Firebase is MANDATORY for SPAMURAI to function."
    echo ""
    echo "FIX:"
    echo "  1. Get Firebase credentials from:"
    echo "     https://console.firebase.google.com/"
    echo "     Project Settings → Service Accounts → Generate New Private Key"
    echo ""
    echo "  2. Run setup script:"
    echo "     ./setup_firebase.sh /path/to/credentials.json"
    echo ""
    echo "  3. Re-run this diagnostic"
    echo ""
    echo "FIREBASE: NOT CONFIGURED" >> "$LOGFILE"
    ((ISSUES_FOUND++))
else
    echo -e "${GREEN}[OK]${NC} Firebase credentials are properly configured"

    # Test Firebase connection if firebase-admin is installed
    if $PIP_CMD show firebase-admin &> /dev/null; then
        echo ""
        echo "Testing Firebase connection..."
        if python3 "$SCRIPT_DIR/test_firebase.py" 2>&1 | grep -q "Firebase enabled mode works"; then
            echo -e "${GREEN}[OK]${NC} Firebase connection successful"
        else
            echo -e "${YELLOW}[WARNING]${NC} Could not verify Firebase connection"
            echo "    Make sure Firebase is enabled in config.json"
        fi
    fi
fi

################################################################################
# STEP 6: Chrome Browser
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 6/10] Chrome Browser Installation"
echo "============================================================================"
echo ""

CHROME_FOUND=0

echo "Checking for Google Chrome..."
echo ""

# Check common Chrome installation paths on macOS
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [ -f "$CHROME_PATH" ]; then
    echo -e "${GREEN}[OK]${NC} Chrome found at: $CHROME_PATH"

    # Get Chrome version
    CHROME_VERSION=$("$CHROME_PATH" --version 2>/dev/null)
    echo "    Version: $CHROME_VERSION"
    echo "CHROME: $CHROME_VERSION" >> "$LOGFILE"

    CHROME_FOUND=1
else
    echo -e "${RED}[ERROR]${NC} Google Chrome is NOT installed"
    echo ""
    echo "FIX:"
    echo "  Option 1: Download from https://www.google.com/chrome/"
    echo "  Option 2: Install via Homebrew:"
    echo "    brew install --cask google-chrome"
    echo ""
    echo "CHROME: NOT FOUND" >> "$LOGFILE"
    ((ISSUES_FOUND++))
fi

################################################################################
# STEP 7: ChromeDriver
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 7/10] ChromeDriver Status"
echo "============================================================================"
echo ""

echo "Checking ChromeDriver..."
echo ""

if [ $PYTHON_FOUND -eq 0 ]; then
    echo -e "${YELLOW}[SKIP]${NC} Cannot check ChromeDriver without Python"
else
    echo -e "${BLUE}[INFO]${NC} ChromeDriver is managed by webdriver-manager"
    echo -e "${BLUE}[INFO]${NC} It will auto-download when first running SPAMURAI"
    echo ""

    # Check if webdriver-manager is installed
    if $PIP_CMD show webdriver-manager &> /dev/null; then
        echo -e "${GREEN}[OK]${NC} webdriver-manager is installed"
        echo "    ChromeDriver will be automatically downloaded on first run"
    else
        echo -e "${YELLOW}[WARNING]${NC} webdriver-manager is not installed"
        echo "    Install with: $PIP_CMD install webdriver-manager"
    fi
fi

################################################################################
# STEP 8: Environment Variables
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 8/10] Environment Variables"
echo "============================================================================"
echo ""

echo "Checking PATH variable..."
echo ""

if echo "$PATH" | grep -q "python"; then
    echo -e "${GREEN}[OK]${NC} Python directory is in PATH"
else
    echo -e "${YELLOW}[WARNING]${NC} Python directory may not be in PATH"
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Full PATH variable logged to: $LOGFILE"
echo "PATH: $PATH" >> "$LOGFILE"

echo ""
echo "Checking SHELL:"
echo "  Current shell: $SHELL"

################################################################################
# STEP 9: File Permissions
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 9/10] File Permissions"
echo "============================================================================"
echo ""

echo "Checking write permissions..."
echo ""

# Test write to temp folder
if echo "test" > "/tmp/spamurai_test.txt" 2>/dev/null; then
    echo -e "${GREEN}[OK]${NC} Can write to temporary directory"
    rm -f "/tmp/spamurai_test.txt"
else
    echo -e "${RED}[ERROR]${NC} Cannot write to temporary directory"
    echo "    This may cause issues with ChromeDriver"
fi

echo ""

# Test write to current directory
if echo "test" > "spamurai_test.txt" 2>/dev/null; then
    echo -e "${GREEN}[OK]${NC} Can write to current directory"
    rm -f "spamurai_test.txt"
else
    echo -e "${RED}[ERROR]${NC} Cannot write to current directory"
    echo "    Check directory permissions"
fi

################################################################################
# STEP 10: Network Connectivity
################################################################################
echo ""
echo "============================================================================"
echo "[STEP 10/10] Network Connectivity"
echo "============================================================================"
echo ""

echo "Checking internet connection..."
echo ""

if ping -c 1 google.com &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} Internet connection is working"
    echo "NETWORK: OK" >> "$LOGFILE"
else
    echo -e "${YELLOW}[WARNING]${NC} Cannot reach google.com"
    echo "    Check your internet connection"
    echo "    SPAMURAI requires internet for WhatsApp Web"
    echo "NETWORK: ISSUE" >> "$LOGFILE"
fi

echo ""
echo "Checking HTTPS connectivity..."
if ping -c 1 web.whatsapp.com &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} Can reach web.whatsapp.com"
else
    echo -e "${YELLOW}[WARNING]${NC} Cannot reach web.whatsapp.com"
    echo "    Check firewall settings"
fi

################################################################################
# SUMMARY
################################################################################
echo ""
echo ""
echo "============================================================================"
echo "                           DIAGNOSTIC SUMMARY"
echo "============================================================================"
echo ""

if [ $PYTHON_FOUND -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Python NOT installed"
else
    echo -e "${GREEN}[OK]${NC} Python installed"
fi

if [ $PIP_FOUND -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} pip NOT installed"
else
    echo -e "${GREEN}[OK]${NC} pip installed"
fi

if [ -n "$MISSING_PACKAGES" ]; then
    echo -e "${RED}[ERROR]${NC} Missing Python packages"
else
    echo -e "${GREEN}[OK]${NC} All packages installed"
fi

if [ $CHROME_FOUND -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Chrome NOT installed"
else
    echo -e "${GREEN}[OK]${NC} Chrome installed"
fi

if [ $FIREBASE_READY -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Firebase NOT configured"
else
    echo -e "${GREEN}[OK]${NC} Firebase configured"
fi

echo ""
echo "============================================================================"

if [ $ISSUES_FOUND -eq 0 ]; then
    echo ""
    echo -e "    ${GREEN}[SUCCESS]${NC} Your system is ready for SPAMURAI!"
    echo ""
    echo "Next steps:"
    echo "  1. Run: streamlit run src/gui.py"
    echo "  2. Or use the launcher: ./run_gui.sh"
    echo ""
else
    echo ""
    echo -e "    ${RED}[ISSUES FOUND]${NC} $ISSUES_FOUND issue(s) need to be fixed"
    echo ""
    echo "Please fix the issues listed above and run this diagnostic again."
    echo ""

    if [ -n "$MISSING_PACKAGES" ]; then
        echo "Quick fix for packages:"
        echo "  $PIP_CMD install$MISSING_PACKAGES"
        echo ""
    fi
fi

echo "Full diagnostic log saved to: $LOGFILE"
echo ""
echo "============================================================================"
echo ""
