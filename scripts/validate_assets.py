from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg",
    ".mp4",
    ".mov",
    ".m4v",
    ".wav",
    ".mp3",
    ".m4a",
    ".ttf",
    ".otf",
    ".pdf",
}


def inspect_assets(path: Path) -> dict[str, object]:
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Pasta nao encontrada: {path}")

    entries = [p for p in path.rglob("*") if p.is_file() or p.is_symlink()]
    symlinks = [str(p) for p in entries if p.is_symlink()]
    files = [p for p in entries if p.is_file() and not p.is_symlink()]
    unexpected = [
        str(p)
        for p in files
        if p.suffix.lower() not in ALLOWED
    ]
    empty = [
        str(p)
        for p in files
        if p.stat().st_size == 0
    ]
    return {
        "path": str(path),
        "count": len(files),
        "total_bytes": sum(p.stat().st_size for p in files),
        "unexpected_extensions": unexpected,
        "empty_files": empty,
        "symlinks": symlinks,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Valida o conjunto basico de assets."
    )
    ap.add_argument("path", nargs="?", default="assets")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    try:
        report = inspect_assets(Path(args.path))
    except FileNotFoundError as exc:
        ap.error(str(exc))

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Assets encontrados: {report['count']}")
        print(
            "Tamanho total (MB): "
            f"{report['total_bytes'] / 1024 / 1024:.2f}"
        )
        for item in report["unexpected_extensions"]:
            print(f"[WARN] extensao inesperada: {item}")
        for item in report["empty_files"]:
            print(f"[WARN] arquivo vazio: {item}")
        for item in report["symlinks"]:
            print(f"[WARN] symlink nao permitido: {item}")
        if not report["count"]:
            print("[WARN] nenhum asset encontrado")

    problems = bool(
        report["unexpected_extensions"]
        or report["empty_files"]
        or report["symlinks"]
        or not report["count"]
    )
    raise SystemExit(1 if args.strict and problems else 0)


if __name__ == "__main__":
    main()
