from __future__ import annotations

import argparse
import json
import subprocess

from tooling import VALID_RENDERERS, renderer_status


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Valida requisitos locais do renderer escolhido."
    )
    ap.add_argument("--renderer", choices=VALID_RENDERERS, default="auto")
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--deep",
        action="store_true",
        help="Roda diagnostico oficial do HyperFrames quando aplicavel.",
    )
    args = ap.parse_args()

    status = renderer_status()
    concrete = ("tesseract", "hyperframes", "remotion")
    status["hybrid"] = {
        "ready": bool(
            status["tesseract"]["ready"]
            and (
                status["hyperframes"]["ready"]
                or status["remotion"]["ready"]
            )
        ),
        "details": {},
    }
    status["auto"] = {
        "ready": any(status[name]["ready"] for name in concrete),
        "details": {
            "note": (
                "auto exige decisao semantica entre renderers disponiveis; "
                "disponibilidade so funciona como filtro."
            )
        },
    }

    if (
        args.deep
        and args.renderer in ("hyperframes", "auto")
        and status["hyperframes"]["ready"]
    ):
        try:
            proc = subprocess.run(
                ["npx", "hyperframes", "doctor", "--json"],
                text=True,
                capture_output=True,
                timeout=120,
                check=False,
            )
            try:
                status["hyperframes"]["doctor"] = json.loads(proc.stdout)
            except json.JSONDecodeError:
                status["hyperframes"]["doctor"] = {
                    "ok": proc.returncode == 0,
                    "stdout": proc.stdout[-2000:],
                    "stderr": proc.stderr[-2000:],
                }
            doctor = status["hyperframes"].get("doctor")
            if isinstance(doctor, dict) and doctor.get("ok") is False:
                status["hyperframes"]["ready"] = False
                status["auto"]["ready"] = any(
                    status[name]["ready"] for name in concrete
                )
        except (OSError, subprocess.SubprocessError) as exc:
            status["hyperframes"]["ready"] = False
            status["hyperframes"]["doctor"] = {
                "ok": False,
                "error": str(exc),
            }
            status["auto"]["ready"] = any(
                status[name]["ready"] for name in concrete
            )

    selected = status[args.renderer]

    if args.json:
        print(
            json.dumps(
                {
                    "selected": args.renderer,
                    "ready": selected["ready"],
                    "status": status,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("== Renderer preflight ==")
        for name in ("tesseract", "hyperframes", "remotion", "hybrid"):
            print(f"{'[OK]' if status[name]['ready'] else '[--]'} {name}")
        if args.renderer == "auto":
            print()
            print(
                "AUTO: escolha pelo job entre renderers que passaram "
                "o preflight."
            )
            print(
                "- HyperFrames: layout/motion deterministico "
                "e iteracao por agente"
            )
            print("- Remotion: React, templates, dados e lotes")
            print(
                "- Tesseract: footage, compositing, masks, "
                "retiming e acabamento"
            )
            print("- Hybrid: combine quando reduzir retrabalho")
            if not selected["ready"]:
                print("[ERROR] nenhum renderer concreto esta pronto.")
        else:
            print()
            state = "ready" if selected["ready"] else "NOT READY"
            print(f"Selecionado: {args.renderer} -> {state}")

    raise SystemExit(0 if selected["ready"] else 1)


if __name__ == "__main__":
    main()
