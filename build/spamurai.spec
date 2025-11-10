# -*- mode: python ; coding: utf-8 -*-
"""
SPAMURAI PyInstaller Specification File
Builds standalone executable for Windows and macOS
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# Collect all Streamlit data files and metadata
streamlit_data = collect_data_files('streamlit')
streamlit_submodules = collect_submodules('streamlit')
streamlit_metadata = copy_metadata('streamlit')

# Helper function to safely copy metadata
def safe_copy_metadata(package_name):
    try:
        return copy_metadata(package_name)
    except:
        return []

# Collect all necessary packages with metadata
altair_data = collect_data_files('altair')
altair_metadata = safe_copy_metadata('altair')
plotly_data = []  # Not using plotly in this build
plotly_metadata = []

# Additional metadata for dependencies
additional_metadata = (
    safe_copy_metadata('click') +
    safe_copy_metadata('tornado') +
    safe_copy_metadata('pyarrow') +
    safe_copy_metadata('packaging') +
    safe_copy_metadata('pandas') +
    safe_copy_metadata('selenium') +
    safe_copy_metadata('requests')
)

block_cipher = None

a = Analysis(
    ['../src/launcher.py'],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../src/gui.py', '.'),  # gui.py at root level for launcher
        ('../src/*.py', 'src'),  # Other Python files in src/
        ('../requirements.txt', '.'),
        ('../config.example.json', '.'),
        ('../GOOGLE_SHEETS_SETUP.md', '.'),
        ('../COMBINATION_SUMMARY_EXAMPLE.md', '.'),
    ] + streamlit_data + streamlit_metadata + altair_data + altair_metadata + plotly_data + plotly_metadata + additional_metadata,
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.chrome.options',
        'webdriver_manager',
        'webdriver_manager.chrome',
        'pandas',
        'pyperclip',
        'openpyxl',
        'requests',
        'google',
        'google.auth',
        'google.oauth2',
        'googleapiclient',
        'googleapiclient.discovery',
        'googleapiclient.errors',
        'altair',
        'plotly',
        'click',
        'tornado',
        'validators',
        'watchdog',
        'cachetools',
        'gitpython',
        'packaging',
        'toml',
        'pyarrow',
    ] + streamlit_submodules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'numpy.distutils',
        'PIL.ImageQt',
        'PyQt5',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SPAMURAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for Streamlit output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if sys.platform == 'win32' else 'icon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SPAMURAI',
)

# For macOS, create a .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='SPAMURAI.app',
        icon='icon.icns',
        bundle_identifier='com.spamurai.app',
        info_plist={
            'CFBundleName': 'SPAMURAI',
            'CFBundleDisplayName': 'SPAMURAI',
            'CFBundleShortVersionString': '1.10.0',
            'CFBundleVersion': '1.10.0',
            'LSMinimumSystemVersion': '10.13',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
        },
    )
