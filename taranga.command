#!/bin/bash
# Simple wrapper script that calls taranga.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make taranga.sh executable
chmod +x "$SCRIPT_DIR/taranga.sh"

# Execute taranga.sh
"$SCRIPT_DIR/taranga.sh"
