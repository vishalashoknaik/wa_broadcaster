@echo off
REM ============================================================================
REM SPAMURAI System Diagnostics - Windows
REM This script checks your system for all requirements and dependencies
REM ============================================================================

setlocal enabledelayedexpansion

REM Color codes (if terminal supports ANSI)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo ============================================================================
echo                    SPAMURAI SYSTEM DIAGNOSTICS
echo                           Windows Edition
echo ============================================================================
echo.
echo This diagnostic will check:
echo   1. Operating System Information
echo   2. Python Installation and Version
echo   3. pip Package Manager
echo   4. Required Python Packages
echo   5. Firebase Credentials (MANDATORY)
echo   6. Chrome Browser Installation
echo   7. ChromeDriver Status
echo   8. Environment Variables
echo   9. File Permissions
echo   10. Network Connectivity
echo.
echo Press any key to start diagnosis...
pause >nul
echo.

REM Create a log file
set "LOGFILE=%TEMP%\spamurai_diagnostics.log"
echo SPAMURAI Diagnostics - %DATE% %TIME% > "%LOGFILE%"
echo. >> "%LOGFILE%"

REM ============================================================================
REM STEP 1: Operating System Information
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 1/9] Operating System Information
echo ============================================================================
echo.

echo Checking Windows version...
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" >> "%LOGFILE%"

echo.
echo Checking system architecture...
wmic os get osarchitecture
wmic os get osarchitecture >> "%LOGFILE%"

echo.
echo [INFO] Windows architecture detected
echo.

REM ============================================================================
REM STEP 2: Python Installation
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 2/9] Python Installation
echo ============================================================================
echo.

set "PYTHON_FOUND=0"
set "PYTHON_VERSION="
set "PYTHON_PATH="

echo Checking for Python...
echo.

REM Check python command
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 'python' command found
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    for /f "tokens=*" %%i in ('where python 2^>nul') do set PYTHON_PATH=%%i
    echo     Version: !PYTHON_VERSION!
    echo     Path: !PYTHON_PATH!
    set "PYTHON_FOUND=1"
    set "PYTHON_CMD=python"
) else (
    echo [WARNING] 'python' command not found
)

echo.
echo Checking for Python 3...

REM Check python3 command
python3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 'python3' command found
    for /f "tokens=*" %%i in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%i
    for /f "tokens=*" %%i in ('where python3 2^>nul') do set PYTHON_PATH=%%i
    echo     Version: !PYTHON_VERSION!
    echo     Path: !PYTHON_PATH!
    set "PYTHON_FOUND=1"
    set "PYTHON_CMD=python3"
) else (
    echo [WARNING] 'python3' command not found
)

echo.
if !PYTHON_FOUND! EQU 0 (
    echo [ERROR] Python is NOT installed or not in PATH
    echo.
    echo FIX:
    echo   1. Download Python from: https://www.python.org/downloads/
    echo   2. During installation, CHECK "Add Python to PATH"
    echo   3. Restart command prompt after installation
    echo.
    echo PYTHON: NOT FOUND >> "%LOGFILE%"
    goto :CHECK_SUMMARY
) else (
    echo [OK] Python is installed and accessible
    echo PYTHON: !PYTHON_VERSION! at !PYTHON_PATH! >> "%LOGFILE%"
)

REM Check Python version (need 3.8+)
echo.
echo Verifying Python version (requires 3.8 or higher)...
%PYTHON_CMD% -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python version is 3.8 or higher
) else (
    echo [ERROR] Python version is too old (need 3.8+)
    echo     Current: !PYTHON_VERSION!
    echo.
    echo FIX: Upgrade Python from https://www.python.org/downloads/
)

REM ============================================================================
REM STEP 3: pip Package Manager
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 3/9] pip Package Manager
echo ============================================================================
echo.

set "PIP_FOUND=0"
set "PIP_VERSION="

echo Checking for pip...
echo.

