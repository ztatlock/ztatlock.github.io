#!/usr/bin/env python3

from __future__ import annotations

import html
from pathlib import Path
from urllib.parse import urlparse

from scripts.page_source import (
    collaborators_index_source_path,
    cv_index_source_path,
    funding_index_source_path,
    PageSourceError,
    page_path,
    publications_index_source_path,
    service_index_source_path,
    students_index_source_path,
    teaching_index_source_path,
    read_page_source,
    read_source_path,
    talks_index_source_path,
)
from scripts.publication_record import (
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    default_publications_dir,
    load_publication_record,
    publication_metadata_image_path,
    publication_page_path,
)
from scripts.sitebuild.site_config import SITE_URL

GENERAL_ALLOWED_FIELDS = {"description", "share_description", "image_path", "title"}


class MetadataError(ValueError):
    pass


def canonical_url(page_stem: str, *, site_url: str = SITE_URL) -> str:
    if page_stem == "index":
        return f"{site_url}/"
    return f"{site_url}/{page_stem}.html"


def default_page_image_path() -> str:
    return "img/favicon-meta.png"


def absolute_url(path_or_url: str, *, site_url: str = SITE_URL) -> str:
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return f"{site_url}/{path_or_url.lstrip('/')}"


def site_domain(*, site_url: str = SITE_URL) -> str:
    parsed = urlparse(site_url)
    if parsed.netloc:
        return parsed.netloc
    if parsed.path:
        return parsed.path.strip("/").split("/", 1)[0]
    return site_url


def escape_content(value: str) -> str:
    return html.escape(value, quote=False).replace('"', "&quot;")


def normalize_general_metadata_entry(
    entry: dict[str, object],
    *,
    context: str,
) -> dict[str, str]:
    unknown_fields = sorted(set(entry) - GENERAL_ALLOWED_FIELDS)
    if unknown_fields:
        raise MetadataError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    description = entry.get("description")
    if not isinstance(description, str) or not description.strip():
        raise MetadataError(f"{context}: missing description")

    share_description = entry.get("share_description")
    if share_description is not None and not isinstance(share_description, str):
        raise MetadataError(f"{context}: share_description must be a string or null")

    image_path = entry.get("image_path")
    if image_path is not None and not isinstance(image_path, str):
        raise MetadataError(f"{context}: image_path must be a string or null")

    title = entry.get("title")
    if title is not None and not isinstance(title, str):
        raise MetadataError(f"{context}: title must be a string or null")

    return {
        "description": description.strip(),
        "share_description": (share_description or "").strip(),
        "image_path": (image_path or "").strip(),
        "title": (title or "").strip(),
    }


def render_metadata_block(
    *,
    title: str,
    description: str,
    share_description: str,
    image_path: str,
    url: str,
    site_url: str = SITE_URL,
) -> str:
    escaped_title = escape_content(title)
    escaped_description = escape_content(description)
    escaped_share_description = escape_content(share_description)
    escaped_url = escape_content(url)
    escaped_image = escape_content(absolute_url(image_path, site_url=site_url))

    lines = [
        f'<meta name="description" content="{escaped_description}">',
        "",
        "<!-- OpenGraph -->",
        f'<meta property="og:url" content="{escaped_url}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{escaped_title}">',
        f'<meta property="og:description" content="{escaped_share_description}">',
        f'<meta property="og:image" content="{escaped_image}">',
        "",
        "<!-- Twitter -->",
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta property="twitter:domain" content="{escape_content(site_domain(site_url=site_url))}">',
        f'<meta property="twitter:url" content="{escaped_url}">',
        f'<meta name="twitter:title" content="{escaped_title}">',
        f'<meta name="twitter:description" content="{escaped_share_description}">',
        f'<meta name="twitter:image" content="{escaped_image}">',
        "",
    ]
    return "\n".join(lines)


def publication_canonical_url(slug: str, *, site_url: str = SITE_URL) -> str:
    return absolute_url(publication_page_path(slug), site_url=site_url)


def render_publication_meta(
    slug: str,
    title: str,
    root: Path,
    *,
    site_url: str = SITE_URL,
) -> str:
    return render_publication_meta_for_slug(
        slug,
        title,
        publication_canonical_url(slug, site_url=site_url),
        root,
        site_url=site_url,
    )


