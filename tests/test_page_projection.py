from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.collaborators_index import (
    COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER,
    COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER,
    RESEARCH_COLLABORATORS_LIST_PLACEHOLDER,
    TEACHING_COLLABORATORS_LIST_PLACEHOLDER,
)
from scripts.funding_index import FUNDING_LIST_PLACEHOLDER
from scripts.news_index import (
    HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER,
    NEWS_MONTH_GROUPS_PLACEHOLDER,
)
from scripts.service_index import render_public_service_section_list_djot
from scripts.sitebuild.page_projection import (
    CV_FUNDING_LIST_PLACEHOLDER,
    CV_PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    CV_PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
    CV_SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
    CV_SERVICE_MENTORING_LIST_PLACEHOLDER,
    CV_SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    CV_SERVICE_REVIEWING_LIST_PLACEHOLDER,
    CV_TALKS_LIST_PLACEHOLDER,
    CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER,
    CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER,
    CV_TEACHING_TA_LIST_PLACEHOLDER,
    CV_STUDENTS_BACHELORS_LIST_PLACEHOLDER,
    CV_STUDENTS_CURRENT_LIST_PLACEHOLDER,
    CV_STUDENTS_MASTERS_LIST_PLACEHOLDER,
    CV_STUDENTS_PHD_LIST_PLACEHOLDER,
    CV_STUDENTS_POSTDOC_LIST_PLACEHOLDER,
    CV_STUDENTS_VISITING_LIST_PLACEHOLDER,
    HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER,
    HOMEPAGE_RECENT_PUBLICATIONS_LIST_PLACEHOLDER,
    HOMEPAGE_RECENT_SERVICE_LIST_PLACEHOLDER,
    HOMEPAGE_RECENT_TEACHING_LIST_PLACEHOLDER,
    SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
    SERVICE_MENTORING_LIST_PLACEHOLDER,
    SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    SERVICE_REVIEWING_LIST_PLACEHOLDER,
    STUDENTS_BACHELORS_LIST_PLACEHOLDER,
    STUDENTS_CURRENT_LIST_PLACEHOLDER,
    STUDENTS_MASTERS_LIST_PLACEHOLDER,
    STUDENTS_PHD_LIST_PLACEHOLDER,
    STUDENTS_POSTDOC_LIST_PLACEHOLDER,
    STUDENTS_VISITING_LIST_PLACEHOLDER,
    TALKS_LIST_PLACEHOLDER,
    TEACHING_SPECIAL_TOPICS_LIST_PLACEHOLDER,
    TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER,
    TEACHING_UW_COURSES_LIST_PLACEHOLDER,
    apply_page_projections,
    render_cv_publications_list_djot,
    render_cv_funding_list_djot,
    render_cv_service_section_list_djot,
    render_cv_talks_list_djot,
    render_cv_teaching_assistant_list_djot,
    render_cv_teaching_instructor_list_djot,
    render_cv_teaching_summer_school_list_djot,
    render_homepage_current_students_list_djot,
    render_homepage_recent_publications_list_djot,
    render_homepage_recent_teaching_list_djot,
    render_cv_students_section_list_djot,
    render_teaching_special_topics_list_djot,
    render_teaching_summer_school_list_djot,
    render_teaching_uw_courses_list_djot,
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
    def test_applies_projection_only_to_about_collaborator_alphabet_section(self) -> None:
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
            pub_dir = pubs_dir / "2025-demo-paper"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [
                            {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                            {"name": "Adam T. Geller", "ref": "Adam Geller"},
                            {"name": "Yisu Remy Wang", "ref": "Remy Wang"},
                            {"name": "Robert Rabe", "ref": ""},
                        ],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# About\n\n"
                f"`{COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER}`\n\n"
                f"`{COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER}`\n"
            )
            rendered = apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=data_dir,
                publications_dir=pubs_dir,
            )
            self.assertEqual(
                rendered,
                "# About\n\n"
                "`B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, S, T, U, V, W, X, Y, Z`\n\n"
                "`A, B, C, D, E, F, H, I, J, K, L, M, N, O, P, Q, S, T, U, V, X, Y, Z`\n",
            )

            self.assertEqual(
                apply_page_projections(
                    "ordinary_page",
                    "notes",
                    body,
                    root=root,
                    data_dir=data_dir,
                    publications_dir=pubs_dir,
                ),
                body,
            )

    def test_applies_projection_only_to_collaborators_index_page(self) -> None:
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
                            "kevin-mu": {
                                "name": "Kevin Mu",
                                "url": "https://example.test/kevin",
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            pub_dir = pubs_dir / "2025-demo-paper"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [
                            {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                            {"name": "Adam T. Geller", "ref": "Adam Geller"},
                            {"name": "Robert Rabe", "ref": ""},
                        ],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            (data_dir / "students.json").write_text(
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
            (data_dir / "teaching.json").write_text(
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
                                                "teaching_assistants": ["kevin-mu"],
                                            }
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

            body = (
                "# Collaborators\n\n"
                "## Research Collaborators\n\n"
                f"{RESEARCH_COLLABORATORS_LIST_PLACEHOLDER}\n\n"
                "## Teaching Collaborators\n\n"
                f"{TEACHING_COLLABORATORS_LIST_PLACEHOLDER}\n"
            )
            rendered = apply_page_projections(
                "collaborators_index_page",
                "collaborators",
                body,
                root=root,
                data_dir=data_dir,
                publications_dir=pubs_dir,
            )
            self.assertNotIn(RESEARCH_COLLABORATORS_LIST_PLACEHOLDER, rendered)
            self.assertNotIn(TEACHING_COLLABORATORS_LIST_PLACEHOLDER, rendered)
            self.assertIn("* [Adam Geller][]", rendered)
            self.assertIn("* Robert Rabe", rendered)
            self.assertIn("* [Kevin Mu][]", rendered)
            self.assertNotIn("Zachary Tatlock", rendered)

            self.assertEqual(
                apply_page_projections(
                    "ordinary_page",
                    "about",
                    body,
                    root=root,
                    data_dir=data_dir,
                    publications_dir=pubs_dir,
                ),
                body,
            )

    def test_renders_cv_funding_list_with_en_dash_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "funding.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": "2020-demo-grant",
                                "title": "Demo Grant",
                                "role": "PI",
                                "sponsor": "NSF",
                                "award_id": "CCF-1234567",
                                "amount_usd": 100000,
                                "start_year": 2020,
                                "end_year": 2023,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_cv_funding_list_djot(
                root,
                funding_path=data_dir / "funding.json",
            )
            self.assertEqual(
                rendered,
                "- Demo Grant \\\n"
                "  PI; NSF CCF-1234567; $100,000; 2020 – 2023\n",
            )

    def test_renders_cv_publication_sections_with_compressed_low_link_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pubs_dir = root / "site" / "pubs"
            newer_main = pubs_dir / "2025-demo-main"
            newer_main.mkdir(parents=True)
            (newer_main / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-05-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [
                            {"name": "Demo Author", "ref": "Demo Author"},
                            {"name": "Collaborator", "ref": ""},
                        ],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "badges": ["★ Distinguished Paper"],
                        "links": {"publisher": "https://example.test/main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            older_main = pubs_dir / "2024-demo-main"
            older_main.mkdir()
            (older_main / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2024,
                        "pub_date": "2024-03-01",
                        "primary_link": "publisher",
                        "title": "Older Main Paper",
                        "authors": [{"name": "Solo Author", "ref": "Solo Author"}],
                        "venue": "OlderConf",
                        "venue_short": "OlderConf",
                        "links": {"publisher": "https://example.test/older-main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            workshop = pubs_dir / "2025-demo-workshop"
            workshop.mkdir()
            (workshop / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2025,
                        "pub_date": "2025-02-01",
                        "primary_link": "publisher",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Workshop Author", "ref": "Workshop Author"}],
                        "venue": "Demo Workshop",
                        "venue_short": "Demo Workshop",
                        "links": {"publisher": "https://example.test/workshop"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            rendered_main = render_cv_publications_list_djot(root, "main", publications_dir=pubs_dir)
            self.assertEqual(
                rendered_main,
                "*Main Paper* \\\n"
                "Demo Author, Collaborator \\\n"
                "DemoConf 2025 \\\n"
                "★ Distinguished Paper\n\n"
                "*Older Main Paper* \\\n"
                "Solo Author \\\n"
                "OlderConf 2024\n",
            )
            self.assertNotIn("https://example.test/main", rendered_main)
            self.assertNotIn("[Demo Author]", rendered_main)

            rendered_workshop = render_cv_publications_list_djot(root, "workshop", publications_dir=pubs_dir)
            self.assertEqual(
                rendered_workshop,
                "*Workshop Paper* \\\n"
                "Workshop Author \\\n"
                "Demo Workshop 2025\n",
            )
            self.assertNotIn("https://example.test/workshop", rendered_workshop)

    def test_renders_public_service_sections_from_canonical_data(self) -> None:
        root = Path(__file__).resolve().parents[1]
        organizing = render_public_service_section_list_djot(root, "organizing")
        self.assertIn("{#fptalks}", organizing)
        self.assertIn("FPTalks Co-Organizer, 2020 - 2025", organizing)
        self.assertIn("[FPTalks 2025, Co-Organizer](https://fpbench.org/talks/fptalks25.html)", organizing)
        self.assertIn("EGRAPHS Community Advisory Board, 2022 - Present", organizing)

        department = render_public_service_section_list_djot(root, "department")
        self.assertIn("UW CSE Faculty Graduate Admissions Co-chair, 2025 - 2027", department)
        self.assertIn("UW Faculty Skit Writer, Producer, and Director, 2015 - Present", department)
        self.assertIn("[Hank Levy][]", department)

    def test_renders_cv_service_sections_with_explicit_cv_policy(self) -> None:
        root = Path(__file__).resolve().parents[1]

        reviewing = render_cv_service_section_list_djot(root, "reviewing")
        self.assertIn("- ICFP 2026, Program Committee", reviewing)
        self.assertIn(
            "- [PLDI 2025, Program Committee Chair](https://pldi25.sigplan.org/committee/pldi-2025-organizing-committee)",
            reviewing,
        )
        self.assertIn("[Review Committee](https://pldi25.sigplan.org/committee/pldi-2025-papers-pldi-review-committee)", reviewing)

        organizing = render_cv_service_section_list_djot(root, "organizing")
        self.assertIn("EGRAPHS Community Advisory Board, 2022 - Present", organizing)
        self.assertIn("[FPTalks Co-Organizer, 2020 - 2025](/service/#fptalks)", organizing)

        mentoring = render_cv_service_section_list_djot(root, "mentoring")
        self.assertIn("PLDI Programming Languages Mentoring Workshop (PLMW) 2018, Panelist", mentoring)

        department = render_cv_service_section_list_djot(root, "department")
        self.assertIn("UW CSE Faculty Graduate Admissions Co-chair, 2025 - 2027", department)
        self.assertNotIn("UW Faculty Skit", department)

    def test_renders_teaching_sections_from_canonical_data(self) -> None:
        rendered_uw = render_teaching_uw_courses_list_djot(Path(__file__).resolve().parents[1])
        self.assertIn("*UW CSE 507: Computer-Aided Reasoning for Software* \\", rendered_uw)
        self.assertIn(
            "- [2026 Spring](https://courses.cs.washington.edu/courses/csep590b/26sp/)",
            rendered_uw,
        )
        self.assertIn("[2025 Autumn](https://courses.cs.washington.edu/courses/cse507/25au/)", rendered_uw)
        self.assertIn("Co-Instructors: [James Wilcox][]", rendered_uw)
        self.assertIn(
            "Teaching Assistants: [Gus Smith][], [Audrey Seo][], and [Anjali Pal][]",
            rendered_uw,
        )
        self.assertIn(
            "Tutors: [James Wilcox][], [Eric Mullen][], and [Joe Redmon][]",
            rendered_uw,
        )
        self.assertIn(
            "Teaching Assistants: [Brendan Murphy][], Jack Zhang, [Mike He][], and [Yihong Zhang][]",
            rendered_uw,
        )
        self.assertNotIn("{.columns .columns-8rem}", rendered_uw)

        rendered_topics = render_teaching_special_topics_list_djot(Path(__file__).resolve().parents[1])
        self.assertIn("*UW CSE 599W: Systems Verification* \\", rendered_topics)
        self.assertIn("Formally verifying systems implementations", rendered_topics)
        self.assertIn("[2016 Spring](https://courses.cs.washington.edu/courses/cse599w/16sp/)", rendered_topics)
        self.assertIn("Co-Instructors: [Bryan Parno][] and [Xi Wang][]", rendered_topics)
        self.assertNotIn("[UW CSE 599W: Systems Verification, \\ 2016 Spring]", rendered_topics)

        rendered_summer = render_teaching_summer_school_list_djot(Path(__file__).resolve().parents[1])
        self.assertIn("- Analysis and Optimizations with Equality Saturation", rendered_summer)
        self.assertIn("[Marktoberdorf Summer School 2024](https://sites.google.com/view/marktoberdorf2024/home)", rendered_summer)

    def test_renders_cv_teaching_sections_with_compressed_low_link_policy(self) -> None:
        root = Path(__file__).resolve().parents[1]

        rendered_instructor = render_cv_teaching_instructor_list_djot(root)
        self.assertIn("- *UW CSE 507: Computer-Aided Reasoning for Software* \\", rendered_instructor)
        self.assertIn("*  2026 Spring", rendered_instructor)
        self.assertIn("- *Special Topics Graduate Courses*", rendered_instructor)
        self.assertNotIn("Co-taught with Xi Wang and Bryan Parno", rendered_instructor)
        self.assertNotIn("[Xi Wang][]", rendered_instructor)
        self.assertNotIn("https://courses.cs.washington.edu/courses/cse507/25au/", rendered_instructor)

        rendered_summer = render_cv_teaching_summer_school_list_djot(root)
        self.assertIn("- *DeepSpec Summer School 2018* \\", rendered_summer)
        self.assertIn("Verifying Distributed Systems Implementations in Coq", rendered_summer)
        self.assertIn("- *Marktoberdorf Summer School 2024* \\", rendered_summer)
        self.assertIn("Analysis and Optimizations with Equality Saturation", rendered_summer)
        self.assertNotIn("https://deepspec.org/event/dsss18/index.html", rendered_summer)

        rendered_ta = render_cv_teaching_assistant_list_djot(root)
        self.assertIn("- *UCSD CSE 231: Advanced Compiler Design* \\", rendered_ta)
        self.assertIn("Graduate course exploring program analyses and compiler optimizations", rendered_ta)

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

    def test_renders_cv_talks_list_from_canonical_bundles(self) -> None:
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
            second.mkdir()
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

            rendered = render_cv_talks_list_djot(root, talks_dir=talks_dir)
            self.assertEqual(
                rendered,
                "- [Everything is a compiler, try Equality Saturation!](https://events.brown.edu/demo) \\\n"
                "  Brown University, PL and Graphics groups, February 2026\n\n"
                "- [Relational Equality Saturation in egg](talk-2023-05-egg-uiuc.html) \\\n"
                "  University of Illinois at Urbana-Champaign, [Compilers Seminar](https://compilerseminar.web.illinois.edu/), May 2023\n",
            )

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

    def test_applies_projection_only_to_cv_talks_section(self) -> None:
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

            body = "# Curriculum Vitae\n\n## Invited Talks\n\n" + CV_TALKS_LIST_PLACEHOLDER + "\n"
            rendered = apply_page_projections(
                "cv_index_page",
                "cv",
                body,
                root=root,
                talks_dir=talks_dir,
            )
            self.assertNotIn(CV_TALKS_LIST_PLACEHOLDER, rendered)
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
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [{"name": "Demo Author", "ref": "Demo Author"}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
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
                        "local_page": False,
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2025,
                        "pub_date": "2025-01-02",
                        "primary_link": "publisher",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Demo Workshop",
                        "venue_short": "Demo Workshop",
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

    def test_applies_projection_only_to_teaching_index_page(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Teaching\n\n"
            "__TEACHING_UW_COURSES_LIST__\n\n"
            "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
            "__TEACHING_SUMMER_SCHOOL_LIST__\n"
        )
        rendered = apply_page_projections(
            "teaching_index_page",
            "teaching",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(TEACHING_UW_COURSES_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(TEACHING_SPECIAL_TOPICS_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER, rendered)
        self.assertIn("Marktoberdorf Summer School 2024", rendered)
        self.assertIn("Co-Instructors: [James Wilcox][]", rendered)
        self.assertIn("Tutors: [James Wilcox][], [Eric Mullen][], and [Joe Redmon][]", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_news_index_page(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = "# News\n\n__NEWS_MONTH_GROUPS__\n"
        rendered = apply_page_projections(
            "news_index_page",
            "news",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn("🗣️ \\ Visiting the PL and Graphics groups at Brown University to give a talk.", rendered)
        self.assertIn(": August 2017", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_homepage_news_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## News\n\n"
            "__HOMEPAGE_NEWS_MONTH_GROUPS__\n\n"
            "Please see [past news](news/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn(": January 2026", rendered)
        self.assertIn(": June 2025", rendered)
        self.assertNotIn(": February 2025", rendered)
        self.assertNotIn(": October 2023", rendered)
        self.assertIn("Please see [past news](news/) for more.", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
                body,
            )

    def test_renders_homepage_current_students_list_from_canonical_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "amy-zhu": {"name": "Amy Zhu", "url": "https://example.test/amy"},
                            "linkless-student": {"name": "Linkless Student"},
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
                                },
                            ),
                            _student_section(
                                "completed_postdoctoral_mentoring",
                                "Completed Postdoctoral Mentoring",
                                {
                                    "key": "amy-zhu-postdoc-2025",
                                    "person_key": "amy-zhu",
                                    "name": "Amy Zhu",
                                    "label": "Postdoc 2025",
                                },
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_homepage_current_students_list_djot(
                root,
                data_dir=data_dir,
            )
            self.assertIn("- [Amy Zhu][], PhD Student", rendered)
            self.assertNotIn("Postdoc 2025", rendered)

            (data_dir / "students.json").write_text(
                json.dumps(
                    {
                        "sections": [
                            {
                                "key": "current_students",
                                "title": "Current Students",
                                "records": [
                                    {
                                        "key": "linkless-student-current",
                                        "person_key": "linkless-student",
                                        "name": "Linkless Student",
                                        "label": "BS Student",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            rendered_linkless = render_homepage_current_students_list_djot(
                root,
                data_dir=data_dir,
            )
            self.assertIn("- Linkless Student, BS Student", rendered_linkless)
            self.assertNotIn("[Linkless Student][]", rendered_linkless)

    def test_applies_projection_only_to_homepage_current_students_section(self) -> None:
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
                            )
                        ]
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# Home\n\n"
                "## Current Students\n\n"
                "{.columns .columns-16rem}\n"
                f"{HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER}\n\n"
                "Please see my [students page](students/) for more.\n"
            )
            rendered = apply_page_projections(
                "ordinary_page",
                "index",
                body,
                root=root,
                data_dir=data_dir,
            )
            self.assertNotIn(HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER, rendered)
            self.assertIn("- [Haobin Ni][], Postdoctoral Scholar", rendered)
            self.assertIn("Please see my [students page](students/) for more.", rendered)

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

    def test_applies_both_homepage_news_and_current_students_projections(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## News\n\n"
            "__HOMEPAGE_NEWS_MONTH_GROUPS__\n\n"
            "Please see [past news](news/) for more.\n\n"
            "## Current Students\n\n"
            "{.columns .columns-16rem}\n"
            "__HOMEPAGE_CURRENT_STUDENTS_LIST__\n\n"
            "Please see my [students page](students/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn("- [Haobin Ni][], Postdoctoral Scholar", rendered)

    def test_renders_homepage_recent_teaching_list_from_recent_window(self) -> None:
        root = Path(__file__).resolve().parents[1]
        rendered = render_homepage_recent_teaching_list_djot(
            root,
            data_dir=root / "site" / "data",
        )
        self.assertIn(
            "- [2026 Spring, UW CSE 507: Computer-Aided Reasoning for Software](https://courses.cs.washington.edu/courses/csep590b/26sp/)",
            rendered,
        )
        self.assertNotIn(
            "- 2026 Spring, UW CSE 507: Computer-Aided Reasoning for Software",
            rendered,
        )
        self.assertIn(
            "- [2025 Autumn, UW CSE 507: Computer-Aided Reasoning for Software](https://courses.cs.washington.edu/courses/cse507/25au/)",
            rendered,
        )
        self.assertIn(
            "- [2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation](https://sites.google.com/view/marktoberdorf2024/home)",
            rendered,
        )
        self.assertNotIn("2023 Autumn, UW CSE 507: Computer-Aided Reasoning for Software", rendered)
        self.assertNotIn("2022 Autumn, UW CSE 341: Programming Languages", rendered)
        self.assertNotIn("2018 Summer, DeepSpec Summer School", rendered)

    def test_applies_projection_only_to_homepage_recent_teaching_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## Recent Teaching\n\n"
            "__HOMEPAGE_RECENT_TEACHING_LIST__\n\n"
            "Please see my [teaching page](teaching/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_RECENT_TEACHING_LIST_PLACEHOLDER, rendered)
        self.assertIn("2026 Spring, UW CSE 507: Computer-Aided Reasoning for Software", rendered)
        self.assertIn("2025 Autumn, UW CSE 507: Computer-Aided Reasoning for Software", rendered)
        self.assertIn("2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation", rendered)
        self.assertNotIn("2023 Autumn, UW CSE 507: Computer-Aided Reasoning for Software", rendered)
        self.assertIn("Please see my [teaching page](teaching/) for more.", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_homepage_recent_service_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## Recent Service / Leadership\n\n"
            "__HOMEPAGE_RECENT_SERVICE_LIST__\n\n"
            "Please see my [service page](service/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_RECENT_SERVICE_LIST_PLACEHOLDER, rendered)
        self.assertIn("- ICFP 2026, Program Committee", rendered)
        self.assertIn("- [FPTalks Co-Organizer, 2020 - 2025](/service/#fptalks)", rendered)
        self.assertIn("Please see my [service page](service/) for more.", rendered)
        self.assertNotIn("Dagstuhl Seminar 26022: EGRAPHS", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_seed_homepage_recent_publications_uses_latest_publication_year_window(self) -> None:
        root = Path(__file__).resolve().parents[1]
        rendered = render_homepage_recent_publications_list_djot(
            root,
            publications_dir=root / "site" / "pubs",
        )
        self.assertIn(
            "- *[Target-Aware Implementation of Real Expressions](https://dl.acm.org/doi/10.1145/3669940.3707277)* (ASPLOS 2025)",
            rendered,
        )
        self.assertIn(
            "- *[Better Together: Unifying Datalog and Equality Saturation](pubs/2023-pldi-egglog/)* (PLDI 2023)",
            rendered,
        )
        self.assertNotIn("Small Proofs from Congruence Closure", rendered)

    def test_applies_projection_only_to_homepage_recent_publications_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## Recent Publications\n\n"
            "__HOMEPAGE_RECENT_PUBLICATIONS_LIST__\n\n"
            "Please see my [publications page](pubs/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            publications_dir=root / "site" / "pubs",
        )
        self.assertNotIn(HOMEPAGE_RECENT_PUBLICATIONS_LIST_PLACEHOLDER, rendered)
        self.assertIn(
            "*[Target-Aware Implementation of Real Expressions](https://dl.acm.org/doi/10.1145/3669940.3707277)*",
            rendered,
        )
        self.assertIn(
            "*[Magic Markup: Maintaining Document-External Markup with an LLM](pubs/2024-programming-magicmarkup/)*",
            rendered,
        )
        self.assertIn("Please see my [publications page](pubs/) for more.", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                publications_dir=root / "site" / "pubs",
            ),
            body,
        )

    def test_applies_homepage_news_current_students_and_recent_teaching_together(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## News\n\n"
            "__HOMEPAGE_NEWS_MONTH_GROUPS__\n\n"
            "Please see [past news](news/) for more.\n\n"
            "## Current Students\n\n"
            "{.columns .columns-16rem}\n"
            "__HOMEPAGE_CURRENT_STUDENTS_LIST__\n\n"
            "Please see my [students page](students/) for more.\n\n"
            "## Recent Teaching\n\n"
            "__HOMEPAGE_RECENT_TEACHING_LIST__\n\n"
            "Please see my [teaching page](teaching/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_TEACHING_LIST_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn("- [Haobin Ni][], Postdoctoral Scholar", rendered)
        self.assertIn("2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation", rendered)

    def test_applies_homepage_news_students_teaching_and_service_together(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## News\n\n"
            "__HOMEPAGE_NEWS_MONTH_GROUPS__\n\n"
            "Please see [past news](news/) for more.\n\n"
            "## Current Students\n\n"
            "{.columns .columns-16rem}\n"
            "__HOMEPAGE_CURRENT_STUDENTS_LIST__\n\n"
            "Please see my [students page](students/) for more.\n\n"
            "## Recent Teaching\n\n"
            "__HOMEPAGE_RECENT_TEACHING_LIST__\n\n"
            "Please see my [teaching page](teaching/) for more.\n\n"
            "## Recent Service / Leadership\n\n"
            "__HOMEPAGE_RECENT_SERVICE_LIST__\n\n"
            "Please see my [service page](service/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_TEACHING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_SERVICE_LIST_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn("- [Haobin Ni][], Postdoctoral Scholar", rendered)
        self.assertIn("2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation", rendered)
        self.assertIn("- ICFP 2026, Program Committee", rendered)
        self.assertIn("- [FPTalks Co-Organizer, 2020 - 2025](/service/#fptalks)", rendered)

    def test_applies_homepage_news_students_teaching_service_and_publications_together(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Home\n\n"
            "## News\n\n"
            "__HOMEPAGE_NEWS_MONTH_GROUPS__\n\n"
            "Please see [past news](news/) for more.\n\n"
            "## Current Students\n\n"
            "{.columns .columns-16rem}\n"
            "__HOMEPAGE_CURRENT_STUDENTS_LIST__\n\n"
            "Please see my [students page](students/) for more.\n\n"
            "## Recent Teaching\n\n"
            "__HOMEPAGE_RECENT_TEACHING_LIST__\n\n"
            "Please see my [teaching page](teaching/) for more.\n\n"
            "## Recent Service / Leadership\n\n"
            "__HOMEPAGE_RECENT_SERVICE_LIST__\n\n"
            "Please see my [service page](service/) for more.\n\n"
            "## Recent Publications\n\n"
            "__HOMEPAGE_RECENT_PUBLICATIONS_LIST__\n\n"
            "Please see my [publications page](pubs/) for more.\n"
        )
        rendered = apply_page_projections(
            "ordinary_page",
            "index",
            body,
            root=root,
            data_dir=root / "site" / "data",
            publications_dir=root / "site" / "pubs",
        )
        self.assertNotIn(HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_CURRENT_STUDENTS_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_TEACHING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_SERVICE_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(HOMEPAGE_RECENT_PUBLICATIONS_LIST_PLACEHOLDER, rendered)
        self.assertIn(": February 2026", rendered)
        self.assertIn("- [Haobin Ni][], Postdoctoral Scholar", rendered)
        self.assertIn("2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation", rendered)
        self.assertIn("- ICFP 2026, Program Committee", rendered)
        self.assertIn("- [FPTalks Co-Organizer, 2020 - 2025](/service/#fptalks)", rendered)
        self.assertIn("*[Target-Aware Implementation of Real Expressions](https://dl.acm.org/doi/10.1145/3669940.3707277)*", rendered)

    def test_homepage_news_overflow_prefers_featured_older_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "news.json").write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "key": f"2026-02-item-{index:02d}",
                                "year": 2026,
                                "month": 2,
                                "kind": "other",
                                "emoji": "🗣️",
                                "body_djot": f"Item {index:02d}.",
                                "homepage_featured": index in {12, 15},
                            }
                            for index in range(1, 18)
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            body = "# Home\n\n## News\n\n__HOMEPAGE_NEWS_MONTH_GROUPS__\n"
            rendered = apply_page_projections(
                "ordinary_page",
                "index",
                body,
                root=root,
                data_dir=data_dir,
            )

            for index in range(1, 11):
                self.assertIn(f"Item {index:02d}.", rendered)
            self.assertIn("Item 12.", rendered)
            self.assertIn("Item 15.", rendered)
            self.assertIn("Item 11.", rendered)
            self.assertIn("Item 13.", rendered)
            self.assertIn("Item 14.", rendered)
            self.assertNotIn("Item 16.", rendered)
            self.assertNotIn("Item 17.", rendered)

    def test_applies_projection_only_to_cv_publications_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pubs_dir = root / "site" / "pubs"
            main_dir = pubs_dir / "2025-test-main"
            main_dir.mkdir(parents=True)
            (main_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {"publisher": "https://example.test/main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            workshop_dir = pubs_dir / "2024-test-workshop"
            workshop_dir.mkdir()
            (workshop_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2024,
                        "pub_date": "2024-01-01",
                        "primary_link": "publisher",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Workshop Author", "ref": ""}],
                        "venue": "WorkshopConf",
                        "venue_short": "WorkshopConf",
                        "links": {"publisher": "https://example.test/workshop"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# Curriculum Vitae\n\n"
                "## Publications\n\n"
                "### _Conference and Journal Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                f"{CV_PUBLICATIONS_MAIN_LIST_PLACEHOLDER}\n\n"
                ":::\n\n"
                "### _Workshop Papers_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                f"{CV_PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER}\n\n"
                ":::\n\n"
                "### _Book Chapters_\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "*Chapter 8: Parameterized Program Equivalence Checking* \\\n"
                "High-Level Verification: Methods and Tools for Verification of System-Level Designs \\\n"
                "Sudipta Kundu, Sorin Lerner, and Rajesh K. Gupta; Springer 2011\n\n"
                ":::\n"
            )
            rendered = apply_page_projections(
                "cv_index_page",
                "cv",
                body,
                root=root,
                publications_dir=pubs_dir,
            )
            self.assertNotIn(CV_PUBLICATIONS_MAIN_LIST_PLACEHOLDER, rendered)
            self.assertNotIn(CV_PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER, rendered)
            self.assertIn("*Main Paper* \\", rendered)
            self.assertIn("*Workshop Paper* \\", rendered)
            self.assertIn("*Chapter 8: Parameterized Program Equivalence Checking* \\", rendered)

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

    def test_applies_projection_only_to_service_index_page(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Service\n\n"
            "__SERVICE_REVIEWING_LIST__\n\n"
            "__SERVICE_ORGANIZING_LIST__\n\n"
            "__SERVICE_MENTORING_LIST__\n\n"
            "__SERVICE_DEPARTMENT_LIST__\n"
        )
        rendered = apply_page_projections(
            "service_index_page",
            "service",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(SERVICE_REVIEWING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(SERVICE_ORGANIZING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(SERVICE_MENTORING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(SERVICE_DEPARTMENT_LIST_PLACEHOLDER, rendered)
        self.assertIn("UW Faculty Skit Writer, Producer, and Director", rendered)
        self.assertIn("[Hank Levy][]", rendered)
        self.assertIn("Program Committee Chair", rendered)
        self.assertIn("PLDI 2025", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_funding_index_page(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = "# Funding\n\n__FUNDING_LIST__\n"
        rendered = apply_page_projections(
            "funding_index_page",
            "funding",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(FUNDING_LIST_PLACEHOLDER, rendered)
        self.assertIn("ComPort: Rigorous Testing Methods to Safeguard Software Porting", rendered)
        self.assertIn("NSF CCF-2017927", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_cv_funding_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = "# Curriculum Vitae\n\n## Funding\n\n__CV_FUNDING_LIST__\n"
        rendered = apply_page_projections(
            "cv_index_page",
            "cv",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(CV_FUNDING_LIST_PLACEHOLDER, rendered)
        self.assertIn("ComPort: Rigorous Testing Methods to Safeguard Software Porting", rendered)
        self.assertIn("2021 – 2024", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )

    def test_applies_projection_only_to_cv_service_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Curriculum Vitae\n\n"
            f"{CV_SERVICE_REVIEWING_LIST_PLACEHOLDER}\n\n"
            f"{CV_SERVICE_ORGANIZING_LIST_PLACEHOLDER}\n\n"
            f"{CV_SERVICE_MENTORING_LIST_PLACEHOLDER}\n\n"
            f"{CV_SERVICE_DEPARTMENT_LIST_PLACEHOLDER}\n"
        )
        rendered = apply_page_projections(
            "cv_index_page",
            "cv",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(CV_SERVICE_REVIEWING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(CV_SERVICE_ORGANIZING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(CV_SERVICE_MENTORING_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(CV_SERVICE_DEPARTMENT_LIST_PLACEHOLDER, rendered)
        self.assertIn("EGRAPHS Community Advisory Board, 2022 - Present", rendered)
        self.assertIn("UW CSE Faculty Graduate Admissions Co-chair", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
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

    def test_renders_linkless_students_and_coadvisors_as_plain_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "demo-student": {"name": "Demo Student"},
                            "coadvisor": {"name": "Co Advisor"},
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
                                    "key": "demo-student-current",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "PhD Student",
                                    "details": [
                                        {"kind": "coadvisor", "person_keys": ["coadvisor"]},
                                    ],
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
                data_dir=data_dir,
            )
            self.assertIn("- Demo Student, PhD Student", rendered)
            self.assertIn("co-advised with Co Advisor", rendered)
            self.assertNotIn("[Demo Student][]", rendered)
            self.assertNotIn("[Co Advisor][]", rendered)

    def test_renders_cv_students_section_with_compressed_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "demo-student": {"name": "Demo Student", "url": "https://example.test/demo"},
                            "coadvisor": {"name": "Co Advisor", "url": "https://example.test/coadvisor"},
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
                                    "key": "demo-student-phd-2025",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "PhD 2025",
                                    "details": [
                                        {
                                            "kind": "thesis",
                                            "title": "Composable Program Synthesis",
                                            "url": "https://example.test/thesis",
                                        },
                                        {"kind": "coadvisor", "person_keys": ["coadvisor"]},
                                        {"kind": "outcome", "djot": "Industry Researcher"},
                                    ],
                                },
                            )
                        ]
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_cv_students_section_list_djot(
                root,
                "current_students",
                data_dir=data_dir,
            )
            self.assertIn("- Demo Student, PhD 2025", rendered)
            self.assertIn("Thesis: Composable Program Synthesis", rendered)
            self.assertIn("Industry Researcher", rendered)
            self.assertNotIn("[Demo Student]", rendered)
            self.assertNotIn("co-advised with", rendered)

    def test_applies_projection_only_to_cv_students_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            data_dir.mkdir(parents=True)
            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "ian-briggs": {"name": "Ian Briggs", "url": "https://example.test/ian"},
                            "demo-student": {"name": "Demo Student", "url": "https://example.test/demo"},
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
                                    "key": "demo-student-current",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "PhD Student",
                                },
                            ),
                            _student_section(
                                "completed_postdoctoral_mentoring",
                                "Completed Postdoctoral Mentoring",
                                {
                                    "key": "demo-student-postdoc",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "Postdoc 2025",
                                },
                            ),
                            _student_section(
                                "graduated_doctoral_students",
                                "Graduated Doctoral Students",
                                {
                                    "key": "demo-student-phd",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "PhD 2024",
                                },
                            ),
                            _student_section(
                                "graduated_masters_students",
                                "Graduated Masters Students",
                                {
                                    "key": "demo-student-ms",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "MS 2023",
                                },
                            ),
                            _student_section(
                                "graduated_bachelors_students",
                                "Graduated Bachelors Students",
                                {
                                    "key": "demo-student-bs",
                                    "person_key": "demo-student",
                                    "name": "Demo Student",
                                    "label": "BS 2022",
                                },
                            ),
                            _student_section(
                                "visiting_students",
                                "Visiting Students and Interns",
                                {
                                    "key": "ian-briggs-visiting",
                                    "person_key": "ian-briggs",
                                    "name": "Ian Briggs",
                                    "label": "PhD, Summer 2022 @ Amazon",
                                },
                            ),
                        ]
                    }
                ),
                encoding="utf-8",
            )

            body = (
                "# Curriculum Vitae\n\n"
                f"{CV_STUDENTS_CURRENT_LIST_PLACEHOLDER}\n\n"
                f"{CV_STUDENTS_POSTDOC_LIST_PLACEHOLDER}\n\n"
                f"{CV_STUDENTS_PHD_LIST_PLACEHOLDER}\n\n"
                f"{CV_STUDENTS_MASTERS_LIST_PLACEHOLDER}\n\n"
                f"{CV_STUDENTS_BACHELORS_LIST_PLACEHOLDER}\n\n"
                f"{CV_STUDENTS_VISITING_LIST_PLACEHOLDER}\n"
            )
            rendered = apply_page_projections(
                "cv_index_page",
                "cv",
                body,
                root=root,
                data_dir=data_dir,
            )
            self.assertNotIn(CV_STUDENTS_CURRENT_LIST_PLACEHOLDER, rendered)
            self.assertNotIn(CV_STUDENTS_VISITING_LIST_PLACEHOLDER, rendered)
            self.assertIn("Ian Briggs, PhD, Summer 2022 @ Amazon", rendered)

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

    def test_applies_projection_only_to_cv_teaching_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        body = (
            "# Curriculum Vitae\n\n"
            f"{CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER}\n\n"
            f"{CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER}\n\n"
            f"{CV_TEACHING_TA_LIST_PLACEHOLDER}\n"
        )
        rendered = apply_page_projections(
            "cv_index_page",
            "cv",
            body,
            root=root,
            data_dir=root / "site" / "data",
        )
        self.assertNotIn(CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER, rendered)
        self.assertNotIn(CV_TEACHING_TA_LIST_PLACEHOLDER, rendered)
        self.assertIn("Marktoberdorf Summer School 2024", rendered)
        self.assertIn("UCSD CSE 231: Advanced Compiler Design", rendered)

        self.assertEqual(
            apply_page_projections(
                "ordinary_page",
                "about",
                body,
                root=root,
                data_dir=root / "site" / "data",
            ),
            body,
        )
