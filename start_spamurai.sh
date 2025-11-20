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
if [ ! -f "$SCRIPT_DIR/config/firebase.json" ] && [ ! -f "$SCRIPT_DIR/config/firebase-credentials.json" ] && [ -z "$FIREBASE_CREDENTIALS" ]; then
    echo "Firebase credentials setup..."
    echo ""
    echo -e "${YELLOW}[NOTICE] Firebase credentials not found. Starting automatic setup...${NC}"
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

    # Verify credentials were created
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
