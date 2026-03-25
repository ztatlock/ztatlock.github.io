"""Discover routes from the configured source layout."""

from __future__ import annotations

from pathlib import Path

from scripts.page_source import DRAFT_HEADING_RE
from scripts.publication_index import publications_index_path
from scripts.publication_record import (
    EXTRA_CONTENT_NAME,
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    publication_assets,
    load_publication_record,
    publication_dir,
    publication_record_path,
)
from scripts.service_record import SERVICE_DATA_NAME, service_index_path
from scripts.student_record import STUDENTS_DATA_NAME, students_index_path
from scripts.teaching_record import TEACHING_DATA_NAME, teaching_index_path
from scripts.talk_record import TALK_RECORD_NAME, discover_talk_slugs, talk_record_path
from scripts.talk_record import TALKS_INDEX_NAME, talks_index_path

from .route_model import Route, RouteModelError, canonical_url, validate_routes
from .site_config import SiteConfig

GENERATED_BUILD_OUTPUTS = frozenset({"sitemap.txt", "sitemap.xml"})


class RouteDiscoveryError(RouteModelError):
    pass


def _is_draft_page(path: Path) -> bool:
    return bool(DRAFT_HEADING_RE.search(path.read_text(encoding="utf-8")))


def _ordinary_page_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    for path in sorted(config.page_source_dir.glob("*.dj")):
        stem = path.stem

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


def _talk_collection_index_route(config: SiteConfig) -> Route | None:
    index_path = talks_index_path(config.repo_root, talks_dir=config.talks_dir)
    if not index_path.exists():
        return None

    legacy_talks_page = config.page_source_dir / "talks.dj"
    if legacy_talks_page.exists():
        raise RouteDiscoveryError(
            f"{legacy_talks_page}: talks index wrapper must live at {index_path}"
        )

    talk_record_paths = tuple(
        talk_record_path(
            config.repo_root,
            slug,
            talks_dir=config.talks_dir,
        )
        for slug in discover_talk_slugs(
            config.repo_root,
            talks_dir=config.talks_dir,
        )
        if (config.talks_dir / slug / TALK_RECORD_NAME).exists()
    )
    return Route(
        kind="talks_index_page",
        key="talks",
        source_paths=(index_path, *talk_record_paths),
        output_relpath="talks/index.html",
        public_url="/talks/",
        canonical_url=canonical_url(config.site_url, "/talks/"),
        is_draft=_is_draft_page(index_path),
    )


def _talks_index_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    talks_route = _talk_collection_index_route(config)
    if talks_route is not None:
        routes.append(talks_route)
    return routes


def _student_collection_index_route(config: SiteConfig) -> Route | None:
    index_path = students_index_path(config.repo_root, students_dir=config.students_dir)
    if not index_path.exists():
        return None

    legacy_students_page = config.page_source_dir / "students.dj"
    if legacy_students_page.exists():
        raise RouteDiscoveryError(
            f"{legacy_students_page}: students index wrapper must live at {index_path}"
        )

    source_paths = [index_path]
    students_data = config.data_dir / STUDENTS_DATA_NAME
    if students_data.exists():
        source_paths.append(students_data)

    return Route(
        kind="students_index_page",
        key="students",
        source_paths=tuple(source_paths),
        output_relpath="students/index.html",
        public_url="/students/",
        canonical_url=canonical_url(config.site_url, "/students/"),
        is_draft=_is_draft_page(index_path),
    )


def _students_index_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    students_route = _student_collection_index_route(config)
    if students_route is not None:
        routes.append(students_route)
    return routes


def _service_collection_index_route(config: SiteConfig) -> Route | None:
    index_path = service_index_path(config.repo_root, service_dir=config.service_dir)
    if not index_path.exists():
        return None

    legacy_service_page = config.page_source_dir / "service.dj"
    if legacy_service_page.exists():
        raise RouteDiscoveryError(
            f"{legacy_service_page}: service index wrapper must live at {index_path}"
        )

    source_paths = [index_path]
    service_data = config.data_dir / SERVICE_DATA_NAME
    if service_data.exists():
        source_paths.append(service_data)

    return Route(
        kind="service_index_page",
        key="service",
        source_paths=tuple(source_paths),
        output_relpath="service/index.html",
        public_url="/service/",
        canonical_url=canonical_url(config.site_url, "/service/"),
        is_draft=_is_draft_page(index_path),
    )


def _service_index_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    service_route = _service_collection_index_route(config)
    if service_route is not None:
        routes.append(service_route)
    return routes


