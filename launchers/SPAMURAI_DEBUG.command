#!/bin/bash
################################################################################
# SPAMURAI Launcher with Debug Mode - macOS
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "============================================================================"
echo "                        SPAMURAI DEBUG LAUNCHER"
echo "============================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${BLUE}[DEBUG]${NC} Starting SPAMURAI with verbose logging"
echo -e "${BLUE}[DEBUG]${NC} Script directory: $SCRIPT_DIR"
echo -e "${BLUE}[DEBUG]${NC} Project directory: $PROJECT_DIR"
echo -e "${BLUE}[DEBUG]${NC} Date/Time: $(date)"
echo ""

# Change to project directory
cd "$PROJECT_DIR" || exit 1
echo -e "${BLUE}[DEBUG]${NC} Working directory: $(pwd)"
echo ""

################################################################################
# Step 1: Check Python
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Checking Python installation..."

PYTHON_CMD=""

# Try python3 first (preferred on macOS)
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}[DEBUG]${NC} Found python3"
    echo -e "${BLUE}[DEBUG]${NC} Version: $(python3 --version)"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    PY_VER=$(python --version 2>&1)
    if [[ $PY_VER == *"Python 3"* ]]; then
        PYTHON_CMD="python"
        echo -e "${GREEN}[DEBUG]${NC} Found python"
        echo -e "${BLUE}[DEBUG]${NC} Version: $PY_VER"
    else
        echo -e "${RED}[ERROR]${NC} Only Python 2 found, need Python 3"
        echo ""
        echo "Please install Python 3:"
        echo "  brew install python3"
        echo "  Or download from: https://www.python.org/downloads/"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo -e "${RED}[ERROR]${NC} Python not found!"
    echo ""
    echo "Please run the diagnostic first:"
    echo "  ./diagnose_mac.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${BLUE}[DEBUG]${NC} Python command: $PYTHON_CMD"
echo ""

################################################################################
# Step 2: Check pip
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Checking pip installation..."

PIP_CMD=""

# Try pip3 first
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo -e "${GREEN}[DEBUG]${NC} Found pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo -e "${GREEN}[DEBUG]${NC} Found pip"
else
    echo -e "${RED}[ERROR]${NC} pip not found!"
    echo ""
    echo "Install pip:"
    echo "  $PYTHON_CMD -m ensurepip --default-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${BLUE}[DEBUG]${NC} pip command: $PIP_CMD"
echo ""

################################################################################
# Step 3: Check required packages
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Checking required packages..."
echo ""

MISSING=""
PACKAGES=("selenium" "webdriver-manager" "pandas" "pyperclip" "openpyxl" "requests" "streamlit")

for pkg in "${PACKAGES[@]}"; do
    if $PIP_CMD show "$pkg" &> /dev/null; then
        echo -e "${GREEN}[DEBUG]${NC} $pkg: INSTALLED"
    else
        echo -e "${RED}[ERROR]${NC} $pkg: MISSING"
        MISSING="$MISSING $pkg"
    fi
done

if [ -n "$MISSING" ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Missing packages:$MISSING"
    echo ""
    echo "Do you want to install them now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${BLUE}[DEBUG]${NC} Installing packages..."
        $PIP_CMD install$MISSING

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[DEBUG]${NC} Packages installed successfully"
        else
            echo -e "${RED}[ERROR]${NC} Package installation failed"
            echo ""
            echo "Try manually:"
            echo "  $PIP_CMD install$MISSING"
            echo ""
            read -p "Press Enter to exit..."
            exit 1
        fi
    else
        echo ""
        echo "Installation cancelled. Cannot proceed without required packages."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}[DEBUG]${NC} All packages installed"
echo ""

################################################################################
# Step 4: Check Chrome
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Checking Chrome installation..."

CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [ -f "$CHROME_PATH" ]; then
    echo -e "${GREEN}[DEBUG]${NC} Chrome found: $CHROME_PATH"
    CHROME_VERSION=$("$CHROME_PATH" --version 2>/dev/null)
    echo -e "${BLUE}[DEBUG]${NC} Version: $CHROME_VERSION"
else
    echo -e "${YELLOW}[WARNING]${NC} Chrome not found"
    echo -e "${BLUE}[INFO]${NC} Chrome will be needed for WhatsApp Web"
fi

echo ""

################################################################################
# Step 5: Check src/gui.py exists
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Checking application files..."

if [ -f "src/gui.py" ]; then
    echo -e "${GREEN}[DEBUG]${NC} Found src/gui.py"
else
    echo -e "${RED}[ERROR]${NC} src/gui.py not found"
    echo -e "${BLUE}[DEBUG]${NC} Current directory: $(pwd)"
    echo -e "${BLUE}[DEBUG]${NC} Expected: $(pwd)/src/gui.py"
    echo ""
    echo "Make sure you're running from the wa_broadcaster directory"
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""

################################################################################
# Step 6: Set Python to unbuffered for real-time output
################################################################################
export PYTHONUNBUFFERED=1

################################################################################
# Step 7: Launch Streamlit
################################################################################
echo -e "${BLUE}[DEBUG]${NC} Launching SPAMURAI..."
echo -e "${BLUE}[DEBUG]${NC} Command: $PYTHON_CMD -m streamlit run src/gui.py"
echo ""
echo "============================================================================"
echo "                         SPAMURAI IS STARTING"
echo "============================================================================"
echo ""
echo -e "${BLUE}[INFO]${NC} Browser should open automatically to: http://localhost:8501"
echo -e "${BLUE}[INFO]${NC} If not, manually open: http://localhost:8501"
echo ""
echo -e "${BLUE}[INFO]${NC} To stop SPAMURAI, press Ctrl+C in this window"
echo ""
echo "============================================================================"
echo ""

# Run with full output
$PYTHON_CMD -m streamlit run src/gui.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "============================================================================"
echo -e "${BLUE}[DEBUG]${NC} SPAMURAI exited with code: $EXIT_CODE"
echo "============================================================================"
echo ""

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} SPAMURAI exited with an error"
    echo ""
    echo "Common issues:"
    echo "  - Port 8501 already in use"
    echo "  - Missing Python packages"
    echo "  - Incorrect file paths"
    echo ""
    echo "Run ./diagnose_mac.sh for full system check"
    echo ""
fi

read -p "Press Enter to exit..."
