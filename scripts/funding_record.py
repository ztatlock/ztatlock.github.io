#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


FUNDING_DATA_NAME = "funding.json"
FUNDING_ROOT_KEY = "records"
FUNDING_ALLOWED_FIELDS = {
    "key",
    "title",
    "role",
    "sponsor",
    "award_id",
    "amount_usd",
    "start_year",
    "end_year",
}
FUNDING_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class FundingRecordError(ValueError):
    pass


@dataclass(frozen=True)
class FundingRecord:
    key: str
    title: str
    role: str
    sponsor: str
    amount_usd: int
    start_year: int
    end_year: int
    award_id: str | None = None


def funding_data_path(root: Path, *, funding_path: Path | None = None) -> Path:
    return (funding_path or (root / "site" / "data" / FUNDING_DATA_NAME)).resolve()


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise FundingRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise FundingRecordError(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise FundingRecordError(f"{context}: missing {field}")
    return raw.strip()


def _optional_nonempty_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    return _require_nonempty_string(raw, context=context, field=field)


def _require_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not FUNDING_KEY_RE.fullmatch(value):
        raise FundingRecordError(f"{context}: invalid {field} {value!r}")
    return value


def _require_year(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise FundingRecordError(f"{context}: {field} must be an integer")
    if raw < 1900 or raw > 2100:
        raise FundingRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _require_amount_usd(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise FundingRecordError(f"{context}: {field} must be an integer")
    if raw <= 0:
        raise FundingRecordError(f"{context}: {field} must be positive")
    return raw


def _normalize_record(raw: object, *, context: str) -> FundingRecord:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - FUNDING_ALLOWED_FIELDS)
    if unknown_fields:
        raise FundingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_key(rows.get("key"), context=context, field="key")
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    role = _require_nonempty_string(rows.get("role"), context=context, field="role")
    sponsor = _require_nonempty_string(rows.get("sponsor"), context=context, field="sponsor")
    award_id = _optional_nonempty_string(rows.get("award_id"), context=context, field="award_id")
    amount_usd = _require_amount_usd(rows.get("amount_usd"), context=context, field="amount_usd")
    start_year = _require_year(rows.get("start_year"), context=context, field="start_year")
    end_year = _require_year(rows.get("end_year"), context=context, field="end_year")
    if start_year > end_year:
        raise FundingRecordError(
            f"{context}: start_year {start_year} must not exceed end_year {end_year}"
        )

    return FundingRecord(
        key=key,
        title=title,
        role=role,
        sponsor=sponsor,
        award_id=award_id,
        amount_usd=amount_usd,
        start_year=start_year,
        end_year=end_year,
    )


def load_funding_records(
    root: Path,
    *,
    funding_path: Path | None = None,
) -> tuple[FundingRecord, ...]:
    path = funding_data_path(root, funding_path=funding_path)

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise FundingRecordError(f"missing funding registry: {path}") from err
    except FundingRecordError as err:
        raise FundingRecordError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise FundingRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {FUNDING_ROOT_KEY}:
        unknown = sorted(set(rows) - {FUNDING_ROOT_KEY})
        if FUNDING_ROOT_KEY not in rows:
            raise FundingRecordError(f"{path}: missing {FUNDING_ROOT_KEY}")
        raise FundingRecordError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    records_raw = rows[FUNDING_ROOT_KEY]
    if not isinstance(records_raw, list) or not records_raw:
        raise FundingRecordError(f"{path}: {FUNDING_ROOT_KEY} must be a non-empty array")

    records = tuple(
        _normalize_record(item, context=f"{path}.records[{index}]")
        for index, item in enumerate(records_raw)
    )

    seen_keys: set[str] = set()
    for record in records:
        if record.key in seen_keys:
            raise FundingRecordError(f"{path}: duplicate record key {record.key!r}")
        seen_keys.add(record.key)

    return records


def find_funding_record_issues(
    root: Path,
    *,
    funding_path: Path | None = None,
) -> list[str]:
    try:
        load_funding_records(root, funding_path=funding_path)
    except FundingRecordError as err:
        return [str(err)]
    return []
