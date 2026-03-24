from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.source_validate import find_source_issues


class SourceValidateTests(unittest.TestCase):
    def test_reports_missing_students_registry_when_students_pages_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (students / "index.dj").write_text(
                "---\n"
                "description: Students\n"
                "---\n\n"
                "# Students\n\n"
                "__STUDENTS_CURRENT_LIST__\n\n"
                "__STUDENTS_POSTDOC_LIST__\n\n"
                "__STUDENTS_PHD_LIST__\n\n"
                "__STUDENTS_MASTERS_LIST__\n\n"
                "__STUDENTS_BACHELORS_LIST__\n\n"
                "__STUDENTS_VISITING_LIST__\n",
                encoding="utf-8",
            )
            (pages / "cv.dj").write_text(
                "---\n"
                "description: CV\n"
                "---\n\n"
                "# CV\n",
                encoding="utf-8",
            )
            (data / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "demo-person": {
                                "name": "Demo Person",
                                "url": "https://example.test/demo",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"missing student registry: {data / 'students.json'}"],
            )

    def test_reports_missing_students_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (students / "index.dj").write_text(
                "---\n"
                "description: Students\n"
                "---\n\n"
                "# Students\n\n"
                "__STUDENTS_CURRENT_LIST__\n\n"
                "__STUDENTS_POSTDOC_LIST__\n\n"
                "__STUDENTS_PHD_LIST__\n\n"
                "__STUDENTS_MASTERS_LIST__\n\n"
                "__STUDENTS_BACHELORS_LIST__\n",
                encoding="utf-8",
            )
            (data / "people.json").write_text(
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
            (data / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [{"key": "demo-student-current", "person_key": "demo-student", "name": "Demo Student", "label": "PhD Student"}],
                            },
                            {
                                "key": "completed_postdoctoral_mentoring",
                                "title": "Completed Postdoctoral Mentoring",
                                "records": [{"key": "demo-student-postdoc", "person_key": "demo-student", "name": "Demo Student", "label": "Postdoc 2025"}],
                            },
                            {
                                "key": "graduated_doctoral_students",
                                "title": "Graduated Doctoral Students",
                                "records": [{"key": "demo-student-phd", "person_key": "demo-student", "name": "Demo Student", "label": "PhD 2024"}],
                            },
                            {
                                "key": "graduated_masters_students",
                                "title": "Graduated Masters Students",
                                "records": [{"key": "demo-student-ms", "person_key": "demo-student", "name": "Demo Student", "label": "MS 2023"}],
                            },
                            {
                                "key": "graduated_bachelors_students",
                                "title": "Graduated Bachelors Students",
                                "records": [{"key": "demo-student-bs", "person_key": "demo-student", "name": "Demo Student", "label": "BS 2022"}],
                            },
                            {
                                "key": "visiting_students",
                                "title": "Visiting Students and Interns",
                                "records": [{"key": "demo-student-visiting", "person_key": "demo-student", "name": "Demo Student", "label": "Intern 2021"}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{students / 'index.dj'}: students index page must contain __STUDENTS_VISITING_LIST__"],
            )

    def test_reports_literal_student_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (students / "index.dj").write_text(
                "---\n"
                "description: Students\n"
                "---\n\n"
                "# Students\n\n"
                "__STUDENTS_CURRENT_LIST__\n\n"
                "- [Demo Student][], PhD Student\n\n"
                "__STUDENTS_POSTDOC_LIST__\n\n"
                "__STUDENTS_PHD_LIST__\n\n"
                "__STUDENTS_MASTERS_LIST__\n\n"
                "__STUDENTS_BACHELORS_LIST__\n\n"
                "__STUDENTS_VISITING_LIST__\n",
                encoding="utf-8",
            )
            (data / "people.json").write_text(
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
            (data / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [{"key": "demo-student-current", "person_key": "demo-student", "name": "Demo Student", "label": "PhD Student"}],
                            },
                            {
                                "key": "completed_postdoctoral_mentoring",
                                "title": "Completed Postdoctoral Mentoring",
                                "records": [{"key": "demo-student-postdoc", "person_key": "demo-student", "name": "Demo Student", "label": "Postdoc 2025"}],
                            },
                            {
                                "key": "graduated_doctoral_students",
                                "title": "Graduated Doctoral Students",
                                "records": [{"key": "demo-student-phd", "person_key": "demo-student", "name": "Demo Student", "label": "PhD 2024"}],
                            },
                            {
                                "key": "graduated_masters_students",
                                "title": "Graduated Masters Students",
                                "records": [{"key": "demo-student-ms", "person_key": "demo-student", "name": "Demo Student", "label": "MS 2023"}],
                            },
                            {
                                "key": "graduated_bachelors_students",
                                "title": "Graduated Bachelors Students",
                                "records": [{"key": "demo-student-bs", "person_key": "demo-student", "name": "Demo Student", "label": "BS 2022"}],
                            },
                            {
                                "key": "visiting_students",
                                "title": "Visiting Students and Interns",
                                "records": [{"key": "demo-student-visiting", "person_key": "demo-student", "name": "Demo Student", "label": "Intern 2021"}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{students / 'index.dj'}: students index page must not contain literal student entry blocks"
                ],
            )

    def test_reports_legacy_students_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "index.dj").write_text(
                "---\n"
                "description: Home\n"
                "---\n"
                "# Home\n\n"
                "[Students](students.html)\n",
                encoding="utf-8",
            )
            (students / "index.dj").write_text(
                "---\n"
                "description: Students\n"
                "---\n"
                "# Students\n\n"
                "__STUDENTS_CURRENT_LIST__\n\n"
                "__STUDENTS_POSTDOC_LIST__\n\n"
                "__STUDENTS_PHD_LIST__\n\n"
                "__STUDENTS_MASTERS_LIST__\n\n"
                "__STUDENTS_BACHELORS_LIST__\n\n"
                "__STUDENTS_VISITING_LIST__\n",
                encoding="utf-8",
            )
            (data / "people.json").write_text(
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
            (data / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [{"key": "demo-student-current", "person_key": "demo-student", "name": "Demo Student", "label": "PhD Student"}],
                            },
                            {
                                "key": "completed_postdoctoral_mentoring",
                                "title": "Completed Postdoctoral Mentoring",
                                "records": [{"key": "demo-student-postdoc", "person_key": "demo-student", "name": "Demo Student", "label": "Postdoc 2025"}],
                            },
                            {
                                "key": "graduated_doctoral_students",
                                "title": "Graduated Doctoral Students",
                                "records": [{"key": "demo-student-phd", "person_key": "demo-student", "name": "Demo Student", "label": "PhD 2024"}],
                            },
                            {
                                "key": "graduated_masters_students",
                                "title": "Graduated Masters Students",
                                "records": [{"key": "demo-student-ms", "person_key": "demo-student", "name": "Demo Student", "label": "MS 2023"}],
                            },
                            {
                                "key": "graduated_bachelors_students",
                                "title": "Graduated Bachelors Students",
                                "records": [{"key": "demo-student-bs", "person_key": "demo-student", "name": "Demo Student", "label": "BS 2022"}],
                            },
                            {
                                "key": "visiting_students",
                                "title": "Visiting Students and Interns",
                                "records": [{"key": "demo-student-visiting", "person_key": "demo-student", "name": "Demo Student", "label": "Intern 2021"}],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'index.dj'}: legacy students link should use canonical collection path: students.html -> students/"],
            )

    def test_reports_missing_publications_main_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n\n"
                "- [DBLP](https://dblp.org/)\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pubs / 'index.dj'}: publications index page must contain __PUBLICATIONS_MAIN_LIST__"
                ],
            )

    def test_reports_missing_publications_workshop_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "## Aggregators\n\n"
                "- [DBLP](https://dblp.org/)\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pubs / 'index.dj'}: publications index page must contain __PUBLICATIONS_WORKSHOP_LIST__"
                ],
            )

    def test_reports_literal_publication_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "{#2025-test-demo}\n"
                "*[Demo Paper](https://example.test/paper)* \\\n"
                "  Demo Author\n"
                "\\\n"
                "DemoConf 2025\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n\n"
                "- [DBLP](https://dblp.org/)\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pubs / 'index.dj'}: publications index page must not contain literal publication entry blocks"
                ],
            )

    def test_accepts_publications_index_projection_wrapper_with_mixed_bundle_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n\n"
                "- [DBLP](https://dblp.org/)\n",
                encoding="utf-8",
            )

            main_dir = pubs / "2025-test-main"
            main_dir.mkdir()
            (main_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {"publisher": "https://example.test/main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            workshop_dir = pubs / "2025-test-workshop"
            workshop_dir.mkdir()
            (workshop_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "listing_group": "workshop",
                        "pub_date": "2025-01-01",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Demo Workshop",
                        "description": "Workshop description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (workshop_dir / "2025-test-workshop-abstract.md").write_text(
                "Demo abstract.\n",
                encoding="utf-8",
            )
            (workshop_dir / "2025-test-workshop.bib").write_text(
                "@inproceedings{demo,\n  title={Demo}\n}\n",
                encoding="utf-8",
            )
            (workshop_dir / "2025-test-workshop.pdf").write_bytes(b"%PDF-1.4\n")
            (workshop_dir / "2025-test-workshop-absimg.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_invalid_talk_bundle_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "index.dj").write_text(
                "---\n"
                "description: Home\n"
                "---\n"
                "# Home\n",
                encoding="utf-8",
            )
            (talks / "index.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n"
                "# Talks\n\n"
                "__TALKS_LIST__\n",
                encoding="utf-8",
            )

            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{talk_dir / 'talk.json'}.when: must provide exactly one of month or season"],
            )

    def test_reports_missing_talks_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (talks / "index.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n"
                "# Talks\n\n"
                "Manual list.\n",
                encoding="utf-8",
            )

            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{talks / 'index.dj'}: talks index page must contain __TALKS_LIST__"],
            )

    def test_reports_missing_talks_index_page_when_talk_bundles_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{talks / 'index.dj'}: talks index page is required when talk bundles exist"],
            )

    def test_reports_legacy_talks_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "index.dj").write_text(
                "---\n"
                "description: Home\n"
                "---\n"
                "# Home\n\n"
                "[Talks](talks.html)\n",
                encoding="utf-8",
            )
            (talks / "index.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n"
                "# Talks\n\n"
                "__TALKS_LIST__\n",
                encoding="utf-8",
            )
            talk_dir = talks / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Demo",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'index.dj'}: legacy talks link should use canonical collection path: talks.html -> talks/"],
            )

    def test_reports_legacy_publications_index_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "index.dj").write_text(
                "---\n"
                "description: Home\n"
                "---\n"
                "# Home\n\n"
                "[Publications](publications.html)\n",
                encoding="utf-8",
            )
            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )
            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pages / 'index.dj'}: legacy publications index link should use canonical collection path: "
                    "publications.html -> pubs/"
                ],
            )

    def test_reports_legacy_publications_wrapper_after_cutover(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "publications.dj").write_text(
                "---\n"
                "description: Legacy publications wrapper\n"
                "---\n"
                "# Publications\n",
                encoding="utf-8",
            )
            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )
            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pages / 'publications.dj'}: publications index wrapper must move to {pubs / 'index.dj'}"
                ],
            )

    def test_accepts_configured_static_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/demo.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )
            (img_dir / "demo.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_configured_static_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/missing.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'about.dj'}: image path does not exist: img/missing.png"],
            )

    def test_reports_missing_front_matter_for_pub_prefix_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            page_path = pages / "pub-demo.dj"
            page_path.write_text("# Demo\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{page_path}: missing front matter metadata"],
            )

    def test_accepts_publication_local_metadata_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)
            (img_dir / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )

            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "meta_image_path": "pubs/2025-test-demo/custom-meta.png",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (pub_dir / "custom-meta.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_publication_metadata_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            img_dir.mkdir(parents=True)
            (img_dir / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )

            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "meta_image_path": "pubs/2025-test-demo/missing-meta.png",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{pub_dir / 'publication.json'}: image path does not exist: pubs/2025-test-demo/missing-meta.png"
                ],
            )

    def test_accepts_index_only_publication_bundle_without_local_page_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )

            pub_dir = pubs / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_legacy_publication_link_in_page_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            page_path = pages / "index.dj"
            page_path.write_text(
                "---\n"
                "description: Demo description\n"
                "---\n"
                "# Home\n\nSee [paper](pub-2024-asplos-lakeroad.html).\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{page_path}: legacy publication link should use canonical publication path: "
                    "pub-2024-asplos-lakeroad.html -> pubs/2024-asplos-lakeroad/"
                ],
            )

    def test_reports_legacy_publication_link_in_publication_extra_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            extra_path = pubs / "2025-test-demo" / "extra.dj"
            extra_path.parent.mkdir()
            extra_path.write_text(
                "See [older paper](pub-2024-asplos-lakeroad.html).\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{extra_path}: legacy publication link should use canonical publication path: "
                    "pub-2024-asplos-lakeroad.html -> pubs/2024-asplos-lakeroad/"
                ],
            )

    def test_reports_root_layout_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)

            (root / "about.dj").write_text("# About\n", encoding="utf-8")
            (root / "robots.txt").write_text("User-agent: *\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<urlset/>\n", encoding="utf-8")
            (root / "img").mkdir()
            (root / "templates").mkdir()
            (root / "pubs").mkdir()

            config = load_site_config(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{root / 'about.dj'}: authored Djot source must live under site/pages/",
                    f"{root / 'sitemap.xml'}: generated sitemap belongs only under build/",
                    f"{root / 'robots.txt'}: static assets must live under site/static/",
                    f"{root / 'img'}: shared images must live under site/static/img/",
                    f"{root / 'pubs'}: publication bundles must live under site/pubs/",
                    f"{root / 'templates'}: templates must live under site/templates/",
                ],
            )
