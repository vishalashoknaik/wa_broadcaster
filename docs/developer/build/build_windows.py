#!/usr/bin/env python3
"""
SPAMURAI Windows Build Script
Creates Windows installer and portable ZIP distribution
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Version info
VERSION = "1.10.0"
APP_NAME = "SPAMURAI"

def print_step(step, total, message):
    """Print a build step with formatting"""
    print(f"\n{Colors.CYAN}[Step {step}/{total}]{Colors.END} {message}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def check_dependencies():
    """Check if required build tools are installed"""
    print_step(1, 7, "Checking build dependencies...")

    try:
        import PyInstaller
        print_success("PyInstaller is installed")
    except ImportError:
        print_error("PyInstaller is not installed")
        print("Install with: pip install pyinstaller")
        return False

    return True

def clean_build_artifacts():
    """Clean previous build artifacts"""
    print_step(2, 7, "Cleaning previous build artifacts...")

    build_dir = Path(__file__).parent
    dirs_to_clean = [
        build_dir.parent / 'dist',
        build_dir / 'dist',
        build_dir.parent / 'build_temp',
        build_dir / '__pycache__',
    ]

    for dir_path in dirs_to_clean:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print_success(f"Removed {dir_path.name}")

    print_success("Build artifacts cleaned")

def build_executable():
    """Build the executable using PyInstaller"""
    print_step(3, 7, "Building executable with PyInstaller...")
    print("This may take several minutes...")

    build_dir = Path(__file__).parent
    spec_file = build_dir / 'spamurai.spec'

    if not spec_file.exists():
        print_error(f"Spec file not found: {spec_file}")
        return False

    try:
        # Run PyInstaller
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', '--clean', str(spec_file)],
            cwd=build_dir.parent,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print_error("PyInstaller build failed")
            print(result.stderr)
            return False

        print_success("Executable built successfully")
        return True

    except Exception as e:
        print_error(f"Build failed: {e}")
        return False

def create_readme_windows():
    """Create Windows-specific README file"""
    print_step(4, 7, "Creating README_WINDOWS.txt...")

    readme_content = f"""================================================================================
                        {APP_NAME} v{VERSION} - Windows
                    WhatsApp Broadcast Messaging Tool
================================================================================

Thank you for downloading {APP_NAME}!

This README will guide you through installation and usage.

================================================================================
                            QUICK START
================================================================================

1. EXTRACT THE ZIP
   - Right-click "{APP_NAME}-Windows-v{VERSION}.zip"
   - Select "Extract All..."
   - Choose a destination folder

2. INSTALL (OPTION 1: Using Installer)
   - Run "{APP_NAME}-Setup.exe"
   - Follow the installation wizard
   - Creates desktop shortcut and Start Menu entry

3. PORTABLE VERSION (OPTION 2: No Installation)
   - Extract the ZIP file
   - Go to the "{APP_NAME}" folder
   - Double-click "{APP_NAME}.exe" to run
   - No installation required!

4. LAUNCH
   - Double-click "{APP_NAME}.exe"
   - Your browser will automatically open to http://localhost:8501

================================================================================
                        FIRST-TIME SECURITY WARNING
================================================================================

When you first run {APP_NAME}, Windows may show a security warning:
   "Windows protected your PC"

THIS IS NORMAL for unsigned applications. Here's how to proceed:

   1. Click "More info"
   2. Click "Run anyway"
   3. This only needs to be done ONCE

If Windows Defender shows a warning:
   - This is a false positive (common with PyInstaller apps)
   - Click "Allow" or add {APP_NAME}.exe to exclusions

================================================================================
                            HOW TO USE
================================================================================

STEP 1: Prepare Your Data
   - Create an Excel file (.xlsx) with two columns:
     * "Name" - Contact name
     * "WhatsApp Number" - Phone number with country code
       Example: 919876543210 (for India)

STEP 2: Prepare Your Message
   - Create a text file (.txt) with your message
   - You can use <nick_name> placeholder for personalization
     Example: "Hi <nick_name>, this is a test message!"

STEP 3: Launch {APP_NAME}
   - Double-click {APP_NAME}.exe
   - Wait for the browser to open automatically
   - You'll see the {APP_NAME} interface

