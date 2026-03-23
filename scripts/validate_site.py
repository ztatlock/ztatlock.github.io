#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from scripts.page_metadata import (
    validate_publication_bridge_metadata,
)
from scripts.sitebuild.artifact_validate import (
    find_broken_link_issues,
    find_placeholder_issues,
    top_level_html_files,
)
from scripts.sitebuild.site_config import load_site_config
from scripts.sitebuild.source_validate import find_source_issues

LEGACY_PLACEHOLDER_RE = re.compile(
    r'TODO|YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)


def find_legacy_metadata_issues(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.glob("*.meta")):
        issues.append(f"{path.name}: legacy raw .meta sidecars are no longer supported")
    return issues


def print_section(title: str, issues: list[str]) -> None:
    if not issues:
        return
    print(title)
    for issue in issues:
        print(issue)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate generated website artifacts and page metadata."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Site root to validate (default: current directory).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = load_site_config(root)
    html_files = top_level_html_files(root)

    placeholder_issues = find_placeholder_issues(
        html_files=[path for path in html_files if path.name.startswith("pub-")],
        relative_to=root,
        placeholder_re=LEGACY_PLACEHOLDER_RE,
    )
    broken_link_issues = find_broken_link_issues(
        html_files=html_files,
        artifact_root=root,
        relative_to=root,
    )
    legacy_metadata_issues = find_legacy_metadata_issues(root)
    source_metadata_issues = find_source_issues(config)
    publication_bridge_issues = validate_publication_bridge_metadata(
        root,
        page_source_dir=config.page_source_dir,
        publications_dir=config.publications_dir,
    )

    if placeholder_issues:
        print_section(
            "ERROR: found unresolved publication placeholders in generated HTML",
            placeholder_issues,
        )
    if broken_link_issues:
        print_section(
            "ERROR: found broken local links in generated HTML",
            broken_link_issues,
        )
    if legacy_metadata_issues:
        print_section("ERROR: found legacy raw page metadata files", legacy_metadata_issues)
    if source_metadata_issues:
        print_section(
            "ERROR: found invalid page metadata source",
            source_metadata_issues,
        )
    if publication_bridge_issues:
        print_section(
            "ERROR: found invalid publication source bridge",
            publication_bridge_issues,
        )

    return 1 if (
        placeholder_issues
        or broken_link_issues
        or legacy_metadata_issues
        or source_metadata_issues
        or publication_bridge_issues
    ) else 0


if __name__ == "__main__":
    sys.exit(main())
