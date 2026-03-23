#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from scripts.publication_record import PublicationPerson, publication_year

PUBLICATIONS_INDEX_NAME = "publications.dj"
LISTING_GROUP_BY_SECTION = {
    "Conference and Journal Papers": "main",
    "Workshop Papers": "workshop",
}
AGGREGATORS_HEADING = "Aggregators"
ENTRY_RE = re.compile(r"^\{#(?P<slug>[^}]+)\}$", re.MULTILINE)
TITLE_RE = re.compile(r"^\*\[(?P<title>.*?)\]\((?P<link>.*?)\)\* \\\n", re.DOTALL)
PERSON_RE = re.compile(r"^\[(?P<name>[^\]]+)\]\[(?P<ref>[^\]]*)\]$")


class PublicationIndexError(ValueError):
    pass


@dataclass(frozen=True)
class PublicationIndexEntry:
    slug: str
    listing_group: str
    title: str
    title_url: str
    authors: tuple[PublicationPerson, ...]
    venue: str
    badges: tuple[str, ...]


def publications_index_path(root: Path, *, page_source_dir: Path | None = None) -> Path:
    pages_dir = page_source_dir or (root / "site" / "pages")
    return pages_dir / PUBLICATIONS_INDEX_NAME


def _normalized_url(raw: str) -> str:
    lines = [line.strip() for line in raw.splitlines()]
    return "".join(lines).strip()


def _normalized_line(line: str) -> str:
    text = line.strip()
    if text.endswith("\\"):
        text = text[:-1].rstrip()
    return text


def _parse_person(line: str, *, context: str) -> PublicationPerson:
    text = line
    if text.startswith("  "):
        text = text[2:]
    elif text.startswith("\\ "):
        text = text[2:]
    text = _normalized_line(text).rstrip(",").strip()
    if not text:
        raise PublicationIndexError(f"{context}: empty author line")

    match = PERSON_RE.fullmatch(text)
    if match is None:
        return PublicationPerson(name=text, ref="")
    return PublicationPerson(
        name=match.group("name"),
        ref=match.group("ref"),
    )


def _parse_entry_block(
    slug: str,
    listing_group: str,
    block: str,
    *,
    path: Path,
) -> PublicationIndexEntry:
    title_match = TITLE_RE.match(block)
    if title_match is None:
        raise PublicationIndexError(f"{path}: malformed entry block for {slug}")

    title = title_match.group("title").strip()
    title_url = _normalized_url(title_match.group("link"))
    remainder = block[title_match.end() :].strip("\n")
    if not remainder:
        raise PublicationIndexError(f"{path}: missing entry body for {slug}")

    lines: list[str] = []
    for raw_line in remainder.splitlines():
        if not raw_line.strip():
            continue
        if raw_line.strip() == ":::":
            break
        lines.append(raw_line.rstrip())
    author_lines: list[str] = []
    index = 0
    while index < len(lines) and (
        lines[index].startswith("  ") or lines[index].startswith("\\ ")
    ):
        author_lines.append(lines[index])
        index += 1

    if not author_lines:
        raise PublicationIndexError(f"{path}: missing authors for {slug}")

    venue_lines = lines[index:]
    if venue_lines and venue_lines[0].strip() == "\\":
        venue_lines = venue_lines[1:]
    if not venue_lines:
        raise PublicationIndexError(f"{path}: missing venue for {slug}")

    normalized_venue_lines = [_normalized_line(line) for line in venue_lines if _normalized_line(line)]
    venue_line = normalized_venue_lines[0]
    year = publication_year(slug)
    suffix = f" {year}"
    if not venue_line.endswith(suffix):
        raise PublicationIndexError(
            f"{path}: venue line for {slug} must end with publication year {year}"
        )
    venue = venue_line[: -len(suffix)]
    badges = tuple(normalized_venue_lines[1:])

    return PublicationIndexEntry(
        slug=slug,
        listing_group=listing_group,
        title=title,
        title_url=title_url,
        authors=tuple(
            _parse_person(line, context=f"{path}: {slug}")
            for line in author_lines
        ),
        venue=venue,
        badges=badges,
    )


def load_publications_index_entries(
    root: Path,
    *,
    page_source_dir: Path | None = None,
) -> tuple[PublicationIndexEntry, ...]:
    path = publications_index_path(root, page_source_dir=page_source_dir)
    if not path.exists():
        raise PublicationIndexError(f"Missing publications index source: {path}")

    text = path.read_text(encoding="utf-8")
    entries: list[PublicationIndexEntry] = []
    seen_slugs: set[str] = set()
    section_positions = [
        (heading, text.find(f"## {heading}"))
        for heading in (*LISTING_GROUP_BY_SECTION.keys(), AGGREGATORS_HEADING)
    ]
    if any(position < 0 for _, position in section_positions):
        missing = ", ".join(heading for heading, position in section_positions if position < 0)
        raise PublicationIndexError(f"{path}: missing expected section headings: {missing}")

    ordered_sections = sorted(section_positions, key=lambda item: item[1])
    for index, (heading, start) in enumerate(ordered_sections):
        if heading == AGGREGATORS_HEADING:
            break
        end = ordered_sections[index + 1][1]
        section_text = text[start:end]
        listing_group = LISTING_GROUP_BY_SECTION[heading]
        matches = list(ENTRY_RE.finditer(section_text))
        for entry_index, match in enumerate(matches):
            slug = match.group("slug")
            if slug in seen_slugs:
                raise PublicationIndexError(f"{path}: duplicate publication slug in index: {slug}")
            block_start = match.end()
            block_end = matches[entry_index + 1].start() if entry_index + 1 < len(matches) else len(section_text)
            block = section_text[block_start:block_end].strip()
            entries.append(
                _parse_entry_block(
                    slug,
                    listing_group,
                    block,
                    path=path,
                )
            )
            seen_slugs.add(slug)

    return tuple(entries)
