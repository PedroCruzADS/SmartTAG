from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import compare_offer
import new_creative
import product_snapshot
import tooling


def validate(
    instance: object,
    schema_name: str,
) -> list[str]:
    schema = json.loads(
        (ROOT / "schemas" / schema_name).read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    return [
        error.message
        for error in validator.iter_errors(instance)
    ]


class TestSafety(unittest.TestCase):
    def test_slug_rejects_path_traversal(self):
        for bad in (
            "../x",
            "a/b",
            "A B",
            "_foo",
            "foo_",
            "-foo",
            "foo-",
        ):
            with self.assertRaises(ValueError, msg=bad):
                tooling.validate_slug(bad)

    def test_safe_repo_path_rejects_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                tooling.safe_repo_path(
                    root,
                    "../outside",
                    "x",
                )

    def test_snapshot_blocks_private_ip(self):
        for url in (
            "http://127.0.0.1/",
            "http://10.0.0.1/",
            "http://localhost/",
        ):
            with self.assertRaises(ValueError, msg=url):
                product_snapshot.validate_url(url)


class TestJobCreation(unittest.TestCase):
    def test_job_versions_increment_and_files_validate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "outputs").mkdir()
            now = datetime(
                2026,
                9,
                26,
                12,
                0,
                tzinfo=timezone.utc,
            )
            first = new_creative.create_job(
                root,
                "esteira-b55",
                now=now,
            )
            second = new_creative.create_job(
                root,
                "esteira-b55",
                now=now,
            )
            self.assertTrue(
                first.name.endswith("_v01")
            )
            self.assertTrue(
                second.name.endswith("_v02")
            )

            request = json.loads(
                (first / "request.json").read_text(
                    encoding="utf-8"
                )
            )
            approvals = json.loads(
                (first / "approvals.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                request["approval"]["final_preview"],
                "human",
            )
            self.assertIsNone(
                approvals["gates"]["storyboard"]["actor_type"]
            )
            self.assertEqual(
                validate(
                    request,
                    "creative-request.schema.json",
                ),
                [],
            )
            self.assertEqual(
                validate(
                    approvals,
                    "approval.schema.json",
                ),
                [],
            )


class TestSchemas(unittest.TestCase):
    CASES = [
        (
            "creative-request.example.json",
            "creative-request.schema.json",
        ),
        (
            "product-offer.example.json",
            "product-offer.schema.json",
        ),
        (
            "storyboard.example.json",
            "storyboard.schema.json",
        ),
        (
            "approval.example.json",
            "approval.schema.json",
        ),
        (
            "asset-manifest.example.json",
            "asset-manifest.schema.json",
        ),
    ]

    def test_examples_validate(self):
        for example_name, schema_name in self.CASES:
            with self.subTest(example=example_name):
                instance = json.loads(
                    (
                        ROOT
                        / "schemas"
                        / example_name
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(
                    validate(instance, schema_name),
                    [],
                )

    def test_human_gate_rejects_agent_approval(self):
        instance = json.loads(
            (
                ROOT
                / "schemas"
                / "approval.example.json"
            ).read_text(encoding="utf-8")
        )
        invalid = deepcopy(instance)
        invalid["gates"]["storyboard"].update(
            {
                "status": "approved",
                "approved_at": "2026-09-26T13:00:00+00:00",
                "approved_by": "agent",
                "actor_type": "agent",
            }
        )
        self.assertTrue(
            validate(invalid, "approval.schema.json")
        )

    def test_storyboard_rejects_empty_direction(self):
        instance = json.loads(
            (
                ROOT
                / "schemas"
                / "storyboard.example.json"
            ).read_text(encoding="utf-8")
        )
        invalid = deepcopy(instance)
        invalid["variants"][1]["scenes"] = []
        self.assertTrue(
            validate(invalid, "storyboard.schema.json")
        )


class TestOfferDiff(unittest.TestCase):
    def test_price_change_detected(self):
        old = {
            "product": {},
            "commercial": {"price": "100"},
        }
        new = {
            "product": {},
            "commercial": {"price": "90"},
        }
        changed = compare_offer.diff(old, new)
        self.assertIn(
            "commercial.price",
            {item["field"] for item in changed},
        )


if __name__ == "__main__":
    unittest.main()
