"""Config-driven source validation for the new build path."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.publication_index import (
    PublicationIndexError,
    load_publications_index_entries,
    publications_index_path,
)
from scripts.publication_record import (
    EXTRA_CONTENT_NAME,
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    load_publication_record,
    publication_page_path,
)
from scripts.talk_record import TALKS_INDEX_NAME, find_talk_record_issues, talks_index_path
from scripts.page_metadata import (
    validate_general_source_metadata_path,
    validate_general_page_metadata,
    validate_publication_record_metadata,
)

from .site_config import SiteConfig
from .talk_projection import TALKS_LIST_PLACEHOLDER

LEGACY_PUBLICATION_LINK_RE = re.compile(r"\b(pub-\d{4}[-a-z0-9]*\.html)\b")
LEGACY_TALKS_LINK_RE = re.compile(r"\b(talks\.html)\b")
ROOT_STATIC_SOURCE_NAMES = (
    "CNAME",
    "robots.txt",
    "style.css",
    "zip-longitude.js",
)


def _legacy_publication_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    seen = sorted(set(LEGACY_PUBLICATION_LINK_RE.findall(text)))
    for target in seen:
        slug = target.removeprefix("pub-").removesuffix(".html")
        issues.append(
            f"{path}: legacy publication link should use canonical publication path: "
            f"{target} -> {publication_page_path(slug)}"
        )
    return issues


def _legacy_talks_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not LEGACY_TALKS_LINK_RE.search(text):
        return []
    return [f"{path}: legacy talks link should use canonical collection path: talks.html -> talks/"]


def _all_authored_djot_sources(config: SiteConfig) -> list[Path]:
    paths = list(sorted(config.page_source_dir.glob("*.dj")))
    talks_index = talks_index_path(config.repo_root, talks_dir=config.talks_dir)
    if talks_index.exists():
        paths.append(talks_index)
    paths.extend(sorted(config.publications_dir.glob(f"*/{EXTRA_CONTENT_NAME}")))
    paths.extend(sorted(config.talks_dir.glob(f"*/{EXTRA_CONTENT_NAME}")))
    return paths


def _find_legacy_publication_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_publication_link_issues(path))
    return issues


def _find_legacy_talks_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_talks_link_issues(path))
    return issues


def _find_root_layout_drift_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in sorted(config.repo_root.glob("*.dj")):
        issues.append(f"{path}: authored Djot source must live under site/pages/")
    for path in sorted(config.repo_root.glob("*.html")):
        issues.append(f"{path}: authored static HTML must live under site/static/")
    for path in sorted(config.repo_root.glob("*.txt")):
        if path.name == "sitemap.txt":
            issues.append(f"{path}: generated sitemap belongs only under build/")
            continue
        if path.name in ROOT_STATIC_SOURCE_NAMES:
            continue
        issues.append(f"{path}: static text assets must live under site/static/")
    if (config.repo_root / "sitemap.xml").exists():
        issues.append(f"{config.repo_root / 'sitemap.xml'}: generated sitemap belongs only under build/")
    for name in ROOT_STATIC_SOURCE_NAMES:
        path = config.repo_root / name
        if path.exists():
            issues.append(f"{path}: static assets must live under site/static/")
    if (config.repo_root / "img").exists():
        issues.append(f"{config.repo_root / 'img'}: shared images must live under site/static/img/")
    if (config.repo_root / "pubs").exists():
        issues.append(f"{config.repo_root / 'pubs'}: publication bundles must live under site/pubs/")
    if (config.repo_root / "templates").exists():
        issues.append(f"{config.repo_root / 'templates'}: templates must live under site/templates/")
    return issues


def _find_talk_projection_issues(config: SiteConfig) -> list[str]:
    if not config.talks_dir.exists():
        return []

    talk_dirs = [path for path in sorted(config.talks_dir.iterdir()) if path.is_dir()]
    if not talk_dirs:
        return []

    talks_page = talks_index_path(config.repo_root, talks_dir=config.talks_dir)
    issues: list[str] = []
    if not talks_page.exists():
        return [f"{talks_page}: talks index page is required when talk bundles exist"]

    legacy_talks_page = config.page_source_dir / "talks.dj"
    if legacy_talks_page.exists():
        issues.append(f"{legacy_talks_page}: talks index wrapper must move to {talks_page}")

    text = talks_page.read_text(encoding="utf-8")
    if TALKS_LIST_PLACEHOLDER not in text:
        issues.append(f"{talks_page}: talks index page must contain {TALKS_LIST_PLACEHOLDER}")

    issues.extend(
        validate_general_source_metadata_path(
            talks_page,
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
    )
    return issues


def _find_publication_index_coverage_issues(config: SiteConfig) -> list[str]:
    index_path = publications_index_path(
        config.repo_root,
        page_source_dir=config.page_source_dir,
    )
    non_draft_records_by_slug: dict[str, object] = {}
    for path in sorted(config.publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}")):
        slug = path.parent.name
        try:
            record = load_publication_record(
                config.repo_root,
                slug,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError:
            continue
        if not record.draft:
            non_draft_records_by_slug[slug] = record

    if not non_draft_records_by_slug and not index_path.exists():
        return []

    if not index_path.exists():
        return [f"{index_path}: publications index page is required when publication bundles exist"]

    try:
        entries = load_publications_index_entries(
            config.repo_root,
            page_source_dir=config.page_source_dir,
        )
    except PublicationIndexError as err:
        return [str(err)]

    issues: list[str] = []
    index_entries_by_slug = {entry.slug: entry for entry in entries}

    for entry in entries:
        record = non_draft_records_by_slug.get(entry.slug)
        if record is None:
            issues.append(
                f"{index_path}: indexed publication missing canonical bundle: {entry.slug}"
            )
            continue
        if record.listing_group != entry.listing_group:
            issues.append(
                f"{index_path}: listing_group mismatch for {entry.slug}: "
                f"index={entry.listing_group}, bundle={record.listing_group}"
            )

    for slug in sorted(non_draft_records_by_slug):
        if slug not in index_entries_by_slug:
            issues.append(
                f"{index_path}: non-draft publication bundle missing from publications index: {slug}"
            )
    return issues


def find_source_issues(config: SiteConfig) -> list[str]:
    return (
        validate_general_page_metadata(
            config.repo_root,
            page_source_dir=config.page_source_dir,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
        + validate_publication_record_metadata(
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
        + find_talk_record_issues(
            config.repo_root,
            talks_dir=config.talks_dir,
        )
        + _find_talk_projection_issues(config)
        + _find_publication_index_coverage_issues(config)
        + _find_legacy_publication_link_issues(config)
        + _find_legacy_talks_link_issues(config)
        + _find_root_layout_drift_issues(config)
    )
