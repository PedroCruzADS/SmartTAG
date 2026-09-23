# Casa do Fitness — Tesseract Creative Lab

Laboratório local para produção de criativos de **mídia paga** usando Tesseract by Mirage com Claude Code ou Codex.

O foco principal é e-commerce: divulgar produtos, benefícios comprovados, preços, descontos, parcelamento, PIX, cupons, frete e campanhas do site sem inventar informações comerciais.

> Tesseract roda localmente. Cloud rendering, Linux e WSL não são suportados atualmente.

## Início rápido

```powershell
git clone https://github.com/PedroCruzADS/tesseract-creative-lab.git
cd tesseract-creative-lab
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
pip install -r requirements.txt
```

## Fluxo recomendado

### 1. Salve os assets
```text
assets/<produto>/
  product/
  lifestyle/
  logo/
  fonts/
  audio/
  references/
```

### 2. Capture uma página de produto
```powershell
python .\scripts\product_snapshot.py "URL_DO_PRODUTO" --out ".\data\produto\offer.json"
```

O snapshot é uma ajuda para registrar a condição encontrada na página. O agente deve validar informações críticas antes de colocá-las em uma peça.

### 3. Crie um job
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\new-creative.ps1 -Slug "produto" -Objective "conversion"
```

### 4. Valide assets
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-assets.ps1 -Path ".\assets\produto"
```

### 5. Abra no Claude Code ou Codex
Use:

```text
Leia AGENTS.md, docs/WORKFLOW.md e o brief do job.
Use Tesseract para criar a peça.
Faça QA visual e comercial antes do export.
```

## Estrutura

```text
assets/      assets reais e referências
briefs/      briefs e template
data/        snapshots comerciais
docs/        workflow, QA, playbooks e guardrails
outputs/     projetos .tsrct, previews e MP4s
prompts/     prompts reutilizáveis
schemas/     exemplos de estruturas de dados
scripts/     setup, ingestão e utilitários
```

## Documentos importantes

- `docs/WORKFLOW.md` — fluxo completo.
- `docs/OFFER-TRUTH.md` — fonte da verdade de preço/condições.
- `docs/QA-PAID-MEDIA.md` — checklist antes de entregar.
- `docs/PAID-MEDIA-PLAYBOOK.md` — princípios de criativos de performance.
- `docs/CREATIVE-MATRIX.md` — como criar variações que testam hipóteses.
- `docs/COPY-GUARDRAILS.md` — limites para copy comercial.
- `docs/ASSET-GUIDE.md` — organização e fidelidade de assets.
- `docs/NAMING.md` — versionamento e nomenclatura.

## Prompts prontos

- `prompts/product-ad-master.txt`
- `prompts/variant-batch.txt`
- `prompts/offer-refresh.txt`
- `prompts/resize-existing.txt`
- `prompts/creative-audit.txt`

## Princípio central

**Produto real + condição verificada + projeto editável + QA antes do render final.**

O lab não deve preencher lacunas comerciais com suposições.