STEP 4: Configure Settings
   - Click "Upload Excel File" and select your contacts file
   - Click "Upload Message File" and select your message file
   - Set delay between messages (recommended: 5-10 seconds)

STEP 5: Login to WhatsApp
   - Click "Start Campaign"
   - Scan the QR code with your phone (WhatsApp → Settings → Linked Devices)
   - Your WhatsApp session will be saved for future use

STEP 6: Send Messages
   - {APP_NAME} will automatically send messages to all contacts
   - Monitor progress in the interface
   - Check logs for delivery status

================================================================================
                         SYSTEM REQUIREMENTS
================================================================================

- Windows 10 or later (64-bit recommended)
- No Python installation required
- No additional software needed
- Internet connection (for WhatsApp Web)
- Google Chrome (installed automatically if not present)

================================================================================
                            IMPORTANT NOTES
================================================================================

1. WhatsApp Session
   - Your WhatsApp login is saved locally on your computer
   - You won't need to scan QR code again unless you log out
   - Session stored in Chrome user data folder

2. Message Delays
   - {APP_NAME} includes delays between messages to prevent blocking
   - Do not reduce delays below 5 seconds
   - Recommended: 7-10 seconds per message

3. WhatsApp Limits
   - WhatsApp may temporarily block accounts sending too many messages
   - Send in small batches (50-100 messages per session)
   - Take breaks between campaigns
   - Use timeout features to add pauses

4. Privacy & Security
   - {APP_NAME} runs entirely on your computer
   - No data is sent to external servers
   - Your WhatsApp credentials stay on your device
   - All logs are stored locally

5. Firewall/Antivirus
   - Allow {APP_NAME}.exe through Windows Firewall
   - Add to antivirus exclusions if flagged

================================================================================
                            TROUBLESHOOTING
================================================================================

PROBLEM: Windows SmartScreen blocks the app
SOLUTION: Click "More info" → "Run anyway"

PROBLEM: Antivirus flags {APP_NAME} as malware
SOLUTION:
   - This is a false positive (common with PyInstaller)
   - Add {APP_NAME}.exe to antivirus exclusions
   - The app is safe and runs locally only

PROBLEM: QR code won't scan
SOLUTION:
   - Make sure your phone has internet connection
   - Try refreshing the QR code
   - Restart {APP_NAME}
   - Clear Chrome user data folder

PROBLEM: Messages not sending
SOLUTION:
   - Check your internet connection
   - Verify Excel file has correct column names ("Name", "WhatsApp Number")
   - Ensure phone numbers include country code (no + sign)
   - Check Windows Firewall isn't blocking Chrome

PROBLEM: Browser doesn't open automatically
SOLUTION:
   - Manually open your browser
   - Go to: http://localhost:8501
   - {APP_NAME} should be running there

PROBLEM: App crashes or freezes
SOLUTION:
   - Close the app completely (check Task Manager)
   - Delete Chrome user data folder
   - Restart {APP_NAME}
   - Check that no other WhatsApp Web sessions are active

PROBLEM: "Address already in use" error
SOLUTION:
   - Another instance of {APP_NAME} is running
   - Close all {APP_NAME} windows
   - Check Task Manager and end {APP_NAME}.exe processes
   - Restart the application

================================================================================
                             FILE LOCATIONS
================================================================================

After installation/extraction, {APP_NAME} creates these folders:

Installation Directory (if using installer):
   C:\\Program Files\\{APP_NAME}\\

Portable Directory (if using ZIP):
   Wherever you extracted the ZIP file

Data Files (created when you run campaigns):
   - config.json - Your configuration settings
   - Chrome user data - WhatsApp login session
   - Log files - Sent messages and errors
   - sent_numbers.txt - Successfully sent numbers
   - error_numbers.txt - Failed numbers

To completely uninstall:
   1. Uninstall via Windows Settings (if using installer)
      OR delete the {APP_NAME} folder (if portable)
   2. Delete Chrome user data folder (if desired)
   3. Delete any config/log files you created

================================================================================
                            COMMAND LINE OPTIONS
================================================================================

