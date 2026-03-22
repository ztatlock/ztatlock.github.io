"""Shared configuration for route discovery and preview builds."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SITE_URL = "https://ztatlock.net"
WEBFILES_URL = "https://cs.washington.edu/homes/ztatlock/WEBFILES"


@dataclass(frozen=True)
class SiteConfig:
    root: Path
    build_dir: Path
    site_url: str
    webfiles_url: str


def load_site_config(root: Path) -> SiteConfig:
    resolved_root = root.resolve()
    return SiteConfig(
        root=resolved_root,
        build_dir=resolved_root / "build",
        site_url=SITE_URL,
        webfiles_url=WEBFILES_URL,
    )
