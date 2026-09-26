# Guia de assets

## Estrutura recomendada

~~~text
assets/<slug-produto>/
  product/
  lifestyle/
  logo/
  fonts/
  audio/
  references/
~~~

## Preferências

- PNG/WebP com transparência para recortes;
- imagens em alta resolução;
- vídeos sem overlays queimados quando possível;
- SVG/PNG oficial para logo;
- fontes oficiais;
- referências separadas de assets reutilizáveis.

## Validação e manifest

~~~bash
python scripts/validate_assets.py assets/<slug> --strict
python scripts/asset_manifest.py assets/<slug> --out outputs/<job>/Source/assets-manifest.json
~~~

O manifest registra path, tamanho e SHA-256 para deixar claro quais arquivos foram autorizados e usados.

## Referência não é asset

Arquivos em references/ servem para direção visual. Não copie logos, textos, produtos, música ou elementos proprietários para a peça.

## Produto

Nunca use geração de imagem para reconstruir o produto quando existe fotografia real fornecida.

## Derivados

Se precisar remover fundo, converter formato ou gerar proxy:

- preserve original;
- salve derivado separadamente;
- registre transformação em notes.md;
- não altere característica visual do produto.

## Git

Conteúdo real de assets/ é ignorado por padrão. Isso reduz risco de publicar material comercial/licenciado sem intenção.
