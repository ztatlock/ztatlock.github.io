"""Shared configuration for route discovery and route-aware builds."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SITE_URL = "https://ztatlock.net"
WEBFILES_URL = "https://cs.washington.edu/homes/ztatlock/WEBFILES"


@dataclass(frozen=True)
class SiteConfig:
    repo_root: Path
    build_dir: Path
    site_url: str
    webfiles_url: str
    page_source_dir: Path
    service_dir: Path
    students_dir: Path
    teaching_dir: Path
    talks_dir: Path
    publications_dir: Path
    templates_dir: Path
    data_dir: Path
    static_source_dir: Path

    @property
    def root(self) -> Path:
        return self.repo_root

    @property
    def people_data_path(self) -> Path:
        return self.data_dir / "people.json"

    @property
    def manual_refs_path(self) -> Path:
        return self.templates_dir / "REFS"


def load_site_config(
    root: Path,
    *,
    build_dir: Path | None = None,
    page_source_dir: Path | None = None,
    service_dir: Path | None = None,
    students_dir: Path | None = None,
    teaching_dir: Path | None = None,
    talks_dir: Path | None = None,
    publications_dir: Path | None = None,
    templates_dir: Path | None = None,
    data_dir: Path | None = None,
    static_source_dir: Path | None = None,
    site_url: str = SITE_URL,
    webfiles_url: str = WEBFILES_URL,
) -> SiteConfig:
    resolved_root = root.resolve()
    return SiteConfig(
        repo_root=resolved_root,
        build_dir=(build_dir or (resolved_root / "build")).resolve(),
        site_url=site_url,
        webfiles_url=webfiles_url,
        page_source_dir=(page_source_dir or (resolved_root / "site" / "pages")).resolve(),
        service_dir=(service_dir or (resolved_root / "site" / "service")).resolve(),
        students_dir=(students_dir or (resolved_root / "site" / "students")).resolve(),
        teaching_dir=(teaching_dir or (resolved_root / "site" / "teaching")).resolve(),
        talks_dir=(talks_dir or (resolved_root / "site" / "talks")).resolve(),
        publications_dir=(publications_dir or (resolved_root / "site" / "pubs")).resolve(),
        templates_dir=(templates_dir or (resolved_root / "site" / "templates")).resolve(),
        data_dir=(data_dir or (resolved_root / "site" / "data")).resolve(),
        static_source_dir=(static_source_dir or (resolved_root / "site" / "static")).resolve(),
    )
