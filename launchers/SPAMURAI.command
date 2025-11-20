#!/bin/bash
# ============================================================================
# SPAMURAI - WhatsApp Broadcast Ninja
# Strike fast. Strike precise. Leave no trace.
# ============================================================================

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to the project directory
cd "$PROJECT_DIR"

echo ""
echo "========================================="
echo "  🥷⚡ SPAMURAI - WhatsApp Broadcast Ninja"
echo "  Strike fast. Strike precise."
echo "========================================="
echo ""

# Step 1: Check Python installation
echo -e "${CYAN}[Step 1/5]${NC} Checking Python installation..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  - Visit: https://www.python.org/downloads/"
    echo "  - Or use Homebrew: brew install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected"
echo ""

# Step 2: Set up virtual environment
echo -e "${CYAN}[Step 2/5]${NC} Setting up virtual environment..."
echo ""

VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"

    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to create virtual environment!"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
else
    echo -e "${GREEN}[OK]${NC} Virtual environment already exists"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${CYAN}[Step 3/5]${NC} Activating virtual environment..."
echo ""

source "$VENV_DIR/bin/activate"

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment!"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Virtual environment activated"
echo ""

# Step 4: Check and install dependencies
echo -e "${CYAN}[Step 4/5]${NC} Checking dependencies..."
echo ""

if ! python -c "import streamlit; import firebase_admin" 2>/dev/null; then
    echo "Required packages not found. Installing dependencies..."
    echo "This may take a few minutes..."
    echo ""

    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to install dependencies!"
        echo ""
        echo "Please check your internet connection and try again."
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi

    echo ""
    echo -e "${GREEN}[OK]${NC} Dependencies installed successfully"
else
    echo -e "${GREEN}[OK]${NC} All dependencies are installed"
fi
echo ""

# Step 5: Check Firebase credentials
echo -e "${CYAN}[Step 5/6]${NC} Checking Firebase credentials..."
echo ""

FIREBASE_READY=0

# Check if environment variable is set
if [ -n "$FIREBASE_CREDENTIALS" ]; then
    echo -e "${GREEN}[OK]${NC} Firebase credentials found in environment variable"
    FIREBASE_READY=1
else
    # Check if credentials file exists (new naming: firebase.json)
    if [ -f "$PROJECT_DIR/config/firebase.json" ]; then
        echo -e "${GREEN}[OK]${NC} Firebase credentials file found"
        FIREBASE_READY=1
    else
        # Also check old naming for backward compatibility
        if [ -f "$PROJECT_DIR/config/firebase-credentials.json" ]; then
            echo -e "${GREEN}[OK]${NC} Firebase credentials file found (old naming)"
            echo -e "${YELLOW}[NOTICE]${NC} Consider renaming to firebase.json for consistency"
            FIREBASE_READY=1
        fi
    fi
fi

if [ $FIREBASE_READY -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} Firebase credentials not configured!"
    echo ""
    echo "Firebase is required for SPAMURAI to function."
    echo ""
    echo "Please contact your POC to get the firebase.json file"
    echo ""
    echo "Save it as: config/firebase.json"
    echo ""
    echo "Then restart this launcher."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi
echo ""

# Step 6: Launch SPAMURAI
echo -e "${CYAN}[Step 6/6]${NC} Launching SPAMURAI GUI..."
echo ""
echo "========================================="
echo "  🚀 GUI will open in your browser"
echo "  📍 URL: http://localhost:8501"
echo "========================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
python -m streamlit run src/gui.py

# If streamlit exits with error, pause to show message
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} SPAMURAI encountered an error!"
    echo ""
    read -p "Press Enter to exit..."
fi
