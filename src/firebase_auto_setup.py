#!/usr/bin/env python3
"""
Automated Firebase Credentials Setup
Called by launcher scripts when firebase.json is missing
"""

import sys
import zipfile
import tempfile
import json
import re
from pathlib import Path

# Auto-install gdown if not present (for Google Drive downloads)
try:
    import gdown
except ImportError:
    print("Installing required dependency: gdown...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
    import gdown


def setup_firebase_credentials(credentials_path="config/firebase.json"):
    """
    Run guided Firebase credentials setup

    Args:
        credentials_path: Path where credentials should be saved (default: config/firebase.json)

    Returns:
        bool: True if setup succeeded, False otherwise
    """
    credentials_path = Path(credentials_path)

    # Ensure config directory exists
    credentials_path.parent.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*80)
    print("FIREBASE CREDENTIALS SETUP")
    print("="*80)
    print("\nFirebase credentials not found. Let's set them up!")
    print("\nYou'll need two pieces of information from your POC:")
    print("  1. Google Drive URL for the credential zip")
    print("  2. Password for the credential zip")
    print("\n" + "="*80 + "\n")

    # Step 1: Get Google Drive URL
    drive_url = _prompt_drive_url()
    if not drive_url:
        print("\n❌ Setup cancelled.")
        return False

    # Step 2: Get zip password
    zip_password = _prompt_password()
    if not zip_password:
        print("\n❌ Setup cancelled.")
        return False

    # Step 3: Download and extract
    print("\n" + "="*80)
    print("DOWNLOADING AND INSTALLING CREDENTIALS")
    print("="*80 + "\n")

    try:
        success = _download_and_extract(drive_url, zip_password, credentials_path)

        if success:
            print("\n" + "="*80)
            print("✓ FIREBASE CREDENTIALS INSTALLED SUCCESSFULLY!")
            print("="*80)
            print(f"\nCredentials saved to: {credentials_path}")
            print("\nContinuing with SPAMURAI launch...")
            print("="*80 + "\n")
            return True
        else:
            print("\n" + "="*80)
            print("❌ SETUP FAILED")
            print("="*80)
            print("\nPlease verify:")
            print("  1. The Google Drive URL is correct")
            print("  2. The password is correct")
            print("  3. You have internet connectivity")
            print("\nContact your POC if the problem persists.")
            print("="*80 + "\n")
            return False

    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        print("\nPlease contact your POC for assistance.")
        return False


def _prompt_drive_url():
    """Prompt user for Google Drive URL"""
    print("[Step 1/2] Google Drive URL")
    print("-" * 80)
    print("Enter the Google Drive URL for the credential zip.")
    print("(This URL is provided by your POC)")
    print()
    print("Example formats:")
    print("  • https://drive.google.com/file/d/FILE_ID/view")
    print("  • https://drive.google.com/uc?id=FILE_ID")
    print()

    while True:
        url = input("Google Drive URL (or 'cancel' to exit): ").strip()

        if url.lower() == 'cancel':
            return None

        if not url:
            print("❌ URL cannot be empty. Please try again.\n")
            continue

        # Validate URL format
        if _is_valid_drive_url(url):
            return url
        else:
            print("❌ Invalid Google Drive URL format. Please try again.\n")


def _prompt_password():
    """Prompt user for zip password"""
    print("\n[Step 2/2] Credential Zip Password")
    print("-" * 80)
    print("Enter the password for the credential zip file.")
    print("(This password is provided by your POC)")
    print()

    # Try to use getpass for hidden input, fallback to regular input
    try:
        import getpass
        password = getpass.getpass("Password (or 'cancel' to exit): ").strip()
    except:
        password = input("Password (or 'cancel' to exit): ").strip()

    if password.lower() == 'cancel':
        return None

    if not password:
        print("❌ Password cannot be empty.")
        return None

    return password


def _is_valid_drive_url(url):
    """Validate Google Drive URL format"""
    patterns = [
        r'drive\.google\.com/file/d/([^/]+)',
        r'drive\.google\.com/uc\?id=([^&]+)',
        r'drive\.google\.com/open\?id=([^&]+)'
    ]

    for pattern in patterns:
        if re.search(pattern, url):
            return True

    return False


def _download_and_extract(drive_url, password, credentials_path):
    """Download zip from Google Drive and extract credentials"""

    # Create temporary directory for download
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / "firebase_credentials.zip"

        # Step 1: Download from Google Drive
        print("📥 Downloading credentials from Google Drive...")
        try:
            gdown.download(drive_url, str(zip_path), quiet=False, fuzzy=True)

            if not zip_path.exists():
                print("❌ Download failed. File not found.")
                return False

            print("✓ Download complete\n")

        except Exception as e:
            print(f"❌ Download failed: {str(e)}")
            return False

        # Step 2: Extract zip with password
        print("📂 Extracting credentials...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                pwd_bytes = password.encode('utf-8')
                zip_ref.extractall(temp_path, pwd=pwd_bytes)

            print("✓ Extraction complete\n")

        except RuntimeError as e:
            if 'Bad password' in str(e):
                print("❌ Incorrect password. Please try again.")
            else:
                print(f"❌ Extraction failed: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Extraction failed: {str(e)}")
            return False

        # Step 3: Find and validate JSON file
        print("🔍 Locating credential file...")
        json_files = list(temp_path.glob("**/*.json"))

        if not json_files:
            print("❌ No JSON file found in the zip archive.")
            return False

        source_json = json_files[0]
        print(f"✓ Found: {source_json.name}\n")

        # Step 4: Validate JSON structure
        print("✓ Validating credentials...")
        try:
            with open(source_json, 'r') as f:
                creds = json.load(f)

            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in creds]

            if missing_fields:
                print(f"❌ Invalid credentials file. Missing fields: {', '.join(missing_fields)}")
                return False

            if creds.get('type') != 'service_account':
                print("❌ Invalid credentials file. Not a service account key.")
                return False

            print("✓ Credentials are valid\n")

        except json.JSONDecodeError:
            print("❌ Invalid JSON file format.")
            return False
        except Exception as e:
            print(f"❌ Validation failed: {str(e)}")
            return False

        # Step 5: Copy to final location
        print(f"💾 Installing credentials to {credentials_path}...")
        try:
            import shutil
            shutil.copy2(source_json, credentials_path)

            print("✓ Installation complete\n")
            return True

        except Exception as e:
            print(f"❌ Installation failed: {str(e)}")
            return False


if __name__ == "__main__":
    # Allow standalone execution for testing
    success = setup_firebase_credentials()
    sys.exit(0 if success else 1)
