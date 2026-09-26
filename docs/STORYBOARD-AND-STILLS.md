# Storyboard e still gate

## Por que 3 variantes

A primeira ideia do agente não deve virar render por inércia. Três direções permitem comparar hipóteses antes do custo de animação.

## Diferença mínima

Cada variante deve mudar pelo menos 2 eixos:

- estrutura narrativa;
- hook;
- ritmo;
- composição;
- tratamento do produto;
- apresentação da oferta;
- transições;
- intensidade de câmera.

## Storyboard mínimo

Cada cena registra:

- id;
- start_s / duration_s;
- purpose;
- assets;
- copy;
- composition;
- motion_intent;
- transition_out;
- truth_sources;
- notes.

Salve em Storyboards/storyboard.json e valide contra schemas/storyboard.schema.json.

## Seleção e gate

selected_variant deve apontar para uma das três variantes.

Se o modo do gate for human, o agente apresenta as direções e espera decisão. Ele não pode marcar aprovação humana por conta própria.

Aprovação:

~~~bash
python scripts/approve_gate.py outputs/<job> storyboard --actor-type human --by "Nome"
python scripts/validate_job.py outputs/<job> --stage storyboard
~~~

## Still gate

Depois da direção selecionada, gere um frame estático por cena.

Nomeie pelo ID da cena:

~~~text
A01.png
A02.png
A03.png
~~~

Revise produto, logo, oferta, contraste, tipografia, margens, safe area, coerência e CTA.

A validação do estágio motion exige um still correspondente a cada cena selecionada e gate stills aprovado.

## Auto

Quando approval mode = auto:

1. compare variantes contra brief/restrições;
2. descarte violações;
3. escolha por critérios explícitos;
4. registre selected_variant e justificativa;
5. aprove o gate com actor-type agent;
6. não use gosto pessoal como critério oculto.
