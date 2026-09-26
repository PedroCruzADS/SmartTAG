from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from tooling import repo_root

GATES = ("storyboard", "stills", "final_preview")


def main() -> None:
    ap = argparse.ArgumentParser(description="Registra aprovacao/rejeicao de um gate do job.")
    ap.add_argument("job_dir")
    ap.add_argument("gate", choices=GATES)
    ap.add_argument("--status", choices=("approved", "rejected"), default="approved")
    ap.add_argument("--by", required=True, help="Nome da pessoa/agente que decidiu.")
    ap.add_argument("--actor-type", choices=("human", "agent"), required=True)
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    root = repo_root()
    job = Path(args.job_dir)
    if not job.is_absolute():
        job = root / job
    job = job.resolve()
    try:
        job.relative_to((root / "outputs").resolve())
    except ValueError:
        ap.error("job_dir deve estar dentro de outputs/.")

    path = job / "approvals.json"
    if not path.is_file():
        ap.error(f"approvals.json ausente em {job}")

    data = json.loads(path.read_text(encoding="utf-8-sig"))
    item = data["gates"][args.gate]
    if item.get("mode") == "human" and args.actor_type != "human":
        ap.error(f"gate {args.gate} exige aprovacao humana; agente nao pode aprova-lo.")

    item["status"] = args.status
    item["approved_at"] = datetime.now(timezone.utc).isoformat() if args.status == "approved" else None
    item["approved_by"] = args.by
    item["actor_type"] = args.actor_type
    item["note"] = args.note
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "
", encoding="utf-8")
    print(f"{args.gate}: {args.status} por {args.by} ({args.actor_type})")


if __name__ == "__main__":
    main()