REM Check pip command
pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 'pip' command found
    for /f "tokens=*" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
    echo     !PIP_VERSION!
    set "PIP_FOUND=1"
    set "PIP_CMD=pip"
) else (
    echo [WARNING] 'pip' command not found
)

echo.
REM Check pip3 command
pip3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] 'pip3' command found
    for /f "tokens=*" %%i in ('pip3 --version 2^>^&1') do set PIP_VERSION=%%i
    echo     !PIP_VERSION!
    set "PIP_FOUND=1"
    set "PIP_CMD=pip3"
) else (
    echo [WARNING] 'pip3' command not found
)

echo.
if !PIP_FOUND! EQU 0 (
    echo [ERROR] pip is NOT installed
    echo.
    echo FIX:
    echo   Run: %PYTHON_CMD% -m ensurepip --default-pip
    echo   Or: %PYTHON_CMD% -m pip install --upgrade pip
    echo.
    echo PIP: NOT FOUND >> "%LOGFILE%"
) else (
    echo [OK] pip is installed and accessible
    echo PIP: !PIP_VERSION! >> "%LOGFILE%"

    REM Check pip upgrade
    echo.
    echo Checking if pip needs upgrade...
    %PIP_CMD% list --outdated | findstr "pip" >nul
    if %ERRORLEVEL% EQU 0 (
        echo [INFO] pip has an update available
        echo     Run: %PYTHON_CMD% -m pip install --upgrade pip
    )
)

REM ============================================================================
REM STEP 4: Required Python Packages
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 4/9] Required Python Packages
echo ============================================================================
echo.

if !PIP_FOUND! EQU 0 (
    echo [SKIP] Cannot check packages without pip
    goto :SKIP_PACKAGES
)

echo Checking required packages...
echo.

set "MISSING_PACKAGES="

REM List of required packages
set "PACKAGES=selenium webdriver-manager pandas pyperclip openpyxl requests streamlit"

for %%P in (%PACKAGES%) do (
    echo Checking: %%P
    %PIP_CMD% show %%P >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        REM Get version
        for /f "tokens=2" %%v in ('%PIP_CMD% show %%P ^| findstr "Version:"') do (
            echo     [OK] %%P version %%v installed
            echo PACKAGE %%P: %%v >> "%LOGFILE%"
        )
    ) else (
        echo     [MISSING] %%P is NOT installed
        echo PACKAGE %%P: NOT INSTALLED >> "%LOGFILE%"
        set "MISSING_PACKAGES=!MISSING_PACKAGES! %%P"
    )
    echo.
)

if not "!MISSING_PACKAGES!"=="" (
    echo [ERROR] Some required packages are missing:!MISSING_PACKAGES!
    echo.
    echo FIX:
    echo   Run: %PIP_CMD% install!MISSING_PACKAGES!
    echo   Or: %PIP_CMD% install -r requirements.txt
    echo.
) else (
    echo [OK] All required packages are installed
)

:SKIP_PACKAGES

REM ============================================================================
REM STEP 5: Firebase Credentials (MANDATORY)
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 5/10] Firebase Credentials (MANDATORY)
echo ============================================================================
echo.

set "FIREBASE_READY=0"

echo Checking Firebase credentials...
echo.

REM Check environment variable
if defined FIREBASE_CREDENTIALS (
    echo [OK] FIREBASE_CREDENTIALS environment variable is set

    REM Validate JSON
    python -c "import json, os; json.loads(os.environ['FIREBASE_CREDENTIALS'])" 2>nul
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Credentials JSON is valid
        set "FIREBASE_READY=1"
        echo FIREBASE: Environment variable (valid^) >> "%LOGFILE%"
    ) else (
        echo [ERROR] FIREBASE_CREDENTIALS contains invalid JSON
        echo FIREBASE: Environment variable (INVALID JSON^) >> "%LOGFILE%"
        set /a ISSUES_FOUND+=1
    )
) else (
    echo [WARNING] FIREBASE_CREDENTIALS environment variable not set
)

echo.