def _teaching_collection_index_route(config: SiteConfig) -> Route | None:
    index_path = teaching_index_path(config.repo_root, teaching_dir=config.teaching_dir)
    if not index_path.exists():
        return None

    legacy_teaching_page = config.page_source_dir / "teaching.dj"
    if legacy_teaching_page.exists():
        raise RouteDiscoveryError(
            f"{legacy_teaching_page}: teaching index wrapper must live at {index_path}"
        )

    source_paths = [index_path]
    teaching_data = config.data_dir / TEACHING_DATA_NAME
    if teaching_data.exists():
        source_paths.append(teaching_data)

    return Route(
        kind="teaching_index_page",
        key="teaching",
        source_paths=tuple(source_paths),
        output_relpath="teaching/index.html",
        public_url="/teaching/",
        canonical_url=canonical_url(config.site_url, "/teaching/"),
        is_draft=_is_draft_page(index_path),
    )


def _teaching_index_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    teaching_route = _teaching_collection_index_route(config)
    if teaching_route is not None:
        routes.append(teaching_route)
    return routes


def _publication_collection_index_route(config: SiteConfig) -> Route | None:
    index_path = publications_index_path(
        config.repo_root,
        publications_dir=config.publications_dir,
    )
    if not index_path.exists():
        return None

    legacy_publications_page = config.page_source_dir / "publications.dj"
    if legacy_publications_page.exists():
        raise RouteDiscoveryError(
            f"{legacy_publications_page}: publications index wrapper must live at {index_path}"
        )

    return Route(
        kind="publications_index_page",
        key="publications",
        source_paths=(index_path,),
        output_relpath="pubs/index.html",
        public_url="/pubs/",
        canonical_url=canonical_url(config.site_url, "/pubs/"),
        is_draft=_is_draft_page(index_path),
    )


def _publications_index_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    publications_route = _publication_collection_index_route(config)
    if publications_route is not None:
        routes.append(publications_route)
    return routes


def _publication_page_route(
    config: SiteConfig,
    slug: str,
    *,
    record=None,
) -> Route:
    record_path = publication_record_path(config.repo_root, slug, publications_dir=config.publications_dir)
    if record is None:
        try:
            record = load_publication_record(
                config.repo_root,
                slug,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError as err:
            raise RouteDiscoveryError(str(err)) from err

    if not record.draft and not record.detail_page:
        raise RouteDiscoveryError(
            f"{record_path}: publication has no local detail page route"
        )

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
    routes: list[Route] = []
    for path in sorted(config.publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}")):
        slug = path.parent.name
        try:
            record = load_publication_record(
                config.repo_root,
                slug,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError as err:
            raise RouteDiscoveryError(str(err)) from err
        if record.draft or record.detail_page:
            routes.append(_publication_page_route(config, slug, record=record))
    return routes


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
def _recursive_static_tree_routes(config: SiteConfig) -> list[Route]:
    routes: list[Route] = []
    if not config.static_source_dir.exists():
        return routes

    for path in sorted(config.static_source_dir.rglob("*")):
        if not path.is_file():
            continue
        relpath = path.relative_to(config.static_source_dir).as_posix()
        if relpath in GENERATED_BUILD_OUTPUTS:
            raise RouteDiscoveryError(
                f"{path}: reserved static path conflicts with generated build artifact: {relpath}"
            )
        routes.append(
            _static_route(
                config,
                key=relpath,
                source_path=path,
                output_relpath=relpath,
            )
        )
    return routes


def _static_routes(config: SiteConfig) -> list[Route]:
    return _recursive_static_tree_routes(config)


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
    talks_index_routes = _talks_index_routes(config)
    service_index_routes = _service_index_routes(config)
    students_index_routes = _students_index_routes(config)
    teaching_index_routes = _teaching_index_routes(config)
    publications_index_routes = _publications_index_routes(config)
    publication_routes = _publication_page_routes(config)
    page_routes = tuple(
        sorted(
            (
                *ordinary_routes,
                *talks_index_routes,
                *service_index_routes,
                *students_index_routes,
                *teaching_index_routes,
                *publications_index_routes,
                *publication_routes,
            ),
            key=lambda route: route.output_relpath,
        )
    )
    static_routes = (
        _static_routes(config)
        + _publication_asset_routes(config, page_routes)
    )
    routes = tuple(sorted((*page_routes, *static_routes), key=lambda route: route.output_relpath))
    validate_routes(routes)
    return routes
