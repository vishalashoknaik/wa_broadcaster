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
# Determine Git command (portable or system)
GIT_CMD=""
if [ -x "../PortableGit/bin/git" ]; then
    GIT_CMD="../PortableGit/bin/git"
    echo -e "${CYAN}[Git]${NC} Using portable Git"
elif command -v git &> /dev/null; then
    GIT_CMD="git"
fi

if [ -n "$GIT_CMD" ]; then
    echo -e "${CYAN}[Updates]${NC} Checking for latest version..."
    echo ""

    # Check if we're in a git repository
    if [ -d ".git" ]; then
        # Fetch latest changes quietly
        $GIT_CMD fetch origin master &> /dev/null

        # Check if we're behind
        LOCAL=$($GIT_CMD rev-parse HEAD)
        REMOTE=$($GIT_CMD rev-parse origin/master)

        if [ "$LOCAL" != "$REMOTE" ]; then
            echo -e "${YELLOW}⚡ New version available! Updating automatically...${NC}"
            echo ""

            # Stash any local changes
            if ! $GIT_CMD diff-index --quiet HEAD -- 2>/dev/null; then
                $GIT_CMD stash push -m "Auto-stash before update" &> /dev/null
            fi

            # Pull latest changes
            if $GIT_CMD pull origin master; then
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
            echo -e "${GREEN}✓${NC} You're on the latest version"
        fi
    fi
    echo ""
fi

# Step 1: Check Python installation
echo -e "${CYAN}[Step 1/5]${NC} Checking Python installation..."
echo ""

# Determine Python command (portable or system)
# Prefer Python 3.11, then 3.10, then any python3
PYTHON_CMD=""
PYTHON_VERSION=""

if [ -x "../python_311_spamurai/bin/python3" ]; then
    PYTHON_CMD="../python_311_spamurai/bin/python3"
    export PATH="../python_311_spamurai/bin:../python_311_spamurai:$PATH"
    echo -e "${CYAN}[Python]${NC} Using portable Python"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  - Visit: https://www.python.org/downloads/"
    echo "  - Or use Homebrew: brew install python@3.11"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

# Check if Python version is too old
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${YELLOW}[WARNING]${NC} Python $PYTHON_VERSION detected (using $PYTHON_CMD)"
    echo -e "${YELLOW}Python 3.10+ is recommended. Your version may have compatibility issues.${NC}"
    echo ""
    echo "Consider upgrading: brew install python@3.11"
    echo ""
    read -p "Press Enter to continue anyway (or Ctrl+C to exit)..."
else
    echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected (using $PYTHON_CMD)"
fi
echo ""

# Step 2: Set up virtual environment
echo -e "${CYAN}[Step 2/5]${NC} Setting up virtual environment..."
echo ""

VENV_DIR="$PROJECT_DIR/venv"
RECREATE_VENV=false

if [ -d "$VENV_DIR" ]; then
    # Check if existing venv uses an old Python version
    if [ -f "$VENV_DIR/bin/python" ]; then
        VENV_PYTHON_VERSION=$("$VENV_DIR/bin/python" --version 2>&1 | awk '{print $2}')
        VENV_MAJOR=$(echo $VENV_PYTHON_VERSION | cut -d. -f1)
        VENV_MINOR=$(echo $VENV_PYTHON_VERSION | cut -d. -f2)

        if [ "$VENV_MAJOR" -lt 3 ] || ([ "$VENV_MAJOR" -eq 3 ] && [ "$VENV_MINOR" -lt 10 ]); then
            echo -e "${YELLOW}[WARNING]${NC} Virtual environment uses Python $VENV_PYTHON_VERSION (outdated)"
            echo "System has Python $PYTHON_VERSION available"
            echo ""
            echo "Recreating virtual environment with newer Python..."
            RECREATE_VENV=true
        else
            echo -e "${GREEN}[OK]${NC} Virtual environment exists (Python $VENV_PYTHON_VERSION)"
        fi
    else
        echo -e "${GREEN}[OK]${NC} Virtual environment already exists"
    fi
fi

if [ ! -d "$VENV_DIR" ] || [ "$RECREATE_VENV" = true ]; then
    if [ "$RECREATE_VENV" = true ]; then
        rm -rf "$VENV_DIR"
    fi

    echo "Creating virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv "$VENV_DIR"

    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to create virtual environment!"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
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

# Export venv's bin directory to PATH for child processes
export PATH="$VENV_DIR/bin:$PATH"

echo ""

# Step 4: Install dependencies
echo -e "${CYAN}[Step 4/5]${NC} Installing/updating dependencies..."
echo ""

echo "Upgrading pip and installing requirements..."
echo "This may take a few minutes..."
echo ""

# Use venv's pip explicitly
python -m pip install --upgrade pip > /dev/null 2>&1
python -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to install dependencies!"
    echo ""
    echo "Please check your internet connection and try again."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo -e "${GREEN}[OK]${NC} Dependencies ready"
echo ""

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

# Launch Streamlit (use venv's python, not system python)
python -m streamlit run src/gui.py

# If streamlit exits with error, pause to show message
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} SPAMURAI encountered an error!"
    echo ""
    read -p "Press Enter to exit..."
fi
