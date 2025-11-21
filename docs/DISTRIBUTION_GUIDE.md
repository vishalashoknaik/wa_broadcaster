# Distribution Guide - Taranga Installer

This guide explains how to distribute the **single-click installer** to Mac users.

## Overview

The `Install_or_Update_SPAMURAI.command` script provides a one-click solution for:
- **First-time installation**: Clones the repository from GitHub
- **Updates**: Pulls latest changes from master branch
- **Git setup**: Automatically installs Git if not present

## How It Works

### First Run (Fresh Install)
1. User double-clicks `Install_or_Update_SPAMURAI.command`
2. Script checks if Git is installed (installs if needed)
3. Asks where to install (defaults to Desktop)
4. Clones repo from GitHub
5. User can then run `SPAMURAI.command` to launch

### Subsequent Runs (Updates)
1. User double-clicks same installer file
2. Script detects existing installation
3. Runs `git pull` to get latest changes
4. Preserves local changes (if any) using git stash
5. User's installation is updated!

## Distribution Steps

### Step 1: Prepare the Installer File

The file is already created and executable:
```bash
Install_or_Update_SPAMURAI.command
```

### Step 2: Create a ZIP File

```bash
# From project root
zip -r Taranga_Installer_Mac.zip Install_or_Update_SPAMURAI.command
```

### Step 3: Distribute to Users

Send users the ZIP file with these instructions:

---

## User Instructions (to include in email/docs)

### Installing Taranga on Mac

1. **Download** the `Taranga_Installer_Mac.zip` file
2. **Unzip** the file (double-click it)
3. **Double-click** `Install_or_Update_SPAMURAI.command`
4. **Follow the prompts**:
   - If asked to install Xcode tools, click "Install" and wait
   - Press ENTER to install on Desktop (or type a custom path)
   - Wait for installation to complete
5. **Launch Taranga**:
   - Go to your Desktop (or chosen location)
   - Open the `wa_broadcaster` folder
   - Double-click `SPAMURAI.command` to start

### Updating Taranga

To get the latest version:
1. **Double-click** the same `Install_or_Update_SPAMURAI.command` file you used before
2. The script will automatically detect your installation and update it
3. That's it! Your installation is now up to date

---

## Technical Details

### What the Script Does

**Git Check:**
- Checks if Git is installed
- If not, installs Xcode Command Line Tools
- Waits for user to complete installation

**Installation Detection:**
- Checks if `wa_broadcaster` folder exists at target location
- If exists: runs `git pull origin master`
- If not exists: runs `git clone`

**Local Changes:**
- If user has uncommitted changes, they're stashed before update
- User can restore them later with `git stash pop`

### Repository Details

- **Source**: `https://github.com/vishalashoknaik/wa_broadcaster.git`
- **Branch**: `master`
- **Folder Name**: `wa_broadcaster`

### Customization

To change the default install location, edit:
```bash
DEFAULT_INSTALL_DIR="$HOME/Desktop"
```

To change the repository URL, edit:
```bash
REPO_URL="https://github.com/vishalashoknaik/wa_broadcaster.git"
```

## Advantages

✅ **Single file distribution** - Just one ZIP to send
✅ **Handles both install and update** - Users don't need separate tools
✅ **Auto-installs Git** - No prerequisites needed
✅ **User-friendly** - Clear prompts and colored output
✅ **Preserves local changes** - Won't overwrite user modifications
✅ **Works offline after first install** - Only needs internet for install/update

## Alternative Distribution Methods

### Option 1: Direct Download Link
Host the ZIP on a file server and provide a direct download link.

### Option 2: Google Drive
1. Upload `Taranga_Installer_Mac.zip` to Google Drive
2. Set sharing to "Anyone with the link"
3. Share the link with users

### Option 3: Include in Documentation
Add the installer to your main documentation repository as a release asset.

## Troubleshooting

### If user sees "cannot be opened because it is from an unidentified developer"

**Solution:**
1. Right-click the file
2. Hold Option key and click "Open"
3. Click "Open" in the dialog
4. Or: System Preferences → Security & Privacy → Click "Open Anyway"

### If Git installation fails

**Solution:**
User should manually install from: https://git-scm.com/download/mac

### If git pull fails

**Possible causes:**
- No internet connection
- Local uncommitted changes conflicting with remote
- User modified core files

**Solution:**
User can run manually in Terminal:
```bash
cd ~/Desktop/wa_broadcaster  # or their install location
git stash
git pull origin master
```

## Security Notes

⚠️ The script requires executable permissions
⚠️ Users may need to explicitly allow execution (macOS Gatekeeper)
⚠️ Script runs with user permissions only (no sudo required)
✅ Source code is visible - users can inspect before running
✅ Only downloads from official GitHub repository

## Version Control

When you update the installer script:
1. Commit changes to GitHub
2. Create new ZIP file
3. Redistribute to users
4. Update version number in documentation

---

**Last Updated**: November 2024
**Maintainer**: wa_broadcaster team
