#!/bin/bash
# Simple wrapper script that calls setup_spamurai.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make setup_spamurai.sh executable
chmod +x "$SCRIPT_DIR/setup_spamurai.sh"

# Execute setup_spamurai.sh
"$SCRIPT_DIR/setup_spamurai.sh"
