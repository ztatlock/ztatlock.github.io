#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

SITE_PUBLICATIONS_PATH = Path("site") / "pubs"
PUBLICATION_RECORD_NAME = "publication.json"
EXTRA_CONTENT_NAME = "extra.dj"
IMAGE_EXTENSIONS = (".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg")
SLIDES_EXTENSIONS = (".pdf", ".pptx")
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
    ref: str


@dataclass(frozen=True)
class PublicationTalk:
    event: str
    speakers: tuple[PublicationPerson, ...]
    url: str
    embed: str
    title: str


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


@dataclass(frozen=True)
class PublicationRecord:
    slug: str
    draft: bool
    title: str
    authors: tuple[PublicationPerson, ...]
    venue: str
    badges: tuple[str, ...]
    description: str
    share_description: str
    meta_image_path: str
    links: dict[str, str]
    talks: tuple[PublicationTalk, ...]


def publication_slug(page_stem: str) -> str | None:
    if page_stem.startswith("pub-"):
        return page_stem.removeprefix("pub-")
    return None


def default_publications_dir(root: Path) -> Path:
    return root / SITE_PUBLICATIONS_PATH


def publication_dir(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    base_dir = publications_dir or default_publications_dir(root)
    return base_dir / slug


def publication_record_path(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    return publication_dir(root, slug, publications_dir=publications_dir) / PUBLICATION_RECORD_NAME


def publication_page_stem(slug: str) -> str:
    return f"pub-{slug}"


def publication_page_path(slug: str) -> str:
    return f"pubs/{slug}/"


def publication_year(slug: str) -> str:
    year, _, _ = slug.partition("-")
    if len(year) != 4 or not year.isdigit():
        raise PublicationRecordError(f"{slug}: invalid publication slug; expected YEAR-...")
    return year


def default_meta_image_path(slug: str) -> str:
    return f"pubs/{slug}/{slug}-meta.png"


def relative_site_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def relative_publication_site_path(path: Path, *, publications_dir: Path) -> str:
    return f"pubs/{path.relative_to(publications_dir).as_posix()}"


def _normalize_optional_string(
    raw: object,
    *,
    context: str,
    field: str,
) -> str:
    if raw is None:
        return ""
    if not isinstance(raw, str):
        raise PublicationRecordError(f"{context}: {field} must be a string or null")
    return raw.strip()


def _normalize_optional_boolean(
    raw: object,
    *,
    context: str,
    field: str,
) -> bool:
    if raw is None:
        return False
    if not isinstance(raw, bool):
        raise PublicationRecordError(f"{context}: {field} must be a boolean or null")
    return raw


def _normalize_required_string(
    raw: object,
    *,
    context: str,
    field: str,
) -> str:
    value = _normalize_optional_string(raw, context=context, field=field)
    if not value:
        raise PublicationRecordError(f"{context}: missing {field}")
    return value


def _normalize_person(raw: object, *, context: str) -> PublicationPerson:
    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{context}: expected a JSON object")

    unknown_fields = sorted(set(raw) - {"name", "ref"})
    if unknown_fields:
        raise PublicationRecordError(
            f"{context}: unknown fields: {', '.join(unknown_fields)}"
        )

    name = _normalize_required_string(raw.get("name"), context=context, field="name")
    ref = _normalize_optional_string(raw.get("ref"), context=context, field="ref")
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

    badges: list[str] = []
    for index, entry in enumerate(raw):
        badge = _normalize_required_string(
            entry,
            context=f"{context}[{index}]",
            field="badge",
        )
        badges.append(badge)
    return tuple(badges)


def _normalize_links(raw: object, *, context: str) -> dict[str, str]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{context}: links must be a JSON object or null")

    unknown_keys = sorted(set(raw) - ALLOWED_LINK_KEYS)
    if unknown_keys:
        raise PublicationRecordError(
            f"{context}: unknown link keys: {', '.join(unknown_keys)}"
        )

    links: dict[str, str] = {}
    for key, value in raw.items():
        normalized = _normalize_required_string(value, context=context, field=key)
        links[key] = normalized
    return links


def _normalize_talk(raw: object, *, context: str) -> PublicationTalk:
    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{context}: expected a JSON object")

    unknown_fields = sorted(set(raw) - {"event", "speakers", "url", "embed", "title"})
    if unknown_fields:
        raise PublicationRecordError(
            f"{context}: unknown fields: {', '.join(unknown_fields)}"
        )

    event = _normalize_required_string(raw.get("event"), context=context, field="event")
    speakers = _normalize_people(raw.get("speakers"), context=f"{context}.speakers")
    url = _normalize_required_string(raw.get("url"), context=context, field="url")
    embed = _normalize_required_string(raw.get("embed"), context=context, field="embed")
    title = _normalize_optional_string(raw.get("title"), context=context, field="title")
    return PublicationTalk(
        event=event,
        speakers=speakers,
        url=url,
        embed=embed,
        title=title,
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
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise PublicationRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise PublicationRecordError(f"{path}: expected a JSON object")

    unknown_fields = sorted(
        set(raw)
        - {
            "draft",
            "title",
            "authors",
            "venue",
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

    publication_year(slug)

    return PublicationRecord(
        slug=slug,
        draft=_normalize_optional_boolean(raw.get("draft"), context=str(path), field="draft"),
        title=_normalize_required_string(raw.get("title"), context=str(path), field="title"),
        authors=_normalize_people(raw.get("authors"), context=f"{path}.authors"),
        venue=_normalize_required_string(raw.get("venue"), context=str(path), field="venue"),
        badges=_normalize_badges(raw.get("badges"), context=f"{path}.badges"),
        description=_normalize_required_string(
            raw.get("description"), context=str(path), field="description"
        ),
        share_description=_normalize_optional_string(
            raw.get("share_description"),
            context=str(path),
            field="share_description",
        ),
        meta_image_path=_normalize_optional_string(
            raw.get("meta_image_path"),
            context=str(path),
            field="meta_image_path",
        ),
        links=_normalize_links(raw.get("links"), context=f"{path}.links"),
        talks=_normalize_talks(raw.get("talks"), context=f"{path}.talks"),
    )


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
    if record.meta_image_path:
        return record.meta_image_path

    actual_publications_dir = publications_dir or default_publications_dir(root)
    assets = publication_assets(root, record.slug, publications_dir=actual_publications_dir)
    if assets.metaimg is not None:
        return relative_publication_site_path(assets.metaimg, publications_dir=actual_publications_dir)
    return relative_publication_site_path(assets.absimg, publications_dir=actual_publications_dir)


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
    line = f"{record.venue} {publication_year(record.slug)}"
    if not record.badges:
        return line
    return line + " \\\n" + " \\\n".join(record.badges)


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
        links["slides"] = relative_publication_site_path(assets.slides, publications_dir=publications_dir)
    if assets.poster is not None:
        links["poster"] = relative_publication_site_path(assets.poster, publications_dir=publications_dir)

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
    actual_publications_dir = publications_dir or default_publications_dir(root)
    assets = publication_assets(root, record.slug, publications_dir=actual_publications_dir)
    abstract_text = assets.abstract.read_text(encoding="utf-8").strip()
    bib_text = assets.bib.read_text(encoding="utf-8").rstrip()
    extra_text = assets.extra.read_text(encoding="utf-8").strip() if assets.extra else ""

    preview_image = relative_publication_site_path(assets.absimg, publications_dir=actual_publications_dir)
    paper_path = relative_publication_site_path(assets.paper, publications_dir=actual_publications_dir)

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

    blocks.extend(["", "", "[📝 publications index](publications.html)"])
    return "\n".join(blocks) + "\n"
