#!/usr/bin/env python3

from __future__ import annotations

import calendar
from pathlib import Path

from scripts.news_record import NewsRecordError, load_news_records


NEWS_INDEX_NAME = "index.dj"
NEWS_MONTH_GROUPS_PLACEHOLDER = "__NEWS_MONTH_GROUPS__"


class NewsIndexError(ValueError):
    pass


def news_index_path(root: Path, *, news_dir: Path | None = None) -> Path:
    actual_news_dir = news_dir or (root / "site" / "news")
    return (actual_news_dir / NEWS_INDEX_NAME).resolve()


def _render_news_item_djot(body_djot: str, *, emoji: str) -> str:
    lines = body_djot.splitlines() or [body_djot]
    rendered = [f"  {emoji} \\ {lines[0]}"]
    rendered.extend(f"  {line}" if line else "" for line in lines[1:])
    return "\n".join(rendered)


def render_public_news_month_groups_djot(
    root: Path,
    *,
    news_path: Path | None = None,
) -> str:
    try:
        records = load_news_records(root, news_path=news_path)
    except NewsRecordError as err:
        raise NewsIndexError(str(err)) from err

    chunks: list[str] = []
    current_group: tuple[int, int] | None = None
    current_items: list[str] = []

    def flush_current_group() -> None:
        nonlocal current_group, current_items
        if current_group is None:
            return
        year, month = current_group
        chunk = f": {calendar.month_name[month]} {year}\n\n" + "\n\n".join(current_items)
        chunks.append(chunk)
        current_group = None
        current_items = []

    for record in records:
        group = (record.year, record.month)
        if current_group is None:
            current_group = group
        elif group != current_group:
            flush_current_group()
            current_group = group
        current_items.append(_render_news_item_djot(record.body_djot, emoji=record.emoji))

    flush_current_group()
    rendered = "\n\n".join(chunks)
    return rendered + ("\n" if rendered else "")
