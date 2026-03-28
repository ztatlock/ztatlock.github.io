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


class PublicationRecordAError(ValueError):
    pass


@dataclass(frozen=True)
class PublicationPersonA:
    name: str
    ref: str | None = None


@dataclass(frozen=True)
class PublicationTalkA:
    event: str
    speakers: tuple[PublicationPersonA, ...]
    url: str
    embed: str
    title: str


@dataclass(frozen=True)
class PublicationTimeA:
    pub_year: int | None = None
    pub_date: date | None = None


@dataclass(frozen=True)
class PublicationVenueA:
    full: str
    short: str | None = None


@dataclass(frozen=True)
class PublicationClassificationA:
    listing_group: str | None = None
    pub_type: str | None = None


@dataclass(frozen=True)
class PublicationRecordA:
    slug: str
    draft: bool
    local_page: bool
    primary_link: str | None
    title: str
    authors: tuple[PublicationPersonA, ...]
    time: PublicationTimeA
    venue: PublicationVenueA
    classification: PublicationClassificationA
    badges: tuple[str, ...] = ()
    description: str = ""
    share_description: str = ""
    meta_image_path: str = ""
    links: dict[str, str] = field(default_factory=dict)
    identifiers: dict[str, str] = field(default_factory=dict)
    talks: tuple[PublicationTalkA, ...] = ()


def default_publications_dir(root: Path) -> Path:
    return root / SITE_PUBLICATIONS_PATH


