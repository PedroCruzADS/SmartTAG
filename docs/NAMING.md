# Convenção de nomes

## Job

YYYYMMDD_produto_objetivo_formato_vNN

Exemplo:

20260926_esteira-b55_conversion_9x16_v01

scripts/new_creative.py cria a próxima versão livre automaticamente.

## Estrutura do job

- brief.md
- request.json
- approvals.json
- notes.md
- Storyboards/storyboard.json
- Stills/<scene-id>.png
- Previews/
- Renders/
- Source/assets-manifest.json

## Master final

Prefira:

- Renders/master.mp4
- Renders/master_9x16.mp4 quando houver múltiplos formatos

## Fonte editável

Depende do renderer:

- Tesseract: projeto .tsrct
- HyperFrames: composição/código na pasta Source ou estrutura do projeto
- Remotion: projeto React/Remotion
- Hybrid: registre claramente os dois artefatos e a ordem de montagem

## Variações

Sufixos úteis:

- _hook-a
- _hook-b
- _cta-a
- _price-focus
- _benefit-focus

Evite final-final2.mp4.