REM Check credentials file
if exist "config\firebase-credentials.json" (
    echo [OK] Credentials file found at: config\firebase-credentials.json

    REM Validate JSON
    python -c "import json; json.load(open('config/firebase-credentials.json'))" 2>nul
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Credentials file JSON is valid
        if "!FIREBASE_READY!"=="0" (
            set "FIREBASE_READY=1"
            echo FIREBASE: File-based (valid^) >> "%LOGFILE%"
        )
    ) else (
        echo [ERROR] Credentials file contains invalid JSON
        echo FIREBASE: File-based (INVALID JSON^) >> "%LOGFILE%"
        set /a ISSUES_FOUND+=1
    )
) else (
    echo [WARNING] No credentials file at: config\firebase-credentials.json
)

echo.

if "!FIREBASE_READY!"=="0" (
    echo [ERROR] Firebase credentials NOT configured!
    echo.
    echo Firebase is MANDATORY for SPAMURAI to function.
    echo.
    echo FIX:
    echo   1. Get Firebase credentials from:
    echo      https://console.firebase.google.com/
    echo      Project Settings -^> Service Accounts -^> Generate New Private Key
    echo.
    echo   2. Run setup script:
    echo      setup_firebase.bat C:\path\to\credentials.json
    echo.
    echo   3. Re-run this diagnostic
    echo.
    echo FIREBASE: NOT CONFIGURED >> "%LOGFILE%"
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] Firebase credentials are properly configured

    REM Test Firebase connection if firebase-admin is installed
    %PIP_CMD% show firebase-admin >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo.
        echo Testing Firebase connection...
        python test_firebase.py 2>&1 | findstr "Firebase enabled mode works" >nul
        if !ERRORLEVEL! EQU 0 (
            echo [OK] Firebase connection successful
        ) else (
            echo [WARNING] Could not verify Firebase connection
            echo     Make sure Firebase is enabled in config.json
        )
    )
)

REM ============================================================================
REM STEP 6: Chrome Browser
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 6/10] Chrome Browser Installation
echo ============================================================================
echo.

set "CHROME_FOUND=0"

echo Checking for Google Chrome...
echo.

REM Check common Chrome installation paths
set "CHROME_PATHS=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "CHROME_PATHS=!CHROME_PATHS! C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
set "CHROME_PATHS=!CHROME_PATHS! %LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

for %%P in (!CHROME_PATHS!) do (
    if exist "%%P" (
        echo [OK] Chrome found at: %%P

        REM Get Chrome version
        for /f "tokens=*" %%v in ('wmic datafile where name^="%%P" get Version ^| findstr /r "[0-9]"') do (
            echo     Version: %%v
            echo CHROME: %%v at %%P >> "%LOGFILE%"
        )

        set "CHROME_FOUND=1"
        goto :CHROME_DONE
    )
)

:CHROME_DONE
echo.
if !CHROME_FOUND! EQU 0 (
    echo [ERROR] Google Chrome is NOT installed
    echo.
    echo FIX:
    echo   Download Chrome from: https://www.google.com/chrome/
    echo.
    echo CHROME: NOT FOUND >> "%LOGFILE%"
) else (
    echo [OK] Google Chrome is installed
)

REM ============================================================================
REM STEP 7: ChromeDriver
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 7/10] ChromeDriver Status
echo ============================================================================
echo.

echo Checking ChromeDriver...
echo.

if !PYTHON_FOUND! EQU 0 (
    echo [SKIP] Cannot check ChromeDriver without Python
    goto :SKIP_CHROMEDRIVER
)

echo [INFO] ChromeDriver is managed by webdriver-manager
echo [INFO] It will auto-download when first running SPAMURAI
echo.

REM Check if webdriver-manager is installed
%PIP_CMD% show webdriver-manager >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo [OK] webdriver-manager is installed
    echo     ChromeDriver will be automatically downloaded on first run
) else (
    echo [WARNING] webdriver-manager is not installed
    echo     Install with: %PIP_CMD% install webdriver-manager
)

