$ErrorActionPreference = "Continue"
Write-Host "== Environment check =="
Write-Host "OS:" ([Environment]::OSVersion.VersionString)
Write-Host "64-bit:" ([Environment]::Is64BitOperatingSystem)
foreach ($cmd in @("git","node","npm","npx","python","ffmpeg","ffprobe")) {
  $c = Get-Command $cmd -ErrorAction SilentlyContinue
  if ($c) { Write-Host ("[OK] {0}: {1}" -f $cmd,$c.Source) } else { Write-Warning ("[MISSING] {0}" -f $cmd) }
}
$candidate = Join-Path $env:LOCALAPPDATA "Tesseract\bin\tsrct.cmd"
if (Test-Path $candidate) {
  Write-Host "[OK] Tesseract:" $candidate
  & $candidate --version
} else {
  Write-Warning "Tesseract CLI nao encontrado no caminho padrao. Rode scripts/bootstrap.ps1 ou siga a skill oficial."
}
