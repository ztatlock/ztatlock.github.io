from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.artifact_validate import (
    find_broken_link_issues,
    find_placeholder_issues,
    recursive_html_files,
    top_level_html_files,
)

PREVIEW_PLACEHOLDER_RE = re.compile(
    r'YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)
LEGACY_PLACEHOLDER_RE = re.compile(
    r'TODO|YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)


class ArtifactValidateTests(unittest.TestCase):
    def test_top_level_html_files_excludes_nested_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text("ok", encoding="utf-8")
            nested = root / "pubs" / "demo"
            nested.mkdir(parents=True)
            (nested / "index.html").write_text("ok", encoding="utf-8")
            self.assertEqual(
                [path.name for path in top_level_html_files(root)],
                ["index.html"],
            )

    def test_placeholder_policy_allows_todo_outside_publications(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "demo.html").write_text("<!-- TODO demo note -->", encoding="utf-8")
            issues = find_placeholder_issues(
                html_files=recursive_html_files(root),
                relative_to=root,
                placeholder_re=PREVIEW_PLACEHOLDER_RE,
                publication_todo_prefixes=("pubs/",),
            )
            self.assertEqual(issues, [])

    def test_placeholder_policy_flags_publication_todo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pub_dir = root / "pubs" / "demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "index.html").write_text("TODO", encoding="utf-8")
            issues = find_placeholder_issues(
                html_files=recursive_html_files(root),
                relative_to=root,
                placeholder_re=PREVIEW_PLACEHOLDER_RE,
                publication_todo_prefixes=("pubs/",),
            )
            self.assertEqual(issues, ["pubs/demo/index.html:1: TODO"])

    def test_legacy_placeholder_policy_flags_publication_todo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "pub-demo.html").write_text("TODO", encoding="utf-8")
            issues = find_placeholder_issues(
                html_files=top_level_html_files(root),
                relative_to=root,
                placeholder_re=LEGACY_PLACEHOLDER_RE,
            )
            self.assertEqual(issues, ["pub-demo.html:1: TODO"])

    def test_root_relative_directory_link_resolves_to_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text('<a href="/pubs/demo/">demo</a>', encoding="utf-8")
            (root / "pubs" / "demo").mkdir(parents=True)
            (root / "pubs" / "demo" / "index.html").write_text("ok", encoding="utf-8")
            issues = find_broken_link_issues(
                html_files=recursive_html_files(root),
                artifact_root=root,
                relative_to=root,
            )
            self.assertEqual(issues, [])

    def test_root_relative_root_link_resolves_to_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text("home", encoding="utf-8")
            (root / "page.html").write_text('<a href="/">home</a>', encoding="utf-8")
            issues = find_broken_link_issues(
                html_files=top_level_html_files(root),
                artifact_root=root,
                relative_to=root,
            )
            self.assertEqual(issues, [])

    def test_reports_missing_local_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "index.html").write_text('<a href="/missing.html">x</a>', encoding="utf-8")
            issues = find_broken_link_issues(
                html_files=top_level_html_files(root),
                artifact_root=root,
                relative_to=root,
            )
            self.assertEqual(issues, ["index.html: /missing.html"])
