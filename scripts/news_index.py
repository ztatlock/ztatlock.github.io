#!/usr/bin/env python3

from __future__ import annotations

import calendar
from pathlib import Path

from scripts.news_record import NewsRecord, NewsRecordError, load_news_records


NEWS_INDEX_NAME = "index.dj"
NEWS_MONTH_GROUPS_PLACEHOLDER = "__NEWS_MONTH_GROUPS__"
HOMEPAGE_NEWS_MONTH_GROUPS_PLACEHOLDER = "__HOMEPAGE_NEWS_MONTH_GROUPS__"


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


def _render_news_month_groups(records: tuple[NewsRecord, ...]) -> str:
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


def _load_news_records_for_projection(
    root: Path,
    *,
    news_path: Path | None = None,
) -> tuple[NewsRecord, ...]:
    try:
        return load_news_records(root, news_path=news_path)
    except NewsRecordError as err:
        raise NewsIndexError(str(err)) from err


def _months_since(latest: tuple[int, int], candidate: tuple[int, int]) -> int:
    latest_year, latest_month = latest
    candidate_year, candidate_month = candidate
    return (latest_year - candidate_year) * 12 + (latest_month - candidate_month)


def _select_homepage_news_records(records: tuple[NewsRecord, ...]) -> tuple[NewsRecord, ...]:
    latest_year_month = (records[0].year, records[0].month)
    window_records = tuple(
        record
        for record in records
        if 0 <= _months_since(latest_year_month, (record.year, record.month)) <= 11
    )
    if len(window_records) <= 15:
        return window_records

    selected_keys = {record.key for record in window_records[:10]}
    older_records = window_records[10:]

    for record in older_records:
        if len(selected_keys) >= 15:
            break
        if record.homepage_featured:
            selected_keys.add(record.key)

    for record in older_records:
        if len(selected_keys) >= 15:
            break
        selected_keys.add(record.key)

    return tuple(record for record in window_records if record.key in selected_keys)


def render_public_news_month_groups_djot(
    root: Path,
    *,
    news_path: Path | None = None,
) -> str:
    records = _load_news_records_for_projection(root, news_path=news_path)
    return _render_news_month_groups(records)


def render_homepage_news_month_groups_djot(
    root: Path,
    *,
    news_path: Path | None = None,
) -> str:
    records = _load_news_records_for_projection(root, news_path=news_path)
    selected = _select_homepage_news_records(records)
    return _render_news_month_groups(selected)
