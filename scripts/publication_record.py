#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

SITE_PUBLICATIONS_PATH = Path("site") / "pubs"
PUBLICATION_RECORD_NAME = "publication.json"
ALLOWED_LINK_KEYS = {
    "talk",
    "teaser",
    "project",
    "code",
    "demo",
    "publisher",
    "arxiv",
    "event",
    "vscode",
}
ALLOWED_LISTING_GROUPS = frozenset({"main", "workshop"})
ALLOWED_PUB_TYPES = frozenset({"conference", "journal", "workshop"})
ALLOWED_IDENTIFIER_KEYS = frozenset({"doi", "arxiv", "hal", "isbn"})

EXTRA_CONTENT_NAME = "extra.dj"
IMAGE_EXTENSIONS = (".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg")
SLIDES_EXTENSIONS = (".pdf", ".pptx")
LINK_ORDER = (
    "paper",
    "teaser",
    "talk",
    "slides",
    "poster",
    "project",
    "code",
    "demo",
    "event",
    "vscode",
    "publisher",
    "arxiv",
    "bib",
)
LINK_LABELS = {
    "arxiv": "arXiv",
    "vscode": "VSCode",
}


class PublicationRecordError(ValueError):
    pass


@dataclass(frozen=True)
class PublicationPerson:
    name: str
    ref: str | None = None


@dataclass(frozen=True)
class PublicationTalk:
    event: str
    speakers: tuple[PublicationPerson, ...]
    url: str
    embed: str
    title: str


@dataclass(frozen=True)
class PublicationTime:
    pub_year: int | None = None
    pub_date: date | None = None


@dataclass(frozen=True)
class PublicationVenue:
    full: str
    short: str | None = None


@dataclass(frozen=True)
class PublicationClassification:
    listing_group: str | None = None
    pub_type: str | None = None


@dataclass(frozen=True)
class PublicationRecord:
    slug: str
    draft: bool
    local_page: bool
    primary_link: str | None
    title: str
    authors: tuple[PublicationPerson, ...]
    time: PublicationTime
    venue: PublicationVenue
    classification: PublicationClassification
    badges: tuple[str, ...] = ()
    description: str = ""
    share_description: str = ""
    meta_image_path: str = ""
    links: dict[str, str] = field(default_factory=dict)
    identifiers: dict[str, str] = field(default_factory=dict)
    talks: tuple[PublicationTalk, ...] = ()


@dataclass(frozen=True)
class PublicationAssets:
    paper: Path
    bib: Path
    abstract: Path
    absimg: Path
    metaimg: Path | None
    slides: Path | None
    poster: Path | None
    extra: Path | None


def default_publications_dir(root: Path) -> Path:
    return root / SITE_PUBLICATIONS_PATH


