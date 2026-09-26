# Storyboard e still gate

## Por que 3 variantes

Pedir 3 storyboards transforma a primeira decisão do agente em uma escolha comparável. As variantes devem testar direções, não trocar apenas cor ou headline.

## Critério de diferença

Cada variante deve mudar pelo menos 2 destes eixos:
- estrutura narrativa;
- hook;
- ritmo;
- composição;
- tratamento do produto;
- forma de apresentar a oferta;
- tipo de transição;
- intensidade de câmera.

## Storyboard mínimo

Cada cena precisa de:
- `id`;
- `start_s` / `duration_s`;
- `purpose`;
- `assets`;
- `copy`;
- `composition`;
- `motion_intent`;
- `transition_out`;
- `truth_sources`;
- `notes`.

Use `schemas/storyboard.example.json` como referência.

## Still gate

Depois da direção selecionada, gere um frame estático representativo de cada cena.

Revise:
- fidelidade do produto;
- logo;
- preço/condição;
- contraste;
- tipografia;
- margens/safe area;
- coerência entre cenas;
- posição do CTA;
- excesso de elementos.

Não avance para motion se o still ainda está errado.

## Aprovação automática quando necessário

Se não houver usuário disponível para escolher entre as 3 direções:
1. compare cada variante contra o brief;
2. descarte qualquer uma que viole uma restrição;
3. escolha a que cobre melhor objetivo, hierarquia e assets disponíveis;
4. registre a decisão em `notes.md`;
5. não invente critérios de preferência pessoal.
