#!/usr/bin/env python3

from __future__ import annotations

import html
from pathlib import Path

from scripts.page_source import PageSourceError, read_page_source
from scripts.publication_record import (
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    load_publication_record,
    load_optional_publication_record,
    publication_metadata_image_path,
    publication_slug,
)

SITE_URL = "https://ztatlock.net"
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
        '<meta property="twitter:domain" content="ztatlock.net">',
        f'<meta property="twitter:url" content="{escaped_url}">',
        f'<meta name="twitter:title" content="{escaped_title}">',
        f'<meta name="twitter:description" content="{escaped_share_description}">',
        f'<meta name="twitter:image" content="{escaped_image}">',
        "",
    ]
    return "\n".join(lines)


def render_publication_meta(
    page_stem: str,
    title: str,
    root: Path,
    *,
    site_url: str = SITE_URL,
) -> str:
    return render_publication_meta_for_url(
        page_stem,
        title,
        canonical_url(page_stem, site_url=site_url),
        root,
        site_url=site_url,
    )


def render_publication_meta_for_url(
    page_stem: str,
    title: str,
    url: str,
    root: Path,
    *,
    publications_dir: Path | None = None,
    site_url: str = SITE_URL,
) -> str:
    slug = publication_slug(page_stem)
    if slug is None:
        raise MetadataError(f"{page_stem} is not a publication page")

    try:
        record = load_optional_publication_record(
            root,
            slug,
            publications_dir=publications_dir,
        )
    except PublicationRecordError as err:
        raise MetadataError(str(err)) from err
    if record is None:
        raise MetadataError(
            "Missing publication metadata record for "
            f"{page_stem}: {publication_record_path(root, slug, publications_dir=publications_dir)}"
        )

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
    if publication_slug(page_stem) is not None:
        raise MetadataError(
            f"{(page_source_dir or root) / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
        )
    return normalize_general_metadata_entry(
        source.front_matter,
        context=f"{(page_source_dir or root) / f'{page_stem}.dj'}: front matter",
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
    row = load_front_matter_general_metadata(
        page_stem,
        root,
        page_source_dir=page_source_dir,
    )
    if row is None:
        raise MetadataError(f"Missing front matter metadata for {page_stem}")

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
    slug = publication_slug(page_stem)
    try:
        source = read_page_source(
            page_stem,
            root,
            page_source_dir=page_source_dir,
            publications_dir=publications_dir,
        )
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if source.is_draft:
        if slug is not None:
            if source.front_matter:
                raise MetadataError(
                    f"{(page_source_dir or root) / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
                )
            return ""
        if source.front_matter:
            return render_general_page_meta_for_url(
                page_stem,
                title,
                canonical_url,
                root,
                page_source_dir=page_source_dir,
                site_url=site_url,
            )
        return ""

    if slug is not None:
        if source.front_matter:
            raise MetadataError(
                f"{(page_source_dir or root) / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
            )
        return render_publication_meta_for_url(
            page_stem,
            title,
            canonical_url,
            root,
            publications_dir=publications_dir,
            site_url=site_url,
        )

    if source.front_matter:
        return render_general_page_meta_for_url(
            page_stem,
            title,
            canonical_url,
            root,
            page_source_dir=page_source_dir,
            site_url=site_url,
        )
    raise MetadataError(f"Missing front matter metadata for {page_stem}")


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
        actual_publications_dir = publications_dir or (root / "pubs")
        return actual_publications_dir / normalized.removeprefix("pubs/")

    actual_static_source_dir = static_source_dir or root
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
    publication_stems = {path.stem for path in actual_page_source_dir.glob("pub-*.dj")}
    page_stem_set = {path.stem for path in actual_page_source_dir.glob("*.dj")} - publication_stems

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


def validate_publication_record_metadata(
    root: Path,
    *,
    publications_dir: Path | None = None,
    static_source_dir: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    actual_publications_dir = publications_dir or (root / "pubs")

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
