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

echo This is how path looks:
echo %PATH%

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo X Streamlit not installed!
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Launch SPAMURAI GUI
echo Launching SPAMURAI GUI...
echo Your browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit
python -m streamlit run src\gui.py
