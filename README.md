# Casa do Fitness — Tesseract Creative Lab

Pipeline local e agent-first para criar criativos de mídia paga a partir de **produto real, oferta verificável, brand kit, referências e aprovação explícita**.

O nome histórico continua Tesseract Creative Lab, mas o sistema é multi-renderer:

- **Tesseract** — edição, footage, masks, compositing, retiming e acabamento.
- **HyperFrames** — motion graphics determinístico em HTML/CSS/GSAP.
- **Remotion** — React, templates, parametrização e lotes.
- **Hybrid** — combina render programático com acabamento editorial.
- **21st.dev** — opcional para cenas de UI/software; não é renderer.

## Princípio central

**Contexto verificável → 3 storyboards → stills → aprovação → motion → preview → aprovação → render final → QA.**

Não existe “one prompt” mágico no Lab. O ganho vem de reduzir o espaço de decisão do agente e tornar cada etapa auditável.

## Requisitos

- Python 3.10+
- Git
- Node.js/npm para instalar skills e para HyperFrames/Remotion
- FFmpeg/FFprobe para HyperFrames e QA técnico de vídeo
- CLI do renderer escolhido

Tesseract atual suporta macOS, Windows e Linux x86_64 em ambientes compatíveis. A skill oficial e a versão instalada são a fonte de verdade para instalação e comandos.

## Setup

~~~bash
git clone https://github.com/PedroCruzADS/tesseract-creative-lab.git
cd tesseract-creative-lab
python -m pip install -r requirements.txt
python scripts/bootstrap.py
python scripts/check_environment.py
~~~

No Windows, os wrappers PowerShell continuam disponíveis.

O bootstrap instala/atualiza skills de Tesseract, HyperFrames e Remotion. 21st.dev é opt-in:

~~~bash
python scripts/bootstrap.py --install-21st
~~~

## Criar um job

~~~bash
python scripts/new_creative.py --slug esteira-b55 --objective conversion --renderer auto --canvas 1080x1920 --duration-seconds 9 --fps 30 --approval-mode human
~~~

O job é versionado automaticamente e nasce com Storyboards, Stills, Previews, Renders, Source, brief.md, request.json, approvals.json e notes.md.

human é o default: o agente não pode autoaprovar gates humanos. Use approval-mode auto somente quando quiser execução autônoma deliberadamente.

## Assets e oferta

Estrutura recomendada:

~~~text
assets/<produto>/
  product/
  lifestyle/
  logo/
  fonts/
  audio/
  references/
~~~

Valide e congele os assets autorizados:

~~~bash
python scripts/validate_assets.py assets/esteira-b55 --strict
python scripts/asset_manifest.py assets/esteira-b55 --out outputs/<job>/Source/assets-manifest.json
~~~

Capture a página de produto:

~~~bash
python scripts/product_snapshot.py "https://www.casadofitness.com.br/produto" --out data/esteira-b55/offer.json
~~~

O snapshot é evidência, não verdade absoluta. Se houver múltiplos preços/variantes, o script evita escolher silenciosamente.

## Workflow e gates

Valide cada etapa:

~~~bash
python scripts/validate_job.py outputs/<job> --stage ingest
python scripts/validate_job.py outputs/<job> --stage storyboard
python scripts/validate_job.py outputs/<job> --stage motion
python scripts/validate_job.py outputs/<job> --stage render
python scripts/validate_job.py outputs/<job> --stage final
~~~

Aprovação humana:

~~~bash
python scripts/approve_gate.py outputs/<job> storyboard --actor-type human --by "Pedro" --note "Direção B aprovada"
~~~

Para gates auto, o agente pode registrar aprovação com actor-type agent. Um gate configurado como human rejeita aprovação de agente.

## QA técnico do render

~~~bash
python scripts/validate_render.py outputs/<job>/Renders/master.mp4 --canvas 1080x1920 --duration 9 --fps 30
~~~

O script usa FFprobe para validar stream de vídeo, resolução, FPS, duração e presença de áudio.

## Git e arquivos pesados

assets/, data/ e outputs/ ficam ignorados por padrão para evitar publicar material de campanha, snapshots voláteis e vídeos pesados sem intenção. Os placeholders/documentação continuam versionados.

Se um projeto precisar versionar mídia, use armazenamento apropriado ou Git LFS de forma deliberada.

## Documentos principais

- AGENTS.md — contrato operacional do agente.
- docs/WORKFLOW.md — gates ponta a ponta.
- docs/RENDERER-ROUTING.md — escolha de renderer.
- docs/OFFER-TRUTH.md — verdade comercial.
- docs/REFERENCE-DIRECTION.md — referências e segurança.
- docs/STORYBOARD-AND-STILLS.md — 3 variantes e still gate.
- docs/QA-PAID-MEDIA.md — QA criativo/comercial/técnico.
- docs/TROUBLESHOOTING.md — falhas comuns.

## Schemas e CI

schemas/ contém JSON Schemas Draft 2020-12, não apenas exemplos. A CI valida sintaxe Python, exemplos de schema e regras básicas de segurança/versionamento.

O Lab deve permanecer **renderer-agnostic, asset-faithful e source-of-truth driven**.
