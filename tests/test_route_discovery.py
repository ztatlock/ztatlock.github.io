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

    def test_discovers_talks_page_route_with_talk_bundle_sources(self) -> None:
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

            (page_source_dir / "talks.dj").write_text("# Talks\n\n__TALKS_LIST__\n", encoding="utf-8")
            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")

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

            route = find_route(routes, kind="ordinary_page", key="talks")
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in route.source_paths],
                [
                    "site/pages/talks.dj",
                    "site/talks/2023-05-uiuc-egg/talk.json",
                    "site/talks/2026-02-brown-eqsat/talk.json",
                ],
            )

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

            style_route = find_route(routes, kind="static_file", key="style.css")
            self.assertEqual(style_route.output_relpath, "style.css")

            image_route = find_route(routes, kind="static_file", key="img/logo.png")
            self.assertEqual(image_route.output_relpath, "img/logo.png")

            nested_route = find_route(routes, kind="static_file", key="nested/notes.txt")
            self.assertEqual(nested_route.output_relpath, "nested/notes.txt")

            paper_route = find_route(
                routes,
                kind="static_file",
                key="pubs/2025-test-demo/2025-test-demo.pdf",
            )
            self.assertEqual(
                paper_route.output_relpath,
                "pubs/2025-test-demo/2025-test-demo.pdf",
            )

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
