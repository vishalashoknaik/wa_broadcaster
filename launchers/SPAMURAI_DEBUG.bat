@echo off
REM ============================================================================
REM SPAMURAI Launcher with Debug Mode - Windows
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo                        SPAMURAI DEBUG LAUNCHER
echo ============================================================================
echo.

REM Check if running in debug mode
set "DEBUG_MODE=1"

echo [DEBUG] Starting SPAMURAI with verbose logging
echo [DEBUG] Working directory: %CD%
echo [DEBUG] Date/Time: %DATE% %TIME%
echo.

REM ============================================================================
REM Step 1: Check Python
REM ============================================================================
echo [DEBUG] Checking Python installation...

set "PYTHON_CMD="

REM Try python3 first
python3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python3"
    echo [DEBUG] Found python3
    for /f "tokens=*" %%i in ('python3 --version') do echo [DEBUG] Version: %%i
    goto :PYTHON_FOUND
)

REM Try python
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
    echo [DEBUG] Found python
    for /f "tokens=*" %%i in ('python --version') do echo [DEBUG] Version: %%i
    goto :PYTHON_FOUND
)

REM Python not found
echo [ERROR] Python not found!
echo.
echo Please run the diagnostic first:
echo   diagnose_windows.bat
echo.
pause
exit /b 1

:PYTHON_FOUND
echo [DEBUG] Python command: !PYTHON_CMD!
echo.

REM ============================================================================
REM Step 2: Check pip
REM ============================================================================
echo [DEBUG] Checking pip installation...

set "PIP_CMD="

REM Try pip3 first
pip3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PIP_CMD=pip3"
    echo [DEBUG] Found pip3
    goto :PIP_FOUND
)

REM Try pip
pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PIP_CMD=pip"
    echo [DEBUG] Found pip
    goto :PIP_FOUND
)

echo [ERROR] pip not found!
echo.
pause
exit /b 1

:PIP_FOUND
echo [DEBUG] pip command: !PIP_CMD!
echo.

REM ============================================================================
REM Step 3: Check required packages
REM ============================================================================
echo [DEBUG] Checking required packages...
echo.

set "MISSING="
set "PACKAGES=selenium webdriver-manager pandas pyperclip openpyxl requests streamlit"

for %%P in (%PACKAGES%) do (
    !PIP_CMD! show %%P >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [DEBUG] %%P: INSTALLED
    ) else (
        echo [ERROR] %%P: MISSING
        set "MISSING=!MISSING! %%P"
    )
)

if not "!MISSING!"=="" (
    echo.
    echo [ERROR] Missing packages:!MISSING!
    echo.
    echo Do you want to install them now? (Y/N)
    choice /C YN /N
    if !ERRORLEVEL! EQU 1 (
        echo.
        echo [DEBUG] Installing packages...
        !PIP_CMD! install!MISSING!

        if !ERRORLEVEL! EQU 0 (
            echo [DEBUG] Packages installed successfully
        ) else (
            echo [ERROR] Package installation failed
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Installation cancelled. Cannot proceed without required packages.
        pause
        exit /b 1
    )
)

echo.
echo [DEBUG] All packages installed
echo.

REM ============================================================================
REM Step 4: Check Chrome
REM ============================================================================
echo [DEBUG] Checking Chrome installation...

set "CHROME_PATHS=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "CHROME_PATHS=!CHROME_PATHS!;C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
set "CHROME_PATHS=!CHROME_PATHS!;%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

set "CHROME_FOUND=0"
for %%P in (!CHROME_PATHS!) do (
    if exist "%%P" (
        echo [DEBUG] Chrome found: %%P
        set "CHROME_FOUND=1"
        goto :CHROME_DONE
    )
)

:CHROME_DONE
if !CHROME_FOUND! EQU 0 (
    echo [WARNING] Chrome not found
    echo [INFO] Chrome will be needed for WhatsApp Web
)

echo.

REM ============================================================================
REM Step 5: Check src/gui.py exists
REM ============================================================================
echo [DEBUG] Checking application files...

if exist "src\gui.py" (
    echo [DEBUG] Found src\gui.py
) else (
    echo [ERROR] src\gui.py not found
    echo [DEBUG] Current directory: %CD%
    echo [DEBUG] Expected: %CD%\src\gui.py
    echo.
    echo Make sure you're running from the wa_broadcaster directory
    pause
    exit /b 1
)

echo.

REM ============================================================================
REM Step 6: Set Python path to unbuffered for real-time output
REM ============================================================================
set PYTHONUNBUFFERED=1

REM ============================================================================
REM Step 7: Launch Streamlit
REM ============================================================================
echo [DEBUG] Launching SPAMURAI...
echo [DEBUG] Command: !PYTHON_CMD! -m streamlit run src\gui.py
echo.
echo ============================================================================
echo                         SPAMURAI IS STARTING
echo ============================================================================
echo.
echo [INFO] Browser should open automatically to: http://localhost:8501
echo [INFO] If not, manually open: http://localhost:8501
echo.
echo [INFO] To stop SPAMURAI, press Ctrl+C in this window
echo.
echo ============================================================================
echo.

REM Run with full output
!PYTHON_CMD! -m streamlit run src\gui.py

REM Capture exit code
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ============================================================================
echo [DEBUG] SPAMURAI exited with code: %EXIT_CODE%
echo ============================================================================
echo.

if %EXIT_CODE% NEQ 0 (
    echo [ERROR] SPAMURAI exited with an error
    echo.
    echo Common issues:
    echo   - Port 8501 already in use
    echo   - Missing Python packages
    echo   - Incorrect file paths
    echo.
    echo Run diagnose_windows.bat for full system check
    echo.
)

pause
