# Reference-directed video workflow

Este fluxo transforma referências visuais em direção, não em cópia literal.

## Pipeline
1. **Context pack** — brief, offer truth, brand kit, assets reais, screenshots e 1–2 referências.
2. **Reference analysis** — descreva pacing, composição, tipografia, câmera, transições e densidade. Não copie logos, texto, produto ou elementos proprietários.
3. **3 storyboards** — gere três direções realmente distintas antes de implementar.
4. **Seleção** — escolha uma direção e registre o porquê em `direction.md`.
5. **Still gate** — gere um still representativo de cada cena. Não anime enquanto composição, produto, copy e oferta não estiverem corretos.
6. **Renderer routing** — escolha Tesseract, Remotion, HyperFrames ou híbrido conforme `docs/RENDERER-ROUTING.md`.
7. **Motion pass** — anime apenas a direção aprovada.
8. **Director notes** — itere com notas específicas: duração, velocidade, corte, push-in, zoom, hold, easing, entrada/saída e foco.
9. **QA** — filmstrip/snapshots + auditoria comercial + visual.
10. **Formats** — adapte conscientemente 9:16, 4:5 e 1:1; não apenas crop.
11. **Export** — preserve fonte, renderer, referência e notas de versão.

## Regra de referências
Referências servem para abstrair linguagem: ritmo, hierarquia, transições e movimento. Não reproduza identidade, assets ou composição distintiva de terceiros de forma literal.

## Context pack mínimo
- objetivo e duração;
- produto e assets autorizados;
- oferta validada;
- logo, cores e fontes reais;
- screenshots reais quando UI/site fizer parte do vídeo;
- 1–2 referências opcionais;
- restrições e claims proibidos;
- formatos de saída.

## Storyboards
Cada variante deve informar:
- hook;
- sequência de cenas;
- duração aproximada por cena;
- mensagem principal;
- asset real usado;
- movimento/câmera;
- transição;
- CTA;
- risco/claim a validar.

## Still gate
Antes de animação, salve `Previews/stills/scene-XX.png` ou equivalente. Reprove qualquer cena que:
- invente produto/UI/logo;
- use condição não validada;
- perca legibilidade mobile;
- dependa de crop destrutivo;
- não tenha hierarquia clara.

## Director notes
Prefira notas mensuráveis: "zoom 0.7x da velocidade", "hold +12 frames", "hard cut", "push-in 4%", "CTA entra 300 ms depois". Evite "deixe melhor" sem critério.
