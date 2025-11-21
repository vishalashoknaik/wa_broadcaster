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
PROJECT_DIR="$SCRIPT_DIR"

# Change to the project directory
cd "$PROJECT_DIR"

echo ""
echo "========================================="
echo "  🥷⚡ SPAMURAI - WhatsApp Broadcast Ninja"
echo "  Strike fast. Strike precise."
echo "========================================="
echo ""

# Step 0: Check for updates
if command -v git &> /dev/null; then
    echo -e "${CYAN}[Updates]${NC} Checking for latest version..."
    echo ""

    # Check if we're in a git repository
    if [ -d ".git" ]; then
        # Fetch latest changes quietly
        git fetch origin master &> /dev/null

        # Check if we're behind
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse origin/master)

        if [ "$LOCAL" != "$REMOTE" ]; then
            echo -e "${YELLOW}⚡ New version available!${NC}"
            echo ""
            echo "Would you like to update now? (y/n)"
            read -p "Update: " UPDATE_CHOICE

            if [ "$UPDATE_CHOICE" = "y" ] || [ "$UPDATE_CHOICE" = "Y" ]; then
                echo ""
                echo "Updating to latest version..."

                # Stash any local changes
                if ! git diff-index --quiet HEAD -- 2>/dev/null; then
                    git stash push -m "Auto-stash before update" &> /dev/null
                fi

                # Pull latest changes
                if git pull origin master; then
                    echo ""
                    echo -e "${GREEN}✅ Updated successfully!${NC}"
                    echo ""
                    echo "Please re-run this script to use the latest version."
                    echo ""
                    read -p "Press Enter to exit..."
                    exit 0
                else
                    echo ""
                    echo -e "${RED}❌ Update failed${NC}"
                    echo "Continuing with current version..."
                fi
            else
                echo "Skipping update. Continuing with current version..."
            fi
        else
            echo -e "${GREEN}✓${NC} You're on the latest version"
        fi
    fi
    echo ""
fi

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
echo -e "${CYAN}[Step 4/5]${NC} Checking and installing dependencies..."
echo ""

if ! python3 -c "import streamlit; import firebase_admin" 2>/dev/null; then
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

# Check if Firebase credentials need setup (do this right after dependencies)
# We need setup if EITHER:
#   1. firebase.json doesn't exist, OR
#   2. config.json doesn't have firebase_config section

NEEDS_FIREBASE_SETUP=false

# Check if firebase.json exists
if [ ! -f "$PROJECT_DIR/config/firebase.json" ] && [ ! -f "$PROJECT_DIR/config/firebase-credentials.json" ] && [ -z "$FIREBASE_CREDENTIALS" ]; then
    NEEDS_FIREBASE_SETUP=true
fi

# Check if config.json has firebase_config section
if [ -f "$PROJECT_DIR/config.json" ]; then
    # Use python to check if firebase_config exists in config.json
    HAS_FIREBASE_CONFIG=$(python3 -c "import json; config = json.load(open('config.json')); print('yes' if 'firebase_config' in config else 'no')" 2>/dev/null || echo "no")

    if [ "$HAS_FIREBASE_CONFIG" = "no" ] || [ -z "$HAS_FIREBASE_CONFIG" ]; then
        NEEDS_FIREBASE_SETUP=true
    fi
else
    # config.json doesn't exist - will need Firebase setup
    NEEDS_FIREBASE_SETUP=true
fi

if [ "$NEEDS_FIREBASE_SETUP" = "true" ]; then
    echo -e "${CYAN}[Step 4b/5]${NC} Firebase credentials setup..."
    echo ""
    echo -e "${YELLOW}[NOTICE]${NC} Firebase configuration incomplete. Starting automatic setup..."
    echo ""

    # Run automated Firebase setup
    python3 src/firebase_auto_setup.py

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[ERROR]${NC} Firebase setup failed or was cancelled."
        echo ""
        echo "Please contact your POC if you need assistance."
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi

    # Verify credentials were created and config updated
    if [ -f "$PROJECT_DIR/config/firebase.json" ]; then
        echo -e "${GREEN}[OK]${NC} Firebase credentials configured successfully"
    else
        echo -e "${RED}[ERROR]${NC} Setup completed but credentials file not found!"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo ""
fi

# Step 5: Launch SPAMURAI
echo -e "${CYAN}[Step 5/5]${NC} Launching SPAMURAI GUI..."
echo ""
echo "========================================="
echo "  🚀 GUI will open in your browser"
echo "  📍 URL: http://localhost:8501"
echo "========================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch Streamlit
python3 -m streamlit run src/gui.py

# If streamlit exits with error, pause to show message
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} SPAMURAI encountered an error!"
    echo ""
    read -p "Press Enter to exit..."
fi
