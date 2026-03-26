from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.collaborators_index import (
    load_collaborator_entries,
    load_research_collaborator_entries,
    load_teaching_collaborator_entries,
    render_missing_collaborator_first_initials,
    render_missing_collaborator_last_initials,
    render_public_research_collaborators_list_djot,
    render_public_teaching_collaborators_list_djot,
)


def _write_publication(
    pubs_dir: Path,
    slug: str,
    *,
    title: str,
    pub_date: str,
    authors: list[dict[str, str]],
) -> None:
    pub_dir = pubs_dir / slug
    pub_dir.mkdir(parents=True)
    (pub_dir / "publication.json").write_text(
        json.dumps(
            {
                "detail_page": False,
                "listing_group": "main",
                "pub_date": pub_date,
                "primary_link": "publisher",
                "title": title,
                "authors": authors,
                "venue": "DemoConf",
                "links": {"publisher": f"https://example.test/{slug}"},
                "talks": [],
            }
        ),
        encoding="utf-8",
    )


class CollaboratorsIndexTests(unittest.TestCase):
    def test_load_collaborator_entries_uses_default_name_and_excludes_self(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "james-wilcox": {
                                "name": "James Wilcox",
                                "url": "https://example.test/james",
                                "aliases": ["James R. Wilcox"],
                            },
                            "michael-ernst": {
                                "name": "Mike Ernst",
                                "url": "https://example.test/michael",
                                "aliases": ["Michael Ernst", "Michael D. Ernst"],
                            },
                            "remy-wang": {
                                "name": "Remy Wang",
                                "url": "https://example.test/remy",
                                "aliases": ["Yisu Remy Wang"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "James R. Wilcox", "ref": "James Wilcox"},
                    {"name": "Michael D. Ernst", "ref": "Mike Ernst"},
                    {"name": "Robert Rabe", "ref": ""},
                ],
            )
            _write_publication(
                pubs_dir,
                "2024-demo-two",
                title="Second Paper",
                pub_date="2024-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "James Wilcox", "ref": "James Wilcox"},
                    {"name": "Mike Ernst", "ref": "Mike Ernst"},
                    {"name": "Remy Wang", "ref": "Remy Wang"},
                ],
            )

            entries = load_collaborator_entries(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
            )

            self.assertEqual(
                [(entry.display_name, entry.is_linked) for entry in entries],
                [
                    ("James Wilcox", True),
                    ("Mike Ernst", True),
                    ("Remy Wang", True),
                    ("Robert Rabe", False),
                ],
            )

    def test_render_public_research_collaborators_list_links_resolved_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)
            students_path = data_dir / "students.json"

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "adam-geller": {
                                "name": "Adam Geller",
                                "url": "https://example.test/adam",
                                "aliases": ["Adam T. Geller"],
                            },
                            "kevin-mu": {
                                "name": "Kevin Mu",
                                "url": "https://example.test/kevin",
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "Adam T. Geller", "ref": "Adam Geller"},
                    {"name": "Robert Rabe", "ref": ""},
                ],
            )
            students_path.write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [
                                    {
                                        "key": "adam-geller-phd-student",
                                        "person_key": "adam-geller",
                                        "name": "Adam Geller",
                                        "label": "PhD Student",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_public_research_collaborators_list_djot(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
                students_path=students_path,
            )

            self.assertEqual(
                rendered,
                "* [Adam Geller][]\n"
                "* Robert Rabe\n",
            )

    def test_resolved_linkless_research_collaborator_renders_as_plain_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)
            students_path = data_dir / "students.json"

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "alpha-person": {
                                "name": "Alpha Person",
                                "aliases": ["A. Person"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "A. Person", "ref": "Alpha Person"},
                ],
            )
            students_path.write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [
                                    {
                                        "key": "alpha-person-student",
                                        "person_key": "alpha-person",
                                        "name": "Alpha Person",
                                        "label": "PhD Student",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_public_research_collaborators_list_djot(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
                students_path=students_path,
            )

            self.assertEqual(rendered, "* Alpha Person\n")

    def test_load_research_collaborator_entries_adds_student_only_people(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)
            students_path = data_dir / "students.json"

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "adam-geller": {
                                "name": "Adam Geller",
                                "url": "https://example.test/adam",
                            },
                            "kevin-mu": {
                                "name": "Kevin Mu",
                                "url": "https://example.test/kevin",
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "Adam Geller", "ref": "Adam Geller"},
                ],
            )
            students_path.write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [
                                    {
                                        "key": "kevin-mu-phd-student",
                                        "person_key": "kevin-mu",
                                        "name": "Kevin Mu",
                                        "label": "PhD Student",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            entries = load_research_collaborator_entries(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
                students_path=students_path,
            )

            self.assertEqual(
                [(entry.display_name, entry.is_linked) for entry in entries],
                [("Adam Geller", True), ("Kevin Mu", True)],
            )

    def test_render_public_teaching_collaborators_list_flattens_staffing_roles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            teaching_path = data_dir / "teaching.json"

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "james-wilcox": {
                                "name": "James Wilcox",
                                "url": "https://example.test/james",
                            },
                            "audrey-seo": {
                                "name": "Audrey Seo",
                                "url": "https://example.test/audrey",
                            },
                            "joe-redmon": {
                                "name": "Joe Redmon",
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            teaching_path.write_text(
                json.dumps(
                    {
                        "groups": [
                            {
                                "key": "uw_courses",
                                "records": [
                                    {
                                        "key": "uw-cse-505",
                                        "kind": "course",
                                        "code": "UW CSE 505",
                                        "title": "Concepts",
                                        "institution": "University of Washington",
                                        "description_djot": "course description",
                                        "offerings": [
                                            {
                                                "year": 2025,
                                                "term": "Spring",
                                                "co_instructors": ["james-wilcox"],
                                                "teaching_assistants": ["audrey-seo"],
                                                "tutors": ["joe-redmon"],
                                            }
                                        ],
                                    }
                                ],
                            }
                            ,
                            {
                                "key": "special_topics",
                                "records": [
                                    {
                                        "key": "uw-cse-599z",
                                        "kind": "course",
                                        "code": "UW CSE 599Z",
                                        "title": "Special Topics",
                                        "institution": "University of Washington",
                                        "details": ["special topics"],
                                        "offerings": [{"year": 2024, "term": "Spring"}],
                                    }
                                ],
                            },
                            {
                                "key": "summer_school",
                                "records": [
                                    {
                                        "key": "summer-school-demo",
                                        "kind": "summer_school",
                                        "title": "Summer School",
                                        "events": [
                                            {"label": "2024 Demo", "url": "https://example.test/summer"}
                                        ],
                                    }
                                ],
                            },
                            {
                                "key": "teaching_assistant",
                                "records": [
                                    {
                                        "key": "demo-ta-course",
                                        "kind": "course",
                                        "code": "Demo 101",
                                        "title": "Demo TA Course",
                                        "institution": "University of Washington",
                                        "description_djot": "teaching assistant history",
                                        "offerings": [{"year": 2024, "term": "Winter"}],
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            entries = load_teaching_collaborator_entries(
                root,
                people_path=data_dir / "people.json",
                teaching_path=teaching_path,
            )
            self.assertEqual(
                [(entry.display_name, entry.is_linked) for entry in entries],
                [("Audrey Seo", True), ("James Wilcox", True), ("Joe Redmon", False)],
            )

            rendered = render_public_teaching_collaborators_list_djot(
                root,
                people_path=data_dir / "people.json",
                teaching_path=teaching_path,
            )
            self.assertEqual(
                rendered,
                "* [Audrey Seo][]\n"
                "* [James Wilcox][]\n"
                "* Joe Redmon\n",
            )

    def test_renders_missing_initials_from_collaborator_display_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "adam-geller": {
                                "name": "Adam Geller",
                                "url": "https://example.test/adam",
                                "aliases": ["Adam T. Geller"],
                            },
                            "remy-wang": {
                                "name": "Remy Wang",
                                "url": "https://example.test/remy",
                                "aliases": ["Yisu Remy Wang"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "Adam T. Geller", "ref": "Adam Geller"},
                    {"name": "Yisu Remy Wang", "ref": "Remy Wang"},
                    {"name": "Robert Rabe", "ref": ""},
                ],
            )

            first_missing = render_missing_collaborator_first_initials(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
            ).split(", ")
            last_missing = render_missing_collaborator_last_initials(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
            ).split(", ")

            self.assertNotIn("A", first_missing)
            self.assertNotIn("R", first_missing)
            self.assertIn("Y", first_missing)
            self.assertIn("Q", first_missing)

            self.assertNotIn("G", last_missing)
            self.assertNotIn("R", last_missing)
            self.assertNotIn("W", last_missing)
            self.assertIn("Q", last_missing)


if __name__ == "__main__":
    unittest.main()
