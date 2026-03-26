#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


NEWS_DATA_NAME = "news.json"
NEWS_ROOT_KEY = "records"
NEWS_ALLOWED_FIELDS = {
    "key",
    "year",
    "month",
    "sort_day",
    "kind",
    "emoji",
    "body_djot",
}
NEWS_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NEWS_KIND_VALUES = (
    "talk",
    "publication",
    "teaching",
    "community",
    "release",
    "recognition",
    "student",
    "media",
    "funding",
    "other",
)
NEWS_KIND_SET = frozenset(NEWS_KIND_VALUES)


class NewsRecordError(ValueError):
    pass


@dataclass(frozen=True)
class NewsRecord:
    key: str
    year: int
    month: int
    kind: str
    emoji: str
    body_djot: str
    sort_day: int | None = None


def news_data_path(root: Path, *, news_path: Path | None = None) -> Path:
    return (news_path or (root / "site" / "data" / NEWS_DATA_NAME)).resolve()


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise NewsRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise NewsRecordError(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise NewsRecordError(f"{context}: missing {field}")
    return raw.strip()


def _require_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not NEWS_KEY_RE.fullmatch(value):
        raise NewsRecordError(f"{context}: invalid {field} {value!r}")
    return value


def _require_year(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise NewsRecordError(f"{context}: {field} must be an integer")
    if raw < 1900 or raw > 2100:
        raise NewsRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _require_month(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise NewsRecordError(f"{context}: {field} must be an integer")
    if raw < 1 or raw > 12:
        raise NewsRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _optional_sort_day(raw: object, *, context: str, field: str) -> int | None:
    if raw is None:
        return None
    if not isinstance(raw, int):
        raise NewsRecordError(f"{context}: {field} must be an integer")
    if raw < 1 or raw > 31:
        raise NewsRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _require_kind(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if value not in NEWS_KIND_SET:
        allowed = ", ".join(NEWS_KIND_VALUES)
        raise NewsRecordError(f"{context}: unknown {field} {value!r}; expected one of {allowed}")
    return value


def _normalize_record(raw: object, *, context: str) -> NewsRecord:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - NEWS_ALLOWED_FIELDS)
    if unknown_fields:
        raise NewsRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_key(rows.get("key"), context=context, field="key")
    year = _require_year(rows.get("year"), context=context, field="year")
    month = _require_month(rows.get("month"), context=context, field="month")
    sort_day = _optional_sort_day(rows.get("sort_day"), context=context, field="sort_day")
    kind = _require_kind(rows.get("kind"), context=context, field="kind")
    emoji = _require_nonempty_string(rows.get("emoji"), context=context, field="emoji")
    body_djot = _require_nonempty_string(rows.get("body_djot"), context=context, field="body_djot")
    return NewsRecord(
        key=key,
        year=year,
        month=month,
        sort_day=sort_day,
        kind=kind,
        emoji=emoji,
        body_djot=body_djot,
    )


def load_news_records(
    root: Path,
    *,
    news_path: Path | None = None,
) -> tuple[NewsRecord, ...]:
    path = news_data_path(root, news_path=news_path)

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise NewsRecordError(f"missing news registry: {path}") from err
    except NewsRecordError as err:
        raise NewsRecordError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise NewsRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {NEWS_ROOT_KEY}:
        unknown = sorted(set(rows) - {NEWS_ROOT_KEY})
        if NEWS_ROOT_KEY not in rows:
            raise NewsRecordError(f"{path}: missing {NEWS_ROOT_KEY}")
        raise NewsRecordError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    records_raw = rows[NEWS_ROOT_KEY]
    if not isinstance(records_raw, list) or not records_raw:
        raise NewsRecordError(f"{path}: {NEWS_ROOT_KEY} must be a non-empty array")

    records = tuple(
        _normalize_record(item, context=f"{path}.records[{index}]")
        for index, item in enumerate(records_raw)
    )

    seen_keys: set[str] = set()
    previous_year_month: tuple[int, int] | None = None
    previous_sort_day: int | None = None
    for record in records:
        if record.key in seen_keys:
            raise NewsRecordError(f"{path}: duplicate record key {record.key!r}")
        seen_keys.add(record.key)

        current_year_month = (record.year, record.month)
        if previous_year_month is not None and current_year_month > previous_year_month:
            raise NewsRecordError(
                f"{path}: records must stay in non-increasing (year, month) order"
            )
        if current_year_month == previous_year_month:
            if previous_sort_day is not None and record.sort_day is not None:
                if record.sort_day > previous_sort_day:
                    raise NewsRecordError(
                        f"{path}: same-month records with sort_day must stay in non-increasing sort_day order"
                    )
        else:
            previous_sort_day = None

        previous_year_month = current_year_month
        previous_sort_day = record.sort_day

    return records


def find_news_record_issues(
    root: Path,
    *,
    news_path: Path | None = None,
) -> list[str]:
    try:
        load_news_records(root, news_path=news_path)
    except NewsRecordError as err:
        return [str(err)]
    return []
