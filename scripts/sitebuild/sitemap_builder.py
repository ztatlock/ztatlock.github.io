"""Route-driven sitemap generation for preview builds."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable
from xml.sax.saxutils import escape as xml_escape

from .route_model import Route


@dataclass(frozen=True)
class SitemapEntry:
    public_url: str
    canonical_url: str
    lastmod: str


def route_is_sitemap_entry(route: Route) -> bool:
    if route.kind in {"ordinary_page", "publication_page"}:
        return not route.is_draft
    if route.kind != "static_file":
        return False
    return route.output_relpath.endswith(".html") or route.output_relpath.endswith(".pdf")


def _git_lastmod(root: Path, source_paths: tuple[Path, ...]) -> str:
    relative_paths = [path.relative_to(root).as_posix() for path in source_paths]
    completed = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%cs", "--", *relative_paths],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def build_sitemap_entries(
    routes: tuple[Route, ...],
    *,
    root: Path,
    lastmod_lookup: Callable[[Path, tuple[Path, ...]], str] | None = None,
    today: str | None = None,
) -> tuple[SitemapEntry, ...]:
    lookup = lastmod_lookup or _git_lastmod
    fallback_today = today or date.today().isoformat()
    entries: list[SitemapEntry] = []
    for route in routes:
        if not route_is_sitemap_entry(route):
            continue
        lastmod = lookup(root, route.source_paths) or fallback_today
        entries.append(
            SitemapEntry(
                public_url=route.public_url,
                canonical_url=route.canonical_url,
                lastmod=lastmod,
            )
        )
    return tuple(entries)


def render_sitemap_txt(entries: tuple[SitemapEntry, ...]) -> str:
    return "".join(f"{entry.canonical_url}\n" for entry in entries)


def render_sitemap_xml(entries: tuple[SitemapEntry, ...]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in entries:
        lines.extend(
            [
                "<url>",
                f"  <loc>{xml_escape(entry.canonical_url)}</loc>",
                f"  <lastmod>{xml_escape(entry.lastmod)}</lastmod>",
                "</url>",
            ]
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"
