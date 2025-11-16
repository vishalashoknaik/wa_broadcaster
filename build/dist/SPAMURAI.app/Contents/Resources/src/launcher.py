#!/usr/bin/env python3
"""
SPAMURAI Launcher for PyInstaller Bundle
Properly launches Streamlit server instead of direct execution
"""

import sys
import os
import subprocess
from pathlib import Path

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    """Launch Streamlit server with gui.py"""
    print("🥷⚡ SPAMURAI - Launching...")

    # Find the gui.py script
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = sys._MEIPASS
        gui_script = os.path.join(bundle_dir, 'gui.py')
    else:
        # Running in development
        gui_script = os.path.join(os.path.dirname(__file__), 'gui.py')

    if not os.path.exists(gui_script):
        print(f"❌ Error: Could not find gui.py at {gui_script}")
        print(f"Bundle dir: {sys._MEIPASS if hasattr(sys, '_MEIPASS') else 'Not in bundle'}")
        print(f"Available files: {os.listdir(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.')}")
        sys.exit(1)

    print(f"📍 Found GUI script: {gui_script}")
    print(f"🚀 Starting Streamlit server...")
    print(f"📍 Browser will open at http://localhost:8501")
    print()

    # Launch Streamlit using the CLI
    try:
        # Use streamlit's main function directly
        from streamlit.web import cli as stcli

        # Set up sys.argv as if we called: streamlit run gui.py
        sys.argv = [
            "streamlit",
            "run",
            gui_script,
            "--global.developmentMode=false",
            "--server.headless=true",
            "--server.port=8501",
            "--browser.serverAddress=localhost"
        ]

        # Run Streamlit
        sys.exit(stcli.main())

    except Exception as e:
        print(f"❌ Failed to launch Streamlit: {e}")
        print()
        print("Falling back to subprocess method...")

        # Fallback: use subprocess
        try:
            result = subprocess.run(
                [sys.executable, "-m", "streamlit", "run", gui_script],
                check=True
            )
            sys.exit(result.returncode)
        except Exception as e2:
            print(f"❌ Subprocess method also failed: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()
