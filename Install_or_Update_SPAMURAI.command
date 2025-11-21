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
REPO_NAME="wa_broadcaster"
DEFAULT_INSTALL_DIR="$HOME/Desktop"

# Step 1: Check Git installation
echo -e "${CYAN}[Step 1/3]${NC} Checking Git installation..."
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
echo -e "${CYAN}[Step 2/3]${NC} Determining installation location..."
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

# Step 3: Install or Update
echo -e "${CYAN}[Step 3/3]${NC} Installing/Updating Taranga..."
echo ""

if [ -d "$FULL_PATH" ]; then
    # Repository exists - UPDATE
    echo -e "${BLUE}Found existing installation!${NC}"
    echo ""
    echo "Updating to latest version..."
    echo ""

    cd "$FULL_PATH"

    # Stash any local changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "Saving your local changes..."
        git stash push -m "Auto-stash before update on $(date)"
        STASHED=true
    fi

    # Pull latest changes
    echo "Fetching updates from GitHub..."
    if git pull origin master; then
        echo ""
        echo -e "${GREEN}✅ UPDATE SUCCESSFUL!${NC}"
        echo ""
        echo "Taranga has been updated to the latest version!"

        if [ "$STASHED" = true ]; then
            echo ""
            echo -e "${YELLOW}Note: Your local changes were stashed.${NC}"
            echo "To restore them, run: git stash pop"
        fi
    else
        echo ""
        echo -e "${RED}[ERROR]${NC} Update failed!"
        echo "Please check your internet connection and try again."
        echo ""
        echo "Press ENTER to exit..."
        read
        exit 1
    fi
else
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
    else
        echo ""
        echo -e "${RED}[ERROR]${NC} Installation failed!"
        echo "Please check your internet connection and try again."
        echo ""
        echo "Press ENTER to exit..."
        read
        exit 1
    fi
fi

# Done!
echo ""
echo "========================================="
echo "  ✅ Setup Complete!"
echo "========================================="
echo ""
echo "📁 Location: $FULL_PATH"
echo ""
echo "To launch Taranga, double-click:"
echo "  • SPAMURAI.command (in the installed folder)"
echo ""
echo "========================================="
echo ""
echo "Press ENTER to finish..."
read
