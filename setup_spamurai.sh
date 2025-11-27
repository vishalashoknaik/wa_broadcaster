#!/bin/bash
# ============================================================================
# Taranga - Installation & Update Script for Mac
# Single-click installer that handles both fresh install and updates
# ============================================================================

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo ""
echo "========================================="
echo "  🌊🏄 Taranga Installer & Updater"
echo "  Ride the wave of connection"
echo "========================================="
echo ""

# Repository details
REPO_URL="https://github.com/vishalashoknaik/wa_broadcaster.git"
REPO_NAME="taranga"
DEFAULT_INSTALL_DIR="$HOME/Desktop"

# Step 1: Check Git installation
echo -e "${CYAN}[Step 1/7]${NC} Checking Git installation..."
echo ""

if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Git not found. Installing...${NC}"
    echo ""
    echo "Installing Xcode Command Line Tools..."
    echo "(A popup will appear - click 'Install')"
    echo ""

    xcode-select --install

    echo ""
    echo -e "${YELLOW}Please complete the installation in the popup window.${NC}"
    echo -e "${YELLOW}Press ENTER when installation is complete...${NC}"
    read

    # Verify installation
    if ! command -v git &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Git installation failed!"
        echo "Please install Xcode Command Line Tools manually."
        echo ""
        echo "Press ENTER to exit..."
        read
        exit 1
    fi

    echo -e "${GREEN}[OK]${NC} Git installed successfully!"
else
    GIT_VERSION=$(git --version 2>&1 | awk '{print $3}')
    echo -e "${GREEN}[OK]${NC} Git $GIT_VERSION detected"
fi
echo ""

# Step 2: Determine installation location
echo -e "${CYAN}[Step 2/7]${NC} Determining installation location..."
echo ""

echo "Where would you like to install/update Taranga?"
echo "Press ENTER for Desktop, or type a custom path:"
echo ""
echo -e "${BLUE}Default: $DEFAULT_INSTALL_DIR${NC}"
echo ""
read -p "Install location: " INSTALL_DIR

if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR="$DEFAULT_INSTALL_DIR"
fi

# Expand ~ to home directory
INSTALL_DIR="${INSTALL_DIR/#\~/$HOME}"

# Create directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo ""
    echo "Creating directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"
FULL_PATH="$INSTALL_DIR/$REPO_NAME"

echo -e "${GREEN}[OK]${NC} Install location: $FULL_PATH"
echo ""

# Step 3: Check for existing installation
echo -e "${CYAN}[Step 3/7]${NC} Checking for existing installation..."
echo ""

if [ -d "$FULL_PATH" ]; then
    # Repository already exists - this script is for CLEAN INSTALL only
    echo -e "${YELLOW}[NOTICE]${NC} Taranga is already installed at:"
    echo "  $FULL_PATH"
    echo ""
    echo -e "${CYAN}This setup script is for clean installations only.${NC}"
    echo ""
    echo "To launch Taranga, use:"
    echo -e "  ${GREEN}taranga.command${NC} (in the installed folder)"
    echo ""
    echo "The launcher will automatically:"
    echo "  • Update to the latest version"
    echo "  • Install dependencies"
    echo "  • Launch the application"
    echo ""
    echo "Press ENTER to exit..."
    read
    exit 0
fi

# Repository doesn't exist - FRESH INSTALL
echo -e "${BLUE}No existing installation found.${NC}"
echo ""
echo "Installing Taranga from GitHub..."
echo ""

if git clone "$REPO_URL" "$FULL_PATH"; then
    echo ""
    echo -e "${GREEN}✅ INSTALLATION SUCCESSFUL!${NC}"
    echo ""
    echo "Taranga has been installed!"
    cd "$FULL_PATH"
else
    echo ""
    echo -e "${RED}[ERROR]${NC} Installation failed!"
    echo "Please check your internet connection and try again."
    echo ""
    echo "Press ENTER to exit..."
    read
    exit 1
fi

# Step 4: Check Python installation
echo -e "${CYAN}[Step 4/7]${NC} Checking Python installation..."
echo ""

PYTHON_NEEDS_INSTALL=false
PYTHON_CMD="python3"

