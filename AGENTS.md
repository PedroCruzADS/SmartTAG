# Agent instructions — Tesseract Creative Lab

Você está trabalhando em um projeto de criativos da Casa do Fitness.

## Regras obrigatórias

- Rode Tesseract **localmente**. Não tente usar GitHub Actions, Linux, WSL ou cloud rendering.
- Antes de editar, leia as skills oficiais instaladas do Tesseract e siga a versão de CLI fixada por elas.
- Nunca trate um arquivo `.tsrct` como JSON bruto nem edite seu ZIP internamente.
- Use `tsrct project checkout` + `project commit` quando precisar editar o documento.
- Use `project schema` e `project schema --document` antes de construir ações/estrutura. Não invente campos.
- Faça preview e filmstrip antes do export final.
- Preserve assets originais.
- Use somente os assets reais fornecidos em `assets/`.
- Não invente ou altere características físicas do produto.
- Não redesenhe logos.
- Não invente preço, desconto, parcelamento, frete ou qualquer condição comercial.
- Se o brief não trouxer uma informação comercial, deixe-a de fora.
- Priorize legibilidade mobile e safe areas para Meta Ads.
- Mantenha textos e elementos editáveis sempre que possível.

## Fluxo esperado

1. Verificar sistema e Tesseract.
2. Ler `briefs/casa-do-fitness-promo.md`.
3. Inspecionar todos os assets disponíveis.
4. Criar uma pasta nova dentro de `outputs/` para cada tentativa.
5. Criar um novo projeto `.tsrct`.
6. Importar assets.
7. Construir o criativo.
8. Renderizar frame de preview.
9. Renderizar filmstrip cobrindo toda a animação.
10. Revisar layout, cortes, timing e legibilidade.
11. Corrigir problemas.
12. Exportar MP4 final.
13. Manter o `.tsrct`, MP4 e previews juntos.

## Formatos preferenciais

Primeiro teste:
- 1080x1920
- 8–10 segundos
- vertical 9:16
- foco em performance / Meta Ads

Depois, se solicitado:
- 1080x1350
- 1080x1080

## Direção visual inicial

- Visual premium, direto e comercial.
- Produto é o elemento principal.
- Não esconder partes importantes do produto com texto.
- Animação suave, limpa e curta.
- Evitar motion excessivo.
- Headline deve ser entendida rapidamente.
- CTA e oferta devem ter hierarquia clara.
- Não usar assets gerados por IA no lugar do produto real.

## Entrega

Dentro da pasta da versão:
- `Project.tsrct`
- `Project.mp4`
- `Previews/Filmstrip.png`
- previews adicionais úteis
- notas de decisões em `.tesseract-work/`

Ao final, informe:
- caminho do MP4
- caminho do projeto editável
- resumo curto do que foi feito
- qualquer limitação encontrada
