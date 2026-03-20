#!/usr/bin/env python3

from __future__ import annotations

import html
import json
from pathlib import Path

from page_source import PageSourceError, read_page_source

SITE_URL = "https://ztatlock.net"
GENERAL_PAGE_METADATA = Path("manifests/page-metadata.json")
PUBLICATION_METADATA = Path("manifests/publication-metadata.json")
GENERAL_ALLOWED_FIELDS = {"description", "share_description", "image_path", "title"}
PUBLICATION_ALLOWED_FIELDS = {"description", "share_description", "image_path"}


class MetadataError(ValueError):
    pass


def canonical_url(page_stem: str) -> str:
    if page_stem == "index":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{page_stem}.html"


def publication_slug(page_stem: str) -> str | None:
    if page_stem.startswith("pub-"):
        return page_stem.removeprefix("pub-")
    return None


def default_publication_image_path(slug: str) -> str:
    return f"pubs/{slug}/{slug}-meta.png"


def default_page_image_path() -> str:
    return "img/favicon-meta.png"


def absolute_url(path_or_url: str) -> str:
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return f"{SITE_URL}/{path_or_url.lstrip('/')}"


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


def normalize_publication_metadata_entry(
    entry: dict[str, object],
    *,
    context: str,
) -> dict[str, str]:
    unknown_fields = sorted(set(entry) - PUBLICATION_ALLOWED_FIELDS)
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

    return {
        "description": description.strip(),
        "share_description": (share_description or "").strip(),
        "image_path": (image_path or "").strip(),
    }


