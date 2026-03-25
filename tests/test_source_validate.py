from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.source_validate import find_source_issues


def _write_publication_bundle(
    publications_dir: Path,
    *,
    slug: str,
    listing_group: str,
    title: str,
    pub_date: str,
) -> None:
    pub_dir = publications_dir / slug
    pub_dir.mkdir()
    (pub_dir / "publication.json").write_text(
        json.dumps(
            {
                "detail_page": False,
                "listing_group": listing_group,
                "pub_date": pub_date,
                "primary_link": "publisher",
                "title": title,
                "authors": [{"name": "Demo Author", "ref": ""}],
                "venue": "Demo Venue",
                "links": {"publisher": f"https://example.test/{slug}"},
                "talks": [],
            }
        ),
        encoding="utf-8",
    )


class SourceValidateTests(unittest.TestCase):
    def test_reports_legacy_cv_wrapper_move(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "cv.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'cv.dj'}: CV wrapper must move to {root / 'site' / 'cv' / 'index.dj'}"],
            )

    def test_reports_legacy_cv_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (pages / "notes.dj").write_text(
                "---\n"
                "description: Notes page\n"
                "---\n\n"
                "# Notes\n\n"
                "- [Curriculum Vitae](cv.html)\n",
                encoding="utf-8",
            )
            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'notes.dj'}: legacy CV link should use canonical collection path: cv.html -> cv/"],
            )

    def test_reports_missing_funding_registry_when_cv_funding_section_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Funding\n\n"
                "- Demo Grant \\\n"
                "  PI; NSF; $100,000; 2020 - 2023\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"missing funding registry: {data / 'funding.json'}"],
            )

    def test_accepts_valid_funding_registry_for_cv_funding_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            funding = root / "site" / "funding"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            funding.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Funding\n\n"
                "- Demo Grant \\\n"
                "  PI; NSF; $100,000; 2020 - 2023\n",
                encoding="utf-8",
            )
            (funding / "index.dj").write_text(
                "---\n"
                "description: Funding page\n"
                "---\n\n"
                "# Funding\n\n"
                "__FUNDING_LIST__\n",
                encoding="utf-8",
            )
            (data / "funding.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2020-demo-grant",
                                "title": "Demo Grant",
                                "role": "PI",
                                "sponsor": "NSF",
                                "amount_usd": 100000,
                                "start_year": 2020,
                                "end_year": 2023,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                funding_dir=funding,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_funding_index_when_canonical_funding_records_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Funding\n\n"
                "- Demo Grant \\\n"
                "  PI; NSF; $100,000; 2020 - 2023\n",
                encoding="utf-8",
            )
            (data / "funding.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2020-demo-grant",
                                "title": "Demo Grant",
                                "role": "PI",
                                "sponsor": "NSF",
                                "amount_usd": 100000,
                                "start_year": 2020,
                                "end_year": 2023,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{root / 'site' / 'funding' / 'index.dj'}: funding index page is required when canonical funding records exist"],
            )

    def test_reports_missing_funding_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            funding = root / "site" / "funding"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            students = root / "site" / "students"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            funding.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Funding\n\n"
                "- Demo Grant \\\n"
                "  PI; NSF; $100,000; 2020 - 2023\n",
                encoding="utf-8",
            )
            (funding / "index.dj").write_text(
                "---\n"
                "description: Funding page\n"
                "---\n\n"
                "# Funding\n\n"
                "Research grants.\n",
                encoding="utf-8",
            )
            (data / "funding.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2020-demo-grant",
                                "title": "Demo Grant",
                                "role": "PI",
                                "sponsor": "NSF",
                                "amount_usd": 100000,
                                "start_year": 2020,
                                "end_year": 2023,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                funding_dir=funding,
                talks_dir=talks,
                publications_dir=pubs,
                students_dir=students,
                service_dir=service,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{funding / 'index.dj'}: funding index page must contain __FUNDING_LIST__"],
            )

    def test_reports_missing_cv_students_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Students\n\n"
                "### _Current Students_\n\n"
                "__CV_STUDENTS_CURRENT_LIST__\n\n"
                "### _Completed Postdoctoral Mentoring_\n\n"
                "__CV_STUDENTS_POSTDOC_LIST__\n\n"
                "### _Graduated Doctoral Students_\n\n"
                "__CV_STUDENTS_PHD_LIST__\n\n"
                "### _Graduated Masters Students_\n\n"
                "__CV_STUDENTS_MASTERS_LIST__\n\n"
                "### _Graduated Bachelors Students_\n\n"
                "__CV_STUDENTS_BACHELORS_LIST__\n\n"
                "### _Visiting Students and Interns_\n\n",
                encoding="utf-8",
            )
            (students / "index.dj").write_text(
                "---\n"
                "description: Students page\n"
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
                            {"key": "current_students", "title": "Current Students", "records": [{"key": "demo-current", "person_key": "demo-student", "name": "Demo Student", "label": "PhD Student"}]},
                            {"key": "completed_postdoctoral_mentoring", "title": "Completed Postdoctoral Mentoring", "records": [{"key": "demo-postdoc", "person_key": "demo-student", "name": "Demo Student", "label": "Postdoc 2025"}]},
                            {"key": "graduated_doctoral_students", "title": "Graduated Doctoral Students", "records": [{"key": "demo-phd", "person_key": "demo-student", "name": "Demo Student", "label": "PhD 2024"}]},
                            {"key": "graduated_masters_students", "title": "Graduated Masters Students", "records": [{"key": "demo-ms", "person_key": "demo-student", "name": "Demo Student", "label": "MS 2023"}]},
                            {"key": "graduated_bachelors_students", "title": "Graduated Bachelors Students", "records": [{"key": "demo-bs", "person_key": "demo-student", "name": "Demo Student", "label": "BS 2022"}]},
                            {"key": "visiting_students", "title": "Visiting Students and Interns", "records": [{"key": "demo-visiting", "person_key": "demo-student", "name": "Demo Student", "label": "Intern 2021"}]},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV students section must contain __CV_STUDENTS_VISITING_LIST__"],
            )

    def test_reports_literal_cv_student_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Students\n\n"
                "### _Current Students_\n\n"
                "__CV_STUDENTS_CURRENT_LIST__\n\n"
                "- Demo Student, PhD Student\n\n"
                "### _Completed Postdoctoral Mentoring_\n\n"
                "__CV_STUDENTS_POSTDOC_LIST__\n\n"
                "### _Graduated Doctoral Students_\n\n"
                "__CV_STUDENTS_PHD_LIST__\n\n"
                "### _Graduated Masters Students_\n\n"
                "__CV_STUDENTS_MASTERS_LIST__\n\n"
                "### _Graduated Bachelors Students_\n\n"
                "__CV_STUDENTS_BACHELORS_LIST__\n\n"
                "### _Visiting Students and Interns_\n\n"
                "__CV_STUDENTS_VISITING_LIST__\n",
                encoding="utf-8",
            )
            (students / "index.dj").write_text(
                "---\n"
                "description: Students page\n"
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
                            {"key": "current_students", "title": "Current Students", "records": [{"key": "demo-current", "person_key": "demo-student", "name": "Demo Student", "label": "PhD Student"}]},
                            {"key": "completed_postdoctoral_mentoring", "title": "Completed Postdoctoral Mentoring", "records": [{"key": "demo-postdoc", "person_key": "demo-student", "name": "Demo Student", "label": "Postdoc 2025"}]},
                            {"key": "graduated_doctoral_students", "title": "Graduated Doctoral Students", "records": [{"key": "demo-phd", "person_key": "demo-student", "name": "Demo Student", "label": "PhD 2024"}]},
                            {"key": "graduated_masters_students", "title": "Graduated Masters Students", "records": [{"key": "demo-ms", "person_key": "demo-student", "name": "Demo Student", "label": "MS 2023"}]},
                            {"key": "graduated_bachelors_students", "title": "Graduated Bachelors Students", "records": [{"key": "demo-bs", "person_key": "demo-student", "name": "Demo Student", "label": "BS 2022"}]},
                            {"key": "visiting_students", "title": "Visiting Students and Interns", "records": [{"key": "demo-visiting", "person_key": "demo-student", "name": "Demo Student", "label": "Intern 2021"}]},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV students section must not contain literal student entry blocks"],
            )

    def test_reports_missing_teaching_registry_when_cv_uses_teaching_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Teaching\n\n"
                "### _Instructor_\n\n"
                "__CV_TEACHING_INSTRUCTOR_LIST__\n\n"
                "### _Summer School Courses_\n\n"
                "__CV_TEACHING_SUMMER_SCHOOL_LIST__\n\n"
                "### _Teaching Assistant_\n\n"
                "__CV_TEACHING_TA_LIST__\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"missing teaching registry: {data / 'teaching.json'}"],
            )

    def test_reports_missing_cv_teaching_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Teaching\n\n"
                "### _Instructor_\n\n"
                "__CV_TEACHING_INSTRUCTOR_LIST__\n\n"
                "### _Summer School Courses_\n\n"
                "__CV_TEACHING_SUMMER_SCHOOL_LIST__\n\n"
                "### _Teaching Assistant_\n\n",
                encoding="utf-8",
            )
            (teaching / "index.dj").write_text(
                "---\n"
                "description: Teaching\n"
                "---\n\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
                "__TEACHING_SUMMER_SCHOOL_LIST__\n",
                encoding="utf-8",
            )
            (data / "teaching.json").write_text(
                json.dumps(
                    {
                        "groups": [
                            {
                                "key": "uw_courses",
                                "records": [
                                    {
                                        "key": "uw-cse-507",
                                        "kind": "course",
                                        "code": "UW CSE 507",
                                        "title": "Course",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2025, "term": "Autumn"}],
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
                                        "title": "Topics",
                                        "details": ["Notes"],
                                        "offerings": [{"year": 2017, "term": "Spring"}],
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
                                        "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
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
                                        "title": "PL",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2012, "term": "Winter"}],
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV teaching section must contain __CV_TEACHING_TA_LIST__"],
            )

    def test_reports_literal_cv_teaching_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Teaching\n\n"
                "### _Instructor_\n\n"
                "__CV_TEACHING_INSTRUCTOR_LIST__\n\n"
                "- *UW CSE 507: Course* \\\n"
                "  Desc\n\n"
                "### _Summer School Courses_\n\n"
                "__CV_TEACHING_SUMMER_SCHOOL_LIST__\n\n"
                "### _Teaching Assistant_\n\n"
                "__CV_TEACHING_TA_LIST__\n",
                encoding="utf-8",
            )
            (teaching / "index.dj").write_text(
                "---\n"
                "description: Teaching\n"
                "---\n\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
                "__TEACHING_SUMMER_SCHOOL_LIST__\n",
                encoding="utf-8",
            )
            (data / "teaching.json").write_text(
                json.dumps(
                    {
                        "groups": [
                            {
                                "key": "uw_courses",
                                "records": [
                                    {
                                        "key": "uw-cse-507",
                                        "kind": "course",
                                        "code": "UW CSE 507",
                                        "title": "Course",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2025, "term": "Autumn"}],
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
                                        "title": "Topics",
                                        "details": ["Notes"],
                                        "offerings": [{"year": 2017, "term": "Spring"}],
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
                                        "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
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
                                        "title": "PL",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2012, "term": "Winter"}],
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV teaching section must not contain literal teaching entry blocks"],
            )

    def test_accepts_cv_publications_projection_wrapper_with_authored_book_chapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            service = root / "site" / "service"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Publications\n\n"
                "### _Conference and Journal Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__CV_PUBLICATIONS_MAIN_LIST__\n\n"
                ":::\n\n"
                "### _Workshop Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__CV_PUBLICATIONS_WORKSHOP_LIST__\n\n"
                ":::\n\n"
                "### _Book Chapters_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "*Chapter 8: Parameterized Program Equivalence Checking* \\\n"
                "High-Level Verification: Methods and Tools for Verification of System-Level Designs \\\n"
                "Sudipta Kundu, Sorin Lerner, and Rajesh K. Gupta; Springer 2011\n\n"
                ":::\n",
                encoding="utf-8",
            )
            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications page\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                ":::\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                ":::\n",
                encoding="utf-8",
            )
            _write_publication_bundle(
                pubs,
                slug="2025-test-main",
                listing_group="main",
                title="Main Paper",
                pub_date="2025-01-01",
            )
            _write_publication_bundle(
                pubs,
                slug="2024-test-workshop",
                listing_group="workshop",
                title="Workshop Paper",
                pub_date="2024-01-01",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                service_dir=service,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(find_source_issues(config), [])

    def test_reports_missing_cv_publications_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            service = root / "site" / "service"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Publications\n\n"
                "### _Conference and Journal Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__CV_PUBLICATIONS_MAIN_LIST__\n\n"
                ":::\n\n"
                "### _Workshop Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                ":::\n",
                encoding="utf-8",
            )
            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications page\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                ":::\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                ":::\n",
                encoding="utf-8",
            )
            _write_publication_bundle(
                pubs,
                slug="2025-test-main",
                listing_group="main",
                title="Main Paper",
                pub_date="2025-01-01",
            )
            _write_publication_bundle(
                pubs,
                slug="2024-test-workshop",
                listing_group="workshop",
                title="Workshop Paper",
                pub_date="2024-01-01",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                service_dir=service,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{cv_dir / 'index.dj'}: CV publications section must contain __CV_PUBLICATIONS_WORKSHOP_LIST__"
                ],
            )

    def test_reports_literal_cv_publication_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            service = root / "site" / "service"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            service.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Publications\n\n"
                "### _Conference and Journal Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__CV_PUBLICATIONS_MAIN_LIST__\n\n"
                "*Main Paper* \\\n"
                "Demo Author \\\n"
                "Demo Venue 2025\n\n"
                ":::\n\n"
                "### _Workshop Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__CV_PUBLICATIONS_WORKSHOP_LIST__\n\n"
                ":::\n",
                encoding="utf-8",
            )
            (pubs / "index.dj").write_text(
                "---\n"
                "description: Publications page\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_MAIN_LIST__\n\n"
                ":::\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "__PUBLICATIONS_WORKSHOP_LIST__\n\n"
                ":::\n",
                encoding="utf-8",
            )
            _write_publication_bundle(
                pubs,
                slug="2025-test-main",
                listing_group="main",
                title="Main Paper",
                pub_date="2025-01-01",
            )
            _write_publication_bundle(
                pubs,
                slug="2024-test-workshop",
                listing_group="workshop",
                title="Workshop Paper",
                pub_date="2024-01-01",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                service_dir=service,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                teaching_dir=teaching,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [
                    f"{cv_dir / 'index.dj'}: CV conference/journal publications subsection must not contain literal publication entry blocks"
                ],
            )

    def test_reports_missing_service_registry_when_cv_uses_service_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Service\n\n"
                "### _Reviewing_\n\n"
                "__CV_SERVICE_REVIEWING_LIST__\n\n"
                "### _Organizing_\n\n"
                "__CV_SERVICE_ORGANIZING_LIST__\n\n"
                "### _Mentoring_\n\n"
                "__CV_SERVICE_MENTORING_LIST__\n\n"
                "### _Department_\n\n"
                "__CV_SERVICE_DEPARTMENT_LIST__\n\n"
                "Faculty skit note.\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"missing service registry: {data / 'service.json'}"],
            )

    def test_reports_missing_cv_service_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Service\n\n"
                "### _Reviewing_\n\n"
                "__CV_SERVICE_REVIEWING_LIST__\n\n"
                "### _Organizing_\n\n"
                "__CV_SERVICE_ORGANIZING_LIST__\n\n"
                "### _Mentoring_\n\n"
                "__CV_SERVICE_MENTORING_LIST__\n\n"
                "### _Department_\n\n"
                "Faculty skit note.\n",
                encoding="utf-8",
            )
            (service / "index.dj").write_text(
                "---\n"
                "description: Service page\n"
                "---\n\n"
                "# Service\n\n"
                "__SERVICE_REVIEWING_LIST__\n\n"
                "__SERVICE_ORGANIZING_LIST__\n\n"
                "__SERVICE_MENTORING_LIST__\n\n"
                "__SERVICE_DEPARTMENT_LIST__\n",
                encoding="utf-8",
            )
            (data / "service.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2025-pldi-program-committee-chair",
                                "year": 2025,
                                "view_groups": ["reviewing", "organizing"],
                                "title": "PLDI",
                                "role": "Program Committee Chair",
                                "url": "https://example.test/pldi",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV service section must contain __CV_SERVICE_DEPARTMENT_LIST__"],
            )

    def test_reports_literal_cv_service_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Service\n\n"
                "### _Reviewing_\n\n"
                "__CV_SERVICE_REVIEWING_LIST__\n\n"
                "- 2026 ICFP Program Committee\n\n"
                "### _Organizing_\n\n"
                "__CV_SERVICE_ORGANIZING_LIST__\n\n"
                "### _Mentoring_\n\n"
                "__CV_SERVICE_MENTORING_LIST__\n\n"
                "### _Department_\n\n"
                "__CV_SERVICE_DEPARTMENT_LIST__\n\n"
                "Faculty skit note.\n",
                encoding="utf-8",
            )
            (service / "index.dj").write_text(
                "---\n"
                "description: Service page\n"
                "---\n\n"
                "# Service\n\n"
                "__SERVICE_REVIEWING_LIST__\n\n"
                "__SERVICE_ORGANIZING_LIST__\n\n"
                "__SERVICE_MENTORING_LIST__\n\n"
                "__SERVICE_DEPARTMENT_LIST__\n",
                encoding="utf-8",
            )
            (data / "service.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2025-pldi-program-committee-chair",
                                "year": 2025,
                                "view_groups": ["reviewing", "organizing"],
                                "title": "PLDI",
                                "role": "Program Committee Chair",
                                "url": "https://example.test/pldi",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                cv_dir=cv_dir,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV service section must not contain literal service entry blocks"],
            )

    def test_reports_missing_service_registry_when_service_index_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            service.mkdir(parents=True)
            (service / "index.dj").write_text(
                "---\n"
                "description: Service\n"
                "---\n\n"
                "# Service\n\n"
                "__SERVICE_REVIEWING_LIST__\n\n"
                "__SERVICE_ORGANIZING_LIST__\n\n"
                "__SERVICE_MENTORING_LIST__\n\n"
                "__SERVICE_DEPARTMENT_LIST__\n",
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                service_dir=service,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"missing service registry: {data / 'service.json'}"],
            )

    def test_reports_missing_service_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            service.mkdir(parents=True)
            (service / "index.dj").write_text(
                "---\n"
                "description: Service\n"
                "---\n\n"
                "# Service\n\n"
                "__SERVICE_REVIEWING_LIST__\n\n"
                "__SERVICE_ORGANIZING_LIST__\n\n"
                "__SERVICE_MENTORING_LIST__\n",
                encoding="utf-8",
            )
            (data / "service.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2025-demo-reviewing",
                                "year": 2025,
                                "view_groups": ["reviewing"],
                                "title": "DemoConf",
                                "role": "Program Committee",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                service_dir=service,
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
                    f"{service / 'index.dj'}: service index page must contain __SERVICE_DEPARTMENT_LIST__",
                ],
            )

    def test_reports_missing_teaching_registry_when_teaching_page_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (teaching / "index.dj").write_text(
                "---\n"
                "description: Teaching\n"
                "---\n\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
                "__TEACHING_SUMMER_SCHOOL_LIST__\n",
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
                [f"missing teaching registry: {data / 'teaching.json'}"],
            )

    def test_reports_missing_teaching_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            teaching.mkdir(parents=True)
            students.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (teaching / "index.dj").write_text(
                "---\n"
                "description: Teaching\n"
                "---\n\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n",
                encoding="utf-8",
            )
            (data / "teaching.json").write_text(
                json.dumps(
                    {
                        "groups": [
                            {
                                "key": "uw_courses",
                                "records": [
                                    {
                                        "key": "uw-cse-507",
                                        "kind": "course",
                                        "code": "UW CSE 507",
                                        "title": "Course",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2025, "term": "Autumn"}],
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
                                        "title": "Topics",
                                        "details": ["Notes"],
                                        "offerings": [{"year": 2017, "term": "Spring"}],
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
                                        "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
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
                                        "title": "PL",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2012, "term": "Winter"}],
                                    }
                                ],
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
                [f"{teaching / 'index.dj'}: teaching index page must contain __TEACHING_SUMMER_SCHOOL_LIST__"],
            )

    def test_reports_missing_students_registry_when_students_pages_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
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
            (cv_dir / "index.dj").write_text(
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
                cv_dir=cv_dir,
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

    def test_reports_legacy_service_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            service = root / "site" / "service"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            service.mkdir(parents=True)
            teaching.mkdir(parents=True)
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
                "[Service](service.html)\n",
                encoding="utf-8",
            )
            (service / "index.dj").write_text(
                "---\n"
                "description: Service\n"
                "---\n\n"
                "# Service\n\n"
                "__SERVICE_REVIEWING_LIST__\n\n"
                "__SERVICE_ORGANIZING_LIST__\n\n"
                "__SERVICE_MENTORING_LIST__\n\n"
                "__SERVICE_DEPARTMENT_LIST__\n",
                encoding="utf-8",
            )
            (data / "service.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2025-demo-reviewing",
                                "year": 2025,
                                "view_groups": ["reviewing"],
                                "title": "DemoConf",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages,
                service_dir=service,
                students_dir=students,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{pages / 'index.dj'}: legacy service link should use canonical collection path: service.html -> service/"],
            )

    def test_reports_legacy_teaching_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            teaching = root / "site" / "teaching"
            students = root / "site" / "students"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"
            pages.mkdir(parents=True)
            teaching.mkdir(parents=True)
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
                "[Teaching](teaching.html)\n",
                encoding="utf-8",
            )
            (teaching / "index.dj").write_text(
                "---\n"
                "description: Teaching\n"
                "---\n\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
                "__TEACHING_SUMMER_SCHOOL_LIST__\n",
                encoding="utf-8",
            )
            (data / "teaching.json").write_text(
                json.dumps(
                    {
                        "groups": [
                            {
                                "key": "uw_courses",
                                "records": [
                                    {
                                        "key": "uw-cse-507",
                                        "kind": "course",
                                        "code": "UW CSE 507",
                                        "title": "Course",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2025, "term": "Autumn"}],
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
                                        "title": "Topics",
                                        "details": ["Notes"],
                                        "offerings": [{"year": 2017, "term": "Spring"}],
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
                                        "events": [{"label": "Marktoberdorf Summer School 2024", "url": "https://example.com/m"}],
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
                                        "title": "PL",
                                        "description_djot": "Desc",
                                        "offerings": [{"year": 2012, "term": "Winter"}],
                                    }
                                ],
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
                [f"{pages / 'index.dj'}: legacy teaching link should use canonical collection path: teaching.html -> teaching/"],
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

    def test_reports_missing_cv_talks_projection_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Invited Talks\n\n"
                "Manual talk list.\n",
                encoding="utf-8",
            )
            (talks / "index.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n\n"
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
                cv_dir=cv_dir,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV invited talks section must contain __CV_TALKS_LIST__"],
            )

    def test_reports_literal_cv_talk_entry_blocks_after_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            talks = root / "site" / "talks"
            pubs = root / "site" / "pubs"
            templates = root / "site" / "templates"
            data = root / "site" / "data"
            static = root / "site" / "static"

            pages.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            talks.mkdir(parents=True)
            pubs.mkdir(parents=True)
            templates.mkdir(parents=True)
            data.mkdir(parents=True)
            static.mkdir(parents=True)
            (static / "img").mkdir(parents=True)
            (static / "img" / "favicon-meta.png").write_bytes(b"PNG")

            (cv_dir / "index.dj").write_text(
                "---\n"
                "description: CV page\n"
                "---\n\n"
                "# Curriculum Vitae\n\n"
                "## Invited Talks\n\n"
                "__CV_TALKS_LIST__\n\n"
                "* Demo Talk \\\n"
                "  Demo Host, February 2026\n",
                encoding="utf-8",
            )
            (talks / "index.dj").write_text(
                "---\n"
                "description: Talks\n"
                "---\n\n"
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
                cv_dir=cv_dir,
                talks_dir=talks,
                publications_dir=pubs,
                templates_dir=templates,
                data_dir=data,
                static_source_dir=static,
            )
            self.assertEqual(
                find_source_issues(config),
                [f"{cv_dir / 'index.dj'}: CV invited talks section must not contain literal talk entry blocks"],
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
