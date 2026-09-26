$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python nao encontrado." }
& $python.Source (Join-Path $PSScriptRoot "check_environment.py")
exit $LASTEXITCODE
