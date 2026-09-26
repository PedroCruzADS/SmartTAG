from __future__ import annotations

import argparse
import shutil
import subprocess

from tooling import node_major


def run(label: str, command: list[str]) -> bool:
    print(f"\n== {label} ==")
    print("+", " ".join(command))
    try:
        proc = subprocess.run(command, check=False)
    except OSError as exc:
        print(f"[WARN] nao foi possivel executar: {exc}")
        return False
    if proc.returncode != 0:
        print(f"[WARN] comando terminou com codigo {proc.returncode}")
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Instala/atualiza skills opcionais do Creative Lab."
    )
    ap.add_argument("--install-21st", action="store_true")
    args = ap.parse_args()

    npx = shutil.which("npx")
    if not npx:
        ap.error("npx nao encontrado. Instale Node.js/npm primeiro.")

    major = node_major()
    print("== Tesseract Creative Lab bootstrap ==")
    print(f"Node major: {major!r}")

    run(
        "Tesseract skills",
        [npx, "skills", "add", "mirage-hq/Tesseract"],
    )

    if major is not None and major >= 22:
        run(
            "HyperFrames skills",
            [npx, "hyperframes", "skills", "update"],
        )
    else:
        print(
            "[WARN] HyperFrames requer Node.js 22+; skill nao configurada."
        )

    run(
        "Remotion skills",
        [
            npx,
            "-y",
            "skills@latest",
            "add",
            "remotion-dev/skills",
            "-g",
            "-y",
        ],
    )

    if args.install_21st:
        run(
            "21st.dev skill",
            [npx, "@21st-dev/cli", "install-skill"],
        )

    print("\nRode: python scripts/check_environment.py")


if __name__ == "__main__":
    main()
