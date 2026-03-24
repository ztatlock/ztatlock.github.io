#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


TEACHING_DATA_NAME = "teaching.json"
TEACHING_ROOT_KEY = "groups"
GROUP_ALLOWED_FIELDS = {"key", "records"}
RECORD_ALLOWED_FIELDS = {
    "key",
    "kind",
    "code",
    "title",
    "institution",
    "audience_label",
    "description_djot",
    "offerings",
    "details",
    "events",
}
OFFERING_ALLOWED_FIELDS = {"year", "term", "url"}
EVENT_ALLOWED_FIELDS = {"label", "url", "links"}
LINK_ALLOWED_FIELDS = {"label", "url"}
GROUP_KEY_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
RECORD_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEACHING_GROUP_KEYS = (
    "uw_courses",
    "special_topics",
    "summer_school",
    "teaching_assistant",
)
TEACHING_GROUP_KEY_SET = frozenset(TEACHING_GROUP_KEYS)
RECORD_KIND_COURSE = "course"
RECORD_KIND_SUMMER_SCHOOL = "summer_school"
RECORD_KINDS = frozenset({RECORD_KIND_COURSE, RECORD_KIND_SUMMER_SCHOOL})
OFFERING_TERMS = ("Winter", "Spring", "Summer", "Autumn")
OFFERING_TERM_SET = frozenset(OFFERING_TERMS)


class TeachingRecordError(ValueError):
    pass


@dataclass(frozen=True)
class TeachingLink:
    label: str
    url: str


@dataclass(frozen=True)
class TeachingOffering:
    year: int
    term: str
    url: str | None = None


@dataclass(frozen=True)
class TeachingEvent:
    label: str
    url: str
    links: tuple[TeachingLink, ...] = ()


@dataclass(frozen=True)
class TeachingRecord:
    key: str
    kind: str
    title: str
    code: str | None = None
    institution: str | None = None
    audience_label: str | None = None
    description_djot: str | None = None
    offerings: tuple[TeachingOffering, ...] = ()
    details: tuple[str, ...] = ()
    events: tuple[TeachingEvent, ...] = ()


@dataclass(frozen=True)
class TeachingGroup:
    key: str
    records: tuple[TeachingRecord, ...]


def teaching_data_path(root: Path, *, teaching_path: Path | None = None) -> Path:
    return (teaching_path or (root / "site" / "data" / TEACHING_DATA_NAME)).resolve()


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise TeachingRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise TeachingRecordError(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise TeachingRecordError(f"{context}: missing {field}")
    return raw.strip()


def _optional_nonempty_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    return _require_nonempty_string(raw, context=context, field=field)


def _require_group_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not GROUP_KEY_RE.fullmatch(value):
        raise TeachingRecordError(f"{context}: invalid {field} {value!r}")
    if value not in TEACHING_GROUP_KEY_SET:
        allowed = ", ".join(TEACHING_GROUP_KEYS)
        raise TeachingRecordError(
            f"{context}: unknown {field} {value!r}; expected one of {allowed}"
        )
    return value


def _require_record_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not RECORD_KEY_RE.fullmatch(value):
        raise TeachingRecordError(f"{context}: invalid {field} {value!r}")
    return value


def _normalize_link(raw: object, *, context: str) -> TeachingLink:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - LINK_ALLOWED_FIELDS)
    if unknown_fields:
        raise TeachingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")
    label = _require_nonempty_string(rows.get("label"), context=context, field="label")
    url = _require_nonempty_string(rows.get("url"), context=context, field="url")
    return TeachingLink(label=label, url=url)


