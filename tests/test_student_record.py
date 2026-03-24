from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.student_record import (
    StudentRecordError,
    find_student_record_issues,
    load_student_sections,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_people(path: Path, people: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"people": people}), encoding="utf-8")


def _write_students(path: Path, sections: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sections": sections}), encoding="utf-8")


class StudentRecordTests(unittest.TestCase):
    def test_seed_students_registry_loads(self) -> None:
        sections = load_student_sections(ROOT)

        self.assertEqual([section.key for section in sections], [
            "current_students",
            "completed_postdoctoral_mentoring",
            "graduated_doctoral_students",
            "graduated_masters_students",
            "graduated_bachelors_students",
            "visiting_students",
        ])
        self.assertEqual(sections[-1].cv_title, "Visiting Summer Students")
        self.assertEqual(sections[0].records[0].person_key, "haobin-ni")
        self.assertEqual(sections[2].records[0].details[0].kind, "thesis")
        self.assertEqual(sections[-1].records[0].person_key, "ian-briggs")
        self.assertEqual(
            sections[4].records[6].name,
            "Zhiyuan (Kevin) Yan",
        )

    def test_duplicate_section_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "duplicated",
                        "title": "One",
                        "records": [{"key": "alpha", "person_key": "alpha-person", "name": "Alpha Person", "label": "BS 2025"}],
                    },
                    {
                        "key": "duplicated",
                        "title": "Two",
                        "records": [{"key": "beta", "person_key": "alpha-person", "name": "Alpha Person", "label": "BS 2024"}],
                    },
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "duplicate section key"):
                load_student_sections(root)

    def test_duplicate_record_key_is_rejected_across_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "one",
                        "title": "One",
                        "records": [{"key": "shared-record", "person_key": "alpha-person", "name": "Alpha Person", "label": "BS 2025"}],
                    },
                    {
                        "key": "two",
                        "title": "Two",
                        "records": [{"key": "shared-record", "person_key": "alpha-person", "name": "Alpha Person", "label": "BS 2024"}],
                    },
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "duplicate record key"):
                load_student_sections(root)

    def test_unknown_person_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "current_students",
                        "title": "Current Students",
                        "records": [{"key": "alpha", "person_key": "missing-person", "name": "Unknown Person", "label": "BS 2025"}],
                    }
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "unknown person_key"):
                load_student_sections(root)

    def test_unknown_coadvisor_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "current_students",
                        "title": "Current Students",
                        "records": [
                            {
                                "key": "alpha",
                                "person_key": "alpha-person",
                                "name": "Alpha Person",
                                "label": "PhD Student",
                                "details": [{"kind": "coadvisor", "person_keys": ["missing-advisor"]}],
                            }
                        ],
                    }
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "unknown person_keys value"):
                load_student_sections(root)

    def test_invalid_detail_kind_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "current_students",
                        "title": "Current Students",
                        "records": [
                            {
                                "key": "alpha",
                                "person_key": "alpha-person",
                                "name": "Alpha Person",
                                "label": "PhD Student",
                                "details": [{"kind": "mystery", "djot": "???!"}],
                            }
                        ],
                    }
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "unknown kind"):
                load_student_sections(root)

    def test_thesis_detail_requires_title_and_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "current_students",
                        "title": "Current Students",
                        "records": [
                            {
                                "key": "alpha",
                                "person_key": "alpha-person",
                                "name": "Alpha Person",
                                "label": "PhD 2025",
                                "details": [{"kind": "thesis", "title": "A Thesis"}],
                            }
                        ],
                    }
                ],
            )

            with self.assertRaisesRegex(StudentRecordError, "missing url"):
                load_student_sections(root)

    def test_display_name_variant_is_allowed_when_person_key_is_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"zhiyuan-yan": {"name": "Zhiyuan Yan", "url": "https://example.com/z"}},
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "graduated_bachelors_students",
                        "title": "Graduated Bachelors Students",
                        "records": [
                            {
                                "key": "zhiyuan-yan-bs-2024",
                                "person_key": "zhiyuan-yan",
                                "name": "Zhiyuan (Kevin) Yan",
                                "label": "BS 2024",
                                "details": [{"kind": "outcome", "djot": "MS Student at UCSD"}],
                            }
                        ],
                    }
                ],
            )

            sections = load_student_sections(root)
            self.assertEqual(sections[0].records[0].name, "Zhiyuan (Kevin) Yan")

    def test_order_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {
                    "alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"},
                    "beta-person": {"name": "Beta Person", "url": "https://example.com/b"},
                    "advisor-person": {"name": "Advisor Person", "url": "https://example.com/c"},
                },
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "second_section",
                        "title": "Second Section",
                        "records": [{"key": "beta", "person_key": "beta-person", "name": "Beta Person", "label": "BS 2024"}],
                    },
                    {
                        "key": "first_section",
                        "title": "First Section",
                        "records": [
                            {
                                "key": "alpha",
                                "person_key": "alpha-person",
                                "name": "Alpha Person",
                                "label": "BS 2025",
                                "details": [
                                    {"kind": "note", "djot": "First detail"},
                                    {"kind": "coadvisor", "person_keys": ["advisor-person"]},
                                ],
                            }
                        ],
                    },
                ],
            )

            sections = load_student_sections(root)
            self.assertEqual([section.key for section in sections], ["second_section", "first_section"])
            self.assertEqual(
                [detail.kind for detail in sections[1].records[0].details],
                ["note", "coadvisor"],
            )

    def test_find_student_record_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_people(
                root / "site" / "data" / "people.json",
                {"alpha-person": {"name": "Alpha Person", "url": "https://example.com/a"}},
            )

            issues = find_student_record_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing student registry", issues[0])


if __name__ == "__main__":
    unittest.main()
