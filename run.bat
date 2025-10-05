@echo off
set GIT_EXE=%CD%\..\PortableGit\bin\git.exe
%GIT_EXE% pull origin master

@echo off
setlocal

wa_broadcaster_execute.bat
pause