# Check for Python 3.11+ first (preferred)
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    PYTHON_VERSION=$(python3.11 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected (using python3.11)"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    PYTHON_VERSION=$(python3.10 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected (using python3.10)"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        echo -e "${YELLOW}Python $PYTHON_VERSION found, but 3.10+ recommended.${NC}"
        echo -e "${YELLOW}Your Python version is past end-of-life and may have compatibility issues.${NC}"
        echo ""
        echo "Would you like to install Python 3.11? (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            PYTHON_NEEDS_INSTALL=true
        else
            echo -e "${YELLOW}Continuing with Python $PYTHON_VERSION...${NC}"
            echo -e "${YELLOW}Note: You may encounter dependency or security issues.${NC}"
        fi
    else
        echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION detected"
    fi
else
    echo -e "${YELLOW}Python 3 not found.${NC}"
    PYTHON_NEEDS_INSTALL=true
fi
echo ""

# Step 5: Check/Install Homebrew (only if Python needs installation)
if [ "$PYTHON_NEEDS_INSTALL" = true ]; then
    echo -e "${CYAN}[Step 5/7]${NC} Checking Homebrew installation..."
    echo ""

    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew not found. Installing...${NC}"
        echo ""
        echo "This will install Homebrew (the package manager for macOS)"
        echo "You may be prompted for your password."
        echo ""

        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        if [ $? -ne 0 ]; then
            echo ""
            echo -e "${RED}[ERROR]${NC} Homebrew installation failed!"
            echo ""
            echo "Press ENTER to exit..."
            read
            exit 1
        fi

        # Add Homebrew to PATH for Apple Silicon Macs
        if [ -f "/opt/homebrew/bin/brew" ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi

        echo ""
        echo -e "${GREEN}[OK]${NC} Homebrew installed successfully!"
    else
        BREW_VERSION=$(brew --version 2>&1 | head -n1 | awk '{print $2}')
        echo -e "${GREEN}[OK]${NC} Homebrew $BREW_VERSION detected"
    fi
    echo ""

    # Step 6: Install Python via Homebrew
    echo -e "${CYAN}[Step 6/7]${NC} Installing Python 3.11..."
    echo ""

    echo "Installing Python 3.11 via Homebrew..."
    echo "This may take a few minutes..."
    echo ""

    brew install python@3.11

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[ERROR]${NC} Python installation failed!"
        echo ""
        echo "Press ENTER to exit..."
        read
        exit 1
    fi

    # Verify Python installation and set PYTHON_CMD
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        PYTHON_VERSION=$(python3.11 --version 2>&1 | awk '{print $2}')
        echo ""
        echo -e "${GREEN}[OK]${NC} Python $PYTHON_VERSION installed successfully!"
        echo ""
    else
        echo ""
        echo -e "${RED}[ERROR]${NC} Python installation verification failed!"
        echo ""
        echo "Press ENTER to exit..."
        read
        exit 1
    fi
else
    echo -e "${CYAN}[Step 5/7]${NC} Homebrew check skipped (Python already installed)"
    echo ""
    echo -e "${CYAN}[Step 6/7]${NC} Python installation skipped (already installed)"
    echo ""
fi

# Step 7: Set up virtual environment
echo -e "${CYAN}[Step 7/8]${NC} Setting up Python virtual environment..."
echo ""

cd "$FULL_PATH"
VENV_PATH="$FULL_PATH/venv"

echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv "$VENV_PATH"

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Failed to create virtual environment!"
    echo ""
    echo "Press ENTER to exit..."
    read
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Virtual environment created"
echo ""

# Activate virtual environment and install dependencies
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment!"
    echo ""
    echo "Press ENTER to exit..."
    read
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip > /dev/null 2>&1

# Check for requirements.txt and install
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    echo "This may take a few minutes..."
    echo ""

    python -m pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${YELLOW}[WARNING]${NC} Some dependencies failed to install."
        echo "You may need to install them manually later."
    else
        echo ""
        echo -e "${GREEN}[OK]${NC} All dependencies installed successfully!"
    fi
else
    echo -e "${YELLOW}[NOTICE]${NC} No requirements.txt found. Skipping dependency installation."
fi
echo ""

# Step 8: Setup Firebase credentials
echo -e "${CYAN}[Step 8/8]${NC} Setting up Firebase credentials..."
echo ""

NEEDS_FIREBASE_SETUP=false

# Check if firebase.json exists
if [ ! -f "config/firebase.json" ]; then
    NEEDS_FIREBASE_SETUP=true
fi

# Check if config.json has firebase_config section
if [ -f "config.json" ]; then
    HAS_FIREBASE_CONFIG=$(python -c "import json; config = json.load(open('config.json')); print('yes' if 'firebase_config' in config else 'no')" 2>/dev/null)
    if [ "$HAS_FIREBASE_CONFIG" != "yes" ]; then
        NEEDS_FIREBASE_SETUP=true
    fi
else
    # config.json doesn't exist - will need Firebase setup
    NEEDS_FIREBASE_SETUP=true
fi

if [ "$NEEDS_FIREBASE_SETUP" = true ]; then
    echo -e "${YELLOW}[NOTICE]${NC} Firebase configuration needed for first-time setup."
    echo ""

    # Run automated Firebase setup
    python src/firebase_auto_setup.py

    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[ERROR]${NC} Firebase setup failed or was cancelled."
        echo ""
        echo "Please contact your POC if you need assistance."
        echo "You can also run the setup later using taranga.command"
        echo ""
        echo "Press ENTER to continue..."
        read
    else
        # Verify credentials were created and config updated
        if [ -f "config/firebase.json" ]; then
            echo ""
            echo -e "${GREEN}[OK]${NC} Firebase credentials configured successfully"
        else
            echo ""
            echo -e "${YELLOW}[WARNING]${NC} Setup completed but credentials file not found!"
            echo "You can run the setup later using taranga.command"
        fi
    fi
else
    echo -e "${GREEN}[OK]${NC} Firebase credentials already configured"
fi
echo ""

# Done!
echo ""
echo "========================================="
echo "  ✅ Setup Complete!"
echo "========================================="
echo ""
echo "📁 Location: $FULL_PATH"
echo ""
echo -e "${GREEN}Python Environment:${NC}"
echo "  • Python: $PYTHON_VERSION ($PYTHON_CMD)"
echo "  • Virtual Environment: $VENV_PATH"
echo "  • Dependencies: Installed"
echo ""
echo "To launch Taranga, double-click:"
echo "  • taranga.command (in the installed folder)"
echo ""
echo -e "${BLUE}Manual Activation (if needed):${NC}"
echo "  cd $FULL_PATH"
echo "  source venv/bin/activate"
echo ""
echo "========================================="
echo ""
echo "Press ENTER to finish..."
read
