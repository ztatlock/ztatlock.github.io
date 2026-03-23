from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.page_metadata import (
    render_page_meta_for_url,
    validate_general_page_metadata,
    validate_publication_metadata,
)


class PageMetadataTests(unittest.TestCase):
    def test_render_page_meta_uses_explicit_site_url_for_absolute_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pages.mkdir(parents=True)
            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/demo.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )

            html = render_page_meta_for_url(
                "about",
                "About",
                canonical_url="https://example.test/about.html",
                root=root,
                site_url="https://example.test",
                page_source_dir=pages,
            )
            self.assertIn('content="https://example.test/img/demo.png"', html)

    def test_validate_general_page_metadata_uses_configured_static_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            static = root / "site" / "static"
            img_dir = static / "img"
            pages.mkdir(parents=True)
            img_dir.mkdir(parents=True)

            (pages / "about.dj").write_text(
                "---\n"
                "description: Demo description\n"
                "image_path: img/demo.png\n"
                "---\n"
                "# About\n",
                encoding="utf-8",
            )
            (img_dir / "demo.png").write_bytes(b"PNG")

            issues = validate_general_page_metadata(
                root,
                page_source_dir=pages,
                static_source_dir=static,
            )
            self.assertEqual(issues, [])

    def test_validate_publication_metadata_uses_configured_publication_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)

            slug = "2025-test-demo"
            (pages / f"pub-{slug}.dj").write_text("# Demo\n", encoding="utf-8")
            pub_dir = pubs / slug
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
            (pub_dir / f"{slug}-abstract.md").write_text("Demo abstract.\n", encoding="utf-8")
            (pub_dir / f"{slug}.bib").write_text("@inproceedings{demo,\n  title={Demo}\n}\n", encoding="utf-8")
            (pub_dir / f"{slug}.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / f"{slug}-absimg.png").write_bytes(b"PNG")

            issues = validate_publication_metadata(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
            )
            self.assertEqual(issues, [])

    def test_validate_publication_metadata_rejects_stub_record_draft_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pubs = root / "site" / "pubs"
            pages.mkdir(parents=True)
            pubs.mkdir(parents=True)

            slug = "2025-test-demo"
            (pages / f"pub-{slug}.dj").write_text("# Demo\n", encoding="utf-8")
            pub_dir = pubs / slug
            pub_dir.mkdir()
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "draft": True,
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            issues = validate_publication_metadata(
                root,
                page_source_dir=pages,
                publications_dir=pubs,
            )
            self.assertEqual(
                issues,
                [
                    f"{pages / f'pub-{slug}.dj'}: draft status must stay in sync with {pub_dir / 'publication.json'}"
                ],
            )
