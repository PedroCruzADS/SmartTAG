# Workflow de produção

## 1. Fonte da verdade
Toda peça deve nascer de fontes verificáveis: assets locais, URL do produto, dados comerciais fornecidos pelo usuário ou snapshot salvo em `data/`.

Nunca inferir preço, desconto, parcelamento, frete, estoque, cupom ou benefício.

## 2. Ingestão
1. Criar uma pasta de trabalho com `scripts/new-creative.ps1`.
2. Salvar assets em `assets/<slug>/`.
3. Se houver URL, gerar snapshot com `scripts/product_snapshot.py`.
4. Preencher o brief usando `briefs/TEMPLATE.md`.

## 3. Produção
- abrir no Claude Code/Codex;
- ler `AGENTS.md`;
- instalar/verificar Tesseract;
- criar `.tsrct`;
- importar assets reais;
- montar a peça;
- gerar preview + filmstrip;
- revisar;
- exportar MP4.

## 4. Variações
Depois de aprovar a master:
- variar hook;
- variar headline;
- variar CTA;
- adaptar 9:16, 4:5 e 1:1;
- preservar produto e condições.

## 5. Entrega
Cada peça deve conter:
- projeto `.tsrct`;
- MP4 final;
- filmstrip;
- brief usado;
- snapshot comercial usado;
- notas da versão.
