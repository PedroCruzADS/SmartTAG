# Casa do Fitness — Tesseract Creative Lab

Laboratório de produção de criativos de **mídia paga** com agentes (Claude Code/Codex) e múltiplos renderers.

O Lab não é mais "um repo para testar Tesseract". Ele é o sistema de produção: recebe produto real, oferta verificada, identidade, referências e direção; cria alternativas de storyboard; aprova frames estáticos; escolhe o renderer adequado; anima; revisa; exporta versões para mídia.

## Princípio central

**Produto real + condição verificada + referências explícitas + storyboard antes de animar + QA antes do render final.**

Nunca invente preço, desconto, parcelamento, PIX, frete, cupom, estoque, benefício técnico, produto, logo ou selo.

## Stack de render

O renderer é escolhido por job:

- **Tesseract** — edição/compositing, footage, máscaras, retiming e acabamento.
- **HyperFrames** — motion graphics determinístico em HTML/CSS/GSAP, ótimo para agentes e iteração rápida.
- **Remotion** — vídeo programático em React, bom para templates, parametrização e lotes.
- **Hybrid** — combina render programático e acabamento no Tesseract.
- **21st.dev** — opcional; use principalmente quando o criativo depende de UI realista/componentes de software.

Veja `docs/RENDERER-ROUTING.md`.

## Início rápido

~~~powershell
git clone https://github.com/PedroCruzADS/tesseract-creative-lab.git
cd tesseract-creative-lab
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
pip install -r requirements.txt
~~~

O bootstrap instala/atualiza as skills de Tesseract, HyperFrames e Remotion quando as ferramentas necessárias estiverem disponíveis. 21st.dev fica opcional.

## Workflow recomendado

### 1. Salve os assets reais

~~~text
assets/<produto>/
  product/
  lifestyle/
  logo/
  fonts/
  audio/
  references/
~~~

Em `references/`, salve links, screenshots autorizados ou notas de vídeos de referência. Referência serve para **pacing, composição, tipografia, câmera e transições**; não para copiar marca, texto ou frames de terceiros.

### 2. Capture a condição comercial

~~~powershell
python .\scripts\product_snapshot.py "URL_DO_PRODUTO" --out ".\data\produto\offer.json"
~~~

A página é volátil. O snapshot registra a condição observada; informações críticas ainda devem ser conferidas.

### 3. Crie um job

~~~powershell
powershell -ExecutionPolicy Bypass -File .\scripts\new-creative.ps1 -Slug "produto" -Objective "conversion" -Renderer "auto"
~~~

O job já nasce com pastas para `Storyboards`, `Stills`, `Renders`, `Previews` e notas de direção.

### 4. Faça o preflight

~~~powershell
powershell -ExecutionPolicy Bypass -File .\scripts\preflight-renderer.ps1 -Renderer auto
~~~

### 5. Abra no Claude Code ou Codex

Use:

~~~text
Leia AGENTS.md, docs/WORKFLOW.md e o brief do job.
Inspecione os assets e referências.
Gere 3 storyboards realmente diferentes.
Gere um still por cena antes de animar.
Escolha o renderer pelo docs/RENDERER-ROUTING.md.
Faça QA visual e comercial antes do export.
~~~

## Fluxo em uma linha

~~~text
produto + oferta + brand kit + referências
                  ↓
       3 direções de storyboard
                  ↓
          still de cada cena
                  ↓
          seleção / correção
                  ↓
     Tesseract | HyperFrames | Remotion
                  ↓
      notas de direção específicas
                  ↓
        9:16 | 4:5 | 1:1 + QA
~~~

## Estrutura

~~~text
assets/      assets reais e referências
briefs/      briefs e template
data/        snapshots comerciais
docs/        workflow, routing, QA, direção e guardrails
outputs/     jobs, storyboards, stills, projetos e renders
prompts/     prompts reutilizáveis para agentes
schemas/     exemplos de request e storyboard
scripts/     setup, ingestão, preflight e validação
~~~

## Documentos importantes

- `docs/WORKFLOW.md` — fluxo completo em gates.
- `docs/RENDERER-ROUTING.md` — quando usar Tesseract, HyperFrames, Remotion ou híbrido.
- `docs/REFERENCE-DIRECTION.md` — como extrair linguagem visual de referências sem copiar.
- `docs/STORYBOARD-AND-STILLS.md` — 3 variantes e aprovação por still.
- `docs/DIRECTOR-NOTES.md` — vocabulário para iteração precisa.
- `docs/OFFER-TRUTH.md` — fonte da verdade de preço/condições.
- `docs/QA-PAID-MEDIA.md` — checklist antes de entregar.
- `docs/PAID-MEDIA-PLAYBOOK.md` — princípios de criativos de performance.
- `docs/CREATIVE-MATRIX.md` — variações que testam hipóteses.

## Prompts prontos

- `prompts/product-ad-master.txt`
- `prompts/reference-deconstruction.txt`
- `prompts/storyboard-3x.txt`
- `prompts/director-pass.txt`
- `prompts/variant-batch.txt`
- `prompts/creative-audit.txt`

## Sobre "one prompt"

O Lab assume que o melhor resultado normalmente não vem de uma frase mágica. O contexto é parte do trabalho: assets, brand kit, referências, oferta, storyboard, stills e notas específicas reduzem o espaço de decisão do agente e tornam o vídeo reproduzível.
