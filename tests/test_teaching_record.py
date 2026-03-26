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


def _write_people(path: Path, people: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"people": people}), encoding="utf-8")


class TeachingRecordTests(unittest.TestCase):
    def test_seed_teaching_registry_loads(self) -> None:
        groups = load_teaching_groups(ROOT)

        self.assertEqual(
            [group.key for group in groups],
            ["uw_courses", "special_topics", "summer_school", "teaching_assistant"],
        )
        self.assertEqual(groups[0].records[0].code, "UW CSE 507")
        self.assertEqual(groups[0].records[1].offerings[0].co_instructors, ("james-wilcox",))
        self.assertEqual(groups[0].records[1].offerings[6].co_instructors, ("leonardo-de-moura",))
        self.assertEqual(
            groups[0].records[1].offerings[7].tutors,
            ("james-wilcox", "eric-mullen", "joe-redmon"),
        )
        self.assertEqual(
            groups[0].records[1].offerings[8].tutors,
            ("eric-mullen", "joe-redmon"),
        )
        self.assertEqual(groups[0].records[1].offerings[9].co_instructors, ("valentin-robert",))
        self.assertEqual(groups[0].records[2].offerings[0].co_instructors, ("anjali-pal",))
        self.assertEqual(groups[0].records[3].offerings[0].co_instructors, ("anjali-pal",))
        self.assertEqual(groups[0].records[0].offerings[0].teaching_assistants, ("audrey-seo",))
        self.assertEqual(
            groups[0].records[1].offerings[0].teaching_assistants,
            ("oliver-flatt", "kevin-mu"),
        )
        self.assertEqual(
            groups[0].records[2].offerings[2].teaching_assistants,
            ("andres-paz", "kenny-wu", "michael-flanders", "jennifer-tao", "kevin-zhu"),
        )
        self.assertEqual(
            groups[0].records[3].offerings[2].teaching_assistants,
            (
                "christopher-chen",
                "viktor-farkas",
                "cody-kesting",
                "chen-qiu",
                "matthew-yang",
                "lucy-zhu",
                "garrett-marconet",
                "sam-gao",
                "qian-yan",
            ),
        )
        self.assertEqual(groups[0].records[0].offerings[0].year, 2025)
        self.assertEqual(
            groups[1].records[1].offerings[0].co_instructors,
            ("bryan-parno", "xi-wang"),
        )
        self.assertEqual(groups[1].records[1].details[0], "Formally verifying systems implementations")
        self.assertEqual(groups[2].records[1].events[0].label, "Marktoberdorf Summer School 2024")
        self.assertEqual(groups[2].records[1].events[0].year, 2024)
        self.assertEqual(groups[3].records[2].offerings[-1].year, 2004)

    def test_summer_school_event_accepts_explicit_year(self) -> None:
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
                                "events": [{"label": "Marktoberdorf Summer School 2024", "year": 2024, "url": "https://example.com/m"}],
                            }
                        ],
                    },
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            groups = load_teaching_groups(root)
            self.assertEqual(groups[2].records[0].events[0].year, 2024)

    def test_summer_school_event_infers_year_from_label_when_omitted(self) -> None:
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
                                "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
                            }
                        ],
                    },
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            groups = load_teaching_groups(root)
            self.assertEqual(groups[2].records[0].events[0].year, 2024)

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

    def test_course_offering_accepts_staffing_fields_keyed_through_people_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {
                    "ada-lovelace": {"name": "Ada Lovelace"},
                    "grace-hopper": {"name": "Grace Hopper"},
                    "alan-kay": {"name": "Alan Kay"},
                },
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "co_instructors": ["ada-lovelace"],
                                        "teaching_assistants": ["grace-hopper", "alan-kay"],
                                        "tutors": ["ada-lovelace"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            groups = load_teaching_groups(root)
            offering = groups[0].records[0].offerings[0]
            self.assertEqual(offering.co_instructors, ("ada-lovelace",))
            self.assertEqual(
                offering.teaching_assistants,
                ("grace-hopper", "alan-kay"),
            )
            self.assertEqual(offering.tutors, ("ada-lovelace",))

    def test_staffing_fields_require_readable_people_registry(self) -> None:
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "co_instructors": ["ada-lovelace"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "missing people registry"):
                load_teaching_groups(root)

    def test_unknown_staffing_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"ada-lovelace": {"name": "Ada Lovelace"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "co_instructors": ["missing-person"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "unknown person key 'missing-person'"):
                load_teaching_groups(root)

    def test_duplicate_staffing_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"grace-hopper": {"name": "Grace Hopper"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "teaching_assistants": ["grace-hopper", "grace-hopper"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "duplicate teaching_assistants key 'grace-hopper'"):
                load_teaching_groups(root)

    def test_empty_staffing_array_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"ada-lovelace": {"name": "Ada Lovelace"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "co_instructors": [],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "co_instructors must be a non-empty array"):
                load_teaching_groups(root)

    def test_unknown_tutor_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"ada-lovelace": {"name": "Ada Lovelace"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "tutors": ["missing-person"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "unknown person key 'missing-person'"):
                load_teaching_groups(root)

    def test_duplicate_tutor_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"grace-hopper": {"name": "Grace Hopper"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "tutors": ["grace-hopper", "grace-hopper"],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "duplicate tutors key 'grace-hopper'"):
                load_teaching_groups(root)

    def test_empty_tutors_array_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"ada-lovelace": {"name": "Ada Lovelace"}},
            )
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
                                "offerings": [
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "tutors": [],
                                    }
                                ],
                            }
                        ],
                    },
                    {"key": "special_topics", "records": [{"key": "uw-cse-599z", "kind": "course", "code": "UW CSE 599Z", "title": "Topics", "details": ["Notes"], "offerings": [{"year": 2017, "term": "Spring"}]}]},
                    {"key": "summer_school", "records": [{"key": "marktoberdorf", "kind": "summer_school", "title": "EqSat", "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}]}]},
                    {"key": "teaching_assistant", "records": [{"key": "ucsd-cse-130", "kind": "course", "code": "UCSD CSE 130", "title": "PL", "description_djot": "Desc", "offerings": [{"year": 2012, "term": "Winter"}]}]},
                ],
            )

            with self.assertRaisesRegex(TeachingRecordError, "tutors must be a non-empty array"):
                load_teaching_groups(root)

    def test_teaching_assistant_history_offering_rejects_staffing_fields(self) -> None:
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
                    {
                        "key": "teaching_assistant",
                        "records": [
                            {
                                "key": "ucsd-cse-130",
                                "kind": "course",
                                "code": "UCSD CSE 130",
                                "title": "PL",
                                "description_djot": "Desc",
                                "offerings": [
                                    {
                                        "year": 2012,
                                        "term": "Winter",
                                        "co_instructors": ["ada-lovelace"],
                                    }
                                ],
                            }
                        ],
                    },
                ],
            )

            with self.assertRaisesRegex(
                TeachingRecordError,
                "teaching_assistant history offerings must not include co_instructors",
            ):
                load_teaching_groups(root)

    def test_teaching_assistant_history_offering_rejects_tutors(self) -> None:
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
                    {
                        "key": "teaching_assistant",
                        "records": [
                            {
                                "key": "ucsd-cse-130",
                                "kind": "course",
                                "code": "UCSD CSE 130",
                                "title": "PL",
                                "description_djot": "Desc",
                                "offerings": [
                                    {
                                        "year": 2012,
                                        "term": "Winter",
                                        "tutors": ["ada-lovelace"],
                                    }
                                ],
                            }
                        ],
                    },
                ],
            )

            with self.assertRaisesRegex(
                TeachingRecordError,
                "teaching_assistant history offerings must not include tutors",
            ):
                load_teaching_groups(root)

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
