from __future__ import annotations

import argparse
import hashlib
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


def schema_errors(
    instance: object,
    schema_path: Path,
) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.path],
    )
    result = []
    for error in errors:
        where = ".".join(str(part) for part in error.path) or "<root>"
        result.append(
            f"{schema_path.name}:{where}: {error.message}"
        )
    return result


def resolve_job(root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    path.relative_to((root / "outputs").resolve())
    return path


def matching_still(
    stills: list[Path],
    scene_id: str,
) -> bool:
    return any(
        path.stem == scene_id
        or path.stem.startswith(scene_id + "_")
        for path in stills
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def problem(
    errors: list[str],
    warnings: list[str],
    message: str,
    hard: bool,
) -> None:
    (errors if hard else warnings).append(message)


def validate_manifest(
    root: Path,
    job: Path,
    assets_target: Path | None,
    require_manifest: bool,
    verify_hashes: bool,
    errors: list[str],
    warnings: list[str],
) -> None:
    manifest_path = job / "Source" / "assets-manifest.json"
    if not manifest_path.is_file():
        problem(
            errors,
            warnings,
            "Source/assets-manifest.json ausente",
            require_manifest,
        )
        return

    try:
        manifest = load_json(manifest_path)
        errors.extend(
            schema_errors(
                manifest,
                root / "schemas" / "asset-manifest.schema.json",
            )
        )
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"asset manifest invalido: {exc}")
        return

    if not isinstance(manifest, dict):
        return

    try:
        manifest_dir = safe_repo_path(
            root,
            str(manifest.get("assets_dir", "")),
            "manifest.assets_dir",
        )
    except ValueError as exc:
        errors.append(str(exc))
        return

    if assets_target is not None and manifest_dir != assets_target:
        errors.append(
            "manifest.assets_dir diverge de request.assets_dir"
        )

    entries = manifest.get("files", [])
    if not isinstance(entries, list):
        return

    manifest_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rel = str(entry.get("path", ""))
        if rel in manifest_paths:
            errors.append(f"asset duplicado no manifest: {rel}")
            continue
        manifest_paths.add(rel)

        raw = Path(rel)
        if raw.is_absolute() or ".." in raw.parts:
            errors.append(f"path inseguro no manifest: {rel!r}")
            continue

        target = (manifest_dir / raw).resolve()
        try:
            target.relative_to(manifest_dir)
        except ValueError:
            errors.append(f"asset escapa de assets_dir: {rel!r}")
            continue

        if target.is_symlink():
            errors.append(f"symlink nao permitido: {rel}")
            continue
        if not target.is_file():
            errors.append(f"asset do manifest ausente: {rel}")
            continue

        expected_bytes = entry.get("bytes")
        if (
            isinstance(expected_bytes, int)
            and target.stat().st_size != expected_bytes
        ):
            errors.append(f"tamanho alterado desde manifest: {rel}")

        expected_hash = entry.get("sha256")
        if verify_hashes and isinstance(expected_hash, str):
            if file_sha256(target) != expected_hash:
                errors.append(f"hash alterado desde manifest: {rel}")

    if manifest_dir.is_dir():
        actual_paths: set[str] = set()
        for path in manifest_dir.rglob("*"):
            if path.is_symlink():
                errors.append(
                    "symlink nao permitido em assets: "
                    + path.relative_to(manifest_dir).as_posix()
                )
                continue
            if path.is_file():
                actual_paths.add(
                    path.relative_to(manifest_dir).as_posix()
                )

        missing = sorted(manifest_paths - actual_paths)
        extra = sorted(actual_paths - manifest_paths)
        if missing:
            errors.append(
                "assets removidos apos manifest: "
                + ", ".join(missing)
            )
        if extra:
            errors.append(
                "assets adicionados apos manifest: "
                + ", ".join(extra)
            )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Valida um job por schema e por estagio do workflow."
    )
    ap.add_argument("job_dir", help="outputs/<job>")
    ap.add_argument(
        "--stage",
        choices=STAGES,
        default="ingest",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Trata warnings como falha.",
    )
    ap.add_argument(
        "--verify-hashes",
        action="store_true",
        help="Recalcula SHA-256 de todos os assets do manifest.",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = repo_root()
    hard_after_ingest = args.stage != "ingest"
    errors: list[str] = []
    warnings: list[str] = []

    try:
        job = resolve_job(root, args.job_dir)
    except ValueError:
        ap.error("job_dir deve estar dentro de outputs/.")

    request_path = job / "request.json"
    brief_path = job / "brief.md"
    approvals_path = job / "approvals.json"

    for path in (
        request_path,
        brief_path,
        approvals_path,
    ):
        if not path.is_file():
            errors.append(f"{path.name} ausente")

    request: dict[str, object] = {}
    approvals: dict[str, object] = {}

    if request_path.is_file():
        try:
            loaded = load_json(request_path)
            if isinstance(loaded, dict):
                request = loaded
            errors.extend(
                schema_errors(
                    loaded,
                    root
                    / "schemas"
                    / "creative-request.schema.json",
                )
            )
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"request.json invalido: {exc}")

    if approvals_path.is_file():
        try:
            loaded = load_json(approvals_path)
            if isinstance(loaded, dict):
                approvals = loaded
            errors.extend(
                schema_errors(
                    loaded,
                    root / "schemas" / "approval.schema.json",
                )
            )
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"approvals.json invalido: {exc}")

    assets_target: Path | None = None
    assets_value = request.get("assets_dir")
    if isinstance(assets_value, str) and assets_value:
        try:
            assets_target = safe_repo_path(
                root,
                assets_value,
                "assets_dir",
            )
            if not assets_target.is_dir():
                problem(
                    errors,
                    warnings,
                    "assets_dir nao existe: "
                    + assets_target.relative_to(root).as_posix(),
                    hard_after_ingest,
                )
        except ValueError as exc:
            errors.append(str(exc))

    offer_value = request.get("offer_snapshot")
    if isinstance(offer_value, str) and offer_value:
        try:
            offer_target = safe_repo_path(
                root,
                offer_value,
                "offer_snapshot",
            )
            if not offer_target.is_file():
                problem(
                    errors,
                    warnings,
                    "offer_snapshot nao existe: "
                    + offer_target.relative_to(root).as_posix(),
                    hard_after_ingest,
                )
            else:
                try:
                    offer = load_json(offer_target)
                    errors.extend(
                        schema_errors(
                            offer,
                            root
                            / "schemas"
                            / "product-offer.schema.json",
                        )
                    )
                except (json.JSONDecodeError, OSError) as exc:
                    errors.append(
                        f"offer_snapshot invalido: {exc}"
                    )
        except ValueError as exc:
            errors.append(str(exc))

    validate_manifest(
        root,
        job,
        assets_target,
        require_manifest=hard_after_ingest,
        verify_hashes=args.verify_hashes,
        errors=errors,
        warnings=warnings,
    )

    requested_modes = request.get("approval", {})
    gate_data = approvals.get("gates", {})
    if isinstance(requested_modes, dict) and isinstance(gate_data, dict):
        for gate in (
            "storyboard",
            "stills",
            "final_preview",
        ):
            req_mode = requested_modes.get(gate)
            current = gate_data.get(gate)
            if (
                isinstance(current, dict)
                and req_mode is not None
                and current.get("mode") != req_mode
            ):
                errors.append(
                    f"approval mode divergente em {gate}"
                )

    storyboard_path = (
        job / "Storyboards" / "storyboard.json"
    )
    storyboard: dict[str, object] = {}

    if args.stage in (
        "storyboard",
        "motion",
        "render",
        "final",
    ):
        if not storyboard_path.is_file():
            errors.append(
                "Storyboards/storyboard.json ausente"
            )
        else:
            try:
                loaded = load_json(storyboard_path)
                if isinstance(loaded, dict):
                    storyboard = loaded
                errors.extend(
                    schema_errors(
                        loaded,
                        root
                        / "schemas"
                        / "storyboard.schema.json",
                    )
                )
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(
                    f"storyboard invalido: {exc}"
                )

    if storyboard:
        if (
            request.get("job_id")
            and storyboard.get("job") != request.get("job_id")
        ):
            errors.append(
                "storyboard.job diverge de request.job_id"
            )

        variants = storyboard.get("variants", [])
        if isinstance(variants, list):
            variant_ids = [
                variant.get("id")
                for variant in variants
                if isinstance(variant, dict)
            ]
            if len(variant_ids) != len(set(variant_ids)):
                errors.append(
                    "storyboard possui IDs de variante duplicados"
                )

            duration = request.get("duration_seconds")
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                scenes = variant.get("scenes", [])
                if not isinstance(scenes, list):
                    continue
                scene_ids = [
                    scene.get("id")
                    for scene in scenes
                    if isinstance(scene, dict)
                ]
                if len(scene_ids) != len(set(scene_ids)):
                    errors.append(
                        "variante "
                        f"{variant.get('id')} possui scene IDs duplicados"
                    )

                starts: list[float] = []
                for scene in scenes:
                    if not isinstance(scene, dict):
                        continue
                    start = scene.get("start_s")
                    scene_duration = scene.get("duration_s")
                    if isinstance(start, (int, float)):
                        starts.append(float(start))
                    if (
                        isinstance(start, (int, float))
                        and isinstance(scene_duration, (int, float))
                        and isinstance(duration, (int, float))
                        and start + scene_duration > duration + 0.001
                    ):
                        errors.append(
                            f"cena {scene.get('id')} excede "
                            f"duracao do job ({duration}s)"
                        )

                    assets = scene.get("assets", [])
                    if (
                        assets_target is not None
                        and isinstance(assets, list)
                    ):
                        for asset in assets:
                            if not isinstance(asset, str) or not asset:
                                continue
                            try:
                                target = safe_repo_path(
                                    root,
                                    asset,
                                    "scene.asset",
                                )
                                target.relative_to(assets_target)
                            except ValueError:
                                errors.append(
                                    f"asset nao autorizado na cena "
                                    f"{scene.get('id')}: {asset}"
                                )
                                continue
                            if not target.is_file():
                                errors.append(
                                    f"asset inexistente na cena "
                                    f"{scene.get('id')}: {asset}"
                                )

                if starts != sorted(starts):
                    warnings.append(
                        f"cenas da variante {variant.get('id')} "
                        "nao estao ordenadas por start_s"
                    )

    gates = (
        approvals.get("gates", {})
        if isinstance(approvals, dict)
        else {}
    )

    if args.stage in (
        "storyboard",
        "motion",
        "render",
        "final",
    ):
        selected = storyboard.get("selected_variant")
        valid_ids = {
            variant.get("id")
            for variant in storyboard.get("variants", [])
            if isinstance(variant, dict)
        }
        if not selected:
            errors.append(
                "storyboard ainda nao possui selected_variant"
            )
        elif selected not in valid_ids:
            errors.append(
                f"selected_variant desconhecida: {selected}"
            )
        if (
            not isinstance(gates, dict)
            or not isinstance(gates.get("storyboard"), dict)
            or gates["storyboard"].get("status") != "approved"
        ):
            errors.append(
                "gate storyboard ainda nao aprovado"
            )

    if (
        args.stage in ("motion", "render", "final")
        and storyboard
    ):
        selected = storyboard.get("selected_variant")
        variant = next(
            (
                item
                for item in storyboard.get("variants", [])
                if isinstance(item, dict)
                and item.get("id") == selected
            ),
            None,
        )
        stills = [
            path
            for path in (job / "Stills").glob("*")
            if path.is_file()
            and path.suffix.lower() in STILL_EXTS
        ]
        scene_ids = (
            [
                str(scene.get("id"))
                for scene in variant.get("scenes", [])
                if isinstance(scene, dict)
            ]
            if isinstance(variant, dict)
            else []
        )
        missing = [
            scene_id
            for scene_id in scene_ids
            if not matching_still(stills, scene_id)
        ]
        if missing:
            errors.append(
                "stills ausentes para cenas: "
                + ", ".join(missing)
            )
        if (
            not isinstance(gates, dict)
            or not isinstance(gates.get("stills"), dict)
            or gates["stills"].get("status") != "approved"
        ):
            errors.append(
                "gate stills ainda nao aprovado"
            )

    if args.stage in ("render", "final"):
        previews = [
            path
            for path in (job / "Previews").glob("*")
            if path.is_file()
            and path.suffix.lower() in PREVIEW_EXTS
        ]
        if not previews:
            errors.append(
                "nenhum preview encontrado em Previews/"
            )
        if (
            not isinstance(gates, dict)
            or not isinstance(gates.get("final_preview"), dict)
            or gates["final_preview"].get("status") != "approved"
        ):
            errors.append(
                "gate final_preview ainda nao aprovado"
            )

    if args.stage == "final":
        renders = [
            path
            for path in (job / "Renders").glob("*")
            if path.is_file()
            and path.suffix.lower() in VIDEO_EXTS
        ]
        if not renders:
            errors.append(
                "nenhum render final encontrado em Renders/"
            )

    report = {
        "job": str(job.relative_to(root)),
        "stage": args.stage,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"== Job validation: {report['job']} "
            f"[{args.stage}] =="
        )
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
