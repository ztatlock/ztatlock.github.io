from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.service_record import (
    ServiceRecordError,
    find_service_record_issues,
    load_service_records,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_service(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class ServiceRecordTests(unittest.TestCase):
    def test_seed_service_registry_loads(self) -> None:
        records = load_service_records(ROOT)
        by_key = {record.key: record for record in records}

        self.assertEqual(len(records), 105)
        self.assertEqual(
            by_key["2025-pldi-program-committee-chair"].view_groups,
            ("reviewing", "organizing"),
        )
        self.assertEqual(
            len(by_key["2025-pldi-program-committee-chair"].details),
            2,
        )
        self.assertEqual(
            by_key["2024-fptalks-co-organizer"].url,
            "https://fpbench.org/talks/fptalks24.html",
        )
        self.assertIn("2022-egraphs-community-advisory-board", by_key)
        self.assertEqual(
            by_key["2026-dagstuhl-seminar-26022-egraphs"].details[0],
            "[Seminar Details](https://www.dagstuhl.de/en/seminars/seminar-calendar/seminar-details/26022)",
        )

    def test_duplicate_record_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-role",
                        "year": 2025,
                        "view_groups": ["reviewing"],
                        "title": "Demo",
                        "role": "Program Committee",
                    },
                    {
                        "key": "2025-demo-role",
                        "year": 2025,
                        "view_groups": ["organizing"],
                        "title": "Other",
                    },
                ],
            )

            with self.assertRaisesRegex(ServiceRecordError, "duplicate record key"):
                load_service_records(root)

    def test_invalid_view_group_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-role",
                        "year": 2025,
                        "view_groups": ["mystery"],
                        "title": "Demo",
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordError, "unknown view_group"):
                load_service_records(root)

    def test_duplicate_view_group_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-role",
                        "year": 2025,
                        "view_groups": ["reviewing", "reviewing"],
                        "title": "Demo",
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordError, "duplicate view_group"):
                load_service_records(root)

    def test_details_must_be_nonempty_array_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-role",
                        "year": 2025,
                        "view_groups": ["reviewing"],
                        "title": "Demo",
                        "details": [],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordError, "details must be a non-empty array"):
                load_service_records(root)

    def test_find_service_record_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            issues = find_service_record_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing service registry", issues[0])


if __name__ == "__main__":
    unittest.main()
