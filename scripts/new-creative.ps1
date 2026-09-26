param(
  [Parameter(Mandatory=$true)][string]$Slug,
  [string]$Objective = "conversion",
  [ValidateSet("auto","tesseract","hyperframes","remotion","hybrid")][string]$Renderer = "auto",
  [ValidateRange(1,120)][int]$DurationSeconds = 9,
  [ValidateSet(24,30,60)][int]$Fps = 30,
  [ValidateSet("1080x1920","1080x1350","1080x1080")][string]$Canvas = "1080x1920",
  [ValidateSet("human","auto")][string]$ApprovalMode = "human"
)
$ErrorActionPreference = "Stop"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw "Python nao encontrado." }

$argsList = @(
  (Join-Path $PSScriptRoot "new_creative.py"),
  "--slug", $Slug,
  "--objective", $Objective,
  "--renderer", $Renderer,
  "--duration-seconds", $DurationSeconds,
  "--fps", $Fps,
  "--canvas", $Canvas,
  "--approval-mode", $ApprovalMode
)
& $python.Source @argsList
exit $LASTEXITCODE
