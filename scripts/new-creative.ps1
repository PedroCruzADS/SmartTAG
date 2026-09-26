param(
  [Parameter(Mandatory=$true)][string]$Slug,
  [string]$Objective = "conversion",
  [ValidateSet("auto","tesseract","hyperframes","remotion","hybrid")][string]$Renderer = "auto",
  [int]$DurationSeconds = 9,
  [int]$Fps = 30
)

$ErrorActionPreference = "Stop"
$date = Get-Date -Format "yyyyMMdd"
$root = Join-Path "outputs" ("{0}_{1}_{2}_9x16_v01" -f $date,$Slug,$Objective)

if (Test-Path $root) { throw "A pasta ja existe: $root" }

foreach ($dir in @(
  $root,
  (Join-Path $root "Storyboards"),
  (Join-Path $root "Stills"),
  (Join-Path $root "Previews"),
  (Join-Path $root "Renders"),
  (Join-Path $root "Source")
)) {
  New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$brief = @"
# Brief local — $Slug

## Objetivo
$Objective

## Produto
- URL:
- SKU:
- Beneficio comprovado:

## Oferta
- Snapshot:
- Preco:
- Parcelamento:
- PIX:
- Cupom:
- Frete:

## Brand kit
- Logo:
- Cores:
- Fontes:

## Referencias
### A
- URL/arquivo:
- Usar:
- Nao copiar:

### B
- URL/arquivo:
- Usar:
- Nao copiar:

## Formato
- Canvas: 1080x1920
- Duracao: ${DurationSeconds}s
- FPS: $Fps

## Renderer
- Preferencia: $Renderer

## Assets autorizados
- assets/$Slug/

## Restricoes
- nao recriar/alterar produto
- nao inventar claims/oferta

## Storyboard
Gerar 3 variantes antes de motion e um still por cena antes do render.
"@

Set-Content -Path (Join-Path $root "brief.md") -Value $brief -Encoding UTF8

$request = [ordered]@{
  product_slug = $Slug
  objective = $Objective
  channel = "meta_ads"
  placements = @("reels","stories")
  canvas = "1080x1920"
  duration_seconds = $DurationSeconds
  fps = $Fps
  renderer = $Renderer
  offer_snapshot = "data/$Slug/offer.json"
  assets_dir = "assets/$Slug"
  brand = [ordered]@{ logo=""; fonts=@(); colors=@(); rules=@() }
  references = @()
  copy = [ordered]@{ hook=""; headline=""; support=""; cta="" }
  storyboard = [ordered]@{ variants=3; require_stills_before_motion=$true }
  variants = [ordered]@{ hooks=2; ctas=2; formats=@("1080x1920","1080x1350","1080x1080") }
  constraints = [ordered]@{ no_product_recreation=$true; no_unverified_claims=$true }
}

$request | ConvertTo-Json -Depth 8 | Set-Content -Path (Join-Path $root "request.json") -Encoding UTF8
Set-Content -Path (Join-Path $root "notes.md") -Value "# Notes`n`n## Renderer decision`n- Pending`n`n## Director notes`n" -Encoding UTF8

Write-Host "Job criado:" $root
Write-Host "Proximo passo: preencher brief/request, adicionar referencias e gerar 3 storyboards."
