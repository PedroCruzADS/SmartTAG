from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

VALID_RENDERERS = ("auto", "tesseract", "hyperframes", "remotion", "hybrid")
VALID_CANVASES = ("1080x1920", "1080x1350", "1080x1080")
VALID_FPS = (24, 30, 60)
VALID_APPROVAL = ("human", "auto")
_SAFE_SLUG = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def validate_slug(value: str, field: str = "slug") -> str:
    if not _SAFE_SLUG.fullmatch(value):
        raise ValueError(
            f"{field} invalido: use 1-64 caracteres ASCII minusculos, numeros e hifen; "
            "nao use caminhos, espacos, '_' ou hifen nas extremidades."
        )
    return value


def command_path(name: str) -> str | None:
    return shutil.which(name)


def node_major() -> int | None:
    node = command_path("node")
    if not node:
        return None
    try:
        out = subprocess.check_output([node, "--version"], text=True, timeout=5).strip().lstrip("v")
        return int(out.split(".", 1)[0])
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def tesseract_cli() -> str | None:
    for name in ("tsrct", "tsrct.cmd", "tsrct.exe"):
        found = command_path(name)
        if found:
            return found

    if platform.system() == "Windows":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidate = Path(local) / "Tesseract" / "bin" / "tsrct.cmd"
            if candidate.exists():
                return str(candidate)
    return None


def renderer_status() -> dict[str, dict[str, object]]:
    node = node_major()
    npx = command_path("npx")
    ffmpeg = command_path("ffmpeg")
    ffprobe = command_path("ffprobe")
    tsrct = tesseract_cli()

    return {
        "tesseract": {
            "ready": bool(tsrct),
            "details": {"cli": tsrct, "platform": platform.system(), "machine": platform.machine()},
        },
        "hyperframes": {
            "ready": bool(node is not None and node >= 22 and npx and ffmpeg and ffprobe),
            "details": {"node_major": node, "npx": npx, "ffmpeg": ffmpeg, "ffprobe": ffprobe},
        },
        "remotion": {
            "ready": bool(node is not None and node >= 16 and npx),
            "details": {"node_major": node, "npx": npx},
        },
    }


def safe_repo_path(root: Path, relative: str, field: str) -> Path:
    raw = Path(relative)
    if raw.is_absolute() or any(part == ".." for part in raw.parts):
        raise ValueError(f"{field} deve ser caminho relativo dentro do repositorio: {relative!r}")
    resolved = (root / raw).resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{field} escapa da raiz do repositorio: {relative!r}") from exc
    return resolved
