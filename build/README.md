# SPAMURAI Build System

This directory contains all the tools and scripts needed to build native installers for SPAMURAI.

> ⚠️ **IMPORTANT NOTE:** Native .app/.exe bundles have **limited functionality** with Streamlit applications due to Streamlit's web server architecture. The **Quick Launchers** (`../launchers/`) are the **recommended distribution method** for SPAMURAI as they provide full functionality and better user experience.
>
> This build system is provided for experimentation and future development, but is **not production-ready** for Streamlit-based applications.

---

## 🎯 What Gets Built

### Phase 1: Quick Launchers (Already Available)
Located in `../launchers/`:
- ✅ `SPAMURAI.bat` - Windows double-click launcher
- ✅ `SPAMURAI.command` - macOS double-click launcher

### Phase 2: Native Installers (This Directory) - ⚠️ EXPERIMENTAL
Built using this directory:
- 📦 `SPAMURAI-Setup.exe` - Windows installer with wizard **(not fully functional)**
- 📦 `SPAMURAI.app` - macOS application bundle **(not fully functional)**

**Known Issues:**
- Streamlit runs in "bare mode" when executed directly
- Missing ScriptRunContext warnings
- Web server doesn't start properly
- **Use Quick Launchers instead for production**

---

## 📋 Prerequisites

### All Platforms
```bash
pip install pyinstaller
```

### Windows Only (for installer)
Download and install [Inno Setup 6](https://jrsoftware.org/isdl.php)

### macOS Only (for signing - optional)
```bash
# Only needed if you want to sign and notarize the app
xcode-select --install
```

---

## 🚀 Quick Start

### Build for Your Current Platform

```bash
cd build
python build.py
```

That's it! The script will:
1. Check dependencies
2. Clean previous builds
3. Create icons (if missing)
4. Run PyInstaller
5. Create installer (Windows only, if Inno Setup installed)
6. Show summary of build outputs

### Build Output Locations

**Windows:**
- Executable: `../dist/SPAMURAI/SPAMURAI.exe`
- Installer: `../dist/SPAMURAI-Setup.exe`

**macOS:**
- Application: `../dist/SPAMURAI.app`

---

## 📁 Files in This Directory

### Build Scripts
- **`build.py`** - Main build script (cross-platform)
- **`spamurai.spec`** - PyInstaller configuration
- **`installer.iss`** - Inno Setup script (Windows installer)

### Icons (Optional)
- **`icon.ico`** - Windows icon (create your own or use default)
- **`icon.icns`** - macOS icon (create your own or use default)

---

## 🎨 Creating Custom Icons

### Windows (.ico)

Option 1: Use an online converter
1. Create a 256x256 PNG logo
2. Convert at [icoconvert.com](https://icoconvert.com/)
3. Save as `build/icon.ico`

Option 2: Use Pillow
```python
from PIL import Image
img = Image.open('logo.png')
img.save('build/icon.ico', format='ICO', sizes=[(256, 256)])
```

### macOS (.icns)

Option 1: Use online converter
1. Create a 1024x1024 PNG logo
2. Convert at [cloudconvert.com](https://cloudconvert.com/png-to-icns)
3. Save as `build/icon.icns`

Option 2: Use iconutil (macOS only)
```bash
# Create iconset directory
mkdir SPAMURAI.iconset

# Create multiple sizes (required)
sips -z 16 16     logo.png --out SPAMURAI.iconset/icon_16x16.png
sips -z 32 32     logo.png --out SPAMURAI.iconset/icon_16x16@2x.png
sips -z 32 32     logo.png --out SPAMURAI.iconset/icon_32x32.png
sips -z 64 64     logo.png --out SPAMURAI.iconset/icon_32x32@2x.png
sips -z 128 128   logo.png --out SPAMURAI.iconset/icon_128x128.png
sips -z 256 256   logo.png --out SPAMURAI.iconset/icon_128x128@2x.png
sips -z 256 256   logo.png --out SPAMURAI.iconset/icon_256x256.png
sips -z 512 512   logo.png --out SPAMURAI.iconset/icon_256x256@2x.png
sips -z 512 512   logo.png --out SPAMURAI.iconset/icon_512x512.png
sips -z 1024 1024 logo.png --out SPAMURAI.iconset/icon_512x512@2x.png

# Convert to .icns
iconutil -c icns SPAMURAI.iconset -o build/icon.icns
```

---

## 🔧 Advanced Configuration

### Customizing PyInstaller Build

Edit `spamurai.spec` to:
- Add/remove hidden imports
- Include additional data files
- Change executable name
- Modify bundle settings

### Customizing Windows Installer

Edit `installer.iss` to:
- Change installation directory
- Modify Start Menu shortcuts
- Add registry entries
- Include additional files
- Change installer appearance

---

## 🐛 Troubleshooting

### Build fails with "PyInstaller not found"
```bash
pip install pyinstaller
```

### Windows installer not created
1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php)
2. Or skip installer - executable is still built

### macOS "Developer cannot be verified" error
The app isn't signed. Users need to:
1. Right-click app → Open
2. Click "Open" in the dialog
3. Or go to System Preferences → Security & Privacy → Allow

To properly sign and notarize:
```bash
# Sign the app (requires Apple Developer account)
codesign --deep --force --sign "Developer ID Application: Your Name" dist/SPAMURAI.app

# Notarize (requires Apple Developer account)
xcrun notarytool submit dist/SPAMURAI.app.zip --apple-id your@email.com --password <app-specific-password> --team-id TEAMID
```

### Build is too large
Edit `spamurai.spec`:
- Add more items to `excludes` list
- Enable UPX compression (already enabled)
- Remove unused data files

### Streamlit doesn't work in built app
Check `hiddenimports` in `spamurai.spec` - you may need to add missing Streamlit submodules.

---

## 📦 Distribution

### Windows
Distribute `SPAMURAI-Setup.exe`:
- Users double-click to install
- Installer handles shortcuts and Start Menu
- Uninstaller automatically created

### macOS
Distribute `SPAMURAI.app`:
- Zip the .app: `cd dist && zip -r SPAMURAI.app.zip SPAMURAI.app`
- Users unzip and drag to Applications folder
- Or create a DMG for professional distribution

### Creating a DMG (macOS)
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "SPAMURAI" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "SPAMURAI.app" 200 190 \
  --hide-extension "SPAMURAI.app" \
  --app-drop-link 600 185 \
  "SPAMURAI-Installer.dmg" \
  "dist/SPAMURAI.app"
```

---

## 🔄 Clean Build

To start fresh:
```bash
# Remove all build artifacts
rm -rf ../dist ../build_temp __pycache__

# Run build again
python build.py
```

---

## 📝 Build Checklist

Before releasing:

- [ ] Update version number in:
  - [ ] `src/gui.py` (`__version__`)
  - [ ] `installer.iss` (`MyAppVersion`)
  - [ ] `spamurai.spec` (macOS `info_plist`)
- [ ] Create/update icons (`icon.ico`, `icon.icns`)
- [ ] Test on clean machine
- [ ] Run security scan on executables
- [ ] Create release notes
- [ ] Sign code (macOS/Windows)

---

## 🆘 Getting Help

- **PyInstaller docs:** https://pyinstaller.org/en/stable/
- **Inno Setup docs:** https://jrsoftware.org/ishelp/
- **GitHub Issues:** https://github.com/fawkess/wa_broadcaster/issues

---

*Built with ⚡ by the SPAMURAI team*
