#!/bin/bash

# Firebase Credentials Setup Script for SPAMURAI
# Automatically configures Firebase credentials as environment variable

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔥 Firebase Credentials Setup for SPAMURAI"
echo "=========================================="
echo ""

# Check if credentials file path is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Please provide path to Firebase credentials JSON file${NC}"
    echo ""
    echo "Usage: $0 /path/to/firebase-credentials.json"
    echo ""
    echo "Example:"
    echo "  $0 ~/Downloads/spamurai-firebase-xxxxx.json"
    echo ""
    exit 1
fi

CREDS_FILE="$1"

# Check if file exists
if [ ! -f "$CREDS_FILE" ]; then
    echo -e "${RED}Error: File not found: $CREDS_FILE${NC}"
    exit 1
fi

# Validate JSON
if ! python3 -c "import json; json.load(open('$CREDS_FILE'))" 2>/dev/null; then
    echo -e "${RED}Error: Invalid JSON file${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Valid Firebase credentials file found"
echo ""

# Read JSON content and escape it for shell
CREDS_JSON=$(cat "$CREDS_FILE" | tr -d '\n' | sed "s/'/'\\\\''/g")

# Detect shell
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
        SHELL_NAME="zsh"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
        SHELL_NAME="bash"
    else
        SHELL_CONFIG="$HOME/.bashrc"
        SHELL_NAME="bash"
    fi
else
    SHELL_CONFIG="$HOME/.profile"
    SHELL_NAME="sh"
fi

echo "Detected shell: $SHELL_NAME"
echo "Config file: $SHELL_CONFIG"
echo ""

# Check if already configured
if grep -q "FIREBASE_CREDENTIALS=" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  FIREBASE_CREDENTIALS already exists in $SHELL_CONFIG${NC}"
    echo ""
    read -p "Do you want to replace it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Remove old entry
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' '/export FIREBASE_CREDENTIALS=/d' "$SHELL_CONFIG"
    else
        # Linux
        sed -i '/export FIREBASE_CREDENTIALS=/d' "$SHELL_CONFIG"
    fi
    echo -e "${GREEN}✓${NC} Removed old FIREBASE_CREDENTIALS"
fi

# Add new entry
echo "" >> "$SHELL_CONFIG"
echo "# Firebase credentials for SPAMURAI (added by setup_firebase.sh)" >> "$SHELL_CONFIG"
echo "export FIREBASE_CREDENTIALS='$CREDS_JSON'" >> "$SHELL_CONFIG"

echo -e "${GREEN}✓${NC} Added FIREBASE_CREDENTIALS to $SHELL_CONFIG"
echo ""

# Source the config
if [ "$SHELL_NAME" = "zsh" ]; then
    export FIREBASE_CREDENTIALS="$CREDS_JSON"
elif [ "$SHELL_NAME" = "bash" ]; then
    export FIREBASE_CREDENTIALS="$CREDS_JSON"
fi

echo -e "${GREEN}✓${NC} Environment variable set for current session"
echo ""

# Test Firebase connection
echo "Testing Firebase connection..."
if python3 "$SCRIPT_DIR/test_firebase.py" 2>&1 | grep -q "Firebase enabled mode works"; then
    echo -e "${GREEN}✓${NC} Firebase connection successful!"
else
    echo -e "${YELLOW}⚠️  Could not verify Firebase connection${NC}"
    echo "   Make sure to enable Firebase in your config.json:"
    echo "   \"firebase_config\": { \"enabled\": true }"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Reload your shell: source $SHELL_CONFIG"
echo "  2. Or restart your terminal"
echo "  3. Enable Firebase in config.json:"
echo "     \"firebase_config\": { \"enabled\": true }"
echo "  4. Run SPAMURAI - it will use environment variable automatically"
echo ""
echo "Note: All installations on this machine will now use these credentials."
echo ""
