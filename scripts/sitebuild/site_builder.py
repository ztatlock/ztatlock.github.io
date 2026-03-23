"""Build the authoritative site artifact into build/."""

from __future__ import annotations

import shutil
from pathlib import Path

from .djot_refs import load_and_render_site_refs
from .page_renderer import PageRenderError, render_page_html
from .route_discovery import discover_routes
from .route_model import Route, normalize_output_relpath
from .site_config import SiteConfig
from .sitemap_builder import build_sitemap_entries, render_sitemap_txt, render_sitemap_xml

SiteBuildError = PageRenderError


def _route_aliases(routes: tuple[Route, ...]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for route in routes:
        aliases[route.output_relpath] = route.public_url
        if route.kind == "ordinary_page" and route.key == "index":
            aliases["index.html"] = route.public_url
    return aliases


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _copy_static_route(route: Route, *, config: SiteConfig) -> None:
    destination = config.build_dir / normalize_output_relpath(route.output_relpath)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(route.source_paths[0], destination)


def build_site(config: SiteConfig) -> tuple[Route, ...]:
    routes = discover_routes(config)

    if config.build_dir.exists():
        shutil.rmtree(config.build_dir)
    config.build_dir.mkdir(parents=True)

    refs_text = load_and_render_site_refs(
        people_path=config.people_data_path,
        refs_path=config.manual_refs_path,
    )
    aliases = _route_aliases(routes)

    for route in routes:
        if route.kind == "static_file":
            _copy_static_route(route, config=config)
            continue
        if route.is_draft:
            continue
        html_text = render_page_html(
            route.kind,
            route.key,
            canonical_url=route.canonical_url,
            refs_text=refs_text,
            root=config.repo_root,
            site_url=config.site_url,
            webfiles_url=config.webfiles_url,
            aliases=aliases,
            page_source_dir=config.page_source_dir,
            publications_dir=config.publications_dir,
            templates_dir=config.templates_dir,
        )
        _write_text(config.build_dir / normalize_output_relpath(route.output_relpath), html_text)

    sitemap_entries = build_sitemap_entries(routes, root=config.repo_root)
    _write_text(config.build_dir / "sitemap.txt", render_sitemap_txt(sitemap_entries))
    _write_text(config.build_dir / "sitemap.xml", render_sitemap_xml(sitemap_entries))

    return routes
