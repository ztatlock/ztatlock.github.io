from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.publication_index import (
    PublicationIndexError,
    render_publications_list_djot,
)


class PublicationIndexTests(unittest.TestCase):
    def test_renders_publication_entries_from_bundles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pubs = root / "site" / "pubs"
            first = pubs / "2025-test-main"
            first.mkdir(parents=True)
            (first / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-02",
                        "primary_link": "publisher",
                        "title": "Main Paper",
                        "authors": [
                            {"name": "First Author", "ref": "First Author"},
                            {"name": "Second Author", "ref": ""},
                        ],
                        "venue": "DemoConf",
                        "badges": ["★ Best Paper"],
                        "links": {"publisher": "https://example.test/main"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            second = pubs / "2025-test-local"
            second.mkdir(parents=True)
            (second / "publication.json").write_text(
                json.dumps(
                    {
                        "listing_group": "main",
                        "pub_date": "2024-12-31",
                        "title": "Local Paper",
                        "authors": [{"name": "Local Author", "ref": "Local Author"}],
                        "venue": "Demo Journal",
                        "description": "Local detail page",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (second / "2025-test-local-abstract.md").write_text("Demo abstract.\n", encoding="utf-8")
            (second / "2025-test-local.bib").write_text("@article{demo}\n", encoding="utf-8")
            (second / "2025-test-local.pdf").write_bytes(b"%PDF-1.4\n")
            (second / "2025-test-local-absimg.png").write_bytes(b"PNG")

            rendered = render_publications_list_djot(root, "main", publications_dir=pubs)
            self.assertIn("{#2025-test-main}", rendered)
            self.assertIn("*[Main Paper](https://example.test/main)* \\", rendered)
            self.assertIn("[First Author][First Author],", rendered)
            self.assertIn("\\ Second Author", rendered)
            self.assertIn("DemoConf 2025 \\\n★ Best Paper", rendered)
            self.assertIn("*[Local Paper](pubs/2025-test-local/)* \\", rendered)
            self.assertLess(rendered.find("Main Paper"), rendered.find("Local Paper"))

    def test_renders_workshop_subset_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pubs = root / "site" / "pubs"

            for slug, group in (("2025-test-main", "main"), ("2025-test-workshop", "workshop")):
                pub_dir = pubs / slug
                pub_dir.mkdir(parents=True)
                (pub_dir / "publication.json").write_text(
                    json.dumps(
                        {
                            "detail_page": False,
                            "listing_group": group,
                            "pub_date": "2025-01-01",
                            "primary_link": "publisher",
                            "title": slug,
                            "authors": [{"name": "Demo Author", "ref": ""}],
                            "venue": "DemoConf",
                            "links": {"publisher": f"https://example.test/{slug}"},
                            "talks": [],
                        }
                    ),
                    encoding="utf-8",
                )

            rendered = render_publications_list_djot(root, "workshop", publications_dir=pubs)
            self.assertIn("{#2025-test-workshop}", rendered)
            self.assertNotIn("{#2025-test-main}", rendered)

    def test_rejects_unknown_listing_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pubs = root / "site" / "pubs"
            pubs.mkdir(parents=True)

            with self.assertRaises(PublicationIndexError):
                render_publications_list_djot(root, "journal", publications_dir=pubs)
