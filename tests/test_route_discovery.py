from __future__ import annotations

import unittest
from pathlib import Path

from scripts.sitebuild.route_discovery import discover_routes
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
            ["about.dj"],
        )

    def test_discovers_future_publication_route(self) -> None:
        route = find_route(self.routes, kind="publication_page", key="2024-asplos-lakeroad")
        self.assertEqual(route.output_relpath, "pubs/2024-asplos-lakeroad/index.html")
        self.assertEqual(route.public_url, "/pubs/2024-asplos-lakeroad/")
        self.assertFalse(route.is_draft)
        self.assertEqual(
            [path.relative_to(ROOT).as_posix() for path in route.source_paths],
            [
                "pub-2024-asplos-lakeroad.dj",
                "pubs/2024-asplos-lakeroad/publication.json",
                "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.bib",
                "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad-abstract.md",
            ],
        )

    def test_discovers_draft_page_route(self) -> None:
        route = find_route(self.routes, kind="ordinary_page", key="course-recipe")
        self.assertTrue(route.is_draft)
        self.assertEqual(route.output_relpath, "course-recipe.html")

    def test_discovers_static_file_route(self) -> None:
        route = find_route(self.routes, kind="static_file", key="style.css")
        self.assertEqual(route.output_relpath, "style.css")
        self.assertEqual(route.public_url, "/style.css")

    def test_discovers_publication_asset_route(self) -> None:
        key = "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf"
        route = find_route(self.routes, kind="static_file", key=key)
        self.assertEqual(route.public_url, "/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf")
