param(
  [ValidateSet("auto","tesseract","hyperframes","remotion","hybrid")][string]$Renderer = "auto"
)

$ErrorActionPreference = "Continue"

function Has-Command($name) {
  return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

$hasNode = Has-Command "node"
$node22 = $false
if ($hasNode) {
  try {
    $v = (node --version).TrimStart("v")
    $node22 = ([int]($v.Split(".")[0]) -ge 22)
  } catch {}
}

$hasNpx = Has-Command "npx"
$hasFfmpeg = Has-Command "ffmpeg"
$tesseract = Join-Path $env:LOCALAPPDATA "Tesseract\bin\tsrct.cmd"
$hasTesseract = Test-Path $tesseract

$hyperframesReady = $node22 -and $hasNpx -and $hasFfmpeg
$remotionReady = $hasNode -and $hasNpx

Write-Host "== Renderer preflight =="
Write-Host "Tesseract :" ($(if ($hasTesseract) {"ready"} else {"not detected"}))
Write-Host "HyperFrames:" ($(if ($hyperframesReady) {"base requirements ready"} else {"missing Node22+/npx/ffmpeg"}))
Write-Host "Remotion  :" ($(if ($remotionReady) {"base requirements ready"} else {"missing node/npx"}))

if ($Renderer -eq "auto") {
  Write-Host ""
  Write-Host "AUTO nao escolhe por disponibilidade apenas."
  Write-Host "Use:"
  Write-Host "- HyperFrames: motion graphics/layout/timing deterministico"
  Write-Host "- Remotion: React/templates/lotes/parametrizacao"
  Write-Host "- Tesseract: footage/compositing/masks/retiming/acabamento"
  Write-Host "- Hybrid: quando duas etapas reduzem retrabalho"
  exit 0
}

switch ($Renderer) {
  "tesseract" {
    if (-not $hasTesseract) { throw "Tesseract solicitado, mas CLI nao detectado." }
  }
  "hyperframes" {
    if (-not $hyperframesReady) { throw "HyperFrames solicitado, mas faltam requisitos." }
    npx hyperframes doctor
  }
  "remotion" {
    if (-not $remotionReady) { throw "Remotion solicitado, mas Node/npx nao estao prontos." }
  }
  "hybrid" {
    if (-not ($hasTesseract -and ($hyperframesReady -or $remotionReady))) {
      throw "Hybrid solicitado, mas a combinacao local nao esta pronta."
    }
  }
}

Write-Host "[OK] Preflight para $Renderer concluido."
