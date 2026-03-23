"""Discover future-oriented preview routes from the configured source layout."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.publication_record import (
    EXTRA_CONTENT_NAME,
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    publication_assets,
    load_publication_record,
    publication_dir,
    publication_record_path,
    publication_slug,
)

from .route_model import Route, RouteModelError, canonical_url, validate_routes
from .site_config import SiteConfig

DRAFT_HEADING_RE = re.compile(r"^# DRAFT$", re.MULTILINE)
TOP_LEVEL_STATIC_FILENAMES = ("CNAME", "robots.txt", "style.css", "zip-longitude.js")


class RouteDiscoveryError(RouteModelError):
    pass


def _is_draft_page(path: Path) -> bool:
    return bool(DRAFT_HEADING_RE.search(path.read_text(encoding="utf-8")))


def _ordinary_page_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    for path in sorted(config.page_source_dir.glob("*.dj")):
        stem = path.stem
        if publication_slug(stem) is not None:
            continue

        public_url = "/" if stem == "index" else f"/{stem}.html"
        routes.append(
            Route(
                kind="ordinary_page",
                key=stem,
                source_paths=(path,),
                output_relpath=f"{stem}.html",
                public_url=public_url,
                canonical_url=canonical_url(config.site_url, public_url),
                is_draft=_is_draft_page(path),
            )
        )
    return routes


def _publication_page_route(config: SiteConfig, slug: str) -> Route:
    record_path = publication_record_path(config.repo_root, slug, publications_dir=config.publications_dir)
    try:
        record = load_publication_record(
            config.repo_root,
            slug,
            publications_dir=config.publications_dir,
        )
    except PublicationRecordError as err:
        raise RouteDiscoveryError(str(err)) from err

    pub_dir = publication_dir(
        config.repo_root,
        slug,
        publications_dir=config.publications_dir,
    )
    extra_path = pub_dir / EXTRA_CONTENT_NAME
    public_url = f"/pubs/{slug}/"
    source_paths: tuple[Path, ...]
    if record.draft:
        ordered_paths: list[Path] = [record_path]
        if extra_path.exists():
            ordered_paths.append(extra_path)
        source_paths = tuple(ordered_paths)
    else:
        try:
            assets = publication_assets(
                config.repo_root,
                slug,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError as err:
            raise RouteDiscoveryError(str(err)) from err
        ordered_paths: list[Path] = [
            record_path,
            assets.bib,
            assets.abstract,
        ]
        if assets.extra is not None:
            ordered_paths.append(assets.extra)
        source_paths = tuple(ordered_paths)
    return Route(
        kind="publication_page",
        key=slug,
        source_paths=source_paths,
        output_relpath=f"pubs/{slug}/index.html",
        public_url=public_url,
        canonical_url=canonical_url(config.site_url, public_url),
        is_draft=record.draft,
    )


def _publication_page_routes(config: SiteConfig) -> list[Route]:
    records = sorted(config.publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}"))
    return [_publication_page_route(config, path.parent.name) for path in records]


def _static_route(
    config: SiteConfig,
    *,
    key: str,
    source_path: Path,
    output_relpath: str,
) -> Route:
    public_url = f"/{output_relpath}"
    return Route(
        kind="static_file",
        key=key,
        source_paths=(source_path,),
        output_relpath=output_relpath,
        public_url=public_url,
        canonical_url=canonical_url(config.site_url, public_url),
        is_draft=False,
    )


def _top_level_static_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []

    for name in TOP_LEVEL_STATIC_FILENAMES:
        path = config.static_source_dir / name
        if path.exists():
            routes.append(
                _static_route(config, key=name, source_path=path, output_relpath=name)
            )

    for path in sorted(config.static_source_dir.glob("*.txt")):
        if path.name == "sitemap.txt":
            continue
        if path.name in TOP_LEVEL_STATIC_FILENAMES:
            continue
        routes.append(
            _static_route(config, key=path.name, source_path=path, output_relpath=path.name)
        )

    generated_stems = {path.stem for path in config.page_source_dir.glob("*.dj")}
    for path in sorted(config.static_source_dir.glob("*.html")):
        if path.stem in generated_stems:
            continue
        routes.append(
            _static_route(config, key=path.name, source_path=path, output_relpath=path.name)
        )

    img_dir = config.shared_img_dir
    if img_dir.exists():
        for path in sorted(img_dir.rglob("*")):
            if not path.is_file():
                continue
            relpath = f"img/{path.relative_to(img_dir).as_posix()}"
            routes.append(_static_route(config, key=relpath, source_path=path, output_relpath=relpath))

    return routes


def _publication_asset_routes(config: SiteConfig, page_routes: tuple[Route, ...]) -> list[Route]:
    routes: list[Route] = []
    seen: set[str] = set()

    for route in page_routes:
        if route.kind != "publication_page" or route.is_draft:
            continue

        slug = route.key
        try:
            assets = publication_assets(
                config.repo_root,
                slug,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError as err:
            raise RouteDiscoveryError(str(err)) from err

        asset_paths = [
            assets.paper,
            assets.bib,
            assets.absimg,
        ]
        if assets.metaimg is not None:
            asset_paths.append(assets.metaimg)
        if assets.slides is not None:
            asset_paths.append(assets.slides)
        if assets.poster is not None:
            asset_paths.append(assets.poster)

        for path in asset_paths:
            relpath = f"pubs/{path.relative_to(config.publications_dir).as_posix()}"
            if relpath in seen:
                continue
            seen.add(relpath)
            routes.append(_static_route(config, key=relpath, source_path=path, output_relpath=relpath))

    return routes


def discover_routes(config: SiteConfig) -> tuple[Route, ...]:
    ordinary_routes = _ordinary_page_routes(config)
    publication_routes = _publication_page_routes(config)
    page_routes = tuple(sorted((*ordinary_routes, *publication_routes), key=lambda route: route.output_relpath))
    static_routes = (
        _top_level_static_routes(config)
        + _publication_asset_routes(config, page_routes)
    )
    routes = tuple(sorted((*page_routes, *static_routes), key=lambda route: route.output_relpath))
    validate_routes(routes)
    return routes
