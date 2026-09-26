# Troubleshooting

## Tesseract não encontrado

Rode:

~~~bash
python scripts/check_environment.py
python scripts/preflight_renderer.py --renderer tesseract
~~~

Prefira tsrct no PATH. A skill oficial deve orientar instalação e versão compatível.

## Linux

Tesseract 0.2.0 adicionou Linux x86_64 e ambientes cloud-agent compatíveis. WSL não deve ser tratado automaticamente como equivalente a uma distribuição suportada; siga os requisitos da skill/CLI instalada.

## HyperFrames falha no doctor

Rode:

~~~bash
python scripts/preflight_renderer.py --renderer hyperframes --deep
~~~

HyperFrames exige Node.js 22+ e FFmpeg/FFprobe. O doctor em JSON deve ser avaliado pelo campo ok, não apenas pelo exit code.

## Remotion não inicia

Confirme Node.js, dependências e versões compatíveis entre remotion e @remotion/*. Use as Agent Skills oficiais e o setup do projeto.

## Snapshot vazio/incompleto

Algumas páginas renderizam preço/condições via JavaScript ou APIs. O snapshot captura HTML/JSON-LD disponível e é conservador quando há múltiplos preços.

Se a condição não aparecer, use outra fonte autorizada. Não preencha por inferência.

## Snapshot bloqueia URL privada

É intencional: o script reduz risco de SSRF/prompt-driven requests a localhost/rede privada. Use --allow-private-network apenas quando você controla a URL e realmente precisa disso.

## Asset não abre

Preserve o original. Gere derivado somente quando necessário e mantenha o original + manifest.

## Fonte ausente

Não substitua silenciosamente fonte de marca. Importe a correta ou registre limitação.

## Preview bom, render ruim

Preview/snapshot é amostragem. Valide o arquivo final com FFprobe:

~~~bash
python scripts/validate_render.py <arquivo.mp4> --canvas 1080x1920 --duration 9 --fps 30
~~~

## Condição mudou

Capture snapshot novo e compare:

~~~bash
python scripts/compare_offer.py old.json new.json --fail-on-change
~~~

Depois use prompts/offer-refresh.txt.

## Arquivos não aparecem no Git

assets/, data/ e outputs/ são ignorados por padrão para evitar vazamento/bloat. Isso é intencional. Versione mídia deliberadamente com solução apropriada quando necessário.
