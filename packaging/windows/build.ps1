$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location -LiteralPath $repo
# Inno's source reader needs short paths even when Git enables long paths.
$work = Join-Path ([IO.Path]::GetTempPath()) 'cloudra-windows-package'
$output = Join-Path $repo 'dist'
$payload = Join-Path $work 'Cloudra'
$resources = Join-Path $payload 'resources'
$pythonVersion = '3.13.16'
$nodeVersion = '22.23.4'

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program failed with exit code $LASTEXITCODE." }
}

if (Test-Path -LiteralPath $work) { Remove-Item -LiteralPath $work -Recurse -Force }
New-Item -ItemType Directory -Force -Path $resources, $output | Out-Null
$buildPython = (Get-Command python.exe).Source
Invoke-Checked $buildPython @('-c', "import sys; assert sys.version_info[:2] == (3, 13), 'Build with Python 3.13'")
$version = & $buildPython -c "import pathlib,tomllib; print(tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project']['version'])"
if ($LASTEXITCODE -ne 0) { throw 'Cannot read project version.' }
$commit = & git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read source commit.' }

Write-Host '[Cloudra] Downloading the application-local Python runtime...'
$pythonZip = Join-Path $work 'python.zip'
Invoke-WebRequest -UseBasicParsing -Uri "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-embed-amd64.zip" -OutFile $pythonZip
# Published SHA256 for the official x64 embeddable distribution.
$pythonSha256 = '97dae5274cc54867065e8d5a3226e48c35017ed332a0fdb0e27d5b5821961297'
if ((Get-FileHash -LiteralPath $pythonZip -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pythonSha256) {
    throw 'Python download checksum did not match the official release.'
}
$pythonDir = Join-Path $resources 'python'
Expand-Archive -LiteralPath $pythonZip -DestinationPath $pythonDir
[IO.File]::WriteAllText((Join-Path $pythonDir 'python313._pth'), "python313.zip`r`n.`r`nLib\site-packages`r`nimport site`r`n", [Text.Encoding]::ASCII)
$sitePackages = Join-Path $pythonDir 'Lib\site-packages'
Write-Host '[Cloudra] Installing core application dependencies into the bundle...'
Invoke-Checked $buildPython @('-m', 'pip', 'install', '--target', $sitePackages, $repo)
# The source commit is recorded below; do not ship a builder's local path.
Get-ChildItem -LiteralPath $sitePackages -Directory -Filter 'cloudra-*.dist-info' | ForEach-Object {
    Remove-Item -LiteralPath (Join-Path $_.FullName 'direct_url.json') -ErrorAction SilentlyContinue
}

# Console-script launchers belong to the builder; desktop startup uses python -m.
foreach ($directory in @('bin', 'Scripts')) {
    Remove-Item -LiteralPath (Join-Path $sitePackages $directory) -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host '[Cloudra] Downloading the application-local Node.js runtime...'
$nodeArchiveName = "node-v$nodeVersion-win-x64.zip"
$nodeZip = Join-Path $work $nodeArchiveName
$nodeBase = "https://nodejs.org/dist/v$nodeVersion"
Invoke-WebRequest -UseBasicParsing -Uri "$nodeBase/$nodeArchiveName" -OutFile $nodeZip
$checksums = (Invoke-WebRequest -UseBasicParsing -Uri "$nodeBase/SHASUMS256.txt").Content
$nodeSha256 = $null
foreach ($line in $checksums.Split("`n")) {
    $parts = $line.Trim().Split(' ', [StringSplitOptions]::RemoveEmptyEntries)
    if ($parts.Count -eq 2 -and $parts[1] -eq $nodeArchiveName) { $nodeSha256 = $parts[0] }
}
if (-not $nodeSha256 -or (Get-FileHash -LiteralPath $nodeZip -Algorithm SHA256).Hash.ToLowerInvariant() -ne $nodeSha256) {
    throw 'Node.js download checksum did not match the official release.'
}
$nodeExtract = Join-Path $work 'node-download'
Expand-Archive -LiteralPath $nodeZip -DestinationPath $nodeExtract
$nodeSource = Join-Path $nodeExtract "node-v$nodeVersion-win-x64"
$nodeDir = Join-Path $resources 'node'
New-Item -ItemType Directory -Path $nodeDir | Out-Null
Copy-Item -LiteralPath (Join-Path $nodeSource 'node.exe'), (Join-Path $nodeSource 'LICENSE') -Destination $nodeDir

Write-Host '[Cloudra] Building the frontend and JavaScript host...'
$npm = (Get-Command npm.cmd).Source
Invoke-Checked $npm @('ci', '--prefix', (Join-Path $repo 'frontend'), '--no-audit', '--no-fund')
Invoke-Checked $npm @('run', 'build', '--prefix', (Join-Path $repo 'frontend'))
$frontend = Join-Path $resources 'frontend'
New-Item -ItemType Directory -Path $frontend | Out-Null
Copy-Item -LiteralPath (Join-Path $repo 'frontend\package.json') -Destination $frontend
Copy-Item -LiteralPath (Join-Path $repo 'frontend\dist') -Destination $frontend -Recurse
Invoke-Checked $buildPython @((Join-Path $repo 'scripts\collect_frontend_licenses.py'), '--frontend', (Join-Path $repo 'frontend'), '--output', (Join-Path $payload 'licenses\frontend'))
Invoke-Checked $npm @('ci', '--prefix', (Join-Path $sitePackages 'cloudra\runtime_v2\js_host'), '--ignore-scripts', '--no-audit', '--no-fund')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'desktop_launcher.py'), (Join-Path $repo 'LICENSE') -Destination $payload
$buildInfo = [ordered]@{
    version = $version
    source_commit = $commit
    source_url = "https://github.com/yyywaa/Cloudra-mechanism-agent/tree/$commit"
    python = $pythonVersion
    node = $nodeVersion
    platform = 'windows-x64'
}
[IO.File]::WriteAllText((Join-Path $payload 'BUILD_INFO.json'), ($buildInfo | ConvertTo-Json), [Text.UTF8Encoding]::new($false))

Write-Host '[Cloudra] Verifying the bundled interpreter and application...'
Invoke-Checked (Join-Path $pythonDir 'python.exe') @('-m', 'cloudra', '--version')
$compiler = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'
if (-not (Test-Path -LiteralPath $compiler)) { $compiler = (Get-Command ISCC.exe).Source }
Write-Host '[Cloudra] Building the native Windows setup wizard...'
Invoke-Checked $compiler @("/DCloudraVersion=$version", "/DPayloadDir=$payload", "/DInstallerOutput=$output", (Join-Path $PSScriptRoot 'cloudra.iss'))
Write-Host "[Cloudra] Installer: $(Join-Path $output "Cloudra-$version-windows-x64-Setup.exe")"
