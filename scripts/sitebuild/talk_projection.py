"""Helpers for rendering talks-page projections from talk bundles."""

from __future__ import annotations

from pathlib import Path

from scripts.talk_record import TalkRecordError, load_talk_records, render_talk_date

TALKS_LIST_PLACEHOLDER = "__TALKS_LIST__"


class TalkProjectionError(ValueError):
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
        raise TalkProjectionError(str(err)) from err

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
) -> str:
    if route_kind != "talks_index_page" or route_key != "talks" or TALKS_LIST_PLACEHOLDER not in body:
        return body
    rendered = render_talks_list_djot(root, talks_dir=talks_dir).rstrip()
    return body.replace(TALKS_LIST_PLACEHOLDER, rendered)
