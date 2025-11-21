@echo off
REM #############################################
REM SPAMURAI GUI Launcher
REM Strike fast. Strike precise. Leave no trace.
REM #############################################

echo.
echo SPAMURAI - WhatsApp Broadcast Ninja
echo ======================================
echo.

set PATH=..\python_311_spamurai;..\python_311_spamurai\Scripts;%PATH%


..\PortableGit\bin\git pull

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to the project directory
cd /d "%SCRIPT_DIR%"

REM Check if streamlit is installed
echo Using python installation from
where python

python -m pip install -r requirements.txt

echo This is how path looks:
echo %PATH%


python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo X Streamlit not installed!
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    pause
)

cls

REM Check if Firebase credentials need setup (do this right after dependencies)
REM We need setup if EITHER:
REM   1. firebase.json doesn't exist, OR
REM   2. config.json doesn't have firebase_config section

set NEEDS_FIREBASE_SETUP=false
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%

REM Check if firebase.json exists
if not exist "%PROJECT_DIR%config\firebase.json" (
    if not exist "%PROJECT_DIR%config\firebase-credentials.json" (
        if not defined FIREBASE_CREDENTIALS (
            set NEEDS_FIREBASE_SETUP=true
        )
    )
)

REM Check if config.json has firebase_config section
if exist "%PROJECT_DIR%config.json" (
    for /f "delims=" %%i in ('python -c "import json; config = json.load(open('config.json')); print('yes' if 'firebase_config' in config else 'no')" 2^>nul') do set HAS_FIREBASE_CONFIG=%%i
    if "!HAS_FIREBASE_CONFIG!" == "no" set NEEDS_FIREBASE_SETUP=true
    if "!HAS_FIREBASE_CONFIG!" == "" set NEEDS_FIREBASE_SETUP=true
) else (
    REM config.json doesn't exist - will need Firebase setup
    set NEEDS_FIREBASE_SETUP=true
)

if "!NEEDS_FIREBASE_SETUP!" == "true" (
    echo [Firebase Setup] Starting Firebase credentials setup...
    echo.
    echo [NOTICE] Firebase configuration incomplete. Starting automatic setup...
    echo.

    REM Run automated Firebase setup
    python src\firebase_auto_setup.py

    if errorlevel 1 (
        echo.
        echo [ERROR] Firebase setup failed or was cancelled.
        echo.
        echo Please contact your POC if you need assistance.
        echo.
        pause
        exit /b 1
    )

    REM Verify credentials were created and config updated
    if exist "%PROJECT_DIR%config\firebase.json" (
        echo [OK] Firebase credentials configured successfully
        echo.
    ) else (
        echo [ERROR] Setup completed but credentials file not found!
        echo.
        pause
        exit /b 1
    )
)

REM Launch SPAMURAI GUI
echo Launching SPAMURAI GUI...
echo Your browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit
python -m streamlit run src\gui.py
