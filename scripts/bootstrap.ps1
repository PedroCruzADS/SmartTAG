$ErrorActionPreference = "Stop"

Write-Host "== Casa do Fitness / Tesseract Creative Lab =="

if (-not [Environment]::Is64BitOperatingSystem) {
    throw "Este projeto requer Windows 64-bit."
}

Write-Host "Windows detectado:" ([Environment]::OSVersion.Version)

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Warning "Node.js/npm nao encontrado. O instalador de skills via npx requer Node.js."
} else {
    Write-Host "Node:" (node --version)
    Write-Host "npm:" (npm --version)
}

Write-Host ""
Write-Host "Instalando/atualizando as skills oficiais do Tesseract..."
if (Get-Command npx -ErrorAction SilentlyContinue) {
    npx skills add mirage-hq/Tesseract
} else {
    Write-Warning "npx indisponivel. Peca ao Claude Code/Codex para instalar as skills seguindo:"
    Write-Host "https://github.com/mirage-hq/Tesseract"
}

Write-Host ""
Write-Host "Depois abra esta pasta no Claude Code ou Codex e diga:"
Write-Host '"Leia AGENTS.md e briefs/casa-do-fitness-promo.md e prepare o primeiro criativo."'
