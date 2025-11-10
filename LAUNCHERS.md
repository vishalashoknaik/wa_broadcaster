# SPAMURAI Launcher System

Complete hybrid launcher system for SPAMURAI - making it simple for everyone to run the application.

---

## 🎯 Two-Phase Approach

### Phase 1: Quick Launchers ✅ COMPLETE
**Location:** `launchers/`

Simple double-click scripts that handle everything:
- ✅ Python installation check
- ✅ Automatic virtual environment setup
- ✅ Dependency auto-install
- ✅ GUI launch

**Files:**
- `launchers/SPAMURAI.bat` - Windows
- `launchers/SPAMURAI.command` - macOS
- `launchers/README.md` - User instructions

### Phase 2: Native Installers ✅ COMPLETE
**Location:** `build/`

Professional installer packages:
- 📦 Windows: `SPAMURAI-Setup.exe` with Install Wizard
- 📦 macOS: `SPAMURAI.app` application bundle

**Files:**
- `build/build.py` - Automated build script
- `build/spamurai.spec` - PyInstaller configuration
- `build/installer.iss` - Windows installer config
- `build/README.md` - Build instructions

---

## 🚀 For End Users

### Windows Users

**Option A: Quick Launcher** (Developers)
1. Download repository
2. Double-click `launchers/SPAMURAI.bat`
3. Wait for first-run setup
4. GUI opens automatically

**Option B: Installer** (Recommended)
1. Download `SPAMURAI-Setup.exe`
2. Run installer wizard
3. Click desktop shortcut or Start Menu
4. Done!

### macOS Users

**Option A: Quick Launcher** (Developers)
1. Download repository
2. Double-click `launchers/SPAMURAI.command`
3. Wait for first-run setup
4. GUI opens automatically

**Option B: Application Bundle** (Recommended)
1. Download `SPAMURAI.app.zip`
2. Unzip and drag to Applications folder
3. Double-click to launch
4. Done!

### Linux Users

Use the original shell script:
```bash
./start_spamurai.sh
```

---

## 🛠️ For Developers

### Testing Quick Launchers

**Windows:**
```cmd
cd wa_broadcaster\launchers
SPAMURAI.bat
```

**macOS:**
```bash
cd wa_broadcaster/launchers
./SPAMURAI.command
```

### Building Native Installers

```bash
# Install PyInstaller
pip install pyinstaller

# Build for your platform
cd build
python build.py

# Output in ../dist/
```

See `build/README.md` for detailed build instructions.

---

## 📋 Feature Comparison

| Feature | Quick Launchers | Native Installers |
|---------|----------------|-------------------|
| **Setup Time** | 2-5 min first run | One-time install |
| **File Size** | Small (~50KB scripts) | Large (~200MB+) |
| **Requirements** | Python installed | Everything bundled |
| **Updates** | git pull | Download new installer |
| **Portability** | Needs Python | Self-contained |
| **Best For** | Developers | End users |

---

## 🎨 Customization

### Adding Custom Icons

**Windows (.ico):**
1. Create 256x256 PNG logo
2. Convert to .ico: https://icoconvert.com/
3. Save as `build/icon.ico`
4. Rebuild

**macOS (.icns):**
1. Create 1024x1024 PNG logo
2. Convert to .icns: https://cloudconvert.com/png-to-icns
3. Save as `build/icon.icns`
4. Rebuild

### Modifying Launcher Behavior

Edit the launcher scripts directly:
- `launchers/SPAMURAI.bat` - Windows behavior
- `launchers/SPAMURAI.command` - macOS behavior

### Changing Build Configuration

Edit build files:
- `build/spamurai.spec` - PyInstaller settings
- `build/installer.iss` - Windows installer wizard
- `build/build.py` - Build process

---

## 🔧 Technical Details

### Quick Launchers

**How they work:**
1. Detect Python installation
2. Create `venv/` directory in project root
3. Activate virtual environment
4. Run `pip install -r requirements.txt` (if needed)
5. Execute `python -m streamlit run src/gui.py`

**Benefits:**
- No compilation needed
- Easy to modify
- Small file size
- Updates via git pull

### Native Installers

**Windows Build Process:**
1. PyInstaller bundles Python + all dependencies
2. Creates standalone executable in `dist/SPAMURAI/`
3. Inno Setup packages into installer wizard
4. Output: `SPAMURAI-Setup.exe`

**macOS Build Process:**
1. PyInstaller bundles Python + all dependencies
2. Creates `.app` bundle with proper structure
3. Optional: Sign and notarize for Gatekeeper
4. Optional: Create DMG for distribution

**Benefits:**
- No Python installation required
- Professional appearance
- Single-file distribution
- Start Menu/Applications folder integration

---

## 📦 Distribution

### Quick Launchers
- Commit to repository
- Users clone/download repo
- Double-click to run

### Native Installers

**Windows:**
- Upload `SPAMURAI-Setup.exe` to GitHub Releases
- Users download and install
- Automatic updates via new releases

**macOS:**
- Zip the .app: `zip -r SPAMURAI.app.zip SPAMURAI.app`
- Upload to GitHub Releases
- Or create DMG for professional feel

---

## 🐛 Troubleshooting

### Quick Launchers

**"Python not found"**
- Install Python 3.8+: https://www.python.org/downloads/
- Check "Add to PATH" during installation (Windows)
- Restart terminal/computer

**"Permission denied" (macOS)**
```bash
chmod +x launchers/SPAMURAI.command
```

**Dependencies fail to install**
- Check internet connection
- Try manual install:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Native Installers

**Windows "SmartScreen" warning**
- App isn't code-signed (requires certificate)
- Click "More info" → "Run anyway"
- Or sign the executable

**macOS "Developer cannot be verified"**
- Right-click app → Open
- Click "Open" in dialog
- Or sign and notarize the app

**Build fails**
- Install PyInstaller: `pip install pyinstaller`
- Check `build/README.md` for detailed troubleshooting

---

## 📝 Maintenance Checklist

When releasing a new version:

- [ ] Update version in `src/gui.py`
- [ ] Update version in `build/installer.iss`
- [ ] Update version in `build/spamurai.spec`
- [ ] Test quick launchers on both platforms
- [ ] Rebuild native installers
- [ ] Test installers on clean machines
- [ ] Create release notes
- [ ] Tag release in git
- [ ] Upload to GitHub Releases

---

## 🎯 Future Enhancements

Potential improvements:
- [ ] Auto-update mechanism
- [ ] Linux .deb and .rpm packages
- [ ] Code signing for Windows/macOS
- [ ] Animated splash screen
- [ ] System tray integration
- [ ] Installer language options

---

## 📚 Related Documentation

- **Quick Launcher Guide:** `launchers/README.md`
- **Build System Guide:** `build/README.md`
- **Main README:** `README.md`
- **Google Sheets Setup:** `GOOGLE_SHEETS_SETUP.md`

---

*Built with ⚡ by the SPAMURAI team*
