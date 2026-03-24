from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.teaching_record import (
    TeachingRecordError,
    find_teaching_record_issues,
    load_teaching_groups,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_teaching(path: Path, groups: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"groups": groups}), encoding="utf-8")


class TeachingRecordTests(unittest.TestCase):
    def test_seed_teaching_registry_loads(self) -> None:
        groups = load_teaching_groups(ROOT)

        self.assertEqual(
            [group.key for group in groups],
            ["uw_courses", "special_topics", "summer_school", "teaching_assistant"],
        )
        self.assertEqual(groups[0].records[0].code, "UW CSE 507")
        self.assertEqual(groups[0].records[0].offerings[0].year, 2025)
        self.assertEqual(groups[1].records[1].details[1], "Co-taught with [Xi Wang][] and [Bryan Parno][]")
        self.assertEqual(groups[2].records[1].events[0].label, "Marktoberdorf Summer School 2024")
        self.assertEqual(groups[3].records[2].offerings[-1].year, 2004)

    def test_duplicate_group_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2025, "term": "Autumn"}],
                            }
                        ],
                    },
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-505",
                                "kind": "course",
                                "code": "UW CSE 505",
                                "title": "Other",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2024, "term": "Winter"}],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "duplicate group key"):
                load_teaching_groups(root)

    def test_missing_group_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2025, "term": "Autumn"}],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "missing group keys: teaching_assistant"):
                load_teaching_groups(root)

    def test_special_topics_course_can_use_details_without_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2025, "term": "Autumn"}],
                            }
                        ],
                    },
                    {
                        "key": "special_topics",
                        "records": [
                            {
                                "key": "uw-cse-599w",
                                "kind": "course",
                                "code": "UW CSE 599W",
                                "title": "Systems Verification",
                                "offerings": [{"year": 2016, "term": "Spring"}],
                                "details": ["Co-taught with [Xi Wang][] and [Bryan Parno][]"],
                            }
                        ],
                    },
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            groups = load_teaching_groups(root)
            self.assertEqual(groups[1].records[0].details[0], "Co-taught with [Xi Wang][] and [Bryan Parno][]")

    def test_course_requires_description_or_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "offerings": [{"year": 2025, "term": "Autumn"}],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "must include description_djot or details"):
                load_teaching_groups(root)

    def test_invalid_term_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2025, "term": "Fall"}],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "invalid term"):
                load_teaching_groups(root)

    def test_summer_school_rejects_course_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_teaching(
                root / "site" / "data" / "teaching.json",
                [
                    {
                        "key": "uw_courses",
                        "records": [
                            {
                                "key": "uw-cse-507",
                                "kind": "course",
                                "code": "UW CSE 507",
                                "title": "Example",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2025, "term": "Autumn"}],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {
                        "key": "summer_school",
                        "records": [
                            {
                                "key": "marktoberdorf",
                                "kind": "summer_school",
                                "title": "EqSat",
                                "code": "BAD",
                                "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
                            }
                        ],
                    },
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "must not include code"):
                load_teaching_groups(root)

    def test_find_teaching_record_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            issues = find_teaching_record_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing teaching registry", issues[0])


if __name__ == "__main__":
    unittest.main()
