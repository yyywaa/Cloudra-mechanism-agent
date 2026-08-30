# kg_vec_service.ps1 - one-shot launcher for the knowledge-card semantic
# retrieval microservice (bge-m3). Usage:
#   powershell -File scripts\kg_vec_service.ps1 [-Port 8765]
# Dependencies live in the external .venv-trans (sentence-transformers /
# torch / numpy); the cloudra venv never installs torch. The default
# interpreter path is a local deployment example - override with -Python
# or the KG_VEC_PYTHON environment variable. ASCII-only on purpose:
# Windows PowerShell 5.1 mis-parses BOM-less UTF-8 comments.
param(
    [int]$Port = 8765,
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

if (-not $Python) {
    $Python = $env:KG_VEC_PYTHON
}
if (-not $Python) {
    $Python = "D:\AAA-LY\work\卢天的帖子\清洗的代码\.venv-trans\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $Python)) {
    Write-Error ("python not found: " + $Python + " (set -Python or $env:KG_VEC_PYTHON)")
    exit 1
}

$env:HF_HUB_OFFLINE = "1"  # model is cached locally; load offline
& $Python -X utf8 (Join-Path $Root "scripts\kg_vec_service.py") --port $Port
