from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.service_index import (
    find_public_service_drift_issues,
    parse_public_service_page_entries,
    public_service_entries_by_group,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_service(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class ServiceIndexTests(unittest.TestCase):
    def test_seed_public_service_entries_include_expected_ranges(self) -> None:
        entries = public_service_entries_by_group(ROOT)
        self.assertIn("2022 - Present EGRAPHS Community Advisory Board", entries["organizing"])
        self.assertIn("2026 Dagstuhl Seminar 26022: EGRAPHS", entries["organizing"])
        self.assertIn("2025 - 2027 : UW CSE Faculty Graduate Admissions Co-chair", entries["department"])

    def test_seed_public_service_page_has_no_drift(self) -> None:
        self.assertEqual(find_public_service_drift_issues(ROOT), [])

    def test_parse_public_service_page_entries_reads_sections(self) -> None:
        entries = parse_public_service_page_entries(ROOT)
        self.assertIn("2026 ICFP Program Committee", entries["reviewing"])
        self.assertIn("2022 - Present EGRAPHS Community Advisory Board", entries["organizing"])

    def test_drift_issues_report_missing_canonical_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages = root / "site" / "pages"
            pages.mkdir(parents=True)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-reviewing",
                        "year": 2025,
                        "view_groups": ["reviewing"],
                        "title": "DemoConf",
                        "role": "Program Committee",
                    }
                ],
            )
            (pages / "service.dj").write_text(
                "---\n"
                "description: Service\n"
                "---\n\n"
                "# Service\n\n"
                "## Reviewing\n\n"
                "- 2025 OtherConf Program Committee\n\n"
                "## Organizing\n\n"
                "## Mentoring\n\n"
                "## Department\n",
                encoding="utf-8",
            )

            issues = find_public_service_drift_issues(root, page_source_dir=pages)
            self.assertEqual(len(issues), 2)
            self.assertIn("missing canonical entries", issues[0] + issues[1])
            self.assertIn("DemoConf", issues[0] + issues[1])

    def test_drift_issues_report_missing_skit_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages = root / "site" / "pages"
            pages.mkdir(parents=True)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-uw-faculty-skit",
                        "series_key": "uw-faculty-skit",
                        "year": 2025,
                        "ongoing": True,
                        "view_groups": ["department"],
                        "title": "UW Faculty Skit",
                        "role": "Writer, Producer, and Director",
                    }
                ],
            )
            (pages / "service.dj").write_text(
                "---\n"
                "description: Service\n"
                "---\n\n"
                "# Service\n\n"
                "## Reviewing\n\n"
                "## Organizing\n\n"
                "## Mentoring\n\n"
                "## Department\n",
                encoding="utf-8",
            )

            issues = find_public_service_drift_issues(root, page_source_dir=pages)
            self.assertEqual(len(issues), 1)
            self.assertTrue(
                issues[0].endswith(": missing annual faculty skit note for canonical service records")
            )


if __name__ == "__main__":
    unittest.main()
