; SPAMURAI Inno Setup Script
; Creates professional Windows installer
; Requires Inno Setup 6.0 or later: https://jrsoftware.org/isdl.php

#define MyAppName "SPAMURAI"
#define MyAppVersion "1.9.0"
#define MyAppPublisher "SPAMURAI Team"
#define MyAppURL "https://github.com/fawkess/wa_broadcaster"
#define MyAppExeName "SPAMURAI.exe"

[Setup]
; Basic app info
AppId={{A1B2C3D4-E5F6-7G8H-9I0J-K1L2M3N4O5P6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=..\dist
OutputBaseFilename=SPAMURAI-Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executable and all dependencies
Source: "..\dist\SPAMURAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Documentation
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "README.txt"
Source: "..\GOOGLE_SHEETS_SETUP.md"; DestDir: "{app}"; Flags: ignoreversion; DestName: "GOOGLE_SHEETS_SETUP.txt"
Source: "..\config.example.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{group}\README"; Filename: "{app}\README.txt"

; Desktop shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Quick Launch
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to launch after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if Python is installed
  if not RegKeyExists(HKEY_CURRENT_USER, 'Software\Python\PythonCore\3.8') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Python\PythonCore\3.8') and
     not RegKeyExists(HKEY_CURRENT_USER, 'Software\Python\PythonCore\3.9') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Python\PythonCore\3.9') and
     not RegKeyExists(HKEY_CURRENT_USER, 'Software\Python\PythonCore\3.10') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Python\PythonCore\3.10') and
     not RegKeyExists(HKEY_CURRENT_USER, 'Software\Python\PythonCore\3.11') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Python\PythonCore\3.11') and
     not RegKeyExists(HKEY_CURRENT_USER, 'Software\Python\PythonCore\3.12') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'Software\Python\PythonCore\3.12') then
  begin
    if MsgBox('Python 3.8 or higher was not detected on your system.' + #13#10 + #13#10 +
              'SPAMURAI requires Python to function properly.' + #13#10 + #13#10 +
              'Would you like to download Python now?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;

    MsgBox('Please install Python and run this installer again.', mbInformation, MB_OK);
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Create config directory
    CreateDir(ExpandConstant('{app}\config'));
  end;
end;
