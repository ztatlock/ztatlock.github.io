from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.service_record_a4 import (
    ServiceRecordA4Error,
    find_service_record_a4_issues,
    load_service_registry_a4,
)


def _write_service(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


def _write_people(path: Path, people: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"people": people}), encoding="utf-8")


class ServiceRecordA4Tests(unittest.TestCase):
    def test_singleton_normalizes_to_one_run_and_one_instance(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2026-dagstuhl-seminar-26022-egraphs",
                        "year": 2026,
                        "view_groups": ["organizing"],
                        "title": "Dagstuhl Seminar 26022: EGRAPHS",
                        "role": "Organizer",
                        "url": "https://example.com/dagstuhl",
                        "details": ["[Seminar Details](https://example.com/details)"],
                    }
                ],
            )

            registry = load_service_registry_a4(root)
            record = registry.record("2026-dagstuhl-seminar-26022-egraphs")
            run = record.runs[0]
            instance = run.instances[0]

            self.assertEqual(record.form, "singleton")
            self.assertIsNone(record.series)
            self.assertEqual(run.key, "2026-dagstuhl-seminar-26022-egraphs")
            self.assertEqual(run.anchor_view_group, "organizing")
            self.assertEqual(run.title, "Dagstuhl Seminar 26022: EGRAPHS")
            self.assertEqual(run.role, "Organizer")
            self.assertEqual(instance.year, 2026)
            self.assertEqual(instance.title, "Dagstuhl Seminar 26022: EGRAPHS")
            self.assertEqual(instance.role, "Organizer")
            self.assertEqual(instance.url, "https://example.com/dagstuhl")
            self.assertEqual(instance.details[0], "[Seminar Details](https://example.com/details)")

    def test_shorthand_normalizes_to_series_and_implicit_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "fptalks",
                        "title": "FPTalks",
                        "role": " Co-Organizer ",
                        "view_groups": ["organizing"],
                        "instances": [
                            {"year": 2025, "url": "https://example.com/2025"},
                            {"year": 2024, "url": "https://example.com/2024"},
                            {"year": 2023, "url": "https://example.com/2023"},
                        ],
                    }
                ],
            )

            registry = load_service_registry_a4(root)
            record = registry.record("fptalks")
            run = record.runs[0]

            self.assertEqual(record.form, "shorthand")
            self.assertEqual(record.series.key, "fptalks")
            self.assertEqual(record.series.title, "FPTalks")
            self.assertEqual(run.key, "fptalks")
            self.assertEqual(run.role, "Co-Organizer")
            self.assertEqual(run.anchor_view_group, "organizing")
            self.assertEqual(tuple(instance.year for instance in run.instances), (2025, 2024, 2023))
            self.assertEqual(run.instances[1].url, "https://example.com/2024")

    def test_explicit_series_inherits_series_level_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {
                    "alpha-person": {
                        "name": "Alpha Person",
                        "url": "https://example.com/alpha",
                    }
                },
            )
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "pacmpl-advisory-board",
                        "title": "PACMPL Advisory Board",
                        "role": "Member",
                        "url": "https://example.com/pacmpl",
                        "details": ["Worked with [Alpha Person][]"],
                        "runs": [
                            {
                                "key": "pacmpl-advisory-board",
                                "view_groups": ["reviewing"],
                                "ongoing": True,
                                "instances": [{"year": 2029}, {"year": 2028}, {"year": 2027}],
                            }
                        ],
                    }
                ],
            )

            registry = load_service_registry_a4(root)
            run = registry.run("pacmpl-advisory-board")
            self.assertEqual(run.title, "PACMPL Advisory Board")
            self.assertEqual(run.role, "Member")
            self.assertEqual(run.url, "https://example.com/pacmpl")
            self.assertEqual(run.details, ("Worked with [Alpha Person][]",))
            self.assertTrue(run.ongoing)
            self.assertEqual(run.instances[0].role, "Member")
            self.assertEqual(run.instances[0].details, ("Worked with [Alpha Person][]",))

    def test_duplicate_top_level_record_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo",
                        "year": 2025,
                        "view_groups": ["reviewing"],
                        "title": "Demo",
                    },
                    {
                        "key": "demo",
                        "year": 2026,
                        "view_groups": ["organizing"],
                        "title": "Other Demo",
                    },
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "duplicate top-level record key"):
                load_service_registry_a4(root)

    def test_run_key_collision_with_unrelated_record_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "fptalks",
                        "title": "FPTalks",
                        "view_groups": ["organizing"],
                        "instances": [{"year": 2025}],
                    },
                    {
                        "key": "other-series",
                        "title": "Other Series",
                        "runs": [
                            {
                                "key": "fptalks",
                                "view_groups": ["reviewing"],
                                "instances": [{"year": 2024}],
                            }
                        ],
                    },
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "duplicate canonical run key"):
                load_service_registry_a4(root)

    def test_allows_parent_record_key_and_run_key_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "pacmpl-advisory-board",
                        "title": "PACMPL Advisory Board",
                        "runs": [
                            {
                                "key": "pacmpl-advisory-board",
                                "view_groups": ["reviewing"],
                                "instances": [{"year": 2026}],
                            }
                        ],
                    }
                ],
            )

            registry = load_service_registry_a4(root)
            self.assertEqual(registry.run("pacmpl-advisory-board").parent_record_key, "pacmpl-advisory-board")

    def test_multi_view_run_requires_anchor_view_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "2025-pldi-program-committee-chair",
                        "year": 2025,
                        "title": "PLDI",
                        "role": "Program Committee Chair",
                        "view_groups": ["organizing", "reviewing"],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "anchor_view_group is required"):
                load_service_registry_a4(root)

    def test_shorthand_non_contiguous_years_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "pnw-plse",
                        "title": "PNW PLSE",
                        "view_groups": ["organizing"],
                        "instances": [{"year": 2023}, {"year": 2018}],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "run years must form one contiguous sequence"):
                load_service_registry_a4(root)

    def test_same_year_multiplicity_requires_explicit_instance_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-series",
                        "title": "Demo Series",
                        "view_groups": ["organizing"],
                        "instances": [{"year": 2025}, {"year": 2025}],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "same-year multiplicity requires explicit instance.key"):
                load_service_registry_a4(root)

    def test_same_year_multiplicity_with_explicit_instance_keys_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-series",
                        "title": "Demo Series",
                        "view_groups": ["organizing"],
                        "instances": [
                            {"key": "spring", "year": 2025, "title": "Demo Spring"},
                            {"key": "fall", "year": 2025, "title": "Demo Fall"},
                        ],
                    }
                ],
            )

            registry = load_service_registry_a4(root)
            run = registry.run("demo-series")
            self.assertEqual(tuple(instance.authored_key for instance in run.instances), ("spring", "fall"))
            self.assertEqual(tuple(instance.title for instance in run.instances), ("Demo Spring", "Demo Fall"))

    def test_explicit_top_level_view_groups_are_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-series",
                        "title": "Demo Series",
                        "view_groups": ["organizing"],
                        "runs": [
                            {
                                "key": "demo-series",
                                "view_groups": ["organizing"],
                                "instances": [{"year": 2025}],
                            }
                        ],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "unknown fields: view_groups"):
                load_service_registry_a4(root)

    def test_details_must_not_target_linkless_person_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {
                    "alpha-person": {
                        "name": "Alpha Person",
                    }
                },
            )
            _write_service(
                root / "site" / "data" / "service.json",
                [
                    {
                        "key": "demo-series",
                        "title": "Demo Series",
                        "view_groups": ["organizing"],
                        "details": ["Worked with [Alpha Person][]"],
                        "instances": [{"year": 2025}],
                    }
                ],
            )

            with self.assertRaisesRegex(ServiceRecordA4Error, "must not target linkless person label"):
                load_service_registry_a4(root)

    def test_find_service_record_a4_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            issues = find_service_record_a4_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing service registry", issues[0])


if __name__ == "__main__":
    unittest.main()
