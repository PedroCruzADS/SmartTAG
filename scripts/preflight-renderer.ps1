param(
  [ValidateSet("auto","tesseract","hyperframes","remotion","hybrid")][string]$Renderer = "auto",
  [switch]$Deep
)
$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python nao encontrado." }
$argsList = @((Join-Path $PSScriptRoot "preflight_renderer.py"), "--renderer", $Renderer)
if ($Deep) { $argsList += "--deep" }
& $python.Source @argsList
exit $LASTEXITCODE