def publication_dir(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    base_dir = publications_dir or default_publications_dir(root)
    return base_dir / slug


def publication_record_a_path(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> Path:
    return publication_dir(root, slug, publications_dir=publications_dir) / PUBLICATION_RECORD_NAME


def publication_page_path(slug: str) -> str:
    return f"pubs/{slug}/"


def publication_slug_year(slug: str) -> int:
    year, _, _ = slug.partition("-")
    if len(year) != 4 or not year.isdigit():
        raise PublicationRecordAError(f"{slug}: invalid publication slug; expected YEAR-...")
    return int(year)


def publication_display_year(record: PublicationRecordA) -> str:
    if record.time.pub_year is None:
        raise PublicationRecordAError(f"{record.slug}: missing canonical pub_year")
    return str(record.time.pub_year)


def publication_index_title_url_a(record: PublicationRecordA) -> str:
    if record.local_page:
        return publication_page_path(record.slug)
    if record.primary_link is None:
        raise PublicationRecordAError(
            f"{record.slug}: thin publication is missing primary_link"
        )
    return record.links[record.primary_link]


def publication_order_key_a(record: PublicationRecordA) -> tuple[int, int, int, str]:
    pub_year = record.time.pub_year or 0
    if record.time.pub_date is None:
        return (-pub_year, 1, 0, record.title)
    return (-pub_year, 0, -record.time.pub_date.toordinal(), record.title)


def load_publication_index_records_a(
    root: Path,
    *,
    publications_dir: Path | None = None,
) -> tuple[PublicationRecordA, ...]:
    actual_publications_dir = publications_dir or default_publications_dir(root)
    records: list[PublicationRecordA] = []
    for path in sorted(actual_publications_dir.glob("*/publication.json")):
        record = load_publication_record_a(
            root,
            path.parent.name,
            publications_dir=actual_publications_dir,
        )
        if record.draft:
            continue
        records.append(record)
    return tuple(sorted(records, key=publication_order_key_a))


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PublicationRecordAError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise PublicationRecordAError(f"{context}: expected a JSON object")
    return raw


def _normalize_optional_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise PublicationRecordAError(f"{context}: {field} must be a string or null")
    value = raw.strip()
    return value or None


def _normalize_required_string(raw: object, *, context: str, field: str) -> str:
    value = _normalize_optional_string(raw, context=context, field=field)
    if value is None:
        raise PublicationRecordAError(f"{context}: missing {field}")
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
        raise PublicationRecordAError(f"{context}: {field} must be a boolean or null")
    return raw


def _normalize_optional_date(raw: object, *, context: str, field: str) -> date | None:
    value = _normalize_optional_string(raw, context=context, field=field)
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as err:
        raise PublicationRecordAError(
            f"{context}: {field} must be a valid ISO date (YYYY-MM-DD)"
        ) from err


def _normalize_optional_year(raw: object, *, context: str, field: str) -> int | None:
    if raw is None:
        return None
    if not isinstance(raw, int):
        raise PublicationRecordAError(f"{context}: {field} must be an integer or null")
    if raw < 1900 or raw > 2100:
        raise PublicationRecordAError(f"{context}: invalid {field} {raw!r}")
    return raw


def _normalize_person(raw: object, *, context: str) -> PublicationPersonA:
    obj = _require_object(raw, context=context)
    unknown_fields = sorted(set(obj) - {"name", "ref"})
    if unknown_fields:
        raise PublicationRecordAError(
            f"{context}: unknown fields: {', '.join(unknown_fields)}"
        )
    name = _normalize_required_string(obj.get("name"), context=context, field="name")
    raw_ref = obj.get("ref")
    if isinstance(raw_ref, str) and not raw_ref.strip():
        ref = None
    else:
        ref = _normalize_optional_string(raw_ref, context=context, field="ref")
    return PublicationPersonA(name=name, ref=ref)


def _normalize_people(raw: object, *, context: str) -> tuple[PublicationPersonA, ...]:
    if not isinstance(raw, list) or not raw:
        raise PublicationRecordAError(f"{context}: expected a non-empty JSON array")
    return tuple(
        _normalize_person(entry, context=f"{context}[{index}]")
        for index, entry in enumerate(raw)
    )


def _normalize_badges(raw: object, *, context: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise PublicationRecordAError(f"{context}: badges must be a JSON array or null")
    return tuple(
        _normalize_required_string(
            entry,
            context=f"{context}[{index}]",
            field="badge",
        )
        for index, entry in enumerate(raw)
    )


def _normalize_links(raw: object, *, context: str) -> dict[str, str]:
    if raw is None:
        return {}
    obj = _require_object(raw, context=context)
    unknown_keys = sorted(set(obj) - ALLOWED_LINK_KEYS)
    if unknown_keys:
        raise PublicationRecordAError(
            f"{context}: unknown link keys: {', '.join(unknown_keys)}"
        )
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
        raise PublicationRecordAError(
            f"{context}: unknown identifier keys: {', '.join(unknown_keys)}"
        )
    return {
        key: _normalize_required_string(value, context=context, field=key)
        for key, value in obj.items()
    }


def _normalize_talk(raw: object, *, context: str) -> PublicationTalkA:
    obj = _require_object(raw, context=context)
    unknown_fields = sorted(set(obj) - {"event", "speakers", "url", "embed", "title"})
    if unknown_fields:
        raise PublicationRecordAError(
            f"{context}: unknown fields: {', '.join(unknown_fields)}"
        )
    return PublicationTalkA(
        event=_normalize_required_string(obj.get("event"), context=context, field="event"),
        speakers=_normalize_people(obj.get("speakers"), context=f"{context}.speakers"),
        url=_normalize_required_string(obj.get("url"), context=context, field="url"),
        embed=_normalize_required_string(obj.get("embed"), context=context, field="embed"),
        title=_normalize_optional_string(obj.get("title"), context=context, field="title") or "",
    )


def _normalize_talks(raw: object, *, context: str) -> tuple[PublicationTalkA, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise PublicationRecordAError(f"{context}: talks must be a JSON array or null")
    return tuple(
        _normalize_talk(entry, context=f"{context}[{index}]")
        for index, entry in enumerate(raw)
    )


def load_publication_record_a(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> PublicationRecordA:
    path = publication_record_a_path(root, slug, publications_dir=publications_dir)
    if not path.exists():
        raise PublicationRecordAError(f"Missing publication record: {path}")

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except json.JSONDecodeError as err:
        raise PublicationRecordAError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise PublicationRecordAError(f"{path}: expected a JSON object")

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
        raise PublicationRecordAError(f"{path}: unknown fields: {', '.join(unknown_fields)}")

    slug_year = publication_slug_year(slug)
    draft = _normalize_optional_boolean(raw.get("draft"), context=str(path), field="draft", default=False)
    local_page = _normalize_optional_boolean(
        raw.get("local_page"),
        context=str(path),
        field="local_page",
        default=True,
    )
    time = PublicationTimeA(
        pub_year=_normalize_optional_year(raw.get("pub_year"), context=str(path), field="pub_year"),
        pub_date=_normalize_optional_date(raw.get("pub_date"), context=str(path), field="pub_date"),
    )
    venue = PublicationVenueA(
        full=_normalize_required_string(raw.get("venue"), context=str(path), field="venue"),
        short=_normalize_optional_string(raw.get("venue_short"), context=str(path), field="venue_short"),
    )
    classification = PublicationClassificationA(
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
    record = PublicationRecordA(
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
            raw.get("description"), context=str(path), field="description"
        )
        or "",
        share_description=_normalize_optional_string(
            raw.get("share_description"), context=str(path), field="share_description"
        )
        or "",
        meta_image_path=_normalize_optional_string(
            raw.get("meta_image_path"), context=str(path), field="meta_image_path"
        )
        or "",
        links=_normalize_links(raw.get("links"), context=f"{path}.links"),
        identifiers=_normalize_identifiers(
            raw.get("identifiers"),
            context=f"{path}.identifiers",
        ),
        talks=_normalize_talks(raw.get("talks"), context=f"{path}.talks"),
    )
    _validate_publication_record_a(record, context=str(path), slug_year=slug_year)
    return record


def load_optional_publication_record_a(
    root: Path,
    slug: str,
    *,
    publications_dir: Path | None = None,
) -> PublicationRecordA | None:
    path = publication_record_a_path(root, slug, publications_dir=publications_dir)
    if not path.exists():
        return None
    return load_publication_record_a(root, slug, publications_dir=publications_dir)


def _validate_publication_record_a(
    record: PublicationRecordA,
    *,
    context: str,
    slug_year: int,
) -> None:
    if record.time.pub_year is not None and record.time.pub_year != slug_year:
        raise PublicationRecordAError(
            f"{context}: pub_year must match slug year {slug_year}"
        )

    if record.classification.listing_group is not None:
        if record.classification.listing_group not in ALLOWED_LISTING_GROUPS:
            allowed = ", ".join(sorted(ALLOWED_LISTING_GROUPS))
            raise PublicationRecordAError(
                f"{context}: listing_group must be one of {allowed}"
            )

    if record.classification.pub_type is not None:
        if record.classification.pub_type not in ALLOWED_PUB_TYPES:
            allowed = ", ".join(sorted(ALLOWED_PUB_TYPES))
            raise PublicationRecordAError(
                f"{context}: pub_type must be one of {allowed}"
            )

    if record.local_page:
        if record.primary_link is not None:
            raise PublicationRecordAError(
                f"{context}: primary_link is only valid when local_page is false"
            )
    else:
        if record.primary_link is None:
            raise PublicationRecordAError(
                f"{context}: missing primary_link for thin publication bundle"
            )
        if record.primary_link not in record.links:
            raise PublicationRecordAError(
                f"{context}: primary_link must name a key present in links"
            )

    if record.draft:
        return

    if record.classification.listing_group is None:
        raise PublicationRecordAError(f"{context}: missing listing_group")
    if record.classification.pub_type is None:
        raise PublicationRecordAError(f"{context}: missing pub_type")
    if record.time.pub_year is None:
        raise PublicationRecordAError(f"{context}: missing pub_year")
    if record.venue.short is None:
        raise PublicationRecordAError(f"{context}: missing venue_short")
    if record.local_page and not record.description:
        raise PublicationRecordAError(
            f"{context}: missing description for publication with local_page"
        )
