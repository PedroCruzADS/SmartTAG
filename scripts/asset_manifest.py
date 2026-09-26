from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(assets_dir: Path) -> dict[str, object]:
    files = []
    for path in sorted(p for p in assets_dir.rglob("*") if p.is_file()):
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
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assets_dir": assets_dir.as_posix(),
        "files": files,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Gera manifest SHA-256 dos assets autorizados."
    )
    ap.add_argument("assets_dir")
    ap.add_argument("--out")
    args = ap.parse_args()
    root = Path(args.assets_dir)
    if not root.is_dir():
        ap.error(f"Pasta nao encontrada: {root}")

    data = build_manifest(root)
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
