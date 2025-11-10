#!/usr/bin/env python3
"""
SPAMURAI Build Script
Builds standalone executables for Windows and macOS
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

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
    print_step(1, 6, "Checking build dependencies...")

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
    print_step(2, 6, "Cleaning previous build artifacts...")

    dirs_to_clean = ['../dist', '../build_temp', '__pycache__']

    for dir_name in dirs_to_clean:
        dir_path = Path(__file__).parent / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print_success(f"Removed {dir_name}")

    print_success("Build artifacts cleaned")

def create_icon_files():
    """Create placeholder icon files if they don't exist"""
    print_step(3, 6, "Checking icon files...")

    build_dir = Path(__file__).parent

    # For now, just create empty icon files
    # Users should replace these with actual icons
    icon_files = []

    if platform.system() == 'Windows':
        icon_files.append(build_dir / 'icon.ico')
    elif platform.system() == 'Darwin':
        icon_files.append(build_dir / 'icon.icns')

    for icon_file in icon_files:
        if not icon_file.exists():
            print_warning(f"{icon_file.name} not found - building without custom icon")
            # Create empty file to prevent PyInstaller errors
            icon_file.touch()

    if all(f.exists() for f in icon_files):
        print_success("Icon files ready")

def build_executable():
    """Build the executable using PyInstaller"""
    print_step(4, 6, "Building executable with PyInstaller...")
    print("This may take several minutes...")

    build_dir = Path(__file__).parent
    spec_file = build_dir / 'spamurai.spec'

    try:
        # Run PyInstaller using python -m to avoid PATH issues
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

def create_installer_windows():
    """Create Windows installer using Inno Setup"""
    if platform.system() != 'Windows':
        return True  # Skip on non-Windows

    print_step(5, 6, "Creating Windows installer...")

    # Check if Inno Setup is installed
    inno_setup_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

    if not os.path.exists(inno_setup_path):
        print_warning("Inno Setup not found - skipping installer creation")
        print("Download from: https://jrsoftware.org/isdl.php")
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

        print_success("Windows installer created")
        return True

    except Exception as e:
        print_error(f"Installer creation failed: {e}")
        return False

def show_build_summary():
    """Show build summary and output locations"""
    print_step(6, 6, "Build complete!")

    dist_dir = Path(__file__).parent.parent / 'dist'

    print(f"\n{Colors.BOLD}Build Output:{Colors.END}")

    if platform.system() == 'Windows':
        exe_path = dist_dir / 'SPAMURAI' / 'SPAMURAI.exe'
        if exe_path.exists():
            print_success(f"Executable: {exe_path}")

        installer_path = dist_dir / 'SPAMURAI-Setup.exe'
        if installer_path.exists():
            print_success(f"Installer: {installer_path}")

    elif platform.system() == 'Darwin':
        app_path = dist_dir / 'SPAMURAI.app'
        if app_path.exists():
            print_success(f"Application: {app_path}")

    print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
    print(f"{Colors.GREEN}Build completed successfully!{Colors.END}")
    print(f"{Colors.GREEN}{'='*50}{Colors.END}\n")

def main():
    """Main build process"""
    print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}SPAMURAI Build Script{Colors.END}")
    print(f"{Colors.BOLD}Platform: {platform.system()}{Colors.END}")
    print(f"{Colors.BOLD}{'='*50}{Colors.END}")

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Clean artifacts
    clean_build_artifacts()

    # Create icon files
    create_icon_files()

    # Build executable
    if not build_executable():
        print_error("\nBuild failed!")
        sys.exit(1)

    # Create Windows installer (if on Windows)
    if not create_installer_windows():
        print_warning("\nInstaller creation failed, but executable is available")

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
        sys.exit(1)
