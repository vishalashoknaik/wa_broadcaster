================================================================================
                    FIREBASE CREDENTIALS FILE
                        firebase_spamurai.json
================================================================================

This file contains the Firebase credentials needed for SPAMURAI to function.

IMPORTANT: Keep this file secure and do not share it publicly!

================================================================================
HOW TO INSTALL
================================================================================

OPTION A: Automatic Setup (Recommended)
----------------------------------------

1. Open Command Prompt (Windows) or Terminal (Mac)
2. Navigate to SPAMURAI folder:

   Windows:
   cd C:\SPAMURAI

   Mac:
   cd /path/to/SPAMURAI

3. Run the setup script:

   Windows:
   setup_firebase.bat firebase_spamurai.json

   Mac:
   ./setup_firebase.sh firebase_spamurai.json

4. Wait for "Setup complete!" message
5. Close and reopen your Command Prompt/Terminal
6. Done!


OPTION B: Manual Setup
-----------------------

1. Copy this file (firebase_spamurai.json) to the SPAMURAI config folder:

   Windows:
   C:\SPAMURAI\config\firebase_spamurai.json

   Mac:
   /path/to/SPAMURAI/config/firebase_spamurai.json

2. Rename it to:
   firebase-credentials.json

3. Done!


================================================================================
VERIFYING INSTALLATION
================================================================================

Run the diagnostic tool to verify Firebase is configured:

Windows:
diagnose_windows.bat

Mac:
./diagnose_mac.sh

You should see:
[OK] Firebase credentials are properly configured


================================================================================
TROUBLESHOOTING
================================================================================

If SPAMURAI shows "Firebase credentials not configured":

1. Make sure you completed one of the setup options above
2. Verify the file is in the correct location:
   - Environment variable set (Option A), OR
   - File at config/firebase-credentials.json (Option B)
3. Restart your terminal/command prompt
4. Try launching SPAMURAI again

To check if environment variable is set:

Windows:
echo %FIREBASE_CREDENTIALS%

Mac:
echo $FIREBASE_CREDENTIALS

If nothing shows, re-run the setup script (Option A).


================================================================================
SECURITY NOTES
================================================================================

- This file grants access to the Firebase project
- Do NOT share this file publicly or commit it to Git
- Keep it secure on your computer
- Only share with authorized SPAMURAI users


================================================================================
NEED HELP?
================================================================================

See the full installation guides:
- Windows: WINDOWS_INSTALLATION.md
- Mac: MAC_INSTALLATION.md (if available)
- Firebase Details: FIREBASE_SETUP.md

Or run the diagnostic tool to identify issues.


================================================================================
