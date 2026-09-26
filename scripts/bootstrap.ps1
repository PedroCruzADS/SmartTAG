param(
  [switch]$Install21st
)

$ErrorActionPreference = "Stop"

Write-Host "== Casa do Fitness / Tesseract Creative Lab =="

if (-not [Environment]::Is64BitOperatingSystem) {
    throw "Este projeto requer Windows 64-bit para a rota Tesseract."
}

Write-Host "OS:" ([Environment]::OSVersion.VersionString)

$nodeOk = $false
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = (node --version).TrimStart("v")
    Write-Host "Node:" $nodeVersion
    try {
        $major = [int]($nodeVersion.Split(".")[0])
        if ($major -ge 22) { $nodeOk = $true }
        else { Write-Warning "HyperFrames requer Node.js 22+. Atualize o Node para habilitar essa rota." }
    } catch {
        Write-Warning "Nao foi possivel validar a versao do Node."
    }
} else {
    Write-Warning "Node.js/npm nao encontrado. HyperFrames, Remotion e instaladores de skills via npx precisam de Node."
}

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "npm:" (npm --version)
}

if (Get-Command npx -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "[1/3] Instalando/atualizando skills do Tesseract..."
    try { npx skills add mirage-hq/Tesseract } catch { Write-Warning "Falha ao instalar skills do Tesseract: $_" }

    if ($nodeOk) {
        Write-Host ""
        Write-Host "[2/3] Instalando/atualizando skills do HyperFrames..."
        try {
            npx hyperframes skills update
            npx hyperframes doctor
        } catch {
            Write-Warning "Falha no setup do HyperFrames: $_"
        }
    }

    Write-Host ""
    Write-Host "[3/3] Instalando/atualizando skills do Remotion..."
    try {
        npx -y skills@latest add remotion-dev/skills -g -y
    } catch {
        Write-Warning "Falha ao instalar skills do Remotion: $_"
    }

    if ($Install21st) {
        Write-Host ""
        Write-Host "Instalando skill do 21st.dev (opcional)..."
        try { npx @21st-dev/cli install-skill } catch { Write-Warning "Falha no setup do 21st.dev: $_" }
    }
} else {
    Write-Warning "npx indisponivel. Instale Node.js antes de configurar as skills."
}

if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "Claude Code detectado. Remotion tambem oferece plugin oficial:"
    Write-Host "  claude plugin marketplace add remotion-dev/claude-code-plugin"
    Write-Host "  claude plugin install remotion@remotion"
}

Write-Host ""
Write-Host "Setup concluido. Rode:"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\check-environment.ps1"
Write-Host ""
Write-Host "Depois abra o repo no Claude Code/Codex e diga:"
Write-Host '"Leia AGENTS.md e docs/WORKFLOW.md; crie 3 storyboards antes de animar."'
