@echo off
setlocal enabledelayedexpansion

REM Set error handling - exit on any error
set "SCRIPT_DIR=%~dp0"
set "SUCCESS=1"
set PYINSTALLER=C:\Data\Project\CICD\git\CDCC\SWF\Astree_KPI\Scripts\pyinstaller.exe

echo Starting build and deployment process...
echo.

REM Step 1: Run PyInstaller
echo [1/6] Running PyInstaller...
"%PYINSTALLER%" --onefile wa_broadcaster.py
if !errorlevel! neq 0 (
    echo ERROR: PyInstaller failed with error code !errorlevel!
    set "SUCCESS=0"
    goto :error
)
echo ✓ PyInstaller completed successfully

REM Step 2: Create releases directory if it doesn't exist
if not exist "releases" (
    echo [2/6] Creating releases directory...
    mkdir releases
    if !errorlevel! neq 0 (
        echo ERROR: Failed to create releases directory
        set "SUCCESS=0"
        goto :error
    )
) else (
    echo [2/6] Releases directory exists
)

REM Step 3: Copy executable to releases
echo [3/6] Copying executable to releases...
copy /Y "dist\wa_broadcaster.exe" "..\"
if !errorlevel! neq 0 (
    echo ERROR: Failed to copy executable
    set "SUCCESS=0"
    goto :error
)
echo ✓ Executable copied successfully


REM Step 5: Git operations
echo [5/6] Starting Git operations...

echo Pulling latest changes from main branch...
git pull origin main
if !errorlevel! neq 0 (
    echo WARNING: Git pull failed, but continuing...
)

echo Adding and committing changes...
git add -u
git commit -m "new release - %date% %time%"
if !errorlevel! neq 0 (
    echo ERROR: Git commit failed
    set "SUCCESS=0"
    goto :git_error
)

echo Pushing to remote repository...
git push origin main
if !errorlevel! neq 0 (
    echo ERROR: Git push failed
    set "SUCCESS=0"
    goto :git_error
)

echo ✓ Git operations completed successfully
cd ..

REM Step 6: Final status
echo [6/6] Build and deployment completed!
echo.
if !SUCCESS! equ 1 (
    echo ✓ SUCCESS: All operations completed successfully
) else (
    echo ✗ FAILURE: Some operations failed
)

goto :end

:git_error
cd ..
goto :error

:error
echo.
echo ✗ Script execution failed at step above
echo Please check the error message and try again

:end
echo.
echo Press any key to exit...
pause > nul