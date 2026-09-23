# Agent instructions — Tesseract Creative Lab

Você está em um laboratório de produção de criativos de performance para e-commerce, com foco atual na Casa do Fitness.

## Antes de qualquer criação

Leia:
1. `docs/WORKFLOW.md`
2. `docs/OFFER-TRUTH.md`
3. `docs/QA-PAID-MEDIA.md`
4. o brief específico
5. o snapshot comercial associado, quando existir

Inspecione visualmente os assets autorizados.

## Regras obrigatórias

- Rode Tesseract localmente. Não tente GitHub Actions, Linux, WSL ou cloud rendering.
- Leia as skills oficiais instaladas do Tesseract e respeite a versão de CLI fixada.
- Nunca edite `.tsrct` como JSON/ZIP bruto.
- Use `project checkout` / `project commit` para documento e `project apply` para ações suportadas.
- Consulte `project schema` e `project schema --document`; não invente campos.
- Faça preview e filmstrip antes de exportar.
- Preserve assets originais e projetos anteriores.
- Não gere substitutos de IA para um produto real disponível.
- Não altere cor, proporção, componentes ou características do produto.
- Não redesenhe logos.
- Não invente fatos comerciais ou técnicos.
- Nunca calcule/assuma desconto, parcela, PIX, frete, cupom, urgência ou estoque sem fonte.
- Se a fonte estiver ausente/conflitante, omita a afirmação ou registre o conflito.
- Mantenha elementos editáveis sempre que possível.
- Priorize legibilidade mobile e hierarquia de performance.

## Fonte da verdade

Ordem:
1. instrução explícita do usuário para a campanha;
2. snapshot comercial versionado;
3. informação claramente presente no asset autorizado;
4. omitir.

A página de produto e condições comerciais são voláteis. Registre timestamp/URL quando usar dados capturados.

## Fluxo

1. Verifique host e Tesseract.
2. Leia brief + snapshot.
3. Inspecione assets.
4. Crie pasta nova em `outputs/`.
5. Crie `Project.tsrct`.
6. Importe assets.
7. Construa a peça.
8. Preview.
9. Filmstrip.
10. Audite com `docs/QA-PAID-MEDIA.md`.
11. Corrija.
12. Exporte MP4.
13. Retenha projeto, filmstrip, brief, snapshot e notas.

## Variações

Depois de uma master aprovada:
- prefira mudar uma hipótese por vez;
- registre o que foi alterado;
- adapte composição em vez de simplesmente esticar/cortar;
- preserve a fonte comercial da master.

Leia `docs/CREATIVE-MATRIX.md` para lotes.

## Formatos iniciais

- 1080x1920
- 1080x1350
- 1080x1080

Não trate especificações de plataforma como permanentes; confirme requisitos atuais quando forem relevantes.

## Entrega

A versão final deve conter, quando aplicável:
- `Project.tsrct`
- `Project.mp4`
- `Previews/Filmstrip.png`
- `brief.md`
- `offer.json`
- `notes.md`

Ao final, informe:
- MP4;
- projeto editável;
- fontes de verdade usadas;
- variação/hipótese;
- limitações ou conflitos encontrados.
