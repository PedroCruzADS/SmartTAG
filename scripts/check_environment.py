from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess

from tooling import node_major, renderer_status, tesseract_cli


def version(command: str, *args: str) -> str | None:
    path = shutil.which(command)
    if not path:
        return None
    try:
        return subprocess.check_output([path, *args], text=True, stderr=subprocess.STDOUT, timeout=8).strip()
    except (OSError, subprocess.SubprocessError):
        return "detected (version unavailable)"


def collect() -> dict[str, object]:
    commands = {
        "git": version("git", "--version"),
        "node": version("node", "--version"),
        "npm": version("npm", "--version"),
        "npx": version("npx", "--version"),
        "python": version("python", "--version") or version("python3", "--version"),
        "ffmpeg": version("ffmpeg", "-version"),
        "ffprobe": version("ffprobe", "-version"),
        "claude": version("claude", "--version"),
        "codex": version("codex", "--version"),
        "tsrct": tesseract_cli(),
    }
    return {
        "platform": {"system": platform.system(), "machine": platform.machine()},
        "node_major": node_major(),
        "commands": commands,
        "renderers": renderer_status(),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Checa o ambiente sem instalar ou modificar ferramentas.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    info = collect()

    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return

    print("== Environment check ==")
    print(f"OS: {info['platform']['system']} / {info['platform']['machine']}")
    for name, value in info["commands"].items():
        status = "[OK]" if value else "[--]"
        first = value.splitlines()[0] if isinstance(value, str) and value else "not found"
        print(f"{status} {name}: {first}")

    print("
== Renderer readiness ==")
    for name, data in info["renderers"].items():
        print(f"{'[OK]' if data['ready'] else '[--]'} {name}")

    print("
Use scripts/preflight_renderer.py --renderer <nome> para gate de um renderer.")


if __name__ == "__main__":
    main()
