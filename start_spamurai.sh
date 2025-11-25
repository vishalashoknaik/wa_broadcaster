#!/bin/bash
#############################################
# SPAMURAI GUI Launcher
# Strike fast. Strike precise. Leave no trace. 🥷⚡
#############################################

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "🥷⚡ SPAMURAI - WhatsApp Broadcast Ninja"
echo "======================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit; import firebase_admin" 2>/dev/null; then
    echo -e "${YELLOW}Required packages not found. Installing dependencies...${NC}"
    echo ""
    pip3 install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies!${NC}"
        echo "Please check your internet connection and try again."
        exit 1
    fi
    echo ""
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${GREEN}✓ All dependencies are installed${NC}"
fi
echo ""

# Check if Firebase credentials need setup (do this right after dependencies)
# We need setup if EITHER:
#   1. firebase.json doesn't exist, OR
#   2. config.json doesn't have firebase_config section

NEEDS_FIREBASE_SETUP=false

# Check if firebase.json exists
if [ ! -f "$SCRIPT_DIR/config/firebase.json" ]; then
    NEEDS_FIREBASE_SETUP=true
fi

# Check if config.json has firebase_config section
if [ -f "$SCRIPT_DIR/config.json" ]; then
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
    echo "Firebase credentials setup..."
    echo ""
    echo -e "${YELLOW}[NOTICE] Firebase configuration incomplete. Starting automatic setup...${NC}"
    echo ""

    # Run automated Firebase setup
    python3 src/firebase_auto_setup.py

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[ERROR] Firebase setup failed or was cancelled.${NC}"
        echo ""
        echo "Please contact your POC if you need assistance."
        echo ""
        exit 1
    fi

    # Verify credentials were created and config updated
    if [ -f "$SCRIPT_DIR/config/firebase.json" ]; then
        echo -e "${GREEN}[OK] Firebase credentials configured successfully${NC}"
    else
        echo -e "${RED}[ERROR] Setup completed but credentials file not found!${NC}"
        echo ""
        exit 1
    fi
    echo ""
fi

# Launch SPAMURAI GUI
echo "🚀 Launching SPAMURAI GUI..."
echo "📍 Your browser will open automatically at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
python3 -m streamlit run src/gui.py
