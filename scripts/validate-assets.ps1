param([string]$Path = "assets")
$ErrorActionPreference = "Stop"
if (-not (Test-Path $Path)) { throw "Pasta nao encontrada: $Path" }
$allowed = @(".png",".jpg",".jpeg",".webp",".svg",".mp4",".mov",".m4v",".wav",".mp3",".m4a",".ttf",".otf",".pdf")
$files = Get-ChildItem -Path $Path -Recurse -File
if ($files.Count -eq 0) { Write-Warning "Nenhum asset encontrado em $Path"; exit 0 }
$bad = @()
foreach ($f in $files) { if ($allowed -notcontains $f.Extension.ToLower()) { $bad += $f.FullName } }
Write-Host "Assets encontrados:" $files.Count
Write-Host "Tamanho total (MB):" ([math]::Round((($files | Measure-Object Length -Sum).Sum / 1MB),2))
if ($bad.Count -gt 0) { Write-Warning "Arquivos fora da lista esperada:"; $bad | ForEach-Object { Write-Host " - $_" } }
Write-Host "OK. O agente deve inspecionar visualmente os assets antes de criar a peca."
