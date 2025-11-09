#!/bin/bash
#############################################
# SPAMURAI GUI Launcher
# Strike fast. Strike precise. Leave no trace. 🥷⚡
#############################################

echo ""
echo "🥷⚡ SPAMURAI - WhatsApp Broadcast Ninja"
echo "======================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo ""
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
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
