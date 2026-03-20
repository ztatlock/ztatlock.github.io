#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from page_metadata import (
    MetadataError,
    load_general_page_metadata,
    load_publication_metadata,
    validate_general_page_metadata,
    validate_publication_metadata,
)

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
META_ATTR_RE = re.compile(r'([A-Za-z_:][-A-Za-z0-9_:]*)="([^"]*)"')
REQUIRED_META_FIELDS = {
    "description",
    "og:description",
    "og:image",
    "og:title",
    "og:type",
    "og:url",
    "twitter:card",
    "twitter:description",
    "twitter:domain",
    "twitter:image",
    "twitter:title",
    "twitter:url",
}


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


def canonical_url(path: Path) -> str:
    if path.stem == "index":
        return "https://ztatlock.net/"
    return f"https://ztatlock.net/{path.stem}.html"


def find_metadata_issues(root: Path) -> list[str]:
    issues: list[str] = []

    for path in sorted(root.glob("*.meta")):
        fields: dict[str, str] = {}
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("<!--"):
                continue
            if not stripped.startswith("<meta "):
                continue
            if not stripped.endswith(">"):
                issues.append(f"{path.name}:{lineno}: malformed meta tag")
                continue

            body = stripped[len("<meta ") : -1].strip()
            matches = list(META_ATTR_RE.finditer(body))
            residue = META_ATTR_RE.sub("", body).strip()
            if residue:
                issues.append(f"{path.name}:{lineno}: malformed meta attributes: {residue}")

            attrs = {match.group(1): match.group(2) for match in matches}
            key = attrs.get("name") or attrs.get("property")
            if not key:
                issues.append(f"{path.name}:{lineno}: missing meta name/property")
                continue
            if "content" not in attrs or not attrs["content"]:
                issues.append(f"{path.name}:{lineno}: missing meta content for {key}")
                continue
            if key in fields:
                issues.append(f"{path.name}:{lineno}: duplicate meta entry for {key}")
                continue
            fields[key] = attrs["content"]

        missing = sorted(REQUIRED_META_FIELDS - fields.keys())
        if missing:
            issues.append(f"{path.name}: missing required fields: {', '.join(missing)}")
            continue

        expected = canonical_url(path)
        if fields["og:url"] != expected:
            issues.append(f"{path.name}: og:url should be {expected}")
        if fields["twitter:url"] != expected:
            issues.append(f"{path.name}: twitter:url should be {expected}")
        if fields["twitter:domain"] != "ztatlock.net":
            issues.append(f"{path.name}: twitter:domain should be ztatlock.net")
        if fields["og:type"] != "website":
            issues.append(f"{path.name}: og:type should be website")
        if fields["twitter:card"] != "summary_large_image":
            issues.append(f"{path.name}: twitter:card should be summary_large_image")

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
        text = path.read_text(encoding="utf-8")
        if re.search(r"^# DRAFT$", text, re.MULTILINE):
            continue
        if path.stem in structured_pages:
            continue
        if not (root / f"{path.stem}.meta").exists():
            warnings.append(f"{path.name}: missing metadata source")

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
    metadata_issues = find_metadata_issues(root)
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
    if metadata_issues:
        print_section("ERROR: found invalid page metadata", metadata_issues)
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
        or metadata_issues
        or general_page_metadata_issues
        or publication_metadata_issues
    ) else 0


if __name__ == "__main__":
    sys.exit(main())
