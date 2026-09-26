from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from tooling import repo_root


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    assets_dir: Path,
    recorded_dir: str,
) -> dict[str, object]:
    files = []
    for path in sorted(assets_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlink nao permitido em assets: {path}")
        if not path.is_file():
            continue
        rel = path.relative_to(assets_dir).as_posix()
        parts = Path(rel).parts
        files.append(
            {
                "path": rel,
                "role": parts[0] if len(parts) > 1 else "root",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    if not files:
        raise ValueError("Nenhum asset encontrado para manifest.")
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assets_dir": recorded_dir,
        "files": files,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Gera manifest SHA-256 dos assets autorizados."
    )
    ap.add_argument("assets_dir")
    ap.add_argument("--out")
    args = ap.parse_args()

    root = repo_root()
    assets_dir = Path(args.assets_dir).resolve()
    if not assets_dir.is_dir():
        ap.error(f"Pasta nao encontrada: {assets_dir}")
    try:
        recorded_dir = assets_dir.relative_to(root).as_posix()
    except ValueError:
        ap.error("assets_dir deve estar dentro do repositorio.")

    try:
        data = build_manifest(assets_dir, recorded_dir)
    except ValueError as exc:
        ap.error(str(exc))

    payload = json.dumps(data, ensure_ascii=False, indent=2) + chr(10)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        print(out)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