:SKIP_CHROMEDRIVER

REM ============================================================================
REM STEP 8: Environment Variables
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 8/10] Environment Variables
echo ============================================================================
echo.

echo Checking PATH variable...
echo.

echo [INFO] Your PATH includes:
echo %PATH% | findstr /i "python"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python directory is in PATH
) else (
    echo [WARNING] Python directory may not be in PATH
)

echo.
echo [INFO] Full PATH variable logged to: %LOGFILE%
echo PATH: %PATH% >> "%LOGFILE%"

REM ============================================================================
REM STEP 9: File Permissions
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 9/10] File Permissions
echo ============================================================================
echo.

echo Checking write permissions...
echo.

REM Test write to temp folder
echo test > "%TEMP%\spamurai_test.txt" 2>nul
if exist "%TEMP%\spamurai_test.txt" (
    echo [OK] Can write to temporary directory
    del "%TEMP%\spamurai_test.txt" >nul 2>&1
) else (
    echo [ERROR] Cannot write to temporary directory
    echo     This may cause issues with ChromeDriver
)

echo.
REM Test write to current directory
echo test > "spamurai_test.txt" 2>nul
if exist "spamurai_test.txt" (
    echo [OK] Can write to current directory
    del "spamurai_test.txt" >nul 2>&1
) else (
    echo [ERROR] Cannot write to current directory
    echo     Try running from a different location or as Administrator
)

REM ============================================================================
REM STEP 10: Network Connectivity
REM ============================================================================
echo.
echo ============================================================================
echo [STEP 10/10] Network Connectivity
echo ============================================================================
echo.

echo Checking internet connection...
echo.

ping -n 1 google.com >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Internet connection is working
    echo NETWORK: OK >> "%LOGFILE%"
) else (
    echo [WARNING] Cannot reach google.com
    echo     Check your internet connection
    echo     SPAMURAI requires internet for WhatsApp Web
    echo NETWORK: ISSUE >> "%LOGFILE%"
)

echo.
echo Checking HTTPS connectivity...
ping -n 1 web.whatsapp.com >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Can reach web.whatsapp.com
) else (
    echo [WARNING] Cannot reach web.whatsapp.com
    echo     Check firewall settings
)

REM ============================================================================
REM SUMMARY
REM ============================================================================
:CHECK_SUMMARY
echo.
echo.
echo ============================================================================
echo                           DIAGNOSTIC SUMMARY
echo ============================================================================
echo.

set "ISSUES_FOUND=0"

if !PYTHON_FOUND! EQU 0 (
    echo [ERROR] Python NOT installed
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] Python installed
)

if !PIP_FOUND! EQU 0 (
    echo [ERROR] pip NOT installed
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] pip installed
)

if not "!MISSING_PACKAGES!"=="" (
    echo [ERROR] Missing Python packages
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] All packages installed
)

if !CHROME_FOUND! EQU 0 (
    echo [ERROR] Chrome NOT installed
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] Chrome installed
)

if "!FIREBASE_READY!"=="0" (
    echo [ERROR] Firebase NOT configured
    set /a ISSUES_FOUND+=1
) else (
    echo [OK] Firebase configured
)

echo.
echo ============================================================================

if !ISSUES_FOUND! EQU 0 (
    echo.
    echo     [SUCCESS] Your system is ready for SPAMURAI!
    echo.
    echo Next steps:
    echo   1. Run: streamlit run src/gui.py
    echo   2. Or use the launcher: SPAMURAI.bat
    echo.
) else (
    echo.
    echo     [ISSUES FOUND] !ISSUES_FOUND! issue(s) need to be fixed
    echo.
    echo Please fix the issues listed above and run this diagnostic again.
    echo.
    if not "!MISSING_PACKAGES!"=="" (
        echo Quick fix for packages:
        echo   %PIP_CMD% install!MISSING_PACKAGES!
        echo.
    )
)

echo Full diagnostic log saved to: %LOGFILE%
echo.
echo ============================================================================
echo.

pause
