from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.preview_builder import build_preview_site
from scripts.sitebuild.site_config import load_site_config


class PreviewBuilderTests(unittest.TestCase):
    def test_builds_preview_from_configured_source_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page_source_dir = root / "site" / "pages"
            publications_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_source_dir = root / "site" / "static"
            shared_img_dir = static_source_dir / "img"

            page_source_dir.mkdir(parents=True)
            publications_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            shared_img_dir.mkdir(parents=True)

            (page_source_dir / "about.dj").write_text(
                "---\n"
                "description: About preview page\n"
                "---\n"
                "# About\n\n"
                "Preview body.\n",
                encoding="utf-8",
            )
            (page_source_dir / "pub-2025-test-demo.dj").write_text(
                "# Demo Preview\n",
                encoding="utf-8",
            )

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

            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")

            (data_dir / "people.json").write_text('{"people": {}}', encoding="utf-8")

            (static_source_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (shared_img_dir / "logo.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=page_source_dir,
                publications_dir=publications_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_source_dir,
                shared_img_dir=shared_img_dir,
            )

            routes = build_preview_site(config)
            self.assertTrue(routes)

            about_html = (config.build_dir / "about.html").read_text(encoding="utf-8")
            self.assertIn('href="https://ztatlock.net/about.html"', about_html)
            self.assertIn("Preview body.", about_html)

            publication_html = (
                config.build_dir / "pubs" / "2025-test-demo" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn(
                'href="https://ztatlock.net/pubs/2025-test-demo/"',
                publication_html,
            )
            self.assertIn(
                'href="/pubs/2025-test-demo/2025-test-demo.pdf"',
                publication_html,
            )

            self.assertTrue((config.build_dir / "style.css").exists())
            self.assertTrue((config.build_dir / "img" / "logo.png").exists())
            self.assertTrue((config.build_dir / "pubs" / "2025-test-demo" / "2025-test-demo.pdf").exists())
