#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQUIRED_REQUEST = [
    "product_slug",
    "objective",
    "canvas",
    "duration_seconds",
    "renderer",
    "assets_dir",
    "storyboard",
    "constraints",
]

VALID_RENDERERS = {"auto", "tesseract", "hyperframes", "remotion", "hybrid"}

def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser(description="Validate a Tesseract Creative Lab job before production.")
    ap.add_argument("job_dir", help="outputs/<job>")
    args = ap.parse_args()

    root = Path(args.job_dir)
    errors = []
    warnings = []

    request_path = root / "request.json"
    brief_path = root / "brief.md"

    if not request_path.exists():
        errors.append("request.json ausente")
    if not brief_path.exists():
        errors.append("brief.md ausente")

    if request_path.exists():
        try:
            req = load_json(request_path)
        except Exception as exc:
            errors.append(f"request.json invalido: {exc}")
            req = {}

        for key in REQUIRED_REQUEST:
            if key not in req:
                errors.append(f"request.json sem campo obrigatorio: {key}")

        if req.get("renderer") not in VALID_RENDERERS:
            errors.append(f"renderer invalido: {req.get('renderer')}")

        storyboard = req.get("storyboard", {})
        if storyboard.get("variants") != 3:
            warnings.append("workflow recomendado usa exatamente 3 variantes de storyboard")
        if storyboard.get("require_stills_before_motion") is not True:
            warnings.append("still gate esta desabilitado")

        assets_dir = Path(req.get("assets_dir", ""))
        if str(assets_dir) and not assets_dir.exists():
            warnings.append(f"assets_dir nao existe localmente: {assets_dir}")

        constraints = req.get("constraints", {})
        if constraints.get("no_product_recreation") is not True:
            warnings.append("no_product_recreation deveria permanecer true")
        if constraints.get("no_unverified_claims") is not True:
            warnings.append("no_unverified_claims deveria permanecer true")

        refs = req.get("references", [])
        if not refs:
            warnings.append("nenhuma referencia declarada; o agente tera mais liberdade visual")

    print("== Job validation ==")
    for item in warnings:
        print(f"[WARN] {item}")
    for item in errors:
        print(f"[ERROR] {item}")

    if errors:
        raise SystemExit(1)

    print("[OK] Estrutura minima valida.")

if __name__ == "__main__":
    main()
