from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path


def probe(path: Path) -> dict[str, object]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe nao encontrado no PATH.")
    proc = subprocess.run(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "ffprobe falhou.")
    return json.loads(proc.stdout)


def parse_rate(value: str | None) -> float | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        return float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None


def validate(path: Path, canvas: str | None, duration: float | None, fps: float | None, tolerance: float, require_audio: bool) -> dict[str, object]:
    if not path.is_file() or path.stat().st_size == 0:
        return {"errors": ["arquivo ausente ou vazio"], "warnings": [], "probe": {}}

    data = probe(path)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    errors: list[str] = []
    warnings: list[str] = []

    if not video:
        errors.append("nenhum stream de video encontrado")
        return {"errors": errors, "warnings": warnings, "probe": data}

    if canvas:
        expected_w, expected_h = [int(x) for x in canvas.lower().split("x", 1)]
        if video.get("width") != expected_w or video.get("height") != expected_h:
            errors.append(f"canvas {video.get('width')}x{video.get('height')} != {canvas}")

    actual_fps = parse_rate(video.get("avg_frame_rate") or video.get("r_frame_rate"))
    if fps is not None and (actual_fps is None or abs(actual_fps - fps) > 0.05):
        errors.append(f"fps {actual_fps!r} != {fps}")

    raw_duration = video.get("duration") or data.get("format", {}).get("duration")
    try:
        actual_duration = float(raw_duration)
    except (TypeError, ValueError):
        actual_duration = None
        warnings.append("duracao nao encontrada no container")

    if duration is not None and (actual_duration is None or abs(actual_duration - duration) > tolerance):
        errors.append(f"duracao {actual_duration!r}s fora de {duration}s ± {tolerance}s")

    if require_audio and not audio:
        errors.append("audio obrigatorio, mas nenhum stream de audio foi encontrado")
    elif not audio:
        warnings.append("render sem audio")

    return {
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "width": video.get("width"),
            "height": video.get("height"),
            "fps": actual_fps,
            "duration": actual_duration,
            "has_audio": bool(audio),
            "bytes": path.stat().st_size,
        },
        "probe": data,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Valida tecnicamente um render final com ffprobe.")
    ap.add_argument("render")
    ap.add_argument("--canvas")
    ap.add_argument("--duration", type=float)
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration-tolerance", type=float, default=0.25)
    ap.add_argument("--require-audio", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        report = validate(Path(args.render), args.canvas, args.duration, args.fps, args.duration_tolerance, args.require_audio)
    except (RuntimeError, json.JSONDecodeError) as exc:
        report = {"errors": [str(exc)], "warnings": []}

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in report.get("warnings", []):
            print(f"[WARN] {item}")
        for item in report.get("errors", []):
            print(f"[ERROR] {item}")
        if not report.get("errors"):
            print("[OK] Render tecnicamente valido.")

    raise SystemExit(1 if report.get("errors") else 0)


if __name__ == "__main__":
    main()
