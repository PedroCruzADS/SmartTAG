from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from tooling import repo_root, safe_repo_path

STAGES = ("ingest", "storyboard", "motion", "render", "final")
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v"}
STILL_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
PREVIEW_EXTS = STILL_EXTS | VIDEO_EXTS


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def schema_errors(instance: object, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda e: [str(p) for p in e.path])
    out = []
    for err in errors:
        where = ".".join(str(p) for p in err.path) or "<root>"
        out.append(f"{schema_path.name}:{where}: {err.message}")
    return out


def resolve_job(root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    path.relative_to((root / "outputs").resolve())
    return path


def matching_still(stills: list[Path], scene_id: str) -> bool:
    return any(path.stem == scene_id or path.stem.startswith(scene_id + "_") for path in stills)


def main() -> None:
    ap = argparse.ArgumentParser(description="Valida um job por schema e por estagio do workflow.")
    ap.add_argument("job_dir", help="outputs/<job>")
    ap.add_argument("--stage", choices=STAGES, default="ingest")
    ap.add_argument("--strict", action="store_true", help="Trata warnings como falha.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = repo_root()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        job = resolve_job(root, args.job_dir)
    except ValueError:
        ap.error("job_dir deve estar dentro de outputs/.")

    request_path = job / "request.json"
    brief_path = job / "brief.md"
    approvals_path = job / "approvals.json"

    for path in (request_path, brief_path, approvals_path):
        if not path.is_file():
            errors.append(f"{path.name} ausente")

    request = {}
    approvals = {}
    if request_path.is_file():
        try:
            request = load_json(request_path)
            errors.extend(schema_errors(request, root / "schemas" / "creative-request.schema.json"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"request.json invalido: {exc}")

    if approvals_path.is_file():
        try:
            approvals = load_json(approvals_path)
            errors.extend(schema_errors(approvals, root / "schemas" / "approval.schema.json"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"approvals.json invalido: {exc}")

    if request:
        for field in ("assets_dir", "offer_snapshot"):
            try:
                target = safe_repo_path(root, str(request.get(field, "")), field)
                if not target.exists():
                    warnings.append(f"{field} nao existe: {target.relative_to(root)}")
            except ValueError as exc:
                errors.append(str(exc))

        requested_modes = request.get("approval", {})
        gate_data = approvals.get("gates", {}) if isinstance(approvals, dict) else {}
        for gate in ("storyboard", "stills", "final_preview"):
            if gate in gate_data and gate in requested_modes and gate_data[gate].get("mode") != requested_modes[gate]:
                errors.append(f"approval mode divergente em {gate}")

    storyboard_path = job / "Storyboards" / "storyboard.json"
    storyboard = {}
    if args.stage in ("storyboard", "motion", "render", "final"):
        if not storyboard_path.is_file():
            errors.append("Storyboards/storyboard.json ausente")
        else:
            try:
                storyboard = load_json(storyboard_path)
                errors.extend(schema_errors(storyboard, root / "schemas" / "storyboard.schema.json"))
                ids = [v.get("id") for v in storyboard.get("variants", []) if isinstance(v, dict)]
                if len(ids) != len(set(ids)):
                    errors.append("storyboard possui IDs de variante duplicados")
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(f"storyboard invalido: {exc}")

    gates = approvals.get("gates", {}) if isinstance(approvals, dict) else {}
    if args.stage in ("storyboard", "motion", "render", "final"):
        selected = storyboard.get("selected_variant") if isinstance(storyboard, dict) else None
        valid_ids = {v.get("id") for v in storyboard.get("variants", []) if isinstance(v, dict)}
        if not selected:
            errors.append("storyboard ainda nao possui selected_variant")
        elif selected not in valid_ids:
            errors.append(f"selected_variant desconhecida: {selected}")
        if gates.get("storyboard", {}).get("status") != "approved":
            errors.append("gate storyboard ainda nao aprovado")

    if args.stage in ("motion", "render", "final") and storyboard:
        selected = storyboard.get("selected_variant")
        variant = next((v for v in storyboard.get("variants", []) if v.get("id") == selected), None)
        stills = [p for p in (job / "Stills").glob("*") if p.is_file() and p.suffix.lower() in STILL_EXTS]
        scene_ids = [str(scene.get("id")) for scene in variant.get("scenes", [])] if variant else []
        missing = [scene_id for scene_id in scene_ids if not matching_still(stills, scene_id)]
        if missing:
            errors.append("stills ausentes para cenas: " + ", ".join(missing))
        if gates.get("stills", {}).get("status") != "approved":
            errors.append("gate stills ainda nao aprovado")

    if args.stage in ("render", "final"):
        previews = [p for p in (job / "Previews").glob("*") if p.is_file() and p.suffix.lower() in PREVIEW_EXTS]
        if not previews:
            errors.append("nenhum preview encontrado em Previews/")
        if gates.get("final_preview", {}).get("status") != "approved":
            errors.append("gate final_preview ainda nao aprovado")

    if args.stage == "final":
        renders = [p for p in (job / "Renders").glob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTS]
        if not renders:
            errors.append("nenhum render final encontrado em Renders/")

    report = {"job": str(job.relative_to(root)), "stage": args.stage, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"== Job validation: {report['job']} [{args.stage}] ==")
        for item in warnings:
            print(f"[WARN] {item}")
        for item in errors:
            print(f"[ERROR] {item}")
        if not errors:
            print("[OK] Gate estrutural satisfeito.")

    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
