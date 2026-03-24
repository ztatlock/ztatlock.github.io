from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.page_projection import (
    TALKS_LIST_PLACEHOLDER,
    apply_page_projections,
    render_talks_list_djot,
)


class PageProjectionTests(unittest.TestCase):
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

    def test_applies_publications_projection_only_to_publications_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pubs_dir = root / "site" / "pubs"
            main_dir = pubs_dir / "2025-test-main"
            main_dir.mkdir(parents=True)
            (main_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [{"name": "Demo Author", "ref": "Demo Author"}],
                        "venue": "DemoConf",
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
                        "detail_page": False,
                        "listing_group": "workshop",
                        "pub_date": "2025-01-02",
                        "primary_link": "publisher",
                        "title": "Workshop Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Demo Workshop",
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
