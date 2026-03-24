from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.site_builder import build_site
from scripts.sitebuild.site_config import load_site_config


class SiteBuilderTests(unittest.TestCase):
    def test_builds_site_from_configured_source_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page_source_dir = root / "site" / "pages"
            teaching_dir = root / "custom" / "teaching"
            talks_dir = root / "site" / "talks"
            publications_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            teaching_dir.mkdir(parents=True)
            talks_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)
            (static_source_dir / "nested").mkdir(parents=True)

            (page_source_dir / "about.dj").write_text(
                "---\n"
                "description: About page\n"
                "---\n"
                "# About\n\n"
                "Site body.\n",
                encoding="utf-8",
            )
            (talks_dir / "index.dj").write_text(
                "---\n"
                "description: Talks page\n"
                "---\n"
                "# Talks\n\n"
                "__TALKS_LIST__\n",
                encoding="utf-8",
            )
            (teaching_dir / "index.dj").write_text(
                "---\n"
                "description: Teaching page\n"
                "---\n"
                "# Teaching\n\n"
                "__TEACHING_UW_COURSES_LIST__\n\n"
                "__TEACHING_SPECIAL_TOPICS_LIST__\n\n"
                "__TEACHING_SUMMER_SCHOOL_LIST__\n",
                encoding="utf-8",
            )

            talk_dir = talks_dir / "2026-02-brown-eqsat"
            talk_dir.mkdir()
            (talk_dir / "talk.json").write_text(
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

            pub_dir = publications_dir / "2025-test-demo"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "badges": [],
                        "description": "Demo description",
                        "share_description": "",
                        "meta_image_path": "",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (pub_dir / "2025-test-demo-abstract.md").write_text(
                "Demo abstract.\n",
                encoding="utf-8",
            )
            (pub_dir / "2025-test-demo.bib").write_text(
                "@inproceedings{demo,\n  title={Demo}\n}\n",
                encoding="utf-8",
            )
            (pub_dir / "2025-test-demo.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / "2025-test-demo-absimg.png").write_bytes(b"PNG")

            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")

            (data_dir / "people.json").write_text('{"people": {}}', encoding="utf-8")
            (data_dir / "teaching.json").write_text(
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
                                        "title": "Computer-Aided Reasoning for Software",
                                        "description_djot": "Doctoral course.",
                                        "offerings": [{"year": 2025, "term": "Spring", "url": "https://example.com/507"}],
                                    }
                                ],
                            },
                            {
                                "key": "special_topics",
                                "records": [
                                    {
                                        "key": "uw-cse-599x",
                                        "kind": "course",
                                        "code": "UW CSE 599X",
                                        "title": "Topics in Program Synthesis",
                                        "details": ["Co-taught special-topics seminar."],
                                        "offerings": [{"year": 2024, "term": "Autumn", "url": "https://example.com/599x"}],
                                    }
                                ],
                            },
                            {
                                "key": "summer_school",
                                "records": [
                                    {
                                        "key": "marktoberdorf-2024",
                                        "kind": "summer_school",
                                        "title": "Marktoberdorf Summer School 2024",
                                        "events": [
                                            {
                                                "label": "Marktoberdorf Summer School, August 2024",
                                                "url": "https://example.com/marktoberdorf",
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "key": "teaching_assistant",
                                "records": [
                                    {
                                        "key": "ucsd-cse-231",
                                        "kind": "course",
                                        "code": "UCSD CSE 231",
                                        "title": "Graduate Programming Languages",
                                        "details": ["Teaching assistant."],
                                        "offerings": [{"year": 2009, "term": "Spring"}],
                                    }
                                ],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (static_source_dir / "nested" / "notes.txt").write_text("demo\n", encoding="utf-8")
            (static_source_dir / "demo.html").write_text("<html>demo</html>\n", encoding="utf-8")
            (img_dir / "logo.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                teaching_dir=teaching_dir,
                talks_dir=talks_dir,
                publications_dir=publications_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
            )

            routes = build_site(config)
            self.assertTrue(routes)

            about_html = (config.build_dir / "about.html").read_text(encoding="utf-8")
            self.assertIn('href="https://ztatlock.net/about.html"', about_html)
            self.assertIn("Site body.", about_html)

            talks_html = (config.build_dir / "talks" / "index.html").read_text(encoding="utf-8")
            self.assertIn("Everything is a compiler, try Equality Saturation!", talks_html)
            self.assertIn("Brown University, PL and Graphics groups, February 2026", talks_html)
            self.assertIn('href="https://events.brown.edu/demo"', talks_html)

            teaching_html = (config.build_dir / "teaching" / "index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn('href="https://ztatlock.net/teaching/"', teaching_html)
            self.assertIn("UW CSE 507: Computer-Aided Reasoning for Software", teaching_html)
            self.assertIn("Marktoberdorf Summer School 2024", teaching_html)

            publication_html = (
                config.build_dir / "pubs" / "2025-test-demo" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn(
                'href="https://ztatlock.net/pubs/2025-test-demo/"',
                publication_html,
            )
            self.assertIn(
                'href="/pubs/2025-test-demo/2025-test-demo.pdf"',
                publication_html,
            )

            self.assertTrue((config.build_dir / "style.css").exists())
            self.assertTrue((config.build_dir / "nested" / "notes.txt").exists())
            self.assertTrue((config.build_dir / "demo.html").exists())
            self.assertTrue((config.build_dir / "img" / "logo.png").exists())
            self.assertTrue((config.build_dir / "pubs" / "2025-test-demo" / "2025-test-demo.pdf").exists())
            self.assertFalse((config.build_dir / "talks.html").exists())

    def test_skips_draft_publication_without_stub_or_public_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page_source_dir = root / "site" / "pages"
            talks_dir = root / "site" / "talks"
            publications_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            talks_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text(
                "---\n"
                "description: About page\n"
                "---\n"
                "# About\n\n"
                "Site body.\n",
                encoding="utf-8",
            )

            pub_dir = publications_dir / "2025-test-draft"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "draft": True,
                        "title": "Draft Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Draft demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")

            (data_dir / "people.json").write_text('{"people": {}}', encoding="utf-8")

            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                talks_dir=talks_dir,
                publications_dir=publications_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
            )

            routes = build_site(config)
            self.assertTrue(routes)

            about_html = (config.build_dir / "about.html").read_text(encoding="utf-8")
            self.assertIn("Site body.", about_html)

            self.assertFalse((config.build_dir / "pubs" / "2025-test-draft" / "index.html").exists())
            self.assertFalse((config.build_dir / "pubs" / "2025-test-draft" / "2025-test-draft.pdf").exists())

    def test_skips_building_index_only_publication_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text(
                "---\n"
                "description: About page\n"
                "---\n"
                "# About\n\n"
                "Site body.\n",
                encoding="utf-8",
            )

            pub_dir = publications_dir / "2025-test-demo"
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

            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")
            (data_dir / "people.json").write_text('{"people": {}}', encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
            )

            build_site(config)

            self.assertFalse((config.build_dir / "pubs" / "2025-test-demo" / "index.html").exists())
