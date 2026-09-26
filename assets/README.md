# Assets

Coloque aqui os arquivos reais do criativo, organizados por produto.

Estrutura sugerida:

~~~text
assets/<slug>/
  product/
  lifestyle/
  logo/
  fonts/
  audio/
  references/
~~~

Depois rode:

~~~bash
python scripts/validate_assets.py assets/<slug> --strict
python scripts/asset_manifest.py assets/<slug> --out outputs/<job>/Source/assets-manifest.json
~~~

O agente não deve inventar produto, logo, preço ou oferta para preencher arquivos ausentes.

Conteúdo real de assets/ é ignorado pelo Git por padrão para evitar publicação acidental de material comercial/licenciado.