def publication_dir(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    base_dir = publications_dir or default_publications_dir(root)
    return base_dir / slug


def publication_record_path(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    return publication_dir(root, slug, publications_dir=publications_dir) / PUBLICATION_RECORD_NAME


def publication_page_path(slug: str) -> str:
    return f"pubs/{slug}/"


def publication_year(slug: str) -> int:
    year, _, _ = slug.partition("-")
    if len(year) != 4 or not year.isdigit():
        raise PublicationRecordError(f"{slug}: invalid publication slug; expected YEAR-...")
    return int(year)


def publication_display_year(record: PublicationRecord) -> str:
    if record.time.pub_year is None:
        raise PublicationRecordError(f"{record.slug}: missing canonical pub_year")
    return str(record.time.pub_year)


def publication_index_title_url(record: PublicationRecord) -> str:
    if record.local_page:
        return publication_page_path(record.slug)
    if record.primary_link is None:
        raise PublicationRecordError(f"{record.slug}: thin publication is missing primary_link")
    return record.links[record.primary_link]


def publication_order_key(record: PublicationRecord) -> tuple[int, int, int, str]:
    pub_year = record.time.pub_year or 0
    if record.time.pub_date is None:
        return (-pub_year, 1, 0, record.title)
    return (-pub_year, 0, -record.time.pub_date.toordinal(), record.title)


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PublicationRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{context}: expected a JSON object")
    return raw


def _normalize_optional_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise PublicationRecordError(f"{context}: {field} must be a string or null")
    value = raw.strip()
    return value or None


def _normalize_required_string(raw: object, *, context: str, field: str) -> str:
    value = _normalize_optional_string(raw, context=context, field=field)
    if value is None:
        raise PublicationRecordError(f"{context}: missing {field}")
    return value


def _normalize_optional_boolean(
    raw: object,
    *,
    context: str,
    field: str,
    default: bool,
) -> bool:
    if raw is None:
        return default
    if not isinstance(raw, bool):
        raise PublicationRecordError(f"{context}: {field} must be a boolean or null")
    return raw


def _normalize_optional_date(raw: object, *, context: str, field: str) -> date | None:
    value = _normalize_optional_string(raw, context=context, field=field)
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as err:
        raise PublicationRecordError(
            f"{context}: {field} must be a valid ISO date (YYYY-MM-DD)"
        ) from err


def _normalize_optional_year(raw: object, *, context: str, field: str) -> int | None:
    if raw is None:
        return None
    if not isinstance(raw, int):
        raise PublicationRecordError(f"{context}: {field} must be an integer or null")
    if raw < 1900 or raw > 2100:
        raise PublicationRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _normalize_person(raw: object, *, context: str) -> PublicationPerson:
    obj = _require_object(raw, context=context)
    unknown_fields = sorted(set(obj) - {"name", "ref"})
    if unknown_fields:
        raise PublicationRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")
    name = _normalize_required_string(obj.get("name"), context=context, field="name")
    raw_ref = obj.get("ref")
    if isinstance(raw_ref, str) and not raw_ref.strip():
        ref = None
    else:
        ref = _normalize_optional_string(raw_ref, context=context, field="ref")
    return PublicationPerson(name=name, ref=ref)


def _normalize_people(raw: object, *, context: str) -> tuple[PublicationPerson, ...]:
    if not isinstance(raw, list) or not raw:
        raise PublicationRecordError(f"{context}: expected a non-empty JSON array")
    return tuple(
        _normalize_person(entry, context=f"{context}[{index}]")
        for index, entry in enumerate(raw)
    )


def _normalize_badges(raw: object, *, context: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise PublicationRecordError(f"{context}: badges must be a JSON array or null")
    return tuple(
        _normalize_required_string(entry, context=f"{context}[{index}]", field="badge")
        for index, entry in enumerate(raw)
    )


def _normalize_links(raw: object, *, context: str) -> dict[str, str]:
    if raw is None:
        return {}
    obj = _require_object(raw, context=context)
    unknown_keys = sorted(set(obj) - ALLOWED_LINK_KEYS)
    if unknown_keys:
        raise PublicationRecordError(f"{context}: unknown link keys: {', '.join(unknown_keys)}")
    return {
        key: _normalize_required_string(value, context=context, field=key)
        for key, value in obj.items()
    }


def _normalize_identifiers(raw: object, *, context: str) -> dict[str, str]:
    if raw is None:
        return {}
    obj = _require_object(raw, context=context)
    unknown_keys = sorted(set(obj) - ALLOWED_IDENTIFIER_KEYS)
    if unknown_keys:
        raise PublicationRecordError(
            f"{context}: unknown identifier keys: {', '.join(unknown_keys)}"
        )
    return {
        key: _normalize_required_string(value, context=context, field=key)
        for key, value in obj.items()
    }


def _normalize_talk(raw: object, *, context: str) -> PublicationTalk:
    obj = _require_object(raw, context=context)
    unknown_fields = sorted(set(obj) - {"event", "speakers", "url", "embed", "title"})
    if unknown_fields:
        raise PublicationRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")
    return PublicationTalk(
        event=_normalize_required_string(obj.get("event"), context=context, field="event"),
        speakers=_normalize_people(obj.get("speakers"), context=f"{context}.speakers"),
        url=_normalize_required_string(obj.get("url"), context=context, field="url"),
        embed=_normalize_required_string(obj.get("embed"), context=context, field="embed"),
        title=_normalize_optional_string(obj.get("title"), context=context, field="title") or "",
    )


def _normalize_talks(raw: object, *, context: str) -> tuple[PublicationTalk, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise PublicationRecordError(f"{context}: talks must be a JSON array or null")
    return tuple(
        _normalize_talk(entry, context=f"{context}[{index}]")
        for index, entry in enumerate(raw)
    )


def load_publication_record(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> PublicationRecord:
    path = publication_record_path(root, slug, publications_dir=publications_dir)
    if not path.exists():
        raise PublicationRecordError(f"Missing publication record: {path}")

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except json.JSONDecodeError as err:
        raise PublicationRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{path}: expected a JSON object")

    unknown_fields = sorted(
        set(raw)
        - {
            "draft",
            "local_page",
            "listing_group",
            "pub_type",
            "pub_year",
            "pub_date",
            "primary_link",
            "title",
            "authors",
            "venue",
            "venue_short",
            "identifiers",
            "badges",
            "description",
            "share_description",
            "meta_image_path",
            "links",
            "talks",
        }
    )
    if unknown_fields:
        raise PublicationRecordError(f"{path}: unknown fields: {', '.join(unknown_fields)}")

    slug_year = publication_year(slug)
    draft = _normalize_optional_boolean(raw.get("draft"), context=str(path), field="draft", default=False)
    local_page = _normalize_optional_boolean(
        raw.get("local_page"),
        context=str(path),
        field="local_page",
        default=True,
    )
    time = PublicationTime(
        pub_year=_normalize_optional_year(raw.get("pub_year"), context=str(path), field="pub_year"),
        pub_date=_normalize_optional_date(raw.get("pub_date"), context=str(path), field="pub_date"),
    )
    venue = PublicationVenue(
        full=_normalize_required_string(raw.get("venue"), context=str(path), field="venue"),
        short=_normalize_optional_string(raw.get("venue_short"), context=str(path), field="venue_short"),
    )
    classification = PublicationClassification(
        listing_group=_normalize_optional_string(
            raw.get("listing_group"),
            context=str(path),
            field="listing_group",
        ),
        pub_type=_normalize_optional_string(
            raw.get("pub_type"),
            context=str(path),
            field="pub_type",
        ),
    )
    record = PublicationRecord(
        slug=slug,
        draft=draft,
        local_page=local_page,
        primary_link=_normalize_optional_string(
            raw.get("primary_link"),
            context=str(path),
            field="primary_link",
        ),
        title=_normalize_required_string(raw.get("title"), context=str(path), field="title"),
        authors=_normalize_people(raw.get("authors"), context=f"{path}.authors"),
        time=time,
        venue=venue,
        classification=classification,
        badges=_normalize_badges(raw.get("badges"), context=f"{path}.badges"),
        description=_normalize_optional_string(
            raw.get("description"),
            context=str(path),
            field="description",
        ) or "",
        share_description=_normalize_optional_string(
            raw.get("share_description"),
            context=str(path),
            field="share_description",
        ) or "",
        meta_image_path=_normalize_optional_string(
            raw.get("meta_image_path"),
            context=str(path),
            field="meta_image_path",
        ) or "",
        links=_normalize_links(raw.get("links"), context=f"{path}.links"),
        identifiers=_normalize_identifiers(raw.get("identifiers"), context=f"{path}.identifiers"),
        talks=_normalize_talks(raw.get("talks"), context=f"{path}.talks"),
    )
    _validate_publication_record(record, context=str(path), slug_year=slug_year)
    return record


def load_optional_publication_record(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> PublicationRecord | None:
    path = publication_record_path(root, slug, publications_dir=publications_dir)
    if not path.exists():
        return None
    return load_publication_record(root, slug, publications_dir=publications_dir)


def _validate_publication_record(
    record: PublicationRecord,
    *,
    context: str,
    slug_year: int,
) -> None:
    if record.time.pub_year is not None and record.time.pub_year != slug_year:
        raise PublicationRecordError(f"{context}: pub_year must match slug year {slug_year}")

    if record.classification.listing_group is not None:
        if record.classification.listing_group not in ALLOWED_LISTING_GROUPS:
            allowed = ", ".join(sorted(ALLOWED_LISTING_GROUPS))
            raise PublicationRecordError(f"{context}: listing_group must be one of {allowed}")

    if record.classification.pub_type is not None:
        if record.classification.pub_type not in ALLOWED_PUB_TYPES:
            allowed = ", ".join(sorted(ALLOWED_PUB_TYPES))
            raise PublicationRecordError(f"{context}: pub_type must be one of {allowed}")

    if record.local_page:
        if record.primary_link is not None:
            raise PublicationRecordError(
                f"{context}: primary_link is only valid when local_page is false"
            )
    else:
        if record.primary_link is None:
            raise PublicationRecordError(f"{context}: missing primary_link for thin publication bundle")
        if record.primary_link not in record.links:
            raise PublicationRecordError(f"{context}: primary_link must name a key present in links")

    if record.draft:
        return

    if record.classification.listing_group is None:
        raise PublicationRecordError(f"{context}: missing listing_group")
    if record.classification.pub_type is None:
        raise PublicationRecordError(f"{context}: missing pub_type")
    if record.time.pub_year is None:
        raise PublicationRecordError(f"{context}: missing pub_year")
    if record.venue.short is None:
        raise PublicationRecordError(f"{context}: missing venue_short")
    if record.local_page and not record.description:
        raise PublicationRecordError(
            f"{context}: missing description for publication with local_page"
        )


def publication_pub_year(record: PublicationRecord) -> int:
    if record.time.pub_year is None:
        raise PublicationRecordError(f"{record.slug}: missing canonical pub_year")
    return record.time.pub_year


def publication_pub_date(record: PublicationRecord):
    return record.time.pub_date


def publication_full_venue_label(record: PublicationRecord) -> str:
    return record.venue.full


def publication_compact_venue_label(record: PublicationRecord) -> str:
    return record.venue.short or record.venue.full


def publication_listing_group(record: PublicationRecord) -> str | None:
    return record.classification.listing_group


def publication_pub_type(record: PublicationRecord) -> str | None:
    return record.classification.pub_type


def default_meta_image_path(slug: str) -> str:
    return f"pubs/{slug}/{slug}-meta.png"


def relative_publication_site_path(path: Path, *, publications_dir: Path) -> str:
    return f"pubs/{path.relative_to(publications_dir).as_posix()}"


def _find_optional_asset(pub_dir: Path, stem: str, extensions: tuple[str, ...]) -> Path | None:
    for ext in extensions:
        candidate = pub_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    return None


def publication_assets(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> PublicationAssets:
    actual_publications_dir = publications_dir or default_publications_dir(root)
    pub_dir = publication_dir(root, slug, publications_dir=actual_publications_dir)
    if not pub_dir.exists():
        raise PublicationRecordError(f"Missing publication directory: {pub_dir}")

    paper = pub_dir / f"{slug}.pdf"
    bib = pub_dir / f"{slug}.bib"
    abstract = pub_dir / f"{slug}-abstract.md"
    absimg = _find_optional_asset(pub_dir, f"{slug}-absimg", IMAGE_EXTENSIONS)
    metaimg = _find_optional_asset(pub_dir, f"{slug}-meta", IMAGE_EXTENSIONS)
    slides = _find_optional_asset(pub_dir, f"{slug}-slides", SLIDES_EXTENSIONS)
    poster = pub_dir / f"{slug}-poster.pdf"
    extra = pub_dir / EXTRA_CONTENT_NAME

    if not paper.exists():
        raise PublicationRecordError(f"Missing canonical publication PDF: {paper}")
    if not bib.exists():
        raise PublicationRecordError(f"Missing canonical publication BibTeX: {bib}")
    if not abstract.exists():
        raise PublicationRecordError(f"Missing canonical publication abstract: {abstract}")
    if absimg is None:
        raise PublicationRecordError(
            f"Missing canonical publication preview image for {slug}: {pub_dir / f'{slug}-absimg.*'}"
        )

    return PublicationAssets(
        paper=paper,
        bib=bib,
        abstract=abstract,
        absimg=absimg,
        metaimg=metaimg,
        slides=slides,
        poster=poster if poster.exists() else None,
        extra=extra if extra.exists() else None,
    )


def publication_metadata_image_path(
    root: Path,
    record: PublicationRecord,
    *,
    publications_dir: Path | None = None,
) -> str:
    if not record.local_page:
        raise PublicationRecordError(
            f"{record.slug}: publication has no local detail page metadata image"
        )
    if record.meta_image_path:
        return record.meta_image_path

    actual_publications_dir = publications_dir or default_publications_dir(root)
    assets = publication_assets(root, record.slug, publications_dir=actual_publications_dir)
    if assets.metaimg is not None:
        return relative_publication_site_path(
            assets.metaimg,
            publications_dir=actual_publications_dir,
        )
    return relative_publication_site_path(
        assets.absimg,
        publications_dir=actual_publications_dir,
    )


def _person_djot(person: PublicationPerson) -> str:
    if person.ref:
        return f"[{person.name}][{person.ref}]"
    return person.name


def _join_people_sentence(people: tuple[PublicationPerson, ...]) -> str:
    rendered = [_person_djot(person) for person in people]
    if len(rendered) == 1:
        return rendered[0]
    if len(rendered) == 2:
        return f"{rendered[0]} and {rendered[1]}"
    return ", ".join(rendered[:-1]) + f", and {rendered[-1]}"


def _render_authors(authors: tuple[PublicationPerson, ...]) -> str:
    lines: list[str] = []
    for index, author in enumerate(authors):
        prefix = "  " if index == 0 else "\\ "
        suffix = "," if index < len(authors) - 1 else ""
        lines.append(f"{prefix}{_person_djot(author)}{suffix}")
    return "\n".join(lines)


def _render_venue_line(record: PublicationRecord) -> str:
    line = f"{publication_full_venue_label(record)} {publication_display_year(record)}"
    if not record.badges:
        return line
    return line + " \\\n" + " \\\n".join(record.badges)


def render_publication_index_entry(record: PublicationRecord) -> str:
    title_url = publication_index_title_url(record)
    return "\n".join(
        [
            f"{{#{record.slug}}}",
            f"*[{record.title}]({title_url})* \\",
            _render_authors(record.authors),
            "\\",
            _render_venue_line(record),
        ]
    )


def _render_photo_block(image_path: str, target_path: str, alt_text: str) -> str:
    return "\n".join(
        [
            "{.photo}",
            ":::",
            f"  [![{alt_text}](",
            f"    {image_path}",
            "  )](",
            f"    {target_path}",
            "  )",
            ":::",
        ]
    )


def _link_label(key: str) -> str:
    return LINK_LABELS.get(key, key)


def _render_links(
    record: PublicationRecord,
    assets: PublicationAssets,
    *,
    publications_dir: Path,
) -> str:
    links: dict[str, str] = {
        "paper": relative_publication_site_path(assets.paper, publications_dir=publications_dir),
        "bib": relative_publication_site_path(assets.bib, publications_dir=publications_dir),
    }
    if assets.slides is not None:
        links["slides"] = relative_publication_site_path(
            assets.slides,
            publications_dir=publications_dir,
        )
    if assets.poster is not None:
        links["poster"] = relative_publication_site_path(
            assets.poster,
            publications_dir=publications_dir,
        )

    links.update(record.links)
    if "talk" not in links and record.talks:
        links["talk"] = record.talks[0].url

    rendered = ["{.columns .columns-8rem}"]
    for key in LINK_ORDER:
        url = links.get(key)
        if not url:
            continue
        rendered.append(f"- [{_link_label(key)}]({url})")
    return "\n".join(rendered)


def _render_talks(record: PublicationRecord) -> str:
    if not record.talks:
        return ""

    blocks = ["## Talk", ""]
    for index, talk in enumerate(record.talks):
        title = talk.title or "YouTube video player"
        blocks.append(f"{talk.event} talk by {_join_people_sentence(talk.speakers)}.")
        blocks.append("")
        blocks.extend(
            [
                "{.photo}",
                ":::",
                "``` =html",
                f'<iframe src="{talk.embed}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                "```",
                ":::",
            ]
        )
        if index < len(record.talks) - 1:
            blocks.append("")
    return "\n".join(blocks)


def render_publication_body(
    root: Path,
    record: PublicationRecord,
    *,
    publications_dir: Path | None = None,
) -> str:
    if not record.local_page:
        raise PublicationRecordError(
            f"{record.slug}: publication has no local detail page body"
        )
    actual_publications_dir = publications_dir or default_publications_dir(root)
    assets = publication_assets(root, record.slug, publications_dir=actual_publications_dir)
    abstract_text = assets.abstract.read_text(encoding="utf-8").strip()
    bib_text = assets.bib.read_text(encoding="utf-8").rstrip()
    extra_text = assets.extra.read_text(encoding="utf-8").strip() if assets.extra else ""

    preview_image = relative_publication_site_path(
        assets.absimg,
        publications_dir=actual_publications_dir,
    )
    paper_path = relative_publication_site_path(
        assets.paper,
        publications_dir=actual_publications_dir,
    )

    blocks = [
        f"# {record.title}",
        "",
        _render_authors(record.authors),
        "",
        _render_venue_line(record),
        "",
        _render_photo_block(preview_image, paper_path, record.title),
        "",
        _render_links(record, assets, publications_dir=actual_publications_dir),
        "",
        "",
        "## Abstract",
        "",
        abstract_text,
    ]

    talk_block = _render_talks(record)
    if talk_block:
        blocks.extend(["", "", talk_block])

    if extra_text:
        blocks.extend(["", "", extra_text])

    blocks.extend(
        [
            "",
            "",
            "## BibTeX",
            "",
            "{.bib}",
            "```",
            bib_text,
            "```",
        ]
    )

    blocks.extend(["", "", "[📝 publications index](pubs/)"])
    return "\n".join(blocks) + "\n"
