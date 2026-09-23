# Troubleshooting

## Tesseract não encontrado
Rode `scripts/check-environment.ps1` e depois `scripts/bootstrap.ps1`.
A skill oficial deve determinar a versão correta do CLI.

## npx não encontrado
Instale Node.js/npm ou peça ao agente para seguir manualmente a instalação oficial da Mirage.

## Linux/WSL
Não usar. O Tesseract atual exige macOS ou Windows 64-bit e execução local.

## Snapshot vazio/incompleto
Algumas páginas renderizam preço/condições via JavaScript ou APIs internas. O script de snapshot captura dados estruturados disponíveis no HTML; ele não deve ser tratado como prova absoluta. Se preço/parcelamento não aparecerem, confirme por outra fonte autorizada.

## Asset não abre
Preserve o original. Gere derivado somente quando necessário e mantenha registro do processo.

## Fonte ausente
Não substituir silenciosamente uma fonte de marca solicitada. Importe a fonte correta ou registre a limitação.

## Filmstrip bom, vídeo ruim
Assista ao MP4 final. Filmstrip é amostragem e pode não revelar flashes, frames únicos, áudio ou problemas entre amostras.

## Condição mudou
Capture um snapshot novo e rode:

```powershell
python .\scripts\compare_offer.py .\data\produto\offer-old.json .\data\produto\offer-new.json
```

Depois use `prompts/offer-refresh.txt`.
