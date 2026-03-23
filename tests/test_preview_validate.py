from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import validate_preview_build
from scripts.sitebuild.preview_builder import build_preview_site
from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.preview_validate import find_sitemap_file_issues


class PreviewValidateTests(unittest.TestCase):
    def test_reports_missing_preview_sitemap_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.assertEqual(
                find_sitemap_file_issues(root),
                ["missing sitemap.txt", "missing sitemap.xml"],
            )

    def test_reports_sitemap_content_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "sitemap.txt").write_text("wrong\n", encoding="utf-8")
            (root / "sitemap.xml").write_text("<wrong/>\n", encoding="utf-8")
            self.assertEqual(
                find_sitemap_file_issues(
                    root,
                    expected_txt="right\n",
                    expected_xml="<right/>\n",
                ),
                [
                    "sitemap.txt does not match route-driven preview sitemap",
                    "sitemap.xml does not match route-driven preview sitemap",
                ],
            )

    def test_preview_validator_reports_source_metadata_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages_dir = root / "site" / "pages"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_dir = root / "site" / "static"

            pages_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            static_dir.mkdir(parents=True)
            (static_dir / "img").mkdir(parents=True)

            (pages_dir / "about.dj").write_text(
                "---\n"
                "description: About preview page\n"
                "image_path: img/missing.png\n"
                "---\n"
                "# About\n\n"
                "Preview body.\n",
                encoding="utf-8",
            )
            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")
            (data_dir / "people.json").write_text(json.dumps({"people": {}}), encoding="utf-8")
            (static_dir / "style.css").write_text("body {}\n", encoding="utf-8")

            config = load_site_config(root)
            build_preview_site(config)

            stdout = io.StringIO()
            with (
                patch("sys.argv", ["validate_preview_build", "--root", str(root)]),
                redirect_stdout(stdout),
            ):
                self.assertEqual(validate_preview_build.main(), 1)

            self.assertIn("ERROR: found invalid preview source", stdout.getvalue())
            self.assertIn("img/missing.png", stdout.getvalue())

    def test_preview_validator_accepts_bundle_only_publications(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages_dir = root / "site" / "pages"
            pubs_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_dir = root / "site" / "static"

            pages_dir.mkdir(parents=True)
            pubs_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            static_dir.mkdir(parents=True)
            (static_dir / "img").mkdir(parents=True)

            (pages_dir / "about.dj").write_text(
                "---\n"
                "description: About preview page\n"
                "---\n"
                "# About\n\n"
                "Preview body.\n",
                encoding="utf-8",
            )
            pub_dir = pubs_dir / "2025-test-demo"
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
            (templates_dir / "HEAD.1").write_text(
                "<html><head><title>__TITLE__</title>"
                '<link rel="canonical" href="__CANON__">',
                encoding="utf-8",
            )
            (templates_dir / "HEAD.2").write_text("</head><body>", encoding="utf-8")
            (templates_dir / "FOOT").write_text("</body></html>\n", encoding="utf-8")
            (templates_dir / "REFS").write_text("", encoding="utf-8")
            (data_dir / "people.json").write_text(json.dumps({"people": {}}), encoding="utf-8")
            (static_dir / "style.css").write_text("body {}\n", encoding="utf-8")
            (static_dir / "img" / "favicon.png").write_bytes(b"PNG")
            (static_dir / "img" / "favicon-meta.png").write_bytes(b"PNG")

            config = load_site_config(
                root,
                page_source_dir=pages_dir,
                publications_dir=pubs_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_dir,
            )
            build_preview_site(config)

            stdout = io.StringIO()
            with (
                patch("sys.argv", ["validate_preview_build", "--root", str(root)]),
                redirect_stdout(stdout),
            ):
                self.assertEqual(validate_preview_build.main(), 0)
            self.assertEqual(stdout.getvalue(), "")
