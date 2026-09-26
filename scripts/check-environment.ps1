$ErrorActionPreference = "Continue"
$isWindows = [System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT

Write-Host "== Environment check =="
Write-Host "OS:" ([Environment]::OSVersion.VersionString)
Write-Host "64-bit:" ([Environment]::Is64BitOperatingSystem)

foreach ($cmd in @("git","node","npm","npx","python","ffmpeg","ffprobe","claude","codex")) {
  $c = Get-Command $cmd -ErrorAction SilentlyContinue
  if ($c) { Write-Host ("[OK] {0}: {1}" -f $cmd,$c.Source) } else { Write-Host ("[--] {0}: not found" -f $cmd) }
}

if (Get-Command node -ErrorAction SilentlyContinue) {
  try {
    $version = (node --version).TrimStart("v")
    $major = [int]($version.Split(".")[0])
    if ($major -ge 22) {
      Write-Host "[OK] Node >=22: HyperFrames compatible"
    } else {
      Write-Warning "Node $version detectado. HyperFrames requer Node 22+."
    }
  } catch {}
}

if ($isWindows -and $env:LOCALAPPDATA) {
  $candidate = Join-Path $env:LOCALAPPDATA "Tesseract\bin\tsrct.cmd"
  if (Test-Path $candidate) {
    Write-Host "[OK] Tesseract:" $candidate
    & $candidate --version
  } else {
    Write-Host "[--] Tesseract CLI nao encontrado no caminho padrao."
  }
} else {
  Write-Host "[--] Tesseract: rota local nao verificada neste sistema."
}

if (Get-Command npx -ErrorAction SilentlyContinue) {
  Write-Host ""
  Write-Host "== HyperFrames doctor =="
  try { npx hyperframes doctor } catch { Write-Warning "HyperFrames indisponivel ou doctor falhou." }

  Write-Host ""
  Write-Host "== HyperFrames skills =="
  try { npx hyperframes skills check } catch { Write-Warning "Nao foi possivel checar skills do HyperFrames." }
}

Write-Host ""
Write-Host "Use scripts/preflight-renderer.ps1 -Renderer auto para recomendacao operacional."
