from __future__ import annotations

import unittest
from pathlib import Path

from scripts.sitebuild.djot_refs import load_and_render_site_refs
from scripts.sitebuild.page_renderer import render_page_html, rewrite_local_html_targets
from scripts.sitebuild.site_config import load_site_config

ROOT = Path(__file__).resolve().parents[1]


class PageRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_site_config(ROOT)
        cls.refs_text = load_and_render_site_refs(
            people_path=ROOT / "site" / "data" / "people.json",
            refs_path=ROOT / "templates" / "REFS",
        )

    def test_render_ordinary_page_uses_explicit_canonical_url(self) -> None:
        canonical = "https://example.com/about-preview"
        html = render_page_html(
            "about",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            webfiles_url=self.config.webfiles_url,
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', html)

    def test_render_publication_page_uses_explicit_canonical_url_and_aliases(self) -> None:
        canonical = "https://ztatlock.net/pubs/2024-asplos-lakeroad/"
        html = render_page_html(
            "pub-2024-asplos-lakeroad",
            canonical_url=canonical,
            refs_text=self.refs_text,
            root=ROOT,
            webfiles_url=self.config.webfiles_url,
            aliases={
                "img/favicon.png": "/img/favicon.png",
                "style.css": "/style.css",
                "publications.html": "/publications.html",
                "pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf": "/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf",
            },
        )
        self.assertIn(f'<link rel="canonical" href="{canonical}">', html)
        self.assertIn('href="/style.css"', html)
        self.assertIn(
            'href="/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf"',
            html,
        )

    def test_rewrites_publication_page_target(self) -> None:
        html = '<a href="pub-2024-asplos-lakeroad.html">paper</a>'
        rewritten = rewrite_local_html_targets(
            html,
            aliases={"pub-2024-asplos-lakeroad.html": "/pubs/2024-asplos-lakeroad/"},
        )
        self.assertIn('href="/pubs/2024-asplos-lakeroad/"', rewritten)

    def test_rewrites_static_asset_target(self) -> None:
        html = '<link rel="stylesheet" href="style.css">'
        rewritten = rewrite_local_html_targets(
            html,
            aliases={"style.css": "/style.css"},
        )
        self.assertIn('href="/style.css"', rewritten)

    def test_leaves_external_targets_alone(self) -> None:
        html = '<a href="https://example.com/">x</a>'
        rewritten = rewrite_local_html_targets(html, aliases={"https://example.com/": "/nope"})
        self.assertEqual(html, rewritten)
