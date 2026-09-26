# Workflow de produção

Este workflow transforma o princípio "contexto antes do render" em gates explícitos.

## Gate 0 — fonte da verdade

Toda peça nasce de:
- instrução explícita da campanha;
- assets locais autorizados;
- URL/snapshot comercial;
- brand kit fornecido;
- referências visuais declaradas.

Nunca inferir preço, desconto, parcelamento, frete, estoque, cupom, benefício técnico ou urgência.

## Gate 1 — contexto e ingestão

1. Crie um job com `scripts/new-creative.ps1`.
2. Salve assets em `assets/<slug>/`.
3. Coloque referências em `assets/<slug>/references/`.
4. Gere snapshot da oferta, quando houver URL.
5. Preencha `brief.md` e `request.json`.
6. Rode `scripts/validate-job.py` e `scripts/preflight-renderer.ps1`.

O agente deve conseguir responder, antes de criar:
- o que está vendendo?
- qual é a condição comprovada?
- qual é o objetivo da mídia?
- qual é a hierarquia visual?
- quais assets podem ser usados?
- quais atributos das referências são desejados?
- quais restrições não podem ser violadas?

## Gate 2 — deconstrução de referências

Use `prompts/reference-deconstruction.txt`.

Para cada referência, extraia somente atributos reutilizáveis:
- duração e densidade;
- hook;
- ritmo de cortes;
- hierarquia tipográfica;
- proporção produto/texto;
- movimentos de câmera;
- tipos de transição;
- fundo e tratamento de luz;
- uso de UI;
- clímax/payoff;
- sensação geral.

Não peça "copie este vídeo". Transforme a referência em direção.

## Gate 3 — três storyboards

Use `prompts/storyboard-3x.txt`.

As 3 variantes devem divergir de verdade. Exemplo:
- A: produto hero + oferta rápida;
- B: problema/benefício + demonstração;
- C: editorial/cinemático + payoff comercial.

Cada cena deve registrar:
- objetivo;
- duração;
- assets;
- copy;
- composição;
- movimento pretendido;
- transição;
- fonte de verdade usada;
- risco/observação.

Não anime ainda.

## Gate 4 — stills antes de motion

Depois da escolha:
1. gere um still representativo por cena;
2. verifique produto, logo, preço, tipografia, margens e safe areas;
3. corrija composição;
4. só então anime.

Stills são baratos de corrigir; motion ruim é caro de retrabalhar.

## Gate 5 — roteamento e produção

Leia `docs/RENDERER-ROUTING.md`.

Registre em `notes.md`:
- renderer;
- motivo;
- versão/skill relevante;
- limitações conhecidas.

Construa a master no formato principal.

## Gate 6 — direção e iteração

Assista a master e anote mudanças em linguagem operacional:
- "reduza o push-in da cena 2 para 70%";
- "hard cut entre 2 e 3";
- "segure o preço 8 frames antes do CTA";
- "desacelere o zoom final";
- "mova o produto 6% à direita";
- "troque fade por wipe horizontal".

Veja `docs/DIRECTOR-NOTES.md`.

## Gate 7 — QA

Faça:
- QA comercial;
- QA de produto;
- QA visual;
- QA de legibilidade mobile;
- QA de pacing;
- QA técnico do renderer.

Para HyperFrames, use lint/check/snapshot quando aplicável.
Para Tesseract, gere preview/filmstrip.
Para Remotion, gere stills/Studio preview e valide a composição.

## Gate 8 — export e variações

Só depois da master aprovada:
- adapte 9:16, 4:5 e 1:1;
- varie hook, headline ou CTA uma hipótese por vez;
- preserve oferta e produto;
- registre as diferenças.

## Entrega

Cada job deve reter:
- projeto/código editável;
- MP4 master;
- variantes;
- `Storyboards/storyboard.json`;
- `Stills/`;
- preview/filmstrip;
- brief;
- request;
- snapshot comercial;
- notas de direção.