def load_general_page_metadata(root: Path) -> dict[str, dict[str, str]]:
    path = root / GENERAL_PAGE_METADATA
    if not path.exists():
        raise MetadataError(f"Missing page metadata manifest: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise MetadataError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise MetadataError(f"{path}: expected a JSON object keyed by page stem")

    rows: dict[str, dict[str, str]] = {}
    for stem, entry in raw.items():
        if not isinstance(stem, str) or not stem:
            raise MetadataError(f"{path}: invalid page stem {stem!r}")
        if not isinstance(entry, dict):
            raise MetadataError(f"{path}: entry for {stem} must be a JSON object")

        rows[stem] = normalize_general_metadata_entry(
            entry,
            context=f"{path}: entry for {stem}",
        )

    return rows


def load_publication_metadata(root: Path) -> dict[str, dict[str, str]]:
    path = root / PUBLICATION_METADATA
    if not path.exists():
        raise MetadataError(f"Missing publication metadata manifest: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise MetadataError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise MetadataError(f"{path}: expected a JSON object keyed by publication slug")

    rows: dict[str, dict[str, str]] = {}
    for slug, entry in raw.items():
        if not isinstance(slug, str) or not slug:
            raise MetadataError(f"{path}: invalid publication slug {slug!r}")
        if not isinstance(entry, dict):
            raise MetadataError(f"{path}: entry for {slug} must be a JSON object")

        rows[slug] = normalize_publication_metadata_entry(
            entry,
            context=f"{path}: entry for {slug}",
        )

    return rows


def write_publication_metadata(root: Path, rows: dict[str, dict[str, str]]) -> None:
    path = root / PUBLICATION_METADATA
    serialized: dict[str, dict[str, str]] = {}
    for slug in sorted(rows):
        row = rows[slug]
        entry = {"description": row["description"]}
        if row.get("share_description"):
            entry["share_description"] = row["share_description"]
        if row.get("image_path"):
            entry["image_path"] = row["image_path"]
        serialized[slug] = entry

    path.write_text(
        json.dumps(serialized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def add_publication_metadata_entry(
    root: Path,
    slug: str,
    description: str = "TODO",
) -> None:
    rows = load_publication_metadata(root)
    if slug in rows:
        raise MetadataError(f"Publication metadata entry for {slug} already exists")
    rows[slug] = {
        "description": description,
        "share_description": "",
        "image_path": "",
    }
    write_publication_metadata(root, rows)


def render_metadata_block(
    *,
    title: str,
    description: str,
    share_description: str,
    image_path: str,
    url: str,
) -> str:
    escaped_title = escape_content(title)
    escaped_description = escape_content(description)
    escaped_share_description = escape_content(share_description)
    escaped_url = escape_content(url)
    escaped_image = escape_content(absolute_url(image_path))

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


def render_publication_meta(page_stem: str, title: str, root: Path) -> str:
    slug = publication_slug(page_stem)
    if slug is None:
        raise MetadataError(f"{page_stem} is not a publication page")

    rows = load_publication_metadata(root)
    if slug not in rows:
        raise MetadataError(f"Missing publication metadata for {page_stem}")

    row = rows[slug]
    description = row["description"]
    share_description = row["share_description"] or description
    image_path = row["image_path"] or default_publication_image_path(slug)
    url = canonical_url(page_stem)

    return render_metadata_block(
        title=title,
        description=description,
        share_description=share_description,
        image_path=image_path,
        url=url,
    )


def load_front_matter_general_metadata(page_stem: str, root: Path) -> dict[str, str] | None:
    try:
        source = read_page_source(page_stem, root)
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if not source.front_matter:
        return None
    if publication_slug(page_stem) is not None:
        raise MetadataError(
            f"{root / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
        )
    return normalize_general_metadata_entry(
        source.front_matter,
        context=f"{root / f'{page_stem}.dj'}: front matter",
    )


def render_general_page_meta(page_stem: str, title: str, root: Path) -> str:
    row = load_front_matter_general_metadata(page_stem, root)
    if row is None:
        rows = load_general_page_metadata(root)
        if page_stem not in rows:
            raise MetadataError(f"Missing structured page metadata for {page_stem}")
        row = rows[page_stem]

    description = row["description"]
    share_description = row["share_description"] or description
    image_path = row["image_path"] or default_page_image_path()
    rendered_title = row["title"] or title
    url = canonical_url(page_stem)

    return render_metadata_block(
        title=rendered_title,
        description=description,
        share_description=share_description,
        image_path=image_path,
        url=url,
    )


def render_page_meta(page_stem: str, title: str, root: Path) -> str:
    slug = publication_slug(page_stem)
    try:
        source = read_page_source(page_stem, root)
    except PageSourceError as err:
        raise MetadataError(str(err)) from err

    if source.is_draft:
        if slug is not None:
            if source.front_matter:
                raise MetadataError(
                    f"{root / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
                )
            rows = load_publication_metadata(root)
            if slug in rows:
                return render_publication_meta(page_stem, title, root)
            return ""
        if source.front_matter:
            return render_general_page_meta(page_stem, title, root)
        general_rows = load_general_page_metadata(root)
        if page_stem in general_rows:
            return render_general_page_meta(page_stem, title, root)
        return ""

    if slug is not None:
        if source.front_matter:
            raise MetadataError(
                f"{root / f'{page_stem}.dj'}: front matter metadata for publication pages is not supported yet"
            )
        return render_publication_meta(page_stem, title, root)

    if source.front_matter:
        return render_general_page_meta(page_stem, title, root)

    general_rows = load_general_page_metadata(root)
    if page_stem in general_rows:
        return render_general_page_meta(page_stem, title, root)
    raise MetadataError(f"Missing structured page metadata for {page_stem}")


def validate_general_page_metadata(root: Path) -> list[str]:
    issues: list[str] = []
    try:
        rows = load_general_page_metadata(root)
    except MetadataError as err:
        issues.append(str(err))
        rows = {}

    publication_stems = {path.stem for path in root.glob("pub-*.dj")}
    page_stem_set = {path.stem for path in root.glob("*.dj")} - publication_stems
    front_matter_stems: set[str] = set()

    extra = sorted(set(rows) - page_stem_set)
    for stem in extra:
        if stem in publication_stems:
            issues.append(f"{GENERAL_PAGE_METADATA}: publication page {stem} belongs in {PUBLICATION_METADATA}")
        else:
            issues.append(f"{GENERAL_PAGE_METADATA}: entry for missing page {stem}.dj")

    for stem in sorted(page_stem_set):
        try:
            source = read_page_source(stem, root)
        except PageSourceError as err:
            issues.append(str(err))
            continue

        if source.front_matter:
            front_matter_stems.add(stem)
            try:
                row = normalize_general_metadata_entry(
                    source.front_matter,
                    context=f"{root / f'{stem}.dj'}: front matter",
                )
            except MetadataError as err:
                issues.append(str(err))
                continue

            if stem in rows:
                issues.append(
                    f"{root / f'{stem}.dj'}: metadata is defined in both front matter and {GENERAL_PAGE_METADATA}"
                )

            image_path = row["image_path"] or default_page_image_path()
            if not image_path.startswith(("http://", "https://")) and not (root / image_path).exists():
                issues.append(f"{root / f'{stem}.dj'}: image path does not exist: {image_path}")
            continue

        if source.is_draft:
            continue
        if stem not in rows:
            issues.append(
                f"{root / f'{stem}.dj'}: missing metadata in front matter or {GENERAL_PAGE_METADATA}"
            )

    for stem in sorted(rows):
        if stem in front_matter_stems or stem in publication_stems:
            continue
        row = rows[stem]
        image_path = row["image_path"] or default_page_image_path()
        if not image_path.startswith(("http://", "https://")) and not (root / image_path).exists():
            issues.append(f"{GENERAL_PAGE_METADATA}: image path for {stem} does not exist: {image_path}")

    return issues


def validate_publication_metadata(root: Path) -> list[str]:
    issues: list[str] = []
    try:
        rows = load_publication_metadata(root)
    except MetadataError as err:
        issues.append(str(err))
        rows = {}

    page_slugs: list[str] = []
    for path in sorted(root.glob("pub-*.dj")):
        try:
            source = read_page_source(path.stem, root)
        except PageSourceError as err:
            issues.append(str(err))
            continue

        if source.front_matter:
            issues.append(f"{path}: front matter metadata for publication pages is not supported yet")
        if not source.is_draft:
            page_slugs.append(path.stem.removeprefix("pub-"))

    manifest_slugs = sorted(rows)

    missing = sorted(set(page_slugs) - set(manifest_slugs))
    extra = sorted(set(manifest_slugs) - set(page_slugs))
    for slug in missing:
        issues.append(f"pub-{slug}.dj: missing manifest entry in {PUBLICATION_METADATA}")
    for slug in extra:
        issues.append(f"{PUBLICATION_METADATA}: entry for missing page pub-{slug}.dj")

    for slug, row in rows.items():
        image_path = row["image_path"] or default_publication_image_path(slug)
        if image_path.startswith(("http://", "https://")):
            continue
        if not (root / image_path).exists():
            issues.append(f"{PUBLICATION_METADATA}: image path for {slug} does not exist: {image_path}")

    return issues
