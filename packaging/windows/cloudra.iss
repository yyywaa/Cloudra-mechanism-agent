#ifndef CloudraVersion
  #error CloudraVersion is supplied by build.ps1
#endif
#ifndef PayloadDir
  #error PayloadDir is supplied by build.ps1
#endif
#ifndef InstallerOutput
  #error InstallerOutput is supplied by build.ps1
#endif

[Setup]
AppId=Cloudra.Windows.Desktop
AppName=Cloudra
AppVersion={#CloudraVersion}
AppPublisher=Cloudra
AppPublisherURL=https://github.com/yyywaa/Cloudra-mechanism-agent
DefaultDirName={localappdata}\Programs\Cloudra
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
WizardStyle=modern
DisableWelcomePage=no
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
OutputDir={#InstallerOutput}
OutputBaseFilename=Cloudra-{#CloudraVersion}-windows-x64-Setup
Compression=lzma2/fast
SolidCompression=yes
UninstallDisplayName=Cloudra
CloseApplications=no
RestartApplications=no

[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "{#PayloadDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Cloudra"; Filename: "{app}\resources\python\pythonw.exe"; Parameters: """{app}\desktop_launcher.py"""; WorkingDir: "{app}\resources"
Name: "{autoprograms}\Stop Cloudra"; Filename: "{app}\resources\python\pythonw.exe"; Parameters: """{app}\desktop_launcher.py"" --stop"; WorkingDir: "{app}\resources"
Name: "{autodesktop}\Cloudra"; Filename: "{app}\resources\python\pythonw.exe"; Parameters: """{app}\desktop_launcher.py"""; WorkingDir: "{app}\resources"; Tasks: desktopicon

[Run]
Filename: "{app}\resources\python\pythonw.exe"; Parameters: """{app}\desktop_launcher.py"""; WorkingDir: "{app}\resources"; Description: "Launch Cloudra"; Flags: nowait postinstall skipifsilent
