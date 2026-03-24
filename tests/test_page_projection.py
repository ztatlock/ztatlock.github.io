from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.page_projection import (
    STUDENTS_BACHELORS_LIST_PLACEHOLDER,
    STUDENTS_CURRENT_LIST_PLACEHOLDER,
    STUDENTS_MASTERS_LIST_PLACEHOLDER,
    STUDENTS_PHD_LIST_PLACEHOLDER,
    STUDENTS_POSTDOC_LIST_PLACEHOLDER,
    STUDENTS_VISITING_LIST_PLACEHOLDER,
    TALKS_LIST_PLACEHOLDER,
    apply_page_projections,
    render_students_section_list_djot,
    render_talks_list_djot,
)


def _student_section(
    key: str,
    title: str,
    record: dict[str, object],
) -> dict[str, object]:
    return {
        "key": key,
        "title": title,
        "records": [record],
    }


class PageProjectionTests(unittest.TestCase):
    def test_renders_talks_list_from_bundles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            first = talks_dir / "2026-02-brown-eqsat"
            first.mkdir(parents=True)
            (first / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Everything is a compiler, try Equality Saturation!",
                        "when": {"year": 2026, "month": 2},
                        "at": [
                            {"text": "Brown University"},
                            {"text": "PL and Graphics groups"},
                        ],
                        "url": "https://events.brown.edu/demo",
                    }
                ),
                encoding="utf-8",
            )
            second = talks_dir / "2023-05-uiuc-egg"
            second.mkdir(parents=True)
            (second / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Relational Equality Saturation in egg",
                        "when": {"year": 2023, "month": 5},
                        "at": [
                            {"text": "University of Illinois at Urbana-Champaign"},
                            {
                                "text": "Compilers Seminar",
                                "url": "https://compilerseminar.web.illinois.edu/",
                            },
                        ],
                        "url": "talk-2023-05-egg-uiuc.html",
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_talks_list_djot(root, talks_dir=talks_dir)
            self.assertIn(
                "- [Everything is a compiler, try Equality Saturation!](https://events.brown.edu/demo) \\",
                rendered,
            )
            self.assertIn(
                "Brown University, PL and Graphics groups, February 2026",
                rendered,
            )
            self.assertIn(
                "- [Relational Equality Saturation in egg](talk-2023-05-egg-uiuc.html) \\",
                rendered,
            )
            self.assertIn(
                "University of Illinois at Urbana-Champaign, [Compilers Seminar](https://compilerseminar.web.illinois.edu/), May 2023",
                rendered,
            )
            self.assertLess(rendered.find("February 2026"), rendered.find("May 2023"))

    def test_applies_projection_only_to_talks_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            talk_dir = talks_dir / "2026-02-brown-eqsat"
            talk_dir.mkdir(parents=True)
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Everything is a compiler, try Equality Saturation!",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            body = "# Talks\n\n" + TALKS_LIST_PLACEHOLDER + "\n"
            rendered = apply_page_projections(
                "talks_index_page",
                "talks",
                body,
                root=root,
                talks_dir=talks_dir,
            )
            self.assertNotIn(TALKS_LIST_PLACEHOLDER, rendered)
            self.assertIn("Brown University, February 2026", rendered)

            self.assertEqual(
                apply_page_projections(
                    "ordinary_page",
                    "about",
                    body,
                    root=root,
                    talks_dir=talks_dir,
                ),
                body,
            )

    def test_applies_publications_projection_only_to_publications_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pubs_dir = root / "site" / "pubs"
            main_dir = pubs_dir / "2025-test-main"
            main_dir.mkdir(parents=True)
            (main_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [{"name": "Demo Author", "ref": "Demo Author"}],
                        "venue": "DemoConf",
                        "links": {"publisher": "https://example.test/main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            workshop_dir = pubs_dir / "2025-test-workshop"
            workshop_dir.mkdir(parents=True)
            (workshop_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "workshop",
                        "pub_date": "2025-01-02",
                        "primary_link": "publisher",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Demo Workshop",
                        "links": {"publisher": "https://example.test/workshop"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# Publications\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n"
            )
            rendered = apply_page_projections(
                "publications_index_page",
                "publications",
                body,
                root=root,
                publications_dir=pubs_dir,
            )
            self.assertNotIn("__PUBLICATIONS_MAIN_LIST__", rendered)
            self.assertNotIn("__PUBLICATIONS_WORKSHOP_LIST__", rendered)
            self.assertIn("https://example.test/main", rendered)
            self.assertIn("https://example.test/workshop", rendered)

            self.assertEqual(
                apply_page_projections(
                    "ordinary_page",
                    "about",
                    body,
                    root=root,
                    publications_dir=pubs_dir,
                ),
                body,
            )

    def test_renders_students_section_from_canonical_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "amy-zhu": {"name": "Amy Zhu", "url": "https://example.test/amy"},
                            "adriana-schulz": {"name": "Adriana Schulz", "url": "https://example.test/adriana"},
                            "zhiyuan-yan": {"name": "Zhiyuan Yan", "url": "https://example.test/zhiyuan"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            (data_dir / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            _student_section(
                                "current_students",
                                "Current Students",
                                {
                                    "key": "amy-zhu-phd-student",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "PhD Student",
                                    "details": [
                                        {"kind": "coadvisor", "person_keys": ["adriana-schulz"]},
                                    ],
                                },
                            ),
                            _student_section(
                                "completed_postdoctoral_mentoring",
                                "Completed Postdoctoral Mentoring",
                                {
                                    "key": "amy-zhu-postdoc-2024",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "Postdoc 2024",
                                },
                            ),
                            _student_section(
                                "graduated_doctoral_students",
                                "Graduated Doctoral Students",
                                {
                                    "key": "amy-zhu-phd-2024",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "PhD 2024",
                                },
                            ),
                            _student_section(
                                "graduated_masters_students",
                                "Graduated Masters Students",
                                {
                                    "key": "amy-zhu-ms-2023",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "MS 2023",
                                },
                            ),
                            _student_section(
                                "graduated_bachelors_students",
                                "Graduated Bachelors Students",
                                {
                                    "key": "zhiyuan-yan-bs-2024",
                                    "person_key": "zhiyuan-yan",
                                    "name": "Zhiyuan (Kevin) Yan",
                                    "label": "BS 2024",
                                    "details": [
                                        {"kind": "outcome", "djot": "MS Student at UCSD"},
                                    ],
                                },
                            ),
                            _student_section(
                                "visiting_students",
                                "Visiting Students and Interns",
                                {
                                    "key": "amy-zhu-visiting-2022",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "Summer Intern 2022",
                                },
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered_current = render_students_section_list_djot(
                root,
                "current_students",
                data_dir=data_dir,
            )
            self.assertIn("- [Amy Zhu][], PhD Student", rendered_current)
            self.assertIn("co-advised with [Adriana Schulz][]", rendered_current)

            rendered_bachelors = render_students_section_list_djot(
                root,
                "graduated_bachelors_students",
                data_dir=data_dir,
            )
            self.assertIn("[Zhiyuan (Kevin) Yan][Zhiyuan Yan], BS 2024", rendered_bachelors)
            self.assertIn("MS Student at UCSD", rendered_bachelors)

    def test_applies_projection_only_to_students_index_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "haobin-ni": {"name": "Haobin Ni", "url": "https://example.test/haobin"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            (data_dir / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            _student_section(
                                "current_students",
                                "Current Students",
                                {
                                    "key": "haobin-ni-postdoctoral-scholar",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "Postdoctoral Scholar",
                                },
                            ),
                            _student_section(
                                "completed_postdoctoral_mentoring",
                                "Completed Postdoctoral Mentoring",
                                {
                                    "key": "haobin-ni-postdoc-2023",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "Postdoc 2023",
                                },
                            ),
                            _student_section(
                                "graduated_doctoral_students",
                                "Graduated Doctoral Students",
                                {
                                    "key": "haobin-ni-phd-2022",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "PhD 2022",
                                },
                            ),
                            _student_section(
                                "graduated_masters_students",
                                "Graduated Masters Students",
                                {
                                    "key": "haobin-ni-ms-2021",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "MS 2021",
                                },
                            ),
                            _student_section(
                                "graduated_bachelors_students",
                                "Graduated Bachelors Students",
                                {
                                    "key": "haobin-ni-bs-2020",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "BS 2020",
                                },
                            ),
                            _student_section(
                                "visiting_students",
                                "Visiting Students and Interns",
                                {
                                    "key": "haobin-ni-visiting-2019",
                                    "person_key": "haobin-ni",
                                    "name": "Haobin Ni",
                                    "label": "Visiting Student 2019",
                                },
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# Students\n\n"
                f"{STUDENTS_CURRENT_LIST_PLACEHOLDER}\n\n"
                f"{STUDENTS_POSTDOC_LIST_PLACEHOLDER}\n\n"
                f"{STUDENTS_PHD_LIST_PLACEHOLDER}\n\n"
                f"{STUDENTS_MASTERS_LIST_PLACEHOLDER}\n\n"
                f"{STUDENTS_BACHELORS_LIST_PLACEHOLDER}\n\n"
                f"{STUDENTS_VISITING_LIST_PLACEHOLDER}\n"
            )
            rendered = apply_page_projections(
                "students_index_page",
                "students",
                body,
                root=root,
                data_dir=data_dir,
            )
            self.assertNotIn(STUDENTS_CURRENT_LIST_PLACEHOLDER, rendered)
            self.assertIn("Haobin Ni", rendered)

            self.assertEqual(
                apply_page_projections(
                    "ordinary_page",
                    "about",
                    body,
                    root=root,
                    data_dir=data_dir,
                ),
                body,
            )

    def test_renders_students_section_from_explicit_data_dir_people_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            default_data_dir = root / "site" / "data"
            explicit_data_dir = root / "alt-data"
            default_data_dir.mkdir(parents=True)
            explicit_data_dir.mkdir(parents=True)

            (default_data_dir / "people.json").write_text(
                json.dumps({"people": {}}),
                encoding="utf-8",
            )
            (explicit_data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "demo-student": {
                                "name": "Demo Student",
                                "url": "https://example.test/demo",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            (explicit_data_dir / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            _student_section(
                                "current_students",
                                "Current Students",
                                {
                                    "key": "demo-student-current",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "PhD Student",
                                },
                            )
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_students_section_list_djot(
                root,
                "current_students",
                data_dir=explicit_data_dir,
            )
            self.assertIn("- [Demo Student][], PhD Student", rendered)
