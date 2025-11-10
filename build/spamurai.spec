# -*- mode: python ; coding: utf-8 -*-
"""
SPAMURAI PyInstaller Specification File
Builds standalone executable for Windows and macOS
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all Streamlit data files
streamlit_data = collect_data_files('streamlit')
streamlit_submodules = collect_submodules('streamlit')

# Collect all necessary packages
altair_data = collect_data_files('altair')
plotly_data = collect_data_files('plotly')

block_cipher = None

a = Analysis(
    ['../src/gui.py'],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../src/*.py', 'src'),
        ('../requirements.txt', '.'),
        ('../config.example.json', '.'),
        ('../GOOGLE_SHEETS_SETUP.md', '.'),
        ('../COMBINATION_SUMMARY_EXAMPLE.md', '.'),
    ] + streamlit_data + altair_data + plotly_data,
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
            'CFBundleShortVersionString': '1.9.0',
            'CFBundleVersion': '1.9.0',
            'LSMinimumSystemVersion': '10.13',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
        },
    )
