#!/bin/bash
# Simple wrapper script that calls setup_taranga.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make setup_taranga.sh executable
chmod +x "$SCRIPT_DIR/setup_taranga.sh"

# Execute setup_taranga.sh
"$SCRIPT_DIR/setup_taranga.sh"