def _normalize_links(raw: object, *, context: str) -> tuple[TeachingLink, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not raw:
        raise TeachingRecordError(f"{context}: links must be a non-empty array")

    links = tuple(
        _normalize_link(item, context=f"{context}[{index}]")
        for index, item in enumerate(raw)
    )
    seen: set[tuple[str, str]] = set()
    for link in links:
        key = (link.label, link.url)
        if key in seen:
            raise TeachingRecordError(
                f"{context}: duplicate link {link.label!r} -> {link.url!r}"
            )
        seen.add(key)
    return links


def _require_year(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise TeachingRecordError(f"{context}: {field} must be an integer")
    if raw < 1900 or raw > 2100:
        raise TeachingRecordError(f"{context}: invalid {field} {raw!r}")
    return raw


def _require_term(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if value not in OFFERING_TERM_SET:
        allowed = ", ".join(OFFERING_TERMS)
        raise TeachingRecordError(
            f"{context}: invalid {field} {value!r}; expected one of {allowed}"
        )
    return value


def _normalize_offering(raw: object, *, context: str) -> TeachingOffering:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - OFFERING_ALLOWED_FIELDS)
    if unknown_fields:
        raise TeachingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")
    year = _require_year(rows.get("year"), context=context, field="year")
    term = _require_term(rows.get("term"), context=context, field="term")
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url")
    return TeachingOffering(year=year, term=term, url=url)


def _normalize_offerings(raw: object, *, context: str) -> tuple[TeachingOffering, ...]:
    if not isinstance(raw, list) or not raw:
        raise TeachingRecordError(f"{context}: offerings must be a non-empty array")

    offerings = tuple(
        _normalize_offering(item, context=f"{context}[{index}]")
        for index, item in enumerate(raw)
    )
    seen: set[tuple[int, str]] = set()
    for offering in offerings:
        key = (offering.year, offering.term)
        if key in seen:
            raise TeachingRecordError(
                f"{context}: duplicate offering {offering.term} {offering.year}"
            )
        seen.add(key)
    return offerings


def _normalize_event(raw: object, *, context: str) -> TeachingEvent:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - EVENT_ALLOWED_FIELDS)
    if unknown_fields:
        raise TeachingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")
    label = _require_nonempty_string(rows.get("label"), context=context, field="label")
    url = _require_nonempty_string(rows.get("url"), context=context, field="url")
    links = _normalize_links(rows.get("links"), context=f"{context}.links")
    return TeachingEvent(label=label, url=url, links=links)


def _normalize_events(raw: object, *, context: str) -> tuple[TeachingEvent, ...]:
    if not isinstance(raw, list) or not raw:
        raise TeachingRecordError(f"{context}: events must be a non-empty array")

    events = tuple(
        _normalize_event(item, context=f"{context}[{index}]")
        for index, item in enumerate(raw)
    )
    seen: set[str] = set()
    for event in events:
        if event.label in seen:
            raise TeachingRecordError(f"{context}: duplicate event label {event.label!r}")
        seen.add(event.label)
    return events


def _normalize_details(raw: object, *, context: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not raw:
        raise TeachingRecordError(f"{context}: details must be a non-empty array")
    return tuple(
        _require_nonempty_string(item, context=f"{context}[{index}]", field="value")
        for index, item in enumerate(raw)
    )


def _normalize_record(raw: object, *, context: str, group_key: str) -> TeachingRecord:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - RECORD_ALLOWED_FIELDS)
    if unknown_fields:
        raise TeachingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_record_key(rows.get("key"), context=context, field="key")
    kind = _require_nonempty_string(rows.get("kind"), context=context, field="kind")
    if kind not in RECORD_KINDS:
        allowed = ", ".join(sorted(RECORD_KINDS))
        raise TeachingRecordError(f"{context}: unknown kind {kind!r}; expected one of {allowed}")

    title = _require_nonempty_string(rows.get("title"), context=context, field="title")

    if group_key == "summer_school":
        if kind != RECORD_KIND_SUMMER_SCHOOL:
            raise TeachingRecordError(
                f"{context}: summer_school group records must use kind {RECORD_KIND_SUMMER_SCHOOL!r}"
            )
    elif kind != RECORD_KIND_COURSE:
        raise TeachingRecordError(
            f"{context}: non-summer-school groups must use kind {RECORD_KIND_COURSE!r}"
        )

    if kind == RECORD_KIND_COURSE:
        code = _require_nonempty_string(rows.get("code"), context=context, field="code")
        institution = _optional_nonempty_string(
            rows.get("institution"),
            context=context,
            field="institution",
        )
        audience_label = _optional_nonempty_string(
            rows.get("audience_label"),
            context=context,
            field="audience_label",
        )
        description_djot = _optional_nonempty_string(
            rows.get("description_djot"),
            context=context,
            field="description_djot",
        )
        offerings = _normalize_offerings(rows.get("offerings"), context=f"{context}.offerings")
        details = _normalize_details(rows.get("details"), context=f"{context}.details")
        if description_djot is None and not details:
            raise TeachingRecordError(
                f"{context}: course records must include description_djot or details"
            )
        unexpected = sorted(field for field in ("events",) if rows.get(field) is not None)
        if unexpected:
            raise TeachingRecordError(
                f"{context}: course record must not include {', '.join(unexpected)}"
            )
        return TeachingRecord(
            key=key,
            kind=kind,
            title=title,
            code=code,
            institution=institution,
            audience_label=audience_label,
            description_djot=description_djot,
            offerings=offerings,
            details=details,
        )

    events = _normalize_events(rows.get("events"), context=f"{context}.events")
    unexpected = sorted(
        field
        for field in (
            "code",
            "institution",
            "audience_label",
            "description_djot",
            "offerings",
            "details",
        )
        if rows.get(field) is not None
    )
    if unexpected:
        raise TeachingRecordError(
            f"{context}: summer_school record must not include {', '.join(unexpected)}"
        )
    return TeachingRecord(
        key=key,
        kind=kind,
        title=title,
        events=events,
    )


def _normalize_group(raw: object, *, context: str) -> TeachingGroup:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - GROUP_ALLOWED_FIELDS)
    if unknown_fields:
        raise TeachingRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_group_key(rows.get("key"), context=context, field="key")
    records_raw = rows.get("records")
    if not isinstance(records_raw, list) or not records_raw:
        raise TeachingRecordError(f"{context}: records must be a non-empty array")

    records = tuple(
        _normalize_record(item, context=f"{context}.records[{index}]", group_key=key)
        for index, item in enumerate(records_raw)
    )
    return TeachingGroup(key=key, records=records)


