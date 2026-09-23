# Casa do Fitness — Tesseract Creative Lab

Laboratório local para gerar criativos em vídeo da Casa do Fitness usando **Tesseract by Mirage** com Claude Code ou Codex.

## Objetivo

Fluxo simples:

1. Clone este repositório na branch `tesseract-lab`.
2. Coloque os assets reais em `assets/`.
3. Abra a pasta no Claude Code ou Codex.
4. Peça ao agente para seguir `AGENTS.md` / `CLAUDE.md`.
5. O agente instala/verifica o Tesseract, cria o projeto `.tsrct`, gera previews e exporta o MP4.

> O Tesseract roda localmente. Cloud rendering, Linux e WSL não são suportados atualmente.

## Início rápido

```powershell
git clone -b tesseract-lab https://github.com/PedroCruzADS/SmartTAG.git
cd SmartTAG
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

Depois abra a pasta no agente e use:

```text
Leia AGENTS.md e briefs/casa-do-fitness-promo.md.
Use somente os assets reais existentes em assets/.
Crie um primeiro criativo vertical de 8 a 10 segundos para Meta Ads.
Não invente nem redesenhe produto, logo, preço ou condição comercial.
Gere preview/filmstrip antes do export final.
```

## Estrutura

```text
assets/          imagens, vídeos, logos, fontes e áudio fornecidos
briefs/          briefs de criação
outputs/         projetos .tsrct, previews e MP4s finais
scripts/         setup e verificações locais
AGENTS.md        instruções para Codex e outros agentes
CLAUDE.md        instruções para Claude Code
```

## Assets

Copie para `assets/` apenas arquivos que podem ser usados na peça. Prefira nomes claros:

```text
assets/
  product-main.png
  product-detail-01.jpg
  product-video.mp4
  logo-casa-do-fitness.png
  font-brand.ttf
  music.mp3
```

O agente deve preservar fielmente os assets enviados.
