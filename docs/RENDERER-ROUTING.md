# Renderer routing

O Lab é renderer-agnostic. Use o que reduz risco e retrabalho para o job.

## Auto-routing

### Tesseract
Prefira quando houver:
- footage real;
- edição temporal tradicional;
- máscaras e compositing;
- speed ramps/retiming;
- acabamento sobre material já renderizado;
- necessidade de projeto visual editável no Tesseract.

### HyperFrames
Prefira quando houver:
- motion graphics baseado em layout;
- produto recortado + tipografia + cards + shapes;
- transições determinísticas;
- necessidade de iteração rápida por agente;
- comparação de snapshots;
- composição HTML/CSS/GSAP;
- peça curta de performance com muita precisão de timing.

Requisitos: Node.js 22+ e FFmpeg.

Preflight:
~~~powershell
npx hyperframes doctor
npx hyperframes skills check
~~~

Ciclo:
~~~powershell
npx hyperframes lint <composicao>
npx hyperframes check <composicao>
npx hyperframes snapshot <composicao>
npx hyperframes preview
npx hyperframes render
~~~

Consulte `npx hyperframes <comando> --help`: a versão instalada é a autoridade.

### Remotion
Prefira quando houver:
- React/components;
- templates reutilizáveis;
- muitas variações parametrizadas;
- dados estruturados alimentando cenas;
- reuso de componentes entre produtos;
- necessidade de render de stills e vídeos a partir da mesma composição.

Skills:
~~~powershell
npx -y skills@latest add remotion-dev/skills -g -y
~~~

Para um projeto novo:
~~~powershell
npx create-video@latest --yes --blank my-video
~~~

### Hybrid
Use quando a combinação reduzir risco. Exemplos:
- HyperFrames para motion + Tesseract para footage/compositing;
- Remotion para lote/parametrização + Tesseract para master hero;
- HyperFrames para opening/price cards + editor para montagem final.

Registre quais etapas pertencem a cada renderer.

## 21st.dev

21st.dev é opcional e **não é um renderer**.

Use quando o produto anunciado for software ou quando uma cena exigir UI plausível/consistente. Para produto físico, prefira componentes próprios do brand kit e assets reais.

Instalação de skill:
~~~powershell
npx @21st-dev/cli install-skill
~~~

Não introduza componentes do 21st apenas para "deixar bonito". Eles devem servir a uma cena e respeitar identidade/brand kit.

## Matriz rápida

| Job | Rota sugerida |
| --- | --- |
| Produto físico + tipografia + preço + motion | HyperFrames |
| UGC/footage + overlays + speed ramp | Tesseract |
| 100 SKUs a partir de um template | Remotion |
| SaaS com telas e UI | Remotion/HyperFrames + 21st opcional |
| Motion programático + acabamento editorial | Hybrid |
| Um único hero film complexo com footage | Tesseract/Hybrid |

## Regra de decisão

"Auto" significa escolher pelo **custo de alteração futura**, não pela velocidade do primeiro render.

Se o criativo vai gerar dezenas de variações, parametrização pesa mais.
Se haverá muita máscara/footage, compositing pesa mais.
Se haverá muitas microcorreções de layout/timing, determinismo pesa mais.
