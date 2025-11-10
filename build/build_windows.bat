@echo off
REM SPAMURAI Windows Build Script
REM This script builds the Windows installer and portable ZIP

echo ====================================
echo SPAMURAI Windows Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Run the build script
echo.
echo Starting build process...
echo.
python build_windows.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Output files are in: build\dist\
echo.
pause
