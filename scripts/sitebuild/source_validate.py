"""Config-driven source validation for the new build path."""

from __future__ import annotations

from scripts.page_metadata import (
    validate_general_page_metadata,
    validate_publication_record_metadata,
)

from .site_config import SiteConfig


def find_source_issues(config: SiteConfig) -> list[str]:
    return validate_general_page_metadata(
        config.repo_root,
        page_source_dir=config.page_source_dir,
        static_source_dir=config.static_source_dir,
    ) + validate_publication_record_metadata(
        config.repo_root,
        publications_dir=config.publications_dir,
        static_source_dir=config.static_source_dir,
    )
