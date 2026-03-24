#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


SERVICE_DATA_NAME = "service.json"
SERVICE_ROOT_KEY = "records"
SERVICE_ALLOWED_FIELDS = {
    "key",
    "series_key",
    "year",
    "view_groups",
    "title",
    "role",
    "url",
    "details",
}
SERVICE_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SERVICE_VIEW_GROUPS = ("reviewing", "organizing", "mentoring", "department")
SERVICE_VIEW_GROUP_SET = frozenset(SERVICE_VIEW_GROUPS)


class ServiceRecordError(ValueError):
    pass


@dataclass(frozen=True)
class ServiceRecord:
    key: str
    year: int
    view_groups: tuple[str, ...]
    title: str
    series_key: str | None = None
    role: str | None = None
    url: str | None = None
    details: tuple[str, ...] = ()


def service_data_path(root: Path, *, service_path: Path | None = None) -> Path:
    return (service_path or (root / "site" / "data" / SERVICE_DATA_NAME)).resolve()


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ServiceRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ServiceRecordError(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ServiceRecordError(f"{context}: missing {field}")
    return raw.strip()


def _optional_nonempty_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    return _require_nonempty_string(raw, context=context, field=field)


def _require_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not SERVICE_KEY_RE.fullmatch(value):
        raise ServiceRecordError(f"{context}: invalid {field} {value!r}")
    return value


def _require_year(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise ServiceRecordError(f"{context}: {field} must be an integer")
    if raw < 1900 or raw > 2100:
        raise ServiceRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _normalize_view_groups(raw: object, *, context: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not raw:
        raise ServiceRecordError(f"{context}: view_groups must be a non-empty array")

    values: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        value = _require_nonempty_string(
            item,
            context=f"{context}[{index}]",
            field="value",
        )
        if value not in SERVICE_VIEW_GROUP_SET:
            allowed = ", ".join(SERVICE_VIEW_GROUPS)
            raise ServiceRecordError(
                f"{context}: unknown view_group {value!r}; expected one of {allowed}"
            )
        if value in seen:
            raise ServiceRecordError(f"{context}: duplicate view_group {value!r}")
        seen.add(value)
        values.append(value)
    return tuple(values)


def _normalize_details(raw: object, *, context: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not raw:
        raise ServiceRecordError(f"{context}: details must be a non-empty array")

    values: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        value = _require_nonempty_string(
            item,
            context=f"{context}[{index}]",
            field="value",
        )
        if value in seen:
            raise ServiceRecordError(f"{context}: duplicate detail {value!r}")
        seen.add(value)
        values.append(value)
    return tuple(values)


def _normalize_record(raw: object, *, context: str) -> ServiceRecord:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - SERVICE_ALLOWED_FIELDS)
    if unknown_fields:
        raise ServiceRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_key(rows.get("key"), context=context, field="key")
    series_key = None
    if rows.get("series_key") is not None:
        series_key = _require_key(rows.get("series_key"), context=context, field="series_key")
    year = _require_year(rows.get("year"), context=context, field="year")
    view_groups = _normalize_view_groups(rows.get("view_groups"), context=f"{context}.view_groups")
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    role = _optional_nonempty_string(rows.get("role"), context=context, field="role")
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url")
    details = _normalize_details(rows.get("details"), context=f"{context}.details")
    return ServiceRecord(
        key=key,
        series_key=series_key,
        year=year,
        view_groups=view_groups,
        title=title,
        role=role,
        url=url,
        details=details,
    )


def load_service_records(
    root: Path,
    *,
    service_path: Path | None = None,
) -> tuple[ServiceRecord, ...]:
    path = service_data_path(root, service_path=service_path)

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise ServiceRecordError(f"missing service registry: {path}") from err
    except ServiceRecordError as err:
        raise ServiceRecordError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise ServiceRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {SERVICE_ROOT_KEY}:
        unknown = sorted(set(rows) - {SERVICE_ROOT_KEY})
        if SERVICE_ROOT_KEY not in rows:
            raise ServiceRecordError(f"{path}: missing {SERVICE_ROOT_KEY}")
        raise ServiceRecordError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    records_raw = rows[SERVICE_ROOT_KEY]
    if not isinstance(records_raw, list) or not records_raw:
        raise ServiceRecordError(f"{path}: {SERVICE_ROOT_KEY} must be a non-empty array")

    records = tuple(
        _normalize_record(item, context=f"{path}.records[{index}]")
        for index, item in enumerate(records_raw)
    )

    seen_keys: set[str] = set()
    for record in records:
        if record.key in seen_keys:
            raise ServiceRecordError(f"{path}: duplicate record key {record.key!r}")
        seen_keys.add(record.key)

    return records


def find_service_record_issues(
    root: Path,
    *,
    service_path: Path | None = None,
) -> list[str]:
    try:
        load_service_records(root, service_path=service_path)
    except ServiceRecordError as err:
        return [str(err)]
    return []
