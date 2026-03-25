from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.service_index import render_public_service_section_list_djot


ROOT = Path(__file__).resolve().parent.parent


def _write_service(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class ServiceIndexTests(unittest.TestCase):
    def test_seed_public_service_render_includes_expected_ranges(self) -> None:
        organizing = render_public_service_section_list_djot(ROOT, "organizing")
        self.assertIn(
            "- 2022 - Present EGRAPHS Community Advisory Board",
            organizing,
        )
        self.assertIn(
            "- [2026 Dagstuhl Seminar 26022: EGRAPHS](https://www.dagstuhl.de/26022)",
            organizing,
        )

        department = render_public_service_section_list_djot(ROOT, "department")
        self.assertIn(
            "- 2025 - 2027 : UW CSE Faculty Graduate Admissions Co-chair",
            department,
        )
        self.assertIn(
            "- 2015 - Present : UW Faculty Skit Writer, Producer, and Director",
            department,
        )
        self.assertIn("  * with [Hank Levy][] and [Adriana Schulz][]", department)

    def test_render_public_service_section_from_temp_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2024-demo-role",
                        "series_key": "demo-role",
                        "year": 2024,
                        "view_groups": ["organizing"],
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "url": "https://example.test/demo",
                    },
                    {
                        "key": "2025-demo-role",
                        "series_key": "demo-role",
                        "year": 2025,
                        "ongoing": True,
                        "view_groups": ["organizing"],
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "url": "https://example.test/demo",
                    },
                ],
            )

            rendered = render_public_service_section_list_djot(root, "organizing")
            self.assertEqual(
                rendered,
                "- [2024 - Present Demo Summit](https://example.test/demo) Co-Organizer\n",
            )

    def test_render_public_service_details_as_nested_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-chair",
                        "year": 2025,
                        "view_groups": ["reviewing"],
                        "title": "DemoConf",
                        "role": "Program Chair",
                        "url": "https://example.test/democonf",
                        "details": [
                            "[Committee](https://example.test/committee)",
                            "[Announcement](https://example.test/announcement)",
                        ],
                    }
                ],
            )

            rendered = render_public_service_section_list_djot(root, "reviewing")
            self.assertEqual(
                rendered,
                "- [2025 DemoConf](https://example.test/democonf) Program Chair\n\n"
                "  * [Committee](https://example.test/committee)\n"
                "  * [Announcement](https://example.test/announcement)\n",
            )

    def test_department_render_treats_skit_as_ordinary_service_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
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
                        "details": ["with [Hank Levy][] and [Adriana Schulz][]"],
                    }
                ],
            )

            rendered = render_public_service_section_list_djot(root, "department")
            self.assertIn(
                "- 2025 - Present : UW Faculty Skit Writer, Producer, and Director",
                rendered,
            )
            self.assertIn("[Hank Levy][]", rendered)


if __name__ == "__main__":
    unittest.main()
