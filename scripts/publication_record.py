#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.publication_record_a import (
    ALLOWED_IDENTIFIER_KEYS,
    ALLOWED_LINK_KEYS,
    ALLOWED_LISTING_GROUPS,
    ALLOWED_PUB_TYPES,
    PUBLICATION_RECORD_NAME,
    SITE_PUBLICATIONS_PATH,
    PublicationClassificationA as PublicationClassification,
    PublicationPersonA as PublicationPerson,
    PublicationRecordA as PublicationRecord,
    PublicationRecordAError as PublicationRecordError,
    PublicationTalkA as PublicationTalk,
    PublicationTimeA as PublicationTime,
    PublicationVenueA as PublicationVenue,
    default_publications_dir,
    load_optional_publication_record_a as load_optional_publication_record,
    load_publication_record_a as load_publication_record,
    publication_dir,
    publication_display_year,
    publication_index_title_url_a as publication_index_title_url,
    publication_order_key_a as publication_order_key,
    publication_page_path,
    publication_slug_year as publication_year,
)

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


def publication_record_path(root: Path, slug: str, *, publications_dir: Path | None = None) -> Path:
    return publication_dir(root, slug, publications_dir=publications_dir) / PUBLICATION_RECORD_NAME


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
