param(
  [Parameter(Mandatory=$true)][string]$Slug,
  [string]$Objective = "conversion"
)

$ErrorActionPreference = "Stop"
$date = Get-Date -Format "yyyyMMdd"
$root = Join-Path "outputs" ("{0}_{1}_{2}_9x16_v01" -f $date,$Slug,$Objective)

if (Test-Path $root) { throw "A pasta ja existe: $root" }
New-Item -ItemType Directory -Path $root | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root "Previews") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $root ".tesseract-work") | Out-Null

$brief = @("# Brief local","","Produto: $Slug","Objetivo: $Objective","","Preencha/aponte:","- URL do produto","- snapshot comercial","- assets autorizados","- hook/headline/CTA","- restricoes")
Set-Content -Path (Join-Path $root "brief.md") -Value $brief -Encoding UTF8
Set-Content -Path (Join-Path $root "notes.md") -Value "# Notes" -Encoding UTF8
Write-Host "Job criado:" $root