def load_teaching_groups(
    root: Path,
    *,
    teaching_path: Path | None = None,
) -> tuple[TeachingGroup, ...]:
    path = teaching_data_path(root, teaching_path=teaching_path)

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise TeachingRecordError(f"missing teaching registry: {path}") from err
    except TeachingRecordError as err:
        raise TeachingRecordError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise TeachingRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {TEACHING_ROOT_KEY}:
        unknown = sorted(set(rows) - {TEACHING_ROOT_KEY})
        if TEACHING_ROOT_KEY not in rows:
            raise TeachingRecordError(f"{path}: missing {TEACHING_ROOT_KEY}")
        raise TeachingRecordError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    groups_raw = rows[TEACHING_ROOT_KEY]
    if not isinstance(groups_raw, list) or not groups_raw:
        raise TeachingRecordError(f"{path}: {TEACHING_ROOT_KEY} must be a non-empty array")

    groups = tuple(
        _normalize_group(item, context=f"{path}.groups[{index}]")
        for index, item in enumerate(groups_raw)
    )

    seen_group_keys: set[str] = set()
    seen_record_keys: set[str] = set()
    for group in groups:
        if group.key in seen_group_keys:
            raise TeachingRecordError(f"{path}: duplicate group key {group.key!r}")
        seen_group_keys.add(group.key)
        for record in group.records:
            if record.key in seen_record_keys:
                raise TeachingRecordError(f"{path}: duplicate record key {record.key!r}")
            seen_record_keys.add(record.key)

    missing_group_keys = [key for key in TEACHING_GROUP_KEYS if key not in seen_group_keys]
    if missing_group_keys:
        raise TeachingRecordError(
            f"{path}: missing group keys: {', '.join(missing_group_keys)}"
        )

    return groups


def find_teaching_record_issues(
    root: Path,
    *,
    teaching_path: Path | None = None,
) -> list[str]:
    try:
        load_teaching_groups(root, teaching_path=teaching_path)
    except TeachingRecordError as err:
        return [str(err)]
    return []
