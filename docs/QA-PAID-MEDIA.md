# QA — Paid Media

Checklist obrigatório antes de considerar uma peça pronta.

## Produto

- produto corresponde aos assets autorizados;
- proporção/cor/componentes não foram alterados;
- nenhum detalhe físico foi inventado;
- texto/overlays não escondem detalhes relevantes;
- assets usados constam no manifest quando houver.

## Oferta

- preço confere com fonte;
- desconto confere com fonte;
- parcelamento confere;
- cupom/frete conferem;
- nenhuma condição vencida foi reaproveitada;
- múltiplas variantes/preços não foram resolvidos por suposição;
- toda afirmação comercial aponta para brief/snapshot autorizado.

## Layout

- headline/CTA legíveis em mobile;
- contraste suficiente;
- safe areas respeitadas;
- sem clipping/overflow;
- logo íntegro;
- hierarquia clara;
- still de cada cena foi revisado antes de motion.

## Motion

- hook compreensível;
- transições não escondem produto;
- tempo de leitura suficiente;
- sem movimento gratuito;
- encerramento não corta CTA/logo;
- notas de direção foram aplicadas localmente quando possível.

## Gates

- storyboard selecionado e aprovado;
- stills aprovados;
- preview final aprovado;
- approvals.json registra ator, horário e nota quando aplicável.

## Técnico

- projeto/código editável preservado;
- preview existe;
- render final abre;
- resolução/FPS/duração validados com scripts/validate_render.py;
- áudio conferido quando houver;
- naming segue docs/NAMING.md.

## Renderer

Não exigir arquivo .tsrct quando o job foi feito em HyperFrames/Remotion. A entrega editável depende da rota escolhida.
