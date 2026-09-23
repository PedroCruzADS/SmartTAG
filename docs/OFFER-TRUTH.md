# Regra de verdade comercial

Preço e condições do site são dados voláteis.

## Hierarquia das fontes
1. dados explicitamente fornecidos pelo usuário para a campanha;
2. snapshot salvo em `data/` com URL e timestamp;
3. conteúdo visível no asset;
4. nenhuma informação.

Se houver conflito, não escolher silenciosamente. Registrar o conflito e usar a fonte explicitamente priorizada pelo usuário.

## Nunca inventar
- preço de/por;
- % OFF;
- quantidade de parcelas;
- valor de parcela;
- desconto no PIX;
- cupom;
- frete grátis;
- prazo;
- estoque;
- garantia;
- especificação técnica.

## Snapshot
Snapshots comerciais devem guardar, quando disponível:
- URL;
- título;
- SKU;
- preço;
- preço anterior;
- disponibilidade;
- imagem principal;
- timestamp;
- texto bruto relevante.

Toda peça deve conseguir apontar qual snapshot/brief originou a oferta.
