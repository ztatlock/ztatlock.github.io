"""Config-driven source validation for the new build path."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.publication_record import EXTRA_CONTENT_NAME, publication_page_path
from scripts.page_metadata import (
    validate_general_page_metadata,
    validate_publication_record_metadata,
)

from .site_config import SiteConfig

LEGACY_PUBLICATION_LINK_RE = re.compile(r"\b(pub-\d{4}[-a-z0-9]*\.html)\b")


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


def _find_legacy_publication_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in sorted(config.page_source_dir.glob("*.dj")):
        issues.extend(_legacy_publication_link_issues(path))
    for path in sorted(config.publications_dir.glob(f"*/{EXTRA_CONTENT_NAME}")):
        issues.extend(_legacy_publication_link_issues(path))
    return issues


def find_source_issues(config: SiteConfig) -> list[str]:
    return validate_general_page_metadata(
        config.repo_root,
        page_source_dir=config.page_source_dir,
        static_source_dir=config.static_source_dir,
    ) + validate_publication_record_metadata(
        config.repo_root,
        publications_dir=config.publications_dir,
        static_source_dir=config.static_source_dir,
    ) + _find_legacy_publication_link_issues(
        config
    )
