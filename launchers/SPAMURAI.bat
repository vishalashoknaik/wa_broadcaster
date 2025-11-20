@echo off
REM ============================================================================
REM SPAMURAI - WhatsApp Broadcast Ninja
REM Strike fast. Strike precise. Leave no trace.
REM ============================================================================

title SPAMURAI Launcher

REM Colors using Windows escape sequences (Windows 10+)
REM If colors don't work on older Windows, they'll just be ignored

echo.
echo =========================================
echo   SPAMURAI - WhatsApp Broadcast Ninja
echo   Strike fast. Strike precise.
echo =========================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

REM Change to the project directory
cd /d "%PROJECT_DIR%"

echo [Step 1/5] Checking Python installation...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected
echo.

echo [Step 2/5] Setting up virtual environment...
echo.

REM Virtual environment path
set "VENV_DIR=%PROJECT_DIR%\venv"

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

echo [Step 3/5] Activating virtual environment...
echo.

REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [Step 4/5] Checking dependencies...
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Streamlit not found. Installing dependencies...
    echo This may take a few minutes...
    echo.

    pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt

    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        echo.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] All dependencies are installed
)
echo.

echo [Step 5/6] Checking Firebase credentials...
echo.

set "FIREBASE_READY=0"

REM Check if environment variable is set
if defined FIREBASE_CREDENTIALS (
    echo [OK] Firebase credentials found in environment variable
    set "FIREBASE_READY=1"
) else (
    REM Check if credentials file exists
    if exist "%PROJECT_DIR%\config\firebase-credentials.json" (
        echo [OK] Firebase credentials file found
        set "FIREBASE_READY=1"
    )
)

if "%FIREBASE_READY%"=="0" (
    echo [ERROR] Firebase credentials not configured!
    echo.
    echo Firebase is required for SPAMURAI to function.
    echo.
    echo Please follow these steps:
    echo   1. Get your Firebase credentials JSON file from:
    echo      https://console.firebase.google.com/
    echo      Project Settings -^> Service Accounts -^> Generate New Private Key
    echo.
    echo   2. Run the Firebase setup script:
    echo      setup_firebase.bat C:\path\to\your-credentials.json
    echo.
    echo   3. Restart this launcher
    echo.
    echo See FIREBASE_SETUP.md for detailed instructions.
    echo.
    pause
    exit /b 1
)
echo.

echo [Step 6/6] Launching SPAMURAI GUI...
echo.
echo =========================================
echo   GUI will open in your browser
echo   URL: http://localhost:8501
echo =========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Launch Streamlit
python -m streamlit run src/gui.py

REM If streamlit exits, pause to show any error messages
if errorlevel 1 (
    echo.
    echo [ERROR] SPAMURAI encountered an error!
    echo.
    pause
)
