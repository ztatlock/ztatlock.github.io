from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.service_index import (
    render_cv_service_section_list_djot,
    render_homepage_recent_service_list_djot,
    render_public_service_section_list_djot,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_service(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class ServiceIndexTests(unittest.TestCase):
    def test_seed_public_service_render_is_run_native(self) -> None:
        organizing = render_public_service_section_list_djot(ROOT, "organizing")
        self.assertIn("{#fptalks}", organizing)
        self.assertIn("- FPTalks Co-Organizer, 2020 - 2025", organizing)
        self.assertIn("  * [FPTalks 2025, Co-Organizer](https://fpbench.org/talks/fptalks25.html)", organizing)
        self.assertIn("{#pldi-workshops}", organizing)
        self.assertIn("- PLDI Workshops Co-chair, 2023 - 2024", organizing)

        department = render_public_service_section_list_djot(ROOT, "department")
        self.assertIn("{#uw-faculty-skit}", department)
        self.assertIn("- UW Faculty Skit Writer, Producer, and Director, 2015 - Present", department)
        self.assertIn("  * with [Hank Levy][] and [Adriana Schulz][]", department)

    def test_render_public_uniform_shorthand_run_as_one_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-summit",
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "view_groups": ["organizing"],
                        "ongoing": True,
                        "instances": [
                            {
                                "key": "2025-demo-summit",
                                "year": 2025,
                                "url": "https://example.test/demo",
                            },
                            {
                                "key": "2024-demo-summit",
                                "year": 2024,
                                "url": "https://example.test/demo",
                            },
                        ],
                    }
                ],
            )

            rendered = render_public_service_section_list_djot(root, "organizing")
            self.assertEqual(
                rendered,
                "{#demo-summit}\n"
                "- [Demo Summit Co-Organizer, 2024 - Present](https://example.test/demo)\n",
            )

    def test_render_public_heterogeneous_run_with_instance_sub_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-summit",
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "view_groups": ["organizing"],
                        "instances": [
                            {
                                "key": "2025-demo-summit",
                                "year": 2025,
                                "url": "https://example.test/2025",
                            },
                            {
                                "key": "2024-demo-summit",
                                "year": 2024,
                                "url": "https://example.test/2024",
                            },
                        ],
                    }
                ],
            )

            rendered = render_public_service_section_list_djot(root, "organizing")
            self.assertEqual(
                rendered,
                "{#demo-summit}\n"
                "- Demo Summit Co-Organizer, 2024 - 2025\n"
                "  * [Demo Summit 2025, Co-Organizer](https://example.test/2025)\n"
                "  * [Demo Summit 2024, Co-Organizer](https://example.test/2024)\n",
            )

    def test_multi_view_anchor_attaches_only_in_anchor_view(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-demo-chair",
                        "year": 2025,
                        "title": "DemoConf",
                        "role": "Program Chair",
                        "view_groups": ["reviewing", "organizing"],
                        "anchor_view_group": "organizing",
                        "url": "https://example.test/democonf",
                    }
                ],
            )

            organizing = render_public_service_section_list_djot(root, "organizing")
            reviewing = render_public_service_section_list_djot(root, "reviewing")
            self.assertIn("{#2025-demo-chair}", organizing)
            self.assertNotIn("{#2025-demo-chair}", reviewing)

    def test_cv_uses_internal_service_anchor_for_multi_url_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-summit",
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "view_groups": ["organizing"],
                        "instances": [
                            {
                                "key": "2025-demo-summit",
                                "year": 2025,
                                "url": "https://example.test/2025",
                            },
                            {
                                "key": "2024-demo-summit",
                                "year": 2024,
                                "url": "https://example.test/2024",
                            },
                        ],
                    }
                ],
            )

            rendered = render_cv_service_section_list_djot(root, "organizing")
            self.assertEqual(
                rendered,
                "- [Demo Summit Co-Organizer, 2024 - 2025](/service/#demo-summit)\n",
            )

    def test_seed_homepage_recent_service_uses_latched_policy(self) -> None:
        rendered = render_homepage_recent_service_list_djot(ROOT, current_year=2026)
        self.assertIn("- EGRAPHS Community Advisory Board, 2022 - Present", rendered)
        self.assertIn("- ICFP 2026, Program Committee", rendered)
        self.assertIn("- [FPTalks Co-Organizer, 2020 - 2025](/service/#fptalks)", rendered)
        self.assertIn(
            "- [PLDI 2025, Program Committee Chair](https://pldi25.sigplan.org/committee/pldi-2025-organizing-committee)",
            rendered,
        )
        self.assertNotIn("Dagstuhl Seminar 26022: EGRAPHS", rendered)
        self.assertNotIn("UW Faculty Skit", rendered)

    def test_homepage_recent_service_uses_non_department_window_and_link_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-series",
                        "title": "Demo Summit",
                        "role": "Co-Organizer",
                        "view_groups": ["organizing"],
                        "instances": [
                            {
                                "key": "2025-demo-summit",
                                "year": 2025,
                                "url": "https://example.test/2025",
                            },
                            {
                                "key": "2024-demo-summit",
                                "year": 2024,
                                "url": "https://example.test/2024",
                            },
                        ],
                    },
                    {
                        "key": "2026-demo-pc",
                        "year": 2026,
                        "title": "DemoConf",
                        "role": "Program Committee",
                        "view_groups": ["reviewing"],
                    },
                    {
                        "key": "2026-department-role",
                        "year": 2026,
                        "title": "Department Role",
                        "view_groups": ["department"],
                    },
                    {
                        "key": "2022-old-role",
                        "year": 2022,
                        "title": "Old Role",
                        "view_groups": ["organizing"],
                    },
                ],
            )

            rendered = render_homepage_recent_service_list_djot(root, current_year=2026)
            self.assertEqual(
                rendered,
                "- DemoConf 2026, Program Committee\n\n"
                "- [Demo Summit Co-Organizer, 2024 - 2025](/service/#demo-series)\n",
            )


if __name__ == "__main__":
    unittest.main()
