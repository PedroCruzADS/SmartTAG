from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from tooling import (
    VALID_APPROVAL,
    VALID_CANVASES,
    VALID_FPS,
    VALID_RENDERERS,
    repo_root,
    validate_slug,
)

FORMAT_LABELS = {
    "1080x1920": "9x16",
    "1080x1350": "4x5",
    "1080x1080": "1x1",
}


def next_job_dir(
    root: Path,
    slug: str,
    objective: str,
    canvas: str,
    now: datetime,
) -> Path:
    stem = (
        f"{now.strftime('%Y%m%d')}_{slug}_{objective}_"
        f"{FORMAT_LABELS[canvas]}"
    )
    for version in range(1, 100):
        candidate = root / f"{stem}_v{version:02d}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(
        f"Nao foi possivel encontrar versao livre para {stem} (v01-v99)."
    )


def create_job(
    root: Path,
    slug: str,
    objective: str = "conversion",
    renderer: str = "auto",
    duration_seconds: int = 9,
    fps: int = 30,
    canvas: str = "1080x1920",
    approval_mode: str = "human",
    now: datetime | None = None,
) -> Path:
    slug = validate_slug(slug, "slug")
    objective = validate_slug(objective, "objective")
    if renderer not in VALID_RENDERERS:
        raise ValueError(f"renderer invalido: {renderer}")
    if canvas not in VALID_CANVASES:
        raise ValueError(f"canvas invalido: {canvas}")
    if fps not in VALID_FPS:
        raise ValueError(f"fps invalido: {fps}")
    if approval_mode not in VALID_APPROVAL:
        raise ValueError(f"approval_mode invalido: {approval_mode}")
    if duration_seconds < 1 or duration_seconds > 120:
        raise ValueError("duration_seconds deve estar entre 1 e 120.")

    now = now or datetime.now().astimezone()
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    job = next_job_dir(outputs, slug, objective, canvas, now)
    for name in (
        "Storyboards",
        "Stills",
        "Previews",
        "Renders",
        "Source",
    ):
        (job / name).mkdir(parents=True, exist_ok=True)

    job_id = job.name
    brief = f"""# Brief local — {slug}

## Objetivo
{objective}

## Produto
- URL:
- SKU:
- Beneficio comprovado:

## Oferta
- Snapshot: data/{slug}/offer.json
- Preco:
- Parcelamento:
- PIX:
- Cupom:
- Frete:

## Brand kit
- Logo:
- Cores:
- Fontes:

## Referencias
### A
- URL/arquivo:
- Usar:
- Nao copiar:

### B
- URL/arquivo:
- Usar:
- Nao copiar:

## Formato
- Canvas: {canvas}
- Duracao: {duration_seconds}s
- FPS: {fps}

## Renderer
- Preferencia: {renderer}

## Approval gates
- Storyboard: {approval_mode}
- Stills: {approval_mode}
- Preview final: {approval_mode}

## Assets autorizados
- assets/{slug}/

## Restricoes
- nao recriar/alterar produto
- nao inventar claims/oferta

## Storyboard
Gerar 3 variantes antes de motion e um still por cena antes do render.
"""

    request = {
        "schema_version": 1,
        "job_id": job_id,
        "created_at": now.isoformat(),
        "product_slug": slug,
        "objective": objective,
        "channel": "meta_ads",
        "placements": ["reels", "stories"],
        "canvas": canvas,
        "duration_seconds": duration_seconds,
        "fps": fps,
        "renderer": renderer,
        "offer_snapshot": f"data/{slug}/offer.json",
        "assets_dir": f"assets/{slug}",
        "brand": {
            "logo": "",
            "fonts": [],
            "colors": [],
            "rules": [],
        },
        "references": [],
        "copy": {
            "hook": "",
            "headline": "",
            "support": "",
            "cta": "",
        },
        "storyboard": {
            "variants": 3,
            "require_stills_before_motion": True,
        },
        "approval": {
            "storyboard": approval_mode,
            "stills": approval_mode,
            "final_preview": approval_mode,
        },
        "variants": {
            "hooks": 2,
            "ctas": 2,
            "formats": [
                "1080x1920",
                "1080x1350",
                "1080x1080",
            ],
        },
        "constraints": {
            "no_product_recreation": True,
            "no_unverified_claims": True,
        },
    }

    def gate() -> dict[str, object]:
        return {
            "mode": approval_mode,
            "status": "pending",
            "approved_at": None,
            "approved_by": None,
            "actor_type": None,
            "note": "",
        }

    approvals = {
        "schema_version": 1,
        "gates": {
            "storyboard": gate(),
            "stills": gate(),
            "final_preview": gate(),
        },
    }

    request_payload = (
        json.dumps(request, ensure_ascii=False, indent=2) + chr(10)
    )
    approvals_payload = (
        json.dumps(approvals, ensure_ascii=False, indent=2) + chr(10)
    )
    notes = """# Notes

## Renderer decision
- Pending

## Director notes
"""

    (job / "brief.md").write_text(brief, encoding="utf-8")
    (job / "request.json").write_text(
        request_payload,
        encoding="utf-8",
    )
    (job / "approvals.json").write_text(
        approvals_payload,
        encoding="utf-8",
    )
    (job / "notes.md").write_text(notes, encoding="utf-8")
    print(f"Job criado: {job.relative_to(root).as_posix()}")
    return job


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Cria um job seguro e versionado "
            "do Tesseract Creative Lab."
        )
    )
    ap.add_argument("--slug", required=True)
    ap.add_argument("--objective", default="conversion")
    ap.add_argument(
        "--renderer",
        choices=VALID_RENDERERS,
        default="auto",
    )
    ap.add_argument("--duration-seconds", type=int, default=9)
    ap.add_argument(
        "--fps",
        type=int,
        choices=VALID_FPS,
        default=30,
    )
    ap.add_argument(
        "--canvas",
        choices=VALID_CANVASES,
        default="1080x1920",
    )
    ap.add_argument(
        "--approval-mode",
        choices=VALID_APPROVAL,
        default="human",
    )
    args = ap.parse_args()
    try:
        create_job(
            repo_root(),
            args.slug,
            args.objective,
            args.renderer,
            args.duration_seconds,
            args.fps,
            args.canvas,
            args.approval_mode,
        )
    except (ValueError, RuntimeError) as exc:
        ap.error(str(exc))


if __name__ == "__main__":
    main()
