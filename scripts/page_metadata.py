#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
from pathlib import Path

SITE_URL = "https://ztatlock.net"
GENERAL_PAGE_METADATA = Path("manifests/page-metadata.json")
PUBLICATION_METADATA = Path("manifests/publication-metadata.json")
GENERAL_ALLOWED_FIELDS = {"description", "share_description", "image_path", "title"}
PUBLICATION_ALLOWED_FIELDS = {"description", "share_description", "image_path"}
DRAFT_HEADING_RE = re.compile(r"^# DRAFT$", re.MULTILINE)


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


def is_draft_page(page_stem: str, root: Path) -> bool:
    path = root / f"{page_stem}.dj"
    if not path.exists():
        return False
    return bool(DRAFT_HEADING_RE.search(path.read_text(encoding="utf-8")))


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

        unknown_fields = sorted(set(entry) - GENERAL_ALLOWED_FIELDS)
        if unknown_fields:
            raise MetadataError(
                f"{path}: entry for {stem} has unknown fields: {', '.join(unknown_fields)}"
            )

        description = entry.get("description")
        if not isinstance(description, str) or not description.strip():
            raise MetadataError(f"{path}: missing description for {stem}")

        share_description = entry.get("share_description")
        if share_description is not None and not isinstance(share_description, str):
            raise MetadataError(f"{path}: share_description for {stem} must be a string or null")

        image_path = entry.get("image_path")
        if image_path is not None and not isinstance(image_path, str):
            raise MetadataError(f"{path}: image_path for {stem} must be a string or null")

        title = entry.get("title")
        if title is not None and not isinstance(title, str):
            raise MetadataError(f"{path}: title for {stem} must be a string or null")

        rows[stem] = {
            "description": description.strip(),
            "share_description": (share_description or "").strip(),
            "image_path": (image_path or "").strip(),
            "title": (title or "").strip(),
        }

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

        unknown_fields = sorted(set(entry) - PUBLICATION_ALLOWED_FIELDS)
        if unknown_fields:
            raise MetadataError(
                f"{path}: entry for {slug} has unknown fields: {', '.join(unknown_fields)}"
            )

        description = entry.get("description")
        if not isinstance(description, str) or not description.strip():
            raise MetadataError(f"{path}: missing description for {slug}")

        share_description = entry.get("share_description")
        if share_description is not None and not isinstance(share_description, str):
            raise MetadataError(f"{path}: share_description for {slug} must be a string or null")

        image_path = entry.get("image_path")
        if image_path is not None and not isinstance(image_path, str):
            raise MetadataError(f"{path}: image_path for {slug} must be a string or null")

        rows[slug] = {
            "description": description.strip(),
            "share_description": (share_description or "").strip(),
            "image_path": (image_path or "").strip(),
        }

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


def render_general_page_meta(page_stem: str, title: str, root: Path) -> str:
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
    if is_draft_page(page_stem, root):
        if slug is not None:
            rows = load_publication_metadata(root)
            if slug in rows:
                return render_publication_meta(page_stem, title, root)
            return ""
        general_rows = load_general_page_metadata(root)
        if page_stem in general_rows:
            return render_general_page_meta(page_stem, title, root)
        return ""

    if slug is not None:
        return render_publication_meta(page_stem, title, root)
    general_rows = load_general_page_metadata(root)
    if page_stem in general_rows:
        return render_general_page_meta(page_stem, title, root)
    raise MetadataError(f"Missing structured page metadata for {page_stem}")


def validate_general_page_metadata(root: Path) -> list[str]:
    issues: list[str] = []
    try:
        rows = load_general_page_metadata(root)
    except MetadataError as err:
        return [str(err)]

    page_stems = sorted(path.stem for path in root.glob("*.dj"))
    publication_stems = {f"pub-{path.stem.removeprefix('pub-')}" for path in root.glob("pub-*.dj")}
    page_stem_set = set(page_stems)

    extra = sorted(set(rows) - page_stem_set)
    for stem in extra:
        issues.append(f"{GENERAL_PAGE_METADATA}: entry for missing page {stem}.dj")

    for stem in sorted(rows):
        if stem in publication_stems:
            issues.append(f"{GENERAL_PAGE_METADATA}: publication page {stem} belongs in {PUBLICATION_METADATA}")

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
        return [str(err)]

    page_slugs = sorted(
        path.stem.removeprefix("pub-")
        for path in root.glob("pub-*.dj")
        if not is_draft_page(path.stem, root)
    )
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