You can run {APP_NAME} from Command Prompt with options:

   {APP_NAME}.exe --config path\\to\\config.json

Example:
   {APP_NAME}.exe --config C:\\Users\\YourName\\Documents\\my_config.json

================================================================================
                            TECHNICAL SUPPORT
================================================================================

For help and support:

- GitHub Issues: https://github.com/fawkess/wa_broadcaster/issues
- Documentation: Check the GitHub repository
- Email: Contact via GitHub

Please include the following in support requests:
   - Windows version (10, 11, etc.)
   - {APP_NAME} version ({VERSION})
   - Error message or screenshot
   - Steps to reproduce the issue
   - Log files (if applicable)

================================================================================
                              UPDATES
================================================================================

To update {APP_NAME} to a newer version:

If using INSTALLER:
   1. Download the latest {APP_NAME}-Setup.exe
   2. Run the installer (it will replace the old version)
   3. Your settings and WhatsApp session will be preserved

If using PORTABLE ZIP:
   1. Download the latest ZIP file
   2. Extract to a new folder
   3. Copy your config.json and data files to the new folder
   4. Delete the old folder

================================================================================
                         CONFIGURATION FILES
================================================================================

{APP_NAME} uses a config.json file for advanced settings.

See config.example.json for a template with all available options:
   - Excel file path
   - Message file path
   - Delay settings
   - Timeout intervals
   - Chrome profile location
   - Log file paths

You can edit config.json with Notepad or any text editor.

For Google Sheets integration, see GOOGLE_SHEETS_SETUP.txt

================================================================================
                              ABOUT
================================================================================

{APP_NAME} v{VERSION}
WhatsApp Broadcast Messaging Tool for Windows

Built with:
   - Python & Streamlit (Web Interface)
   - Selenium WebDriver (WhatsApp Web Automation)
   - PyInstaller (Native Windows Executable)
   - Inno Setup (Windows Installer)

License: See LICENSE file in GitHub repository
Copyright: {APP_NAME} Team

Built with ⚡ by the {APP_NAME} team

================================================================================
                            LEGAL DISCLAIMER
================================================================================

This tool is for legitimate marketing and communication purposes only.

Users must:
   - Comply with WhatsApp Terms of Service
   - Obtain consent from recipients
   - Not send spam or unsolicited messages
   - Follow local laws and regulations

The developers are not responsible for:
   - Account bans or restrictions
   - Misuse of the software
   - Violations of WhatsApp policies

Use responsibly and ethically.

================================================================================

Thank you for using {APP_NAME}!

For the latest updates and documentation, visit:
https://github.com/fawkess/wa_broadcaster

