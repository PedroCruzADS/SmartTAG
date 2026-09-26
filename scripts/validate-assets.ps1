param([string]$Path = "assets", [switch]$Strict)
$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python nao encontrado." }
$argsList = @((Join-Path $PSScriptRoot "validate_assets.py"), $Path)
if ($Strict) { $argsList += "--strict" }
& $python.Source @argsList
exit $LASTEXITCODE
