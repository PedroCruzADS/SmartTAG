param([switch]$Install21st)
$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python nao encontrado." }
$argsList = @((Join-Path $PSScriptRoot "bootstrap.py"))
if ($Install21st) { $argsList += "--install-21st" }
& $python.Source @argsList
exit $LASTEXITCODE