def render_publication_meta_for_slug(
    slug: str,
    title: str,
    url: str,
    root: Path,
    *,
    publications_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    try:
        record = load_publication_record(
            root,
            slug,
            publications_dir=publications_dir,
        )
    except PublicationRecordError as err:
        raise MetadataError(str(err)) from err

    description = record.description
    share_description = record.share_description or description
    image_path = publication_metadata_image_path(
        root,
        record,
        publications_dir=publications_dir,
    )
    return render_metadata_block(
        title=title,
        description=description,
        share_description=share_description,
        image_path=image_path,
        url=url,
        site_url=site_url,
    )


def load_front_matter_general_metadata(
    page_stem: str,
    root: Path,
    *,
    page_source_dir: Path | None = None,
) -> dict[str, str] | None:
    try:
        source = read_page_source(page_stem, root, page_source_dir=page_source_dir)
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if not source.front_matter:
        return None
    return normalize_general_metadata_entry(
        source.front_matter,
        context=f"{(page_source_dir or root) / f'{page_stem}.dj'}: front matter",
    )


def load_front_matter_general_metadata_for_path(path: Path) -> dict[str, str] | None:
    try:
        source = read_source_path(path)
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if not source.front_matter:
        return None
    return normalize_general_metadata_entry(
        source.front_matter,
        context=f"{path}: front matter",
    )


def render_general_page_meta(
    page_stem: str,
    title: str,
    root: Path,
    *,
    site_url: str = SITE_URL,
) -> str:
    return render_general_page_meta_for_url(
        page_stem,
        title,
        canonical_url(page_stem, site_url=site_url),
        root,
        site_url=site_url,
    )


def render_general_page_meta_for_url(
    page_stem: str,
    title: str,
    url: str,
    root: Path,
    *,
    page_source_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    actual_page_source_dir = page_source_dir or root
    return render_general_source_meta_for_url(
        actual_page_source_dir / f"{page_stem}.dj",
        title,
        url,
        site_url=site_url,
    )


def render_general_source_meta_for_url(
    source_path: Path,
    title: str,
    url: str,
    *,
    site_url: str = SITE_URL,
) -> str:
    row = load_front_matter_general_metadata_for_path(
        source_path,
    )
    if row is None:
        raise MetadataError(f"Missing front matter metadata for {source_path}")

    description = row["description"]
    share_description = row["share_description"] or description
    image_path = row["image_path"] or default_page_image_path()
    rendered_title = row["title"] or title
    return render_metadata_block(
        title=rendered_title,
        description=description,
        share_description=share_description,
        image_path=image_path,
        url=url,
        site_url=site_url,
    )


def render_page_meta(
    page_stem: str,
    title: str,
    root: Path,
    *,
    site_url: str = SITE_URL,
) -> str:
    return render_page_meta_for_url(
        page_stem,
        title,
        canonical_url=canonical_url(page_stem, site_url=site_url),
        root=root,
        site_url=site_url,
    )


def render_page_meta_for_url(
    page_stem: str,
    title: str,
    *,
    canonical_url: str,
    root: Path,
    page_source_dir: Path | None = None,
    publications_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_route_meta_for_url(
        "ordinary_page",
        page_stem,
        title,
        canonical_url=canonical_url,
        root=root,
        page_source_dir=page_source_dir,
        publications_dir=publications_dir,
        site_url=site_url,
    )


def render_ordinary_page_meta_for_url(
    page_stem: str,
    title: str,
    *,
    canonical_url: str,
    root: Path,
    page_source_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    actual_page_source_dir = page_source_dir or root
    return render_djot_source_meta_for_url(
        actual_page_source_dir / f"{page_stem}.dj",
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_talks_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    talks_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        talks_index_source_path(
            root,
            talks_dir=talks_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_cv_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    cv_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        cv_index_source_path(
            root,
            cv_dir=cv_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_collaborators_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    collaborators_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        collaborators_index_source_path(
            root,
            collaborators_dir=collaborators_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_students_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    students_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        students_index_source_path(
            root,
            students_dir=students_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_service_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    service_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        service_index_source_path(
            root,
            service_dir=service_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_funding_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    funding_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        funding_index_source_path(
            root,
            funding_dir=funding_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_teaching_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    teaching_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        teaching_index_source_path(
            root,
            teaching_dir=teaching_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_publications_index_meta_for_url(
    title: str,
    *,
    canonical_url: str,
    root: Path,
    publications_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    return render_djot_source_meta_for_url(
        publications_index_source_path(
            root,
            publications_dir=publications_dir,
        ),
        title,
        canonical_url=canonical_url,
        site_url=site_url,
    )


def render_djot_source_meta_for_url(
    source_path: Path,
    title: str,
    *,
    canonical_url: str,
    site_url: str = SITE_URL,
) -> str:
    try:
        source = read_source_path(source_path)
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if source.is_draft:
        if source.front_matter:
            return render_general_source_meta_for_url(
                source_path,
                title,
                canonical_url,
                site_url=site_url,
            )
        return ""

    if source.front_matter:
        return render_general_source_meta_for_url(
            source_path,
            title,
            canonical_url,
            site_url=site_url,
        )
    raise MetadataError(f"Missing front matter metadata for {source_path}")


def render_route_meta_for_url(
    route_kind: str,
    route_key: str,
    title: str,
    *,
    canonical_url: str,
    root: Path,
    page_source_dir: Path | None = None,
    collaborators_dir: Path | None = None,
    cv_dir: Path | None = None,
    funding_dir: Path | None = None,
    service_dir: Path | None = None,
    students_dir: Path | None = None,
    teaching_dir: Path | None = None,
    talks_dir: Path | None = None,
    publications_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    if route_kind == "ordinary_page":
        return render_ordinary_page_meta_for_url(
            route_key,
            title,
            canonical_url=canonical_url,
            root=root,
            page_source_dir=page_source_dir,
            site_url=site_url,
        )
    if route_kind == "collaborators_index_page":
        if route_key != "collaborators":
            raise MetadataError(f"unsupported collaborators index route key: {route_key}")
        return render_collaborators_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            collaborators_dir=collaborators_dir,
            site_url=site_url,
        )
    if route_kind == "cv_index_page":
        if route_key != "cv":
            raise MetadataError(f"unsupported CV index route key: {route_key}")
        return render_cv_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            cv_dir=cv_dir,
            site_url=site_url,
        )
    if route_kind == "talks_index_page":
        if route_key != "talks":
            raise MetadataError(f"unsupported talks index route key: {route_key}")
        return render_talks_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            talks_dir=talks_dir,
            site_url=site_url,
        )
    if route_kind == "service_index_page":
        if route_key != "service":
            raise MetadataError(f"unsupported service index route key: {route_key}")
        return render_service_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            service_dir=service_dir,
            site_url=site_url,
        )
    if route_kind == "funding_index_page":
        if route_key != "funding":
            raise MetadataError(f"unsupported funding index route key: {route_key}")
        return render_funding_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            funding_dir=funding_dir,
            site_url=site_url,
        )
    if route_kind == "students_index_page":
        if route_key != "students":
            raise MetadataError(f"unsupported students index route key: {route_key}")
        return render_students_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            students_dir=students_dir,
            site_url=site_url,
        )
    if route_kind == "teaching_index_page":
        if route_key != "teaching":
            raise MetadataError(f"unsupported teaching index route key: {route_key}")
        return render_teaching_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            teaching_dir=teaching_dir,
            site_url=site_url,
        )
    if route_kind == "publications_index_page":
        if route_key != "publications":
            raise MetadataError(f"unsupported publications index route key: {route_key}")
        return render_publications_index_meta_for_url(
            title,
            canonical_url=canonical_url,
            root=root,
            publications_dir=publications_dir,
            site_url=site_url,
        )
    if route_kind == "publication_page":
        try:
            record = load_publication_record(
                root,
                route_key,
                publications_dir=publications_dir,
            )
        except PublicationRecordError as err:
            raise MetadataError(str(err)) from err
        if record.draft:
            return ""
        if not record.detail_page:
            raise MetadataError(
                f"{route_key}: publication has no local detail page metadata"
            )
        return render_publication_meta_for_slug(
            route_key,
            title,
            canonical_url,
            root,
            publications_dir=publications_dir,
            site_url=site_url,
        )
    raise MetadataError(f"unsupported route kind for metadata rendering: {route_kind}")


def resolve_public_asset_source_path(
    path_or_url: str,
    *,
    root: Path,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> Path | None:
    if path_or_url.startswith(("http://", "https://")):
        return None

    normalized = path_or_url.lstrip("/")
    if normalized.startswith("pubs/"):
        actual_publications_dir = publications_dir or default_publications_dir(root)
        return actual_publications_dir / normalized.removeprefix("pubs/")

    actual_static_source_dir = static_source_dir or (root / "site" / "static")
    return actual_static_source_dir / normalized


def validate_general_page_metadata(
    root: Path,
    *,
    page_source_dir: Path | None = None,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    actual_page_source_dir = page_source_dir or root
    page_stem_set = {path.stem for path in actual_page_source_dir.glob("*.dj")}

    for stem in sorted(page_stem_set):
        try:
            source = read_page_source(stem, root, page_source_dir=actual_page_source_dir)
        except PageSourceError as err:
            issues.append(str(err))
            continue

        if source.front_matter:
            try:
                row = normalize_general_metadata_entry(
                    source.front_matter,
                    context=f"{actual_page_source_dir / f'{stem}.dj'}: front matter",
                )
            except MetadataError as err:
                issues.append(str(err))
                continue

            image_path = row["image_path"] or default_page_image_path()
            source_image_path = resolve_public_asset_source_path(
                image_path,
                root=root,
                publications_dir=publications_dir,
                static_source_dir=static_source_dir,
            )
            if source_image_path is not None and not source_image_path.exists():
                issues.append(f"{actual_page_source_dir / f'{stem}.dj'}: image path does not exist: {image_path}")
            continue

        if source.is_draft:
            continue
        issues.append(f"{actual_page_source_dir / f'{stem}.dj'}: missing front matter metadata")

    return issues


def validate_general_source_metadata_path(
    path: Path,
    root: Path,
    *,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> list[str]:
    issues: list[str] = []

    try:
        source = read_source_path(path)
    except PageSourceError as err:
        return [str(err)]

    if source.front_matter:
        try:
            row = normalize_general_metadata_entry(
                source.front_matter,
                context=f"{path}: front matter",
            )
        except MetadataError as err:
            return [str(err)]

        image_path = row["image_path"] or default_page_image_path()
        source_image_path = resolve_public_asset_source_path(
            image_path,
            root=root,
            publications_dir=publications_dir,
            static_source_dir=static_source_dir,
        )
        if source_image_path is not None and not source_image_path.exists():
            issues.append(f"{path}: image path does not exist: {image_path}")
        return issues

    if not source.is_draft:
        issues.append(f"{path}: missing front matter metadata")
    return issues


def validate_publication_record_metadata(
    root: Path,
    *,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    actual_publications_dir = publications_dir or default_publications_dir(root)

    for path in sorted(actual_publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}")):
        slug = path.parent.name
        try:
            record = load_publication_record(
                root,
                slug,
                publications_dir=actual_publications_dir,
            )
        except PublicationRecordError as err:
            issues.append(str(err))
            continue

        if record.draft:
            continue
        if not record.detail_page:
            continue

        try:
            image_path = publication_metadata_image_path(
                root,
                record,
                publications_dir=actual_publications_dir,
            )
        except PublicationRecordError as err:
            issues.append(str(err))
            continue

        source_image_path = resolve_public_asset_source_path(
            image_path,
            root=root,
            publications_dir=actual_publications_dir,
            static_source_dir=static_source_dir,
        )
        if source_image_path is not None and not source_image_path.exists():
            issues.append(f"{path}: image path does not exist: {image_path}")

    return issues


def validate_publication_metadata(
    root: Path,
    *,
    page_source_dir: Path | None = None,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> list[str]:
    return validate_publication_record_metadata(
        root,
        publications_dir=publications_dir,
        static_source_dir=static_source_dir,
    )
