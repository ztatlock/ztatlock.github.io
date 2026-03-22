from __future__ import annotations

import unittest

from scripts.sitebuild.preview_builder import rewrite_local_html_targets


class PreviewBuilderTests(unittest.TestCase):
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
