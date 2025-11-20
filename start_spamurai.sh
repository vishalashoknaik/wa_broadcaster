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

# Check Firebase credentials
echo "Checking Firebase credentials..."
FIREBASE_READY=0

if [ -n "$FIREBASE_CREDENTIALS" ]; then
    echo -e "${GREEN}✓ Firebase credentials found in environment variable${NC}"
    FIREBASE_READY=1
else
    # Check for firebase.json (new naming)
    if [ -f "$SCRIPT_DIR/config/firebase.json" ]; then
        echo -e "${GREEN}✓ Firebase credentials file found${NC}"
        FIREBASE_READY=1
    else
        # Check for firebase-credentials.json (legacy naming)
        if [ -f "$SCRIPT_DIR/config/firebase-credentials.json" ]; then
            echo -e "${GREEN}✓ Firebase credentials file found (old naming)${NC}"
            echo -e "${YELLOW}[NOTICE] Consider renaming to firebase.json for consistency${NC}"
            FIREBASE_READY=1
        fi
    fi
fi

if [ $FIREBASE_READY -eq 0 ]; then
    echo -e "${RED}❌ Firebase credentials not configured!${NC}"
    echo ""
    echo "Firebase is required for SPAMURAI to function."
    echo ""
    echo "Please contact your POC to get the firebase.json file"
    echo "Save it as: config/firebase.json"
    echo ""
    echo "Then restart this launcher."
    exit 1
fi
echo ""

# Launch SPAMURAI GUI
echo "🚀 Launching SPAMURAI GUI..."
echo "📍 Your browser will open automatically at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
python3 -m streamlit run src/gui.py
