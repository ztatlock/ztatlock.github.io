from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_scale_stats import ScaleStats, build_scale_stats, render_scale_stats


def _write_people(path: Path, people: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"people": people}), encoding="utf-8")


def _write_students(path: Path, sections: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"sections": sections}), encoding="utf-8")


def _write_teaching(path: Path, groups: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"groups": groups}), encoding="utf-8")


def _write_publication(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")


class BuildScaleStatsTests(unittest.TestCase):
    def test_build_scale_stats_renders_domain_block_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_people(
                root / "site" / "data" / "people.json",
                {
                    "phd-one": {"name": "PhD One", "url": "https://example.test/phd-one"},
                    "postdoc-one": {"name": "Postdoc One", "url": "https://example.test/postdoc-one"},
                    "bs-one": {"name": "BS One", "url": "https://example.test/bs-one"},
                    "grad-phd-one": {"name": "Grad PhD One", "url": "https://example.test/grad-phd-one"},
                    "grad-phd-two": {"name": "Grad PhD Two", "url": "https://example.test/grad-phd-two"},
                    "grad-ms-one": {"name": "Grad MS One", "url": "https://example.test/grad-ms-one"},
                    "grad-bs-one": {"name": "Grad BS One", "url": "https://example.test/grad-bs-one"},
                    "grad-bs-two": {"name": "Grad BS Two", "url": "https://example.test/grad-bs-two"},
                    "grad-bs-three": {"name": "Grad BS Three", "url": "https://example.test/grad-bs-three"},
                    "alum-postdoc": {"name": "Alum Postdoc", "url": "https://example.test/alum-postdoc"},
                    "visiting-one": {"name": "Visiting One", "url": "https://example.test/visiting-one"},
                    "visiting-two": {"name": "Visiting Two", "url": "https://example.test/visiting-two"},
                },
            )
            _write_students(
                root / "site" / "data" / "students.json",
                [
                    {
                        "key": "current_students",
                        "title": "Current Students",
                        "records": [
                            {
                                "key": "phd-one",
                                "person_key": "phd-one",
                                "name": "PhD One",
                                "label": "PhD Student",
                            },
                            {
                                "key": "postdoc-one",
                                "person_key": "postdoc-one",
                                "name": "Postdoc One",
                                "label": "Postdoctoral Scholar",
                            },
                            {
                                "key": "bs-one",
                                "person_key": "bs-one",
                                "name": "BS One",
                                "label": "BS Student",
                            },
                        ],
                    },
                    {
                        "key": "completed_postdoctoral_mentoring",
                        "title": "Completed Postdoctoral Mentoring",
                        "records": [
                            {
                                "key": "alum-postdoc",
                                "person_key": "alum-postdoc",
                                "name": "Alum Postdoc",
                                "label": "Postdoc 2023",
                            }
                        ],
                    },
                    {
                        "key": "graduated_doctoral_students",
                        "title": "Graduated Doctoral Students",
                        "records": [
                            {
                                "key": "grad-phd-one",
                                "person_key": "grad-phd-one",
                                "name": "Grad PhD One",
                                "label": "PhD 2024",
                            },
                            {
                                "key": "grad-phd-two",
                                "person_key": "grad-phd-two",
                                "name": "Grad PhD Two",
                                "label": "PhD 2025",
                            },
                        ],
                    },
                    {
                        "key": "graduated_masters_students",
                        "title": "Graduated Masters Students",
                        "records": [
                            {
                                "key": "grad-ms-one",
                                "person_key": "grad-ms-one",
                                "name": "Grad MS One",
                                "label": "MS 2024",
                            }
                        ],
                    },
                    {
                        "key": "graduated_bachelors_students",
                        "title": "Graduated Bachelors Students",
                        "records": [
                            {
                                "key": "grad-bs-one",
                                "person_key": "grad-bs-one",
                                "name": "Grad BS One",
                                "label": "BS 2023",
                            },
                            {
                                "key": "grad-bs-two",
                                "person_key": "grad-bs-two",
                                "name": "Grad BS Two",
                                "label": "BS 2024",
                            },
                            {
                                "key": "grad-bs-three",
                                "person_key": "grad-bs-three",
                                "name": "Grad BS Three",
                                "label": "BS 2025",
                            },
                        ],
                    },
                    {
                        "key": "visiting_students",
                        "title": "Visiting Students",
                        "records": [
                            {
                                "key": "visiting-one",
                                "person_key": "visiting-one",
                                "name": "Visiting One",
                                "label": "BS, Summer 2023",
                            },
                            {
                                "key": "visiting-two",
                                "person_key": "visiting-two",
                                "name": "Visiting Two",
                                "label": "HS, Summer 2024",
                            },
                        ],
                    },
                ],
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
                                "title": "Computer-Aided Reasoning for Software",
                                "description_djot": "Desc",
                                "offerings": [
                                    {"year": 2026, "term": "Spring"},
                                    {
                                        "year": 2025,
                                        "term": "Autumn",
                                        "enrollment": {
                                            "students": 20,
                                            "evidence_url": "https://example.test/aut2025",
                                        },
                                    },
                                ],
                            }
                        ],
                    },
                    {
                        "key": "special_topics",
                        "records": [
                            {
                                "key": "uw-cse-599z",
                                "kind": "course",
                                "code": "UW CSE 599Z",
                                "title": "Accurate Computing",
                                "details": ["Notes"],
                                "offerings": [
                                    {
                                        "year": 2017,
                                        "term": "Spring",
                                        "enrollment": {
                                            "students": 11,
                                            "evidence_url": "https://example.test/spr2017",
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "key": "summer_school",
                        "records": [
                            {
                                "key": "marktoberdorf",
                                "kind": "summer_school",
                                "title": "EqSat",
                                "events": [
                                    {
                                        "label": "Marktoberdorf Summer School 2024",
                                        "url": "https://example.test/marktoberdorf",
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "key": "teaching_assistant",
                        "records": [
                            {
                                "key": "ucsd-cse-130",
                                "kind": "course",
                                "code": "UCSD CSE 130",
                                "title": "Programming Languages",
                                "description_djot": "Desc",
                                "offerings": [{"year": 2012, "term": "Winter"}],
                            }
                        ],
                    },
                ],
            )
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author One"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )
            _write_publication(
                root / "site" / "pubs" / "2024-demo-journal" / "publication.json",
                {
                    "local_page": True,
                    "listing_group": "main",
                    "pub_type": "journal",
                    "pub_year": 2024,
                    "title": "Journal Paper",
                    "authors": [{"name": "Author Two"}],
                    "venue": "<Programming>",
                    "venue_short": "<Programming>",
                    "description": "Local page description.",
                    "links": {"publisher": "https://example.test/journal"},
                    "talks": [],
                },
            )

            report = render_scale_stats(build_scale_stats(root))
            self.assertEqual(
                report,
                "Scale stats\n"
                "===========\n"
                "Generated from canonical site data.\n"
                "\n"
                "Students\n"
                "- Current advisees: 3 total (1 PhD, 1 postdoc, 1 BS)\n"
                "- Graduated advisees: 6 total (2 PhD, 1 MS, 3 BS)\n"
                "- Completed postdoctoral mentoring: 1\n"
                "- Visiting students: 2\n"
                "\n"
                "Publications\n"
                "- Indexed publications: 2\n"
                "\n"
                "Teaching\n"
                "- Completed UW instructor-led offerings with enrollment present: 2\n"
                "- UW students taught across those offerings: 31\n"
                "- Excludes 1 offering without enrollment: UW CSE 507 Spring 2026\n",
            )

    def test_render_scale_stats_omits_exclusion_line_when_none(self) -> None:
        report = render_scale_stats(
            ScaleStats(
                current_advisees_total=2,
                current_advisees_breakdown=(("PhD", 1), ("postdoc", 1)),
                graduated_advisees_total=3,
                graduated_advisees_breakdown=(("PhD", 2), ("MS", 1)),
                completed_postdoctoral_mentoring=1,
                visiting_students=0,
                indexed_publications=5,
                completed_uw_offerings_with_enrollment=4,
                uw_students_taught=120,
                excluded_teaching_offerings=(),
            )
        )
        self.assertIn("Students\n", report)
        self.assertIn("- Indexed publications: 5\n", report)
        self.assertNotIn("Excludes ", report)
