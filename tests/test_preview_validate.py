from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

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
