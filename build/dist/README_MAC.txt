================================================================================
                        SPAMURAI v1.10.0 - macOS
                    WhatsApp Broadcast Messaging Tool
================================================================================

Thank you for downloading SPAMURAI!

This README will guide you through installation and usage.

================================================================================
                            QUICK START
================================================================================

1. EXTRACT THE APP
   - Double-click "SPAMURAI-macOS-v1.10.0.zip" to extract
   - You'll see "SPAMURAI.app"

2. INSTALL
   - Drag "SPAMURAI.app" to your Applications folder
   - That's it! Installation complete.

3. LAUNCH
   - Double-click "SPAMURAI.app" to start
   - Your browser will automatically open to http://localhost:8501

================================================================================
                        FIRST-TIME SECURITY WARNING
================================================================================

When you first open SPAMURAI, macOS will show a security warning:
   "SPAMURAI cannot be opened because the developer cannot be verified"

THIS IS NORMAL. Here's how to fix it:

   METHOD 1 (Recommended):
   1. Right-click (or Control+click) on SPAMURAI.app
   2. Select "Open" from the menu
   3. Click "Open" in the security dialog
   4. This only needs to be done ONCE

   METHOD 2 (Alternative):
   1. Go to System Preferences → Security & Privacy
   2. Click "Open Anyway" for SPAMURAI
   3. Confirm by clicking "Open"

After this one-time setup, SPAMURAI will open normally every time.

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

STEP 3: Launch SPAMURAI
   - Double-click SPAMURAI.app
   - Wait for the browser to open automatically
   - You'll see the SPAMURAI interface

STEP 4: Configure Settings
   - Click "Upload Excel File" and select your contacts file
   - Click "Upload Message File" and select your message file
   - Set delay between messages (recommended: 5-10 seconds)

STEP 5: Login to WhatsApp
   - Click "Start Campaign"
   - Scan the QR code with your phone (WhatsApp → Settings → Linked Devices)
   - Your WhatsApp session will be saved for future use

STEP 6: Send Messages
   - SPAMURAI will automatically send messages to all contacts
   - Monitor progress in the interface
   - Check logs for delivery status

================================================================================
                         SYSTEM REQUIREMENTS
================================================================================

- macOS 10.13 (High Sierra) or later
- No Python installation required
- No additional software needed
- Internet connection (for WhatsApp Web)

================================================================================
                            IMPORTANT NOTES
================================================================================

1. WhatsApp Session
   - Your WhatsApp login is saved locally on your computer
   - You won't need to scan QR code again unless you log out

2. Message Delays
   - SPAMURAI includes delays between messages to prevent blocking
   - Do not reduce delays below 5 seconds

3. WhatsApp Limits
   - WhatsApp may temporarily block accounts sending too many messages
   - Send in small batches (50-100 messages per session)
   - Take breaks between campaigns

4. Privacy & Security
   - SPAMURAI runs entirely on your computer
   - No data is sent to external servers
   - Your WhatsApp credentials stay on your device

================================================================================
                            TROUBLESHOOTING
================================================================================

PROBLEM: App won't open
SOLUTION: Follow the "First-Time Security Warning" steps above

PROBLEM: QR code won't scan
SOLUTION:
   - Make sure your phone has internet connection
   - Try refreshing the QR code
   - Restart SPAMURAI

PROBLEM: Messages not sending
SOLUTION:
   - Check your internet connection
   - Verify Excel file has correct column names
   - Ensure phone numbers include country code

PROBLEM: Browser doesn't open automatically
SOLUTION:
   - Manually open your browser
   - Go to: http://localhost:8501
   - SPAMURAI should be running there

PROBLEM: App crashes or freezes
SOLUTION:
   - Quit the app completely
   - Restart SPAMURAI
   - Check that no other WhatsApp Web sessions are active

================================================================================
                             FILE LOCATIONS
================================================================================

After installation, SPAMURAI creates these files:

Configuration & Data:
   - Config files: Same folder as your Excel/Message files
   - Chrome profile: Saves WhatsApp login session
   - Log files: Tracks sent messages and errors

To completely uninstall:
   1. Delete SPAMURAI.app from Applications
   2. Delete Chrome profile folder (if desired)
   3. Delete any config/log files you created

================================================================================
                            TECHNICAL SUPPORT
================================================================================

For help and support:

- GitHub Issues: https://github.com/fawkess/wa_broadcaster/issues
- Documentation: Check the GitHub repository
- Email: Contact via GitHub

Please include the following in support requests:
   - macOS version
   - SPAMURAI version (1.10.0)
   - Error message or screenshot
   - Steps to reproduce the issue

================================================================================
                              UPDATES
================================================================================

To update SPAMURAI to a newer version:

1. Download the latest version
2. Delete the old SPAMURAI.app from Applications
3. Install the new version following the Quick Start guide
4. Your settings and WhatsApp session will be preserved

================================================================================
                              ABOUT
================================================================================

SPAMURAI v1.10.0
WhatsApp Broadcast Messaging Tool

Built with:
   - Python & Streamlit (Web Interface)
   - Selenium WebDriver (WhatsApp Web Automation)
   - PyInstaller (Native macOS Bundle)

License: See LICENSE file in GitHub repository
Copyright: SPAMURAI Team

Built with ⚡ by the SPAMURAI team

================================================================================

Thank you for using SPAMURAI!

For the latest updates and documentation, visit:
https://github.com/fawkess/wa_broadcaster

================================================================================
