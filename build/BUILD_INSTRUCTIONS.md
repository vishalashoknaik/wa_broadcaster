# Windows Build Instructions

This guide explains how to build SPAMURAI for Windows distribution.

## What Gets Built

The Windows build script creates TWO distribution packages:

1. **Portable ZIP Package** - `SPAMURAI-Windows-v1.10.0.zip`
   - No installation required
   - Extract and run
   - Perfect for users who don't want to install software
   - Similar to the macOS .zip distribution

2. **Windows Installer** - `SPAMURAI-Setup-v1.10.0.exe`
   - Professional installer using Inno Setup
   - Creates Start Menu shortcuts
   - Optional desktop icon
   - Proper uninstaller
   - Checks for Python installation

## Prerequisites

### Required:
- **Python 3.8+** installed on your system
- **PyInstaller**: Install with `pip install pyinstaller`

### Optional (for installer):
- **Inno Setup 6**: Download from https://jrsoftware.org/isdl.php
  - Only needed if you want to create the `.exe` installer
  - ZIP package will still be created without it

## How to Build

### Method 1: Using the Batch File (Easiest)

1. Open Command Prompt or PowerShell
2. Navigate to the build directory:
   ```cmd
   cd build
   ```
3. Run the build script:
   ```cmd
   build_windows.bat
   ```
4. Wait for the build to complete (may take 5-10 minutes)
5. Find your distributions in `build/dist/`:
   - `SPAMURAI-Windows-v1.10.0.zip`
   - `SPAMURAI-Setup-v1.10.0.exe` (if Inno Setup is installed)
   - `README_WINDOWS.txt`

### Method 2: Using Python Directly

```cmd
cd build
python build_windows.py
```

## Build Output

After a successful build, you'll find in `build/dist/`:

```
build/dist/
├── SPAMURAI-Windows-v1.10.0.zip       # Portable package (~230 MB)
├── SPAMURAI-Setup-v1.10.0.exe         # Installer (~120 MB)
└── README_WINDOWS.txt                  # User instructions
```

## What's Inside the ZIP Package

```
SPAMURAI-Windows-v1.10.0.zip
├── SPAMURAI/                   # Main application folder
│   ├── SPAMURAI.exe           # Main executable
│   └── _internal/             # Dependencies and libraries
├── README_WINDOWS.txt         # Windows-specific instructions
├── README.md                  # General documentation
├── GOOGLE_SHEETS_SETUP.md    # Google Sheets integration guide
└── config.example.json        # Example configuration file
```

## Build Process Steps

The build script performs these steps:

1. **Check Dependencies** - Verifies PyInstaller is installed
2. **Clean Artifacts** - Removes previous build files
3. **Build Executable** - Runs PyInstaller with spamurai.spec
4. **Create README** - Generates Windows-specific README
5. **Create ZIP** - Packages everything into a portable ZIP
6. **Create Installer** - Builds Inno Setup installer (if available)
7. **Show Summary** - Displays build results

## Troubleshooting

### PyInstaller Not Found
```cmd
pip install pyinstaller
```

### Build Fails
- Check Python version: `python --version` (must be 3.8+)
- Install missing dependencies: `pip install -r requirements.txt`
- Clear previous builds: Delete `dist` and `build` folders

### Inno Setup Not Found
- Installer creation will be skipped
- ZIP package will still be created
- Install Inno Setup from: https://jrsoftware.org/isdl.php

### "Module not found" Errors
- Make sure you're in the `build` directory
- Check that `../src/launcher.py` exists
- Run: `pip install -r ../requirements.txt`

## Testing the Build

### Test the ZIP Package:
1. Extract the ZIP to a test folder
2. Navigate to the `SPAMURAI` folder
3. Double-click `SPAMURAI.exe`
4. Browser should open to http://localhost:8501

### Test the Installer:
1. Run `SPAMURAI-Setup-v1.10.0.exe`
2. Follow installation wizard
3. Launch from Start Menu or Desktop
4. Browser should open to http://localhost:8501

## Distribution

### Uploading to GitHub Releases

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Upload both files:
   - `SPAMURAI-Windows-v1.10.0.zip`
   - `SPAMURAI-Setup-v1.10.0.exe`
4. Add release notes

### Recommended Release Description

```markdown
## SPAMURAI v1.10.0 - Windows

### Downloads

**Choose one:**
- **Installer** (Recommended): `SPAMURAI-Setup-v1.10.0.exe` - Installs to Program Files
- **Portable ZIP**: `SPAMURAI-Windows-v1.10.0.zip` - No installation required

### What's New
- [List your changes here]

### Installation

**Using Installer:**
1. Download `SPAMURAI-Setup-v1.10.0.exe`
2. Run the installer
3. Follow the setup wizard

**Using Portable ZIP:**
1. Download `SPAMURAI-Windows-v1.10.0.zip`
2. Extract to any folder
3. Run `SPAMURAI.exe` from the extracted folder

See `README_WINDOWS.txt` for detailed instructions.
```

## Customization

### Change Version Number

Edit these files:
- `build_windows.py` - Line 21: `VERSION = "1.10.0"`
- `installer.iss` - Line 6: `#define MyAppVersion "1.10.0"`
- `spamurai.spec` - Line 145: `'CFBundleShortVersionString': '1.10.0'`

### Customize README

Edit `build_windows.py` starting at line 183 (the `create_readme_windows()` function)

### Add/Remove Documentation Files

Edit `build_windows.py` around line 467:
```python
doc_files = [
    'README.md',
    'GOOGLE_SHEETS_SETUP.md',
    'config.example.json',
    # Add your files here
]
```

## File Size Information

Typical sizes:
- ZIP Package: ~230 MB (compressed)
- Installer: ~120 MB
- Extracted size: ~350 MB

Large size is due to:
- Python runtime
- Streamlit and web framework
- Selenium and ChromeDriver
- All dependencies bundled

## Comparing with macOS Build

| Feature | Windows | macOS |
|---------|---------|-------|
| Portable Package | ZIP (230 MB) | ZIP (232 MB) |
| Installer | Inno Setup (.exe) | .app bundle |
| README | README_WINDOWS.txt | README_MAC.txt |
| Build Script | build_windows.py | build.py |
| Launcher | build_windows.bat | ./build.py |

## Next Steps

1. Test both packages thoroughly
2. Create GitHub release
3. Upload both distributions
4. Update documentation
5. Announce the release

## Support

For build issues:
- Check GitHub Issues
- Review PyInstaller documentation
- Check Inno Setup documentation

---

**Note:** The first build may take 10-15 minutes. Subsequent builds are faster.
