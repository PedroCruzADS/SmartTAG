# Renderer routing

Escolha o renderer que reduz risco e custo de alteração futura.

A disponibilidade local é apenas um filtro; não é o critério criativo.

## Tesseract

Prefira quando houver:

- footage real;
- edição temporal tradicional;
- máscaras/compositing;
- speed ramps/retiming;
- acabamento sobre material renderizado;
- necessidade de projeto .tsrct editável.

A versão 0.2.0 adicionou suporte a Linux x86_64, além de macOS e Windows. Use a skill oficial para requisitos/instalação da versão atual e verificação de checksum.

Setup de skills:

~~~bash
npx skills add mirage-hq/Tesseract
~~~

Não assuma path fixo. O Lab considera Tesseract pronto quando encontra tsrct/tsrct.cmd no PATH, com fallback Windows legado.

## HyperFrames

Prefira quando houver:

- produto recortado + tipografia/cards/shapes;
- layout/motion determinístico;
- microajustes frequentes de timing;
- HTML/CSS/GSAP;
- necessidade de snapshots/comparação;
- peça curta de performance.

Requisitos atuais: Node.js 22+ e FFmpeg/FFprobe.

Preflight:

~~~bash
python scripts/preflight_renderer.py --renderer hyperframes --deep
~~~

Loop recomendado:

~~~bash
npx hyperframes check --strict
npx hyperframes snapshot --at 0.5,2.0,5.0
npx hyperframes preview
# aprovação final
npx hyperframes render --output Renders/master.mp4
~~~

check já inclui lint/runtime/layout checks. inspect, validate e layout são aliases depreciados e não devem entrar em instruções novas.

doctor --json pode sair com código 0 mesmo quando há problemas; em automação, leia o campo ok. O preflight do Lab faz isso.

## Remotion

Prefira quando houver:

- React/componentização;
- templates reutilizáveis;
- lotes e muitas variações;
- dados estruturados alimentando cenas;
- reuso entre produtos/formatos.

Skills:

~~~bash
npx -y skills@latest add remotion-dev/skills -g -y
~~~

Projeto novo:

~~~bash
npx create-video@latest --yes --blank my-video
~~~

A documentação atual exige pelo menos Node.js 16. Siga requisitos da versão instalada e mantenha remotion e @remotion/* em versões compatíveis.

## Hybrid

Use quando separar responsabilidades reduzir retrabalho, por exemplo:

- HyperFrames para motion cards + Tesseract para footage/compositing;
- Remotion para lote + Tesseract para master hero;
- renderer programático para overlays + editor para montagem final.

Registre em notes.md quais etapas pertencem a cada ferramenta.

## 21st.dev

21st.dev é opcional e não é renderer.

Use somente quando uma cena precisar de UI plausível de software. A instalação de skill oficial é:

~~~bash
npx @21st-dev/cli install-skill
~~~

Componentes entram como código de terceiros: revise diff, dependências, tokens e estilos. Não use por estética genérica em anúncio de produto físico.

## Matriz rápida

| Job | Rota provável |
| --- | --- |
| Produto físico + tipografia + preço | HyperFrames |
| UGC/footage + overlays + speed ramp | Tesseract |
| 100 SKUs parametrizados | Remotion |
| SaaS com telas reais | Remotion/HyperFrames + 21st opcional |
| Motion programático + acabamento editorial | Hybrid |
| Hero film com footage complexo | Tesseract/Hybrid |

## Auto

auto escolhe pelo custo esperado de revisão:

- muita parametrização → Remotion ganha peso;
- muita máscara/footage → Tesseract ganha peso;
- muitas microcorreções de layout/timing → HyperFrames ganha peso;
- responsabilidades distintas → Hybrid.
