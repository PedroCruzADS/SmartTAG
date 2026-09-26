from __future__ import annotations

import argparse
import json
from pathlib import Path

FIELDS = [
    ("product.name", "product", "name"),
    ("product.sku", "product", "sku"),
    ("product.availability", "product", "availability"),
    ("commercial.price", "commercial", "price"),
    ("commercial.price_currency", "commercial", "price_currency"),
    ("commercial.old_price", "commercial", "old_price"),
    ("commercial.discount_percent", "commercial", "discount_percent"),
    ("commercial.pix_price", "commercial", "pix_price"),
    ("commercial.installments", "commercial", "installments"),
    ("commercial.installment_value", "commercial", "installment_value"),
    ("commercial.coupon", "commercial", "coupon"),
    ("commercial.shipping", "commercial", "shipping"),
]


def load(path: str) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def diff(
    old: dict[str, object], new: dict[str, object]
) -> list[dict[str, object]]:
    changed = []
    for label, section, key in FIELDS:
        old_value = (old.get(section) or {}).get(key)
        new_value = (new.get(section) or {}).get(key)
        if old_value != new_value:
            changed.append(
                {"field": label, "old": old_value, "new": new_value}
            )
    return changed


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compara campos comerciais monitorados entre snapshots."
    )
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on-change", action="store_true")
    args = ap.parse_args()

    try:
        changed = diff(load(args.old), load(args.new))
    except (OSError, json.JSONDecodeError) as exc:
        ap.error(str(exc))

    if args.json:
        print(
            json.dumps(
                {"changed": changed, "count": len(changed)},
                ensure_ascii=False,
                indent=2,
            )
        )
    elif not changed:
        print("Nenhuma mudanca comercial monitorada.")
    else:
        print("Mudancas encontradas:")
        for item in changed:
            print(
                f"- {item['field']}: {item['old']!r} -> {item['new']!r}"
            )

    if args.fail_on_change and changed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
