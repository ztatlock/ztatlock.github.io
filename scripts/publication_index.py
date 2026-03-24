#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from scripts.publication_record import (
    PublicationRecord,
    PublicationRecordError,
    default_publications_dir,
    load_publication_record,
    render_publication_index_entry,
)

PUBLICATIONS_INDEX_NAME = "index.dj"
PUBLICATIONS_MAIN_LIST_PLACEHOLDER = "__PUBLICATIONS_MAIN_LIST__"
PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER = "__PUBLICATIONS_WORKSHOP_LIST__"
PLACEHOLDER_BY_LISTING_GROUP = {
    "main": PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    "workshop": PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
}


class PublicationIndexError(ValueError):
    pass


def publications_index_path(root: Path, *, publications_dir: Path | None = None) -> Path:
    actual_publications_dir = publications_dir or default_publications_dir(root)
    return actual_publications_dir / PUBLICATIONS_INDEX_NAME


def _publication_sort_key(record: PublicationRecord) -> tuple[int, str]:
    if record.pub_date is None:
        raise PublicationIndexError(f"{record.slug}: missing pub_date")
    return (-record.pub_date.toordinal(), record.title)


def load_publication_index_records(
    root: Path,
    *,
    publications_dir: Path | None = None,
) -> tuple[PublicationRecord, ...]:
    actual_publications_dir = publications_dir or default_publications_dir(root)
    records: list[PublicationRecord] = []
    try:
        for path in sorted(actual_publications_dir.glob("*/publication.json")):
            record = load_publication_record(
                root,
                path.parent.name,
                publications_dir=actual_publications_dir,
            )
            if record.draft:
                continue
            records.append(record)
    except PublicationRecordError as err:
        raise PublicationIndexError(str(err)) from err
    return tuple(sorted(records, key=_publication_sort_key))


def render_publications_list_djot(
    root: Path,
    listing_group: str,
    *,
    publications_dir: Path | None = None,
) -> str:
    if listing_group not in PLACEHOLDER_BY_LISTING_GROUP:
        allowed = ", ".join(sorted(PLACEHOLDER_BY_LISTING_GROUP))
        raise PublicationIndexError(
            f"unsupported publication listing group {listing_group!r}; expected one of {allowed}"
        )
    chunks = [
        render_publication_index_entry(record)
        for record in load_publication_index_records(root, publications_dir=publications_dir)
        if record.listing_group == listing_group
    ]
    return "\n\n".join(chunks) + ("\n" if chunks else "")
