#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from page_metadata import (
    MetadataError,
    load_general_page_metadata,
    load_front_matter_general_metadata,
    load_publication_metadata,
    publication_slug,
    validate_general_page_metadata,
    validate_publication_metadata,
)
from page_source import PageSourceError, read_page_source

IGNORED_TARGET_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "data:",
    "javascript:",
)
PLACEHOLDER_RE = re.compile(
    r'TODO|YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)
HTML_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def find_placeholder_issues(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.glob("pub-*.html")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                issues.append(f"{path.name}:{lineno}: {line.strip()}")
    return issues


def find_broken_link_issues(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for target in HTML_LINK_RE.findall(text):
            if target.startswith(IGNORED_TARGET_PREFIXES):
                continue
            relpath = target.split("#", 1)[0].split("?", 1)[0]
            if not relpath:
                continue
            if not (root / relpath).exists():
                issues.append(f"{path.name}: {target}")
    return issues


def find_legacy_metadata_issues(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.glob("*.meta")):
        issues.append(f"{path.name}: legacy raw .meta sidecars are no longer supported")
    return issues


def find_missing_metadata_warnings(root: Path) -> list[str]:
    warnings: list[str] = []
    structured_pages: set[str] = set()

    try:
        structured_pages.update(load_general_page_metadata(root).keys())
    except MetadataError:
        pass

    try:
        structured_pages.update(f"pub-{slug}" for slug in load_publication_metadata(root).keys())
    except MetadataError:
        pass

    for path in sorted(root.glob("*.dj")):
        try:
            source = read_page_source(path.stem, root)
        except PageSourceError:
            continue

        if source.is_draft:
            continue

        if publication_slug(path.stem) is not None:
            if f"pub-{publication_slug(path.stem)}" in structured_pages:
                continue
            warnings.append(f"{path.name}: missing structured metadata entry")
            continue

        if path.stem in structured_pages:
            continue
        try:
            if load_front_matter_general_metadata(path.stem, root) is not None:
                continue
        except MetadataError:
            continue
        warnings.append(f"{path.name}: missing structured metadata entry")

    return warnings


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

    placeholder_issues = find_placeholder_issues(root)
    broken_link_issues = find_broken_link_issues(root)
    legacy_metadata_issues = find_legacy_metadata_issues(root)
    general_page_metadata_issues = validate_general_page_metadata(root)
    publication_metadata_issues = validate_publication_metadata(root)
    missing_metadata_warnings = find_missing_metadata_warnings(root)

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
    if general_page_metadata_issues:
        print_section(
            "ERROR: found invalid page metadata source",
            general_page_metadata_issues,
        )
    if publication_metadata_issues:
        print_section(
            "ERROR: found invalid publication metadata source",
            publication_metadata_issues,
        )
    if missing_metadata_warnings:
        print_section("WARNING: missing page metadata", missing_metadata_warnings)

    return 1 if (
        placeholder_issues
        or broken_link_issues
        or legacy_metadata_issues
        or general_page_metadata_issues
        or publication_metadata_issues
    ) else 0


if __name__ == "__main__":
    sys.exit(main())
