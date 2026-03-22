#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from scripts.sitebuild.artifact_validate import (
    find_broken_link_issues,
    find_placeholder_issues,
    recursive_html_files,
)
from scripts.sitebuild.route_discovery import discover_routes
from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.sitemap_builder import build_sitemap_entries, render_sitemap_txt, render_sitemap_xml
from scripts.sitebuild.preview_validate import find_sitemap_file_issues

PREVIEW_PLACEHOLDER_RE = re.compile(
    r'YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)


def _print_section(title: str, issues: list[str]) -> None:
    if not issues:
        return
    print(title)
    for issue in issues:
        print(issue)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the preview site built under build/."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    config = load_site_config(Path(args.root))
    build_root = config.build_dir
    html_files = recursive_html_files(build_root)
    placeholder_issues = find_placeholder_issues(
        html_files=html_files,
        relative_to=build_root,
        placeholder_re=PREVIEW_PLACEHOLDER_RE,
        publication_todo_prefixes=("pubs/",),
    )
    broken_link_issues = find_broken_link_issues(
        html_files=html_files,
        artifact_root=build_root,
        relative_to=build_root,
    )
    routes = discover_routes(config)
    sitemap_entries = build_sitemap_entries(routes, root=config.root)
    sitemap_issues = find_sitemap_file_issues(
        build_root,
        expected_txt=render_sitemap_txt(sitemap_entries),
        expected_xml=render_sitemap_xml(sitemap_entries),
    )

    if placeholder_issues:
        _print_section(
            "ERROR: found unresolved placeholders in preview HTML",
            placeholder_issues,
        )
    if broken_link_issues:
        _print_section(
            "ERROR: found broken local links in preview HTML",
            broken_link_issues,
        )
    if sitemap_issues:
        _print_section(
            "ERROR: found invalid preview sitemaps",
            sitemap_issues,
        )

    return 1 if placeholder_issues or broken_link_issues or sitemap_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
