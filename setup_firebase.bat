@echo off
REM Firebase Credentials Setup Script for SPAMURAI (Windows)
REM Automatically configures Firebase credentials as environment variable

setlocal enabledelayedexpansion

echo.
echo Firebase Credentials Setup for SPAMURAI
echo ==========================================
echo.

set PATH=..\python_311_spamurai;..\python_311_spamurai\Scripts;%PATH%

REM Check if credentials file path is provided
if "%~1"=="" (
    echo Error: Please provide path to Firebase credentials JSON file
    echo.
    echo Usage: %~nx0 path\to\firebase-credentials.json
    echo.
    echo Example:
    echo   %~nx0 C:\Users\YourName\Downloads\spamurai-firebase-xxxxx.json
    echo.
    exit /b 1
)

set CREDS_FILE=%~1

REM Check if file exists
if not exist "%CREDS_FILE%" (
    echo Error: File not found: %CREDS_FILE%
    exit /b 1
)

echo [OK] Valid Firebase credentials file found
echo.

REM Read JSON content (basic validation)
echo %CREDS_FILE%
python -c "import json; json.load(open(r'%CREDS_FILE%'))" 2>nul
if errorlevel 1 (
    echo Error: Invalid JSON file
    exit /b 1
)

REM Read file content into variable (escape quotes)
set CREDS_JSON=
for /f "delims=" %%i in (%CREDS_FILE%) do (
    set "line=%%i"
    set "line=!line:"=\"!"
    set "CREDS_JSON=!CREDS_JSON!!line!"
)

echo Setting environment variable...
echo.

REM Set system environment variable (requires admin)
setx FIREBASE_CREDENTIALS "%CREDS_JSON%" >nul 2>&1
if errorlevel 1 (
    echo Warning: Could not set system-wide environment variable
    echo Try running as Administrator for system-wide setup
    echo.
    echo Setting for current user only...
    setx FIREBASE_CREDENTIALS "%CREDS_JSON%" /M >nul 2>&1
)

echo [OK] FIREBASE_CREDENTIALS environment variable set
echo.

echo ==========================================
echo Setup complete!
echo.
echo Next steps:
echo   1. RESTART your terminal/command prompt
echo   2. Enable Firebase in config.json:
echo      "firebase_config": { "enabled": true }
echo   3. Run SPAMURAI - it will use environment variable automatically
echo.
echo Note: All SPAMURAI installations on this machine will use these credentials.
echo.

pause
