from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.route_discovery import RouteDiscoveryError, discover_routes
from scripts.sitebuild.site_config import load_site_config

ROOT = Path(__file__).resolve().parents[1]


def find_route(routes, *, kind: str, key: str):
    for route in routes:
        if route.kind == kind and route.key == key:
            return route
    raise AssertionError(f"missing route {kind}:{key}")


class RouteDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_site_config(ROOT)
        cls.routes = discover_routes(cls.config)

    def test_discovers_ordinary_page_route(self) -> None:
        route = find_route(self.routes, kind="ordinary_page", key="about")
        self.assertEqual(route.output_relpath, "about.html")
        self.assertEqual(route.public_url, "/about.html")
        self.assertFalse(route.is_draft)
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/pages/about.dj"],
        )

    def test_discovers_ordinary_page_route_with_pub_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "pub-demo.dj").write_text("# Demo\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            routes = discover_routes(config)

            route = find_route(routes, kind="ordinary_page", key="pub-demo")
            self.assertEqual(route.output_relpath, "pub-demo.html")
            self.assertEqual(route.public_url, "/pub-demo.html")

    def test_discovers_future_publication_route(self) -> None:
        route = find_route(self.routes, kind="publication_page", key="2024-asplos-lakeroad")
        self.assertEqual(route.output_relpath, "pubs/2024-asplos-lakeroad/index.html")
        self.assertEqual(route.public_url, "/pubs/2024-asplos-lakeroad/")
        self.assertFalse(route.is_draft)
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            [
                "site/pubs/2024-asplos-lakeroad/publication.json",
                "site/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.bib",
                "site/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad-abstract.md",
            ],
        )

    def test_discovers_draft_page_route(self) -> None:
        route = find_route(self.routes, kind="ordinary_page", key="course-recipe")
        self.assertTrue(route.is_draft)
        self.assertEqual(route.output_relpath, "course-recipe.html")

    def test_discovers_talks_index_route_with_talk_bundle_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            talks_dir = root / "site" / "talks"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            talks_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (talks_dir / "index.dj").write_text("# Talks\n\n__TALKS_LIST__\n", encoding="utf-8")

            brown_dir = talks_dir / "2026-02-brown-eqsat"
            brown_dir.mkdir()
            (brown_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Everything is a compiler, try Equality Saturation!",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            uiuc_dir = talks_dir / "2023-05-uiuc-egg"
            uiuc_dir.mkdir()
            (uiuc_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Relational Equality Saturation in egg",
                        "when": {"year": 2023, "month": 5},
                        "at": [{"text": "University of Illinois at Urbana-Champaign"}],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                talks_dir=talks_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            routes = discover_routes(config)

            route = find_route(routes, kind="talks_index_page", key="talks")
            self.assertEqual(route.output_relpath, "talks/index.html")
            self.assertEqual(route.public_url, "/talks/")
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in route.source_paths],
                [
                    "site/talks/index.dj",
                    "site/talks/2023-05-uiuc-egg/talk.json",
                    "site/talks/2026-02-brown-eqsat/talk.json",
                ],
            )

    def test_discovers_cv_index_route(self) -> None:
        route = find_route(self.routes, kind="cv_index_page", key="cv")
        self.assertEqual(route.output_relpath, "cv/index.html")
        self.assertEqual(route.public_url, "/cv/")
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/cv/index.dj"],
        )

    def test_discovers_publications_index_route(self) -> None:
        route = find_route(self.routes, kind="publications_index_page", key="publications")
        self.assertEqual(route.output_relpath, "pubs/index.html")
        self.assertEqual(route.public_url, "/pubs/")
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/pubs/index.dj"],
        )

    def test_discovers_service_index_route(self) -> None:
        route = find_route(self.routes, kind="service_index_page", key="service")
        self.assertEqual(route.output_relpath, "service/index.html")
        self.assertEqual(route.public_url, "/service/")
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/service/index.dj", "site/data/service.json"],
        )

    def test_discovers_students_index_route(self) -> None:
        route = find_route(self.routes, kind="students_index_page", key="students")
        self.assertEqual(route.output_relpath, "students/index.html")
        self.assertEqual(route.public_url, "/students/")
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/students/index.dj", "site/data/students.json"],
        )

    def test_discovers_teaching_index_route(self) -> None:
        route = find_route(self.routes, kind="teaching_index_page", key="teaching")
        self.assertEqual(route.output_relpath, "teaching/index.html")
        self.assertEqual(route.public_url, "/teaching/")
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            ["site/teaching/index.dj", "site/data/teaching.json"],
        )

    def test_rejects_legacy_and_collection_talk_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            talks_dir = root / "site" / "talks"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            talks_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "talks.dj").write_text("# Talks\n", encoding="utf-8")
            (talks_dir / "index.dj").write_text("# Talks\n\n__TALKS_LIST__\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                talks_dir=talks_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_legacy_and_collection_publications_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "publications.dj").write_text("# Publications\n", encoding="utf-8")
            (publications_dir / "index.dj").write_text("# Publications\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_legacy_and_collection_service_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            service_dir = root / "site" / "service"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            service_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "service.dj").write_text("# Service\n", encoding="utf-8")
            (service_dir / "index.dj").write_text("# Service\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                service_dir=service_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_legacy_and_collection_students_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            students_dir = root / "site" / "students"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            students_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "students.dj").write_text("# Students\n", encoding="utf-8")
            (students_dir / "index.dj").write_text("# Students\n", encoding="utf-8")
            (data_dir / "students.json").write_text('{"sections":[]}\n', encoding="utf-8")
            (data_dir / "people.json").write_text('{"people":{}}\n', encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                students_dir=students_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_legacy_and_collection_cv_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            cv_dir = root / "site" / "cv"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            cv_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "cv.dj").write_text("# CV\n", encoding="utf-8")
            (cv_dir / "index.dj").write_text("# CV\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                cv_dir=cv_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_legacy_and_collection_teaching_wrappers_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            teaching_dir = root / "site" / "teaching"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            teaching_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "teaching.dj").write_text("# Teaching\n", encoding="utf-8")
            (teaching_dir / "index.dj").write_text("# Teaching\n", encoding="utf-8")
            (data_dir / "teaching.json").write_text('{"groups":[]}\n', encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
            )

            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_discovers_static_file_route(self) -> None:
        route = find_route(self.routes, kind="static_file", key="style.css")
        self.assertEqual(route.output_relpath, "style.css")
        self.assertEqual(route.public_url, "/style.css")

    def test_discovers_publication_asset_route(self) -> None:
        key = "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf"
        route = find_route(self.routes, kind="static_file", key=key)
        self.assertEqual(route.public_url, "/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf")

    def test_discovers_routes_from_configured_source_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)
            (static_source_dir / "nested").mkdir(parents=True)

            (page_source_dir / "about.dj").write_text("# About\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (static_source_dir / "nested" / "notes.txt").write_text("demo\n", encoding="utf-8")
            (img_dir / "logo.png").write_bytes(b"PNG")

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

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            routes = discover_routes(config)

            about_route = find_route(routes, kind="ordinary_page", key="about")
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in about_route.source_paths],
                ["site/pages/about.dj"],
            )

            publication_route = find_route(
                routes,
                kind="publication_page",
                key="2025-test-demo",
            )
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in publication_route.source_paths],
                [
                    "site/pubs/2025-test-demo/publication.json",
                    "site/pubs/2025-test-demo/2025-test-demo.bib",
                    "site/pubs/2025-test-demo/2025-test-demo-abstract.md",
                ],
            )
            self.assertEqual(
                publication_route.output_relpath,
                "pubs/2025-test-demo/index.html",
            )

    def test_skips_published_index_only_publication_page_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text("# About\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

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

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            routes = discover_routes(config)

            publication_page_routes = [route for route in routes if route.kind == "publication_page"]
            self.assertEqual(publication_page_routes, [])

            style_route = find_route(routes, kind="static_file", key="style.css")
            self.assertEqual(style_route.output_relpath, "style.css")
            publication_asset_routes = [
                route for route in routes if route.kind == "static_file" and route.key.startswith("pubs/")
            ]
            self.assertEqual(publication_asset_routes, [])

    def test_discovers_draft_publication_route_from_record_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text("# About\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

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

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            routes = discover_routes(config)

            route = find_route(routes, kind="publication_page", key="2025-test-draft")
            self.assertTrue(route.is_draft)
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in route.source_paths],
                ["site/pubs/2025-test-draft/publication.json"],
            )

    def test_rejects_public_publication_route_missing_canonical_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"
            img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text("# About\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            pub_dir = publications_dir / "2025-test-broken"
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Broken Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Broken demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)

    def test_rejects_reserved_generated_static_paths_in_recursive_static_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            static_source_dir = root / "site" / "static"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            static_source_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text("# About\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (static_source_dir / "sitemap.txt").write_text("bad\n", encoding="utf-8")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            with self.assertRaises(RouteDiscoveryError):
                discover_routes(config)
