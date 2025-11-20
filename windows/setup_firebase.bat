@echo off
REM Firebase Credentials Setup Script for SPAMURAI (Windows)
REM Automatically configures Firebase credentials as environment variable

setlocal enabledelayedexpansion

echo.
echo Firebase Credentials Setup for SPAMURAI
echo ==========================================
echo.

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

REM Check if file contains wildcard, try to expand it
echo %CREDS_FILE% | findstr /C:"*" >nul
if not errorlevel 1 (
    echo Expanding wildcard pattern: %CREDS_FILE%
    echo.

    REM Try to find matching files
    set FOUND_FILE=
    set FILE_COUNT=0
    for %%F in (%CREDS_FILE%) do (
        set /a FILE_COUNT+=1
        set FOUND_FILE=%%F
        echo Found: %%F
    )

    if !FILE_COUNT! EQU 0 (
        echo Error: No files match pattern: %CREDS_FILE%
        echo.
        exit /b 1
    )

    if !FILE_COUNT! GTR 1 (
        echo.
        echo Error: Multiple files found. Please specify exact file.
        echo.
        exit /b 1
    )

    echo.
    echo Using: !FOUND_FILE!
    echo.
    set CREDS_FILE=!FOUND_FILE!
)

REM Check if file exists
if not exist "%CREDS_FILE%" (
    echo Error: File not found: %CREDS_FILE%
    echo.
    echo Please provide the exact file path, for example:
    echo   %~nx0 "C:\Users\YourName\Downloads\spamurai-15b49-firebase-adminsdk-fbsvc-3194c88bcf.json"
    echo.
    exit /b 1
)

echo [OK] File found: %CREDS_FILE%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Warning: Python not found in PATH. Skipping JSON validation.
    echo.
) else (
    REM Read JSON content (basic validation)
    echo Validating JSON format...
    python -c "import json; json.load(open(r'%CREDS_FILE%'))"
    if errorlevel 1 (
        echo.
        echo Error: Invalid JSON file or failed to read file
        echo.
        echo Troubleshooting:
        echo   1. Make sure the file is a valid JSON file
        echo   2. Try enclosing the path in quotes if it contains spaces
        echo   3. Check if the file is corrupted
        echo.
        echo File being validated: %CREDS_FILE%
        echo.
        pause
        exit /b 1
    )
    echo [OK] JSON format is valid
    echo.
)

REM Read file content into variable (escape quotes)
set CREDS_JSON=
for /f "usebackq delims=" %%i in ("%CREDS_FILE%") do (
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
