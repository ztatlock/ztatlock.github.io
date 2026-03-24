"""Helpers for rendering projection-backed collection pages."""

from __future__ import annotations

from pathlib import Path

from scripts.publication_index import (
    PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
    PublicationIndexError,
    render_publications_list_djot,
)
from scripts.talk_record import TalkRecordError, load_talk_records, render_talk_date

TALKS_LIST_PLACEHOLDER = "__TALKS_LIST__"


class PageProjectionError(ValueError):
    pass


def _render_segment_text(text: str, url: str | None) -> str:
    if not url:
        return text
    return f"[{text}]({url})"


def _render_title(title: str, url: str | None) -> str:
    if not url:
        return title
    return f"[{title}]({url})"


def render_talks_list_djot(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> str:
    try:
        records = load_talk_records(root, talks_dir=talks_dir)
    except TalkRecordError as err:
        raise PageProjectionError(str(err)) from err

    chunks: list[str] = []
    for record in records:
        title = _render_title(record.title, record.url)
        at_text = ", ".join(_render_segment_text(segment.text, segment.url) for segment in record.at)
        date_text = render_talk_date(record.when)
        chunks.append(f"- {title} \\\n  {at_text}, {date_text}")
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def apply_page_projections(
    route_kind: str,
    route_key: str,
    body: str,
    *,
    root: Path,
    talks_dir: Path | None = None,
    publications_dir: Path | None = None,
) -> str:
    if route_kind == "talks_index_page" and route_key == "talks" and TALKS_LIST_PLACEHOLDER in body:
        rendered = render_talks_list_djot(root, talks_dir=talks_dir).rstrip()
        return body.replace(TALKS_LIST_PLACEHOLDER, rendered)

    if route_kind == "publications_index_page" and route_key == "publications":
        try:
            rendered_main = render_publications_list_djot(
                root,
                "main",
                publications_dir=publications_dir,
            ).rstrip()
            rendered_workshop = render_publications_list_djot(
                root,
                "workshop",
                publications_dir=publications_dir,
            ).rstrip()
        except PublicationIndexError as err:
            raise PageProjectionError(str(err)) from err
        return (
            body.replace(PUBLICATIONS_MAIN_LIST_PLACEHOLDER, rendered_main).replace(
                PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
                rendered_workshop,
            )
        )

    return body