================================================================================
"""

    build_dir = Path(__file__).parent
    readme_path = build_dir / 'dist' / 'README_WINDOWS.txt'
    readme_path.parent.mkdir(exist_ok=True)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print_success("README_WINDOWS.txt created")
    return True

def create_windows_zip():
    """Create portable ZIP distribution"""
    print_step(5, 7, "Creating portable ZIP package...")

    build_dir = Path(__file__).parent
    dist_dir = build_dir.parent / 'dist'
    spamurai_dir = dist_dir / APP_NAME

    if not spamurai_dir.exists():
        print_error(f"Build directory not found: {spamurai_dir}")
        return False

    # Create output directory
    output_dir = build_dir / 'dist'
    output_dir.mkdir(exist_ok=True)

    zip_name = f"{APP_NAME}-Windows-v{VERSION}.zip"
    zip_path = output_dir / zip_name

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the entire SPAMURAI directory
            for root, dirs, files in os.walk(spamurai_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = Path(APP_NAME) / file_path.relative_to(spamurai_dir)
                    zipf.write(file_path, arcname)

            # Add README
            readme_path = output_dir / 'README_WINDOWS.txt'
            if readme_path.exists():
                zipf.write(readme_path, 'README_WINDOWS.txt')

            # Add documentation files from parent directory
            parent_dir = build_dir.parent
            doc_files = [
                'README.md',
                'GOOGLE_SHEETS_SETUP.md',
                'config.example.json',
            ]

            for doc_file in doc_files:
                doc_path = parent_dir / doc_file
                if doc_path.exists():
                    zipf.write(doc_path, doc_file)

        # Get file size
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print_success(f"ZIP package created: {zip_name} ({size_mb:.1f} MB)")
        return True

    except Exception as e:
        print_error(f"Failed to create ZIP: {e}")
        return False

def create_installer_windows():
    """Create Windows installer using Inno Setup"""
    print_step(6, 7, "Creating Windows installer...")

    # Check if Inno Setup is installed
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]

    inno_setup_path = None
    for path in inno_paths:
        if os.path.exists(path):
            inno_setup_path = path
            break

    if not inno_setup_path:
        print_warning("Inno Setup not found - skipping installer creation")
        print("Download from: https://jrsoftware.org/isdl.php")
        print("Note: ZIP package is still available for portable use")
        return True

    build_dir = Path(__file__).parent
    iss_file = build_dir / 'installer.iss'

    if not iss_file.exists():
        print_warning("installer.iss not found - skipping installer creation")
        return True

    try:
        result = subprocess.run(
            [inno_setup_path, str(iss_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print_error("Installer creation failed")
            print(result.stderr)
            return False

        # Move installer to build/dist
        output_dir = build_dir / 'dist'
        output_dir.mkdir(exist_ok=True)

        installer_src = build_dir.parent / 'dist' / f'{APP_NAME}-Setup.exe'
        installer_dst = output_dir / f'{APP_NAME}-Setup-v{VERSION}.exe'

        if installer_src.exists():
            shutil.copy2(installer_src, installer_dst)
            size_mb = installer_dst.stat().st_size / (1024 * 1024)
            print_success(f"Windows installer created: {installer_dst.name} ({size_mb:.1f} MB)")

        return True

    except Exception as e:
        print_error(f"Installer creation failed: {e}")
        return False

def show_build_summary():
    """Show build summary and output locations"""
    print_step(7, 7, "Build complete!")

    build_dir = Path(__file__).parent
    output_dir = build_dir / 'dist'

    print(f"\n{Colors.BOLD}Build Output:{Colors.END}")
    print(f"\nLocation: {output_dir}\n")

    # List all outputs
    if output_dir.exists():
        outputs = []

        # ZIP package
        zip_file = output_dir / f"{APP_NAME}-Windows-v{VERSION}.zip"
        if zip_file.exists():
            size_mb = zip_file.stat().st_size / (1024 * 1024)
            outputs.append(f"📦 Portable ZIP: {zip_file.name} ({size_mb:.1f} MB)")

        # Installer
        installer_file = output_dir / f"{APP_NAME}-Setup-v{VERSION}.exe"
        if installer_file.exists():
            size_mb = installer_file.stat().st_size / (1024 * 1024)
            outputs.append(f"💿 Installer: {installer_file.name} ({size_mb:.1f} MB)")

        # README
        readme_file = output_dir / 'README_WINDOWS.txt'
        if readme_file.exists():
            outputs.append(f"📄 README: {readme_file.name}")

        for output in outputs:
            print_success(output)

    print(f"\n{Colors.BOLD}Distribution Options:{Colors.END}")
    print(f"  • ZIP Package: For portable/no-install use")
    print(f"  • Installer: For traditional Windows installation")

    print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}Build completed successfully!{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}\n")

    print(f"{Colors.CYAN}Next steps:{Colors.END}")
    print(f"  1. Test the executable/installer")
    print(f"  2. Upload to GitHub releases")
    print(f"  3. Share the ZIP or installer with users")

def main():
    """Main build process"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{APP_NAME} Windows Build Script{Colors.END}")
    print(f"{Colors.BOLD}Version: {VERSION}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Clean artifacts
    clean_build_artifacts()

    # Build executable
    if not build_executable():
        print_error("\nBuild failed!")
        sys.exit(1)

    # Create README
    if not create_readme_windows():
        print_warning("\nREADME creation failed, but build continues")

    # Create ZIP package
    if not create_windows_zip():
        print_error("\nZIP creation failed!")
        sys.exit(1)

    # Create Windows installer (optional)
    if not create_installer_windows():
        print_warning("\nInstaller creation failed, but ZIP is available")

    # Show summary
    show_build_summary()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Build cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
