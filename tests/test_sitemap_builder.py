from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.route_model import Route
from scripts.sitebuild.sitemap_builder import (
    build_sitemap_entries,
    render_sitemap_txt,
    render_sitemap_xml,
    route_is_sitemap_entry,
)


def route(
    *,
    kind: str,
    key: str,
    source_paths: tuple[Path, ...],
    output_relpath: str,
    public_url: str,
    canonical_url: str,
    is_draft: bool = False,
) -> Route:
    return Route(
        kind=kind,
        key=key,
        source_paths=source_paths,
        output_relpath=output_relpath,
        public_url=public_url,
        canonical_url=canonical_url,
        is_draft=is_draft,
    )


class SitemapBuilderTests(unittest.TestCase):
    def test_filters_to_public_pages_static_html_and_pdfs(self) -> None:
        routes = (
            route(
                kind="ordinary_page",
                key="about",
                source_paths=(Path("about.dj"),),
                output_relpath="about.html",
                public_url="/about.html",
                canonical_url="https://ztatlock.net/about.html",
            ),
            route(
                kind="talks_index_page",
                key="talks",
                source_paths=(Path("site/talks/index.dj"),),
                output_relpath="talks/index.html",
                public_url="/talks/",
                canonical_url="https://ztatlock.net/talks/",
            ),
            route(
                kind="students_index_page",
                key="students",
                source_paths=(Path("site/students/index.dj"), Path("site/data/students.json")),
                output_relpath="students/index.html",
                public_url="/students/",
                canonical_url="https://ztatlock.net/students/",
            ),
            route(
                kind="teaching_index_page",
                key="teaching",
                source_paths=(Path("site/teaching/index.dj"), Path("site/data/teaching.json")),
                output_relpath="teaching/index.html",
                public_url="/teaching/",
                canonical_url="https://ztatlock.net/teaching/",
            ),
            route(
                kind="publication_page",
                key="demo",
                source_paths=(Path("pub-demo.dj"), Path("pubs/demo/publication.json")),
                output_relpath="pubs/demo/index.html",
                public_url="/pubs/demo/",
                canonical_url="https://ztatlock.net/pubs/demo/",
            ),
            route(
                kind="ordinary_page",
                key="draft-page",
                source_paths=(Path("draft-page.dj"),),
                output_relpath="draft-page.html",
                public_url="/draft-page.html",
                canonical_url="https://ztatlock.net/draft-page.html",
                is_draft=True,
            ),
            route(
                kind="static_file",
                key="demo-html",
                source_paths=(Path("demo.html"),),
                output_relpath="demo.html",
                public_url="/demo.html",
                canonical_url="https://ztatlock.net/demo.html",
            ),
            route(
                kind="static_file",
                key="paper",
                source_paths=(Path("pubs/demo/demo.pdf"),),
                output_relpath="pubs/demo/demo.pdf",
                public_url="/pubs/demo/demo.pdf",
                canonical_url="https://ztatlock.net/pubs/demo/demo.pdf",
            ),
            route(
                kind="static_file",
                key="style",
                source_paths=(Path("style.css"),),
                output_relpath="style.css",
                public_url="/style.css",
                canonical_url="https://ztatlock.net/style.css",
            ),
        )

        included = [item.key for item in routes if route_is_sitemap_entry(item)]
        self.assertEqual(included, ["about", "talks", "students", "teaching", "demo", "demo-html", "paper"])

    def test_build_entries_uses_lookup_and_fallback_today(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            routes = (
                route(
                    kind="ordinary_page",
                    key="about",
                    source_paths=(root / "about.dj",),
                    output_relpath="about.html",
                    public_url="/about.html",
                    canonical_url="https://ztatlock.net/about.html",
                ),
                route(
                    kind="static_file",
                    key="paper",
                    source_paths=(root / "pubs" / "demo.pdf",),
                    output_relpath="pubs/demo.pdf",
                    public_url="/pubs/demo.pdf",
                    canonical_url="https://ztatlock.net/pubs/demo.pdf",
                ),
            )

            def lookup(_root: Path, source_paths: tuple[Path, ...]) -> str:
                if source_paths[0].name == "about.dj":
                    return "2026-03-20"
                return ""

            entries = build_sitemap_entries(
                routes,
                root=root,
                lastmod_lookup=lookup,
                today="2026-03-22",
            )

        self.assertEqual(entries[0].lastmod, "2026-03-20")
        self.assertEqual(entries[1].lastmod, "2026-03-22")

    def test_renders_txt_and_xml(self) -> None:
        entries = build_sitemap_entries(
            (
                route(
                    kind="ordinary_page",
                    key="about",
                    source_paths=(Path("about.dj"),),
                    output_relpath="about.html",
                    public_url="/about.html",
                    canonical_url="https://ztatlock.net/about.html",
                ),
            ),
            root=Path("."),
            lastmod_lookup=lambda _root, _paths: "2026-03-21",
        )

        txt = render_sitemap_txt(entries)
        xml = render_sitemap_xml(entries)

        self.assertEqual(txt, "https://ztatlock.net/about.html\n")
        self.assertIn("<loc>https://ztatlock.net/about.html</loc>", xml)
        self.assertIn("<lastmod>2026-03-21</lastmod>", xml)
