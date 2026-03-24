from __future__ import annotations

import unittest
from pathlib import Path

from scripts.sitebuild.route_model import Route, RouteModelError, canonical_url, validate_routes


def route(
    *,
    kind: str,
    key: str,
    output_relpath: str,
    public_url: str,
    canonical_url_value: str,
) -> Route:
    return Route(
        kind=kind,
        key=key,
        source_paths=(Path("source"),),
        output_relpath=output_relpath,
        public_url=public_url,
        canonical_url=canonical_url_value,
        is_draft=False,
    )


class RouteModelTests(unittest.TestCase):
    def test_canonical_url_handles_root(self) -> None:
        self.assertEqual(canonical_url("https://ztatlock.net", "/"), "https://ztatlock.net/")

    def test_canonical_url_handles_page(self) -> None:
        self.assertEqual(
            canonical_url("https://ztatlock.net", "/about.html"),
            "https://ztatlock.net/about.html",
        )

    def test_validate_routes_rejects_duplicate_output_path(self) -> None:
        routes = (
            route(
                kind="ordinary_page",
                key="about",
                output_relpath="about.html",
                public_url="/about.html",
                canonical_url_value="https://ztatlock.net/about.html",
            ),
            route(
                kind="static_file",
                key="about-copy",
                output_relpath="about.html",
                public_url="/about-copy.html",
                canonical_url_value="https://ztatlock.net/about-copy.html",
            ),
        )
        with self.assertRaises(RouteModelError):
            validate_routes(routes)

    def test_validate_routes_rejects_duplicate_public_url(self) -> None:
        routes = (
            route(
                kind="ordinary_page",
                key="about",
                output_relpath="about.html",
                public_url="/about.html",
                canonical_url_value="https://ztatlock.net/about.html",
            ),
            route(
                kind="publication_page",
                key="pub",
                output_relpath="pubs/pub/index.html",
                public_url="/about.html",
                canonical_url_value="https://ztatlock.net/pubs/pub/",
            ),
        )
        with self.assertRaises(RouteModelError):
            validate_routes(routes)

    def test_validate_routes_rejects_absolute_output_relpath(self) -> None:
        routes = (
            route(
                kind="ordinary_page",
                key="about",
                output_relpath="/about.html",
                public_url="/about.html",
                canonical_url_value="https://ztatlock.net/about.html",
            ),
        )
        with self.assertRaises(RouteModelError):
            validate_routes(routes)

    def test_validate_routes_accepts_talks_index_page(self) -> None:
        routes = (
            route(
                kind="talks_index_page",
                key="talks",
                output_relpath="talks/index.html",
                public_url="/talks/",
                canonical_url_value="https://ztatlock.net/talks/",
            ),
        )
        validate_routes(routes)

    def test_validate_routes_accepts_students_index_page(self) -> None:
        routes = (
            route(
                kind="students_index_page",
                key="students",
                output_relpath="students/index.html",
                public_url="/students/",
                canonical_url_value="https://ztatlock.net/students/",
            ),
        )
        validate_routes(routes)

    def test_validate_routes_accepts_publications_index_page(self) -> None:
        routes = (
            route(
                kind="publications_index_page",
                key="publications",
                output_relpath="pubs/index.html",
                public_url="/pubs/",
                canonical_url_value="https://ztatlock.net/pubs/",
            ),
        )
        validate_routes(routes)
