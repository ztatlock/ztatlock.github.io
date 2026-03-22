from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.preview_validate import find_broken_link_issues, find_placeholder_issues


class PreviewValidateTests(unittest.TestCase):
    def test_static_html_todo_comment_is_not_treated_as_generated_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "demo.html").write_text("<!-- TODO demo note -->", encoding="utf-8")
            self.assertEqual(find_placeholder_issues(root), [])

    def test_publication_html_todo_is_treated_as_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pub_dir = root / "pubs" / "demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "index.html").write_text("TODO", encoding="utf-8")
            self.assertEqual(find_placeholder_issues(root), ["pubs/demo/index.html:1: TODO"])

    def test_root_relative_directory_link_resolves_to_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text('<a href="/pubs/demo/">demo</a>', encoding="utf-8")
            (root / "pubs" / "demo").mkdir(parents=True)
            (root / "pubs" / "demo" / "index.html").write_text("ok", encoding="utf-8")
            self.assertEqual(find_broken_link_issues(root), [])

    def test_root_relative_root_link_resolves_to_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text("home", encoding="utf-8")
            (root / "page.html").write_text('<a href="/">home</a>', encoding="utf-8")
            self.assertEqual(find_broken_link_issues(root), [])

    def test_reports_missing_local_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text('<a href="/missing.html">x</a>', encoding="utf-8")
            issues = find_broken_link_issues(root)
            self.assertEqual(issues, ["index.html: /missing.html"])
