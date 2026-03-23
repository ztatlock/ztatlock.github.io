#!/usr/bin/env python3

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

TALK_RECORD_NAME = "talk.json"
TALKS_INDEX_NAME = "index.dj"
EXTRA_CONTENT_NAME = "extra.dj"
ALLOWED_SEASONS = frozenset({"spring", "summer", "fall", "winter"})
SEASON_ORDER = {
    "winter": 1,
    "spring": 4,
    "summer": 7,
    "fall": 10,
}


class TalkRecordError(ValueError):
    pass


@dataclass(frozen=True)
class TalkDate:
    year: int
    month: int | None = None
    season: str | None = None


@dataclass(frozen=True)
class TalkAt:
    text: str
    url: str | None = None


@dataclass(frozen=True)
class TalkRecord:
    slug: str
    title: str
    when: TalkDate
    at: tuple[TalkAt, ...]
    url: str | None = None


def talks_root(root: Path, *, talks_dir: Path | None = None) -> Path:
    return (talks_dir or (root / "site" / "talks")).resolve()


def talks_index_path(root: Path, *, talks_dir: Path | None = None) -> Path:
    return talks_root(root, talks_dir=talks_dir) / TALKS_INDEX_NAME


def talk_dir(root: Path, slug: str, *, talks_dir: Path | None = None) -> Path:
    return talks_root(root, talks_dir=talks_dir) / slug


def talk_record_path(root: Path, slug: str, *, talks_dir: Path | None = None) -> Path:
    return talk_dir(root, slug, talks_dir=talks_dir) / TALK_RECORD_NAME


def talk_extra_path(root: Path, slug: str, *, talks_dir: Path | None = None) -> Path:
    return talk_dir(root, slug, talks_dir=talks_dir) / EXTRA_CONTENT_NAME


def discover_talk_slugs(root: Path, *, talks_dir: Path | None = None) -> tuple[str, ...]:
    actual_talks_dir = talks_root(root, talks_dir=talks_dir)
    if not actual_talks_dir.exists():
        return ()
    return tuple(
        path.name
        for path in sorted(actual_talks_dir.iterdir())
        if path.is_dir()
    )


def talk_sort_key(record: TalkRecord) -> tuple[int, int, str]:
    month_or_season = record.when.month
    if month_or_season is None:
        month_or_season = SEASON_ORDER[record.when.season or "winter"]
    return (record.when.year, month_or_season, record.slug)


def render_talk_date(date: TalkDate) -> str:
    if date.month is not None:
        month_name = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )[date.month - 1]
        return f"{month_name} {date.year}"
    season = date.season or "winter"
    return f"{season.capitalize()} {date.year}"


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise TalkRecordError(f"{context}: must be a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise TalkRecordError(f"{context}: must be a non-empty string")
    return raw.strip()


def _normalize_optional_url(raw: object, *, context: str) -> str | None:
    if raw is None:
        return None
    value = _require_nonempty_string(raw, context=context)
    return value


def _normalize_talk_date(raw: object, *, context: str) -> TalkDate:
    rows = _require_object(raw, context=context)
    allowed_keys = {"year", "month", "season"}
    unknown = sorted(set(rows) - allowed_keys)
    if unknown:
        raise TalkRecordError(f"{context}: unknown keys: {', '.join(unknown)}")

    year = rows.get("year")
    if not isinstance(year, int):
        raise TalkRecordError(f"{context}.year: must be an integer")

    month = rows.get("month")
    season = rows.get("season")
    if (month is None) == (season is None):
        raise TalkRecordError(f"{context}: must provide exactly one of month or season")

    if month is not None:
        if not isinstance(month, int) or not (1 <= month <= 12):
            raise TalkRecordError(f"{context}.month: must be an integer in 1..12")
        return TalkDate(year=year, month=month)

    if not isinstance(season, str) or season not in ALLOWED_SEASONS:
        allowed = ", ".join(sorted(ALLOWED_SEASONS))
        raise TalkRecordError(f"{context}.season: must be one of {allowed}")
    return TalkDate(year=year, season=season)


def _normalize_at_segments(raw: object, *, context: str) -> tuple[TalkAt, ...]:
    if not isinstance(raw, list) or not raw:
        raise TalkRecordError(f"{context}: must be a non-empty JSON array")

    segments: list[TalkAt] = []
    for index, item in enumerate(raw):
        rows = _require_object(item, context=f"{context}[{index}]")
        allowed_keys = {"text", "url"}
        unknown = sorted(set(rows) - allowed_keys)
        if unknown:
            raise TalkRecordError(f"{context}[{index}]: unknown keys: {', '.join(unknown)}")
        text = _require_nonempty_string(rows.get("text"), context=f"{context}[{index}].text")
        url = _normalize_optional_url(rows.get("url"), context=f"{context}[{index}].url")
        segments.append(TalkAt(text=text, url=url))
    return tuple(segments)


def load_talk_record(
    root: Path,
    slug: str,
    *,
    talks_dir: Path | None = None,
) -> TalkRecord:
    path = talk_record_path(root, slug, talks_dir=talks_dir)
    if not path.exists():
        raise TalkRecordError(f"Missing talk record: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise TalkRecordError(f"{path}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    allowed_keys = {"title", "when", "at", "url"}
    unknown = sorted(set(rows) - allowed_keys)
    if unknown:
        raise TalkRecordError(f"{path}: unknown keys: {', '.join(unknown)}")

    title = _require_nonempty_string(rows.get("title"), context=f"{path}.title")
    when = _normalize_talk_date(rows.get("when"), context=f"{path}.when")
    at = _normalize_at_segments(rows.get("at"), context=f"{path}.at")
    url = _normalize_optional_url(rows.get("url"), context=f"{path}.url")

    return TalkRecord(
        slug=slug,
        title=title,
        when=when,
        at=at,
        url=url,
    )


def load_talk_records(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> tuple[TalkRecord, ...]:
    records = [
        load_talk_record(root, slug, talks_dir=talks_dir)
        for slug in discover_talk_slugs(root, talks_dir=talks_dir)
    ]
    return tuple(sorted(records, key=talk_sort_key, reverse=True))


def find_talk_record_issues(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    actual_talks_dir = talks_root(root, talks_dir=talks_dir)
    if not actual_talks_dir.exists():
        return issues

    for path in sorted(actual_talks_dir.iterdir()):
        if path.name == TALKS_INDEX_NAME and path.is_file():
            continue
        if not path.is_dir():
            issues.append(f"{path}: talk bundles must be directories")
            continue

        record_path = path / TALK_RECORD_NAME
        if not record_path.exists():
            issues.append(f"{path}: missing {TALK_RECORD_NAME}")
            continue

        try:
            load_talk_record(root, path.name, talks_dir=actual_talks_dir)
        except TalkRecordError as err:
            issues.append(str(err))

    return issues


def main() -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
