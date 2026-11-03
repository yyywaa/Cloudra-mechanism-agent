$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repo

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed (exit code $LASTEXITCODE). See the error above."
    }
}

try {
    $node = Get-Command node.exe -ErrorAction SilentlyContinue
    $npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if (-not $node -or -not $npm) {
        throw 'Install Node.js 22.12 or newer with npm from https://nodejs.org/ and run install.cmd again.'
    }
    $nodeVersion = & $node.Source -p 'process.versions.node'
    if ($LASTEXITCODE -ne 0 -or [version]$nodeVersion -lt [version]'22.12.0') {
        throw 'Cloudra needs Node.js 22.12 or newer. Install it from https://nodejs.org/ and try again.'
    }

    $python = Join-Path $repo '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) {
        $basePython = $null
        foreach ($name in @('python.exe', 'py.exe')) {
            $candidate = Get-Command $name -ErrorAction SilentlyContinue
            if (-not $candidate) { continue }
            $pythonArgs = @()
            if ($name -eq 'py.exe') { $pythonArgs = @('-3') }
            $found = & $candidate.Source @pythonArgs -c 'import sys; sys.exit(1) if sys.version_info < (3, 11) else print(sys.executable)'
            if ($LASTEXITCODE -eq 0) {
                $basePython = $found
                break
            }
        }
        if (-not $basePython) {
            throw 'Install Python 3.13 from https://www.python.org/downloads/windows/ (enable Add python.exe to PATH), then try again. Python 3.11 or newer is required.'
        }
        Write-Host '[Cloudra] Creating the project Python environment...'
        Invoke-Checked $basePython @('-m', 'venv', (Join-Path $repo '.venv'))
    }
    Invoke-Checked $python @('-c', 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)')

    Write-Host '[Cloudra] Installing Python dependencies...'
    Invoke-Checked $python @('-m', 'pip', 'install', '--upgrade', 'pip')
    Invoke-Checked $python @('-m', 'pip', 'install', '-e', $repo)

    Write-Host '[Cloudra] Installing the JavaScript tool runtime...'
    Invoke-Checked $npm.Source @('ci', '--prefix', (Join-Path $repo 'cloudra\runtime_v2\js_host'), '--ignore-scripts', '--no-audit', '--no-fund')
    Write-Host '[Cloudra] Installing and building the web interface...'
    Invoke-Checked $npm.Source @('ci', '--prefix', (Join-Path $repo 'frontend'), '--no-audit', '--no-fund')
    Invoke-Checked $npm.Source @('run', 'build', '--prefix', (Join-Path $repo 'frontend'))

    # Explorer shortcuts may inherit a different PATH from the installation shell.
    $nodeDirectory = Split-Path -Parent $node.Source
    [IO.File]::WriteAllText((Join-Path $repo '.venv\cloudra-node-path.txt'), $nodeDirectory, [Text.UTF8Encoding]::new($false))
    $desktop = [Environment]::GetFolderPath('DesktopDirectory')
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut((Join-Path $desktop 'Cloudra.lnk'))
    $shortcut.TargetPath = Join-Path $repo 'launch-cloudra.cmd'
    $shortcut.WorkingDirectory = $repo
    $shortcut.Description = 'Open the Cloudra web interface'
    $shortcut.Save()

    Write-Host ''
    Write-Host '[Cloudra] Installation complete. Double-click Cloudra on your desktop.' -ForegroundColor Green
    Write-Host '[Cloudra] Configure your models in Global Settings after the browser opens.'
    exit 0
} catch {
    Write-Host ''
    Write-Host "[Cloudra] Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host '[Cloudra] See docs/INSTALL_WINDOWS_CN.md or docs/INSTALL_WINDOWS.md for help.'
    exit 1
}
