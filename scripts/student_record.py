#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from scripts.sitebuild.people_registry import (
    PERSON_KEY_RE,
    PeopleRegistry,
    PeopleRegistryError,
    load_people_registry,
)

STUDENTS_DATA_NAME = "students.json"
STUDENTS_INDEX_NAME = "index.dj"
STUDENTS_ROOT_KEY = "sections"
SECTION_ALLOWED_FIELDS = {"key", "title", "cv_title", "records"}
RECORD_ALLOWED_FIELDS = {"key", "person_key", "name", "label", "details"}
DETAIL_ALLOWED_FIELDS = {"kind", "title", "url", "person_keys", "djot"}
DETAIL_KIND_THESIS = "thesis"
DETAIL_KIND_COADVISOR = "coadvisor"
DETAIL_KIND_OUTCOME = "outcome"
DETAIL_KIND_NOTE = "note"
DETAIL_KINDS = frozenset(
    {
        DETAIL_KIND_THESIS,
        DETAIL_KIND_COADVISOR,
        DETAIL_KIND_OUTCOME,
        DETAIL_KIND_NOTE,
    }
)
RECORD_KEY_RE = re.compile(PERSON_KEY_RE.pattern)
SECTION_KEY_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class StudentRecordError(ValueError):
    pass


@dataclass(frozen=True)
class StudentDetail:
    kind: str
    title: str | None = None
    url: str | None = None
    person_keys: tuple[str, ...] = ()
    djot: str | None = None


@dataclass(frozen=True)
class StudentRecord:
    key: str
    person_key: str
    name: str
    label: str
    details: tuple[StudentDetail, ...] = ()


@dataclass(frozen=True)
class StudentSection:
    key: str
    title: str
    cv_title: str | None
    records: tuple[StudentRecord, ...]


def students_data_path(root: Path, *, students_path: Path | None = None) -> Path:
    return (students_path or (root / "site" / "data" / STUDENTS_DATA_NAME)).resolve()


def default_students_dir(root: Path) -> Path:
    return (root / "site" / "students").resolve()


def students_index_path(root: Path, *, students_dir: Path | None = None) -> Path:
    return (students_dir or default_students_dir(root)) / STUDENTS_INDEX_NAME


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise StudentRecordError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise StudentRecordError(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise StudentRecordError(f"{context}: missing {field}")
    return raw.strip()


def _require_key(raw: object, *, context: str, field: str, pattern: re.Pattern[str]) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if not pattern.fullmatch(value):
        raise StudentRecordError(
            f"{context}: invalid {field} {value!r}"
        )
    return value


def _require_section_key(raw: object, *, context: str, field: str) -> str:
    value = _require_key(raw, context=context, field=field, pattern=SECTION_KEY_RE)
    if "-" in value:
        raise StudentRecordError(
            f"{context}: invalid {field} {value!r}; expected lowercase words joined by underscores"
        )
    return value


def _require_record_key(raw: object, *, context: str, field: str) -> str:
    value = _require_key(raw, context=context, field=field, pattern=RECORD_KEY_RE)
    if "_" in value:
        raise StudentRecordError(
            f"{context}: invalid {field} {value!r}; expected lowercase words joined by hyphens"
        )
    return value


def _require_person_key(
    raw: object,
    *,
    context: str,
    field: str,
    registry: PeopleRegistry,
) -> str:
    person_key = _require_record_key(raw, context=context, field=field)
    try:
        registry.person(person_key)
    except PeopleRegistryError as err:
        raise StudentRecordError(f"{context}: unknown {field} {person_key!r}") from err
    return person_key


def _require_person_keys(
    raw: object,
    *,
    context: str,
    field: str,
    registry: PeopleRegistry,
) -> tuple[str, ...]:
    if not isinstance(raw, list) or not raw:
        raise StudentRecordError(f"{context}: {field} must be a non-empty array")

    values: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(raw):
        value = _require_record_key(entry, context=f"{context}.{field}[{index}]", field="value")
        if value in seen:
            raise StudentRecordError(f"{context}: duplicate {field} value {value!r}")
        seen.add(value)
        try:
            registry.person(value)
        except PeopleRegistryError as err:
            raise StudentRecordError(f"{context}: unknown {field} value {value!r}") from err
        values.append(value)
    return tuple(values)


def _normalize_detail(
    raw: object,
    *,
    context: str,
    registry: PeopleRegistry,
) -> StudentDetail:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - DETAIL_ALLOWED_FIELDS)
    if unknown_fields:
        raise StudentRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    kind = _require_nonempty_string(rows.get("kind"), context=context, field="kind")
    if kind not in DETAIL_KINDS:
        allowed = ", ".join(sorted(DETAIL_KINDS))
        raise StudentRecordError(f"{context}: unknown kind {kind!r}; expected one of {allowed}")

    if kind == DETAIL_KIND_THESIS:
        title = _require_nonempty_string(rows.get("title"), context=context, field="title")
        url = _require_nonempty_string(rows.get("url"), context=context, field="url")
        unexpected = sorted(
            field for field in ("person_keys", "djot") if rows.get(field) is not None
        )
        if unexpected:
            raise StudentRecordError(
                f"{context}: thesis detail must not include {', '.join(unexpected)}"
            )
        return StudentDetail(kind=kind, title=title, url=url)

    if kind == DETAIL_KIND_COADVISOR:
        person_keys = _require_person_keys(
            rows.get("person_keys"),
            context=context,
            field="person_keys",
            registry=registry,
        )
        unexpected = sorted(
            field for field in ("title", "url", "djot") if rows.get(field) is not None
        )
        if unexpected:
            raise StudentRecordError(
                f"{context}: coadvisor detail must not include {', '.join(unexpected)}"
            )
        return StudentDetail(kind=kind, person_keys=person_keys)

    djot = _require_nonempty_string(rows.get("djot"), context=context, field="djot")
    unexpected = sorted(
        field for field in ("title", "url", "person_keys") if rows.get(field) is not None
    )
    if unexpected:
        raise StudentRecordError(
            f"{context}: {kind} detail must not include {', '.join(unexpected)}"
        )
    return StudentDetail(kind=kind, djot=djot)


def _normalize_details(
    raw: object,
    *,
    context: str,
    registry: PeopleRegistry,
) -> tuple[StudentDetail, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not raw:
        raise StudentRecordError(f"{context}: details must be a non-empty array")

    return tuple(
        _normalize_detail(item, context=f"{context}[{index}]", registry=registry)
        for index, item in enumerate(raw)
    )


def _normalize_record(
    raw: object,
    *,
    context: str,
    registry: PeopleRegistry,
) -> StudentRecord:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - RECORD_ALLOWED_FIELDS)
    if unknown_fields:
        raise StudentRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_record_key(rows.get("key"), context=context, field="key")
    person_key = _require_person_key(
        rows.get("person_key"),
        context=context,
        field="person_key",
        registry=registry,
    )
    name = _require_nonempty_string(rows.get("name"), context=context, field="name")
    label = _require_nonempty_string(rows.get("label"), context=context, field="label")
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        registry=registry,
    )

    return StudentRecord(
        key=key,
        person_key=person_key,
        name=name,
        label=label,
        details=details,
    )


def _normalize_section(
    raw: object,
    *,
    context: str,
    registry: PeopleRegistry,
) -> StudentSection:
    rows = _require_object(raw, context=context)
    unknown_fields = sorted(set(rows) - SECTION_ALLOWED_FIELDS)
    if unknown_fields:
        raise StudentRecordError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    key = _require_section_key(rows.get("key"), context=context, field="key")
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    cv_title_raw = rows.get("cv_title")
    cv_title = None
    if cv_title_raw is not None:
        cv_title = _require_nonempty_string(cv_title_raw, context=context, field="cv_title")

    records_raw = rows.get("records")
    if not isinstance(records_raw, list) or not records_raw:
        raise StudentRecordError(f"{context}: records must be a non-empty array")

    records = tuple(
        _normalize_record(
            item,
            context=f"{context}.records[{index}]",
            registry=registry,
        )
        for index, item in enumerate(records_raw)
    )
    return StudentSection(
        key=key,
        title=title,
        cv_title=cv_title,
        records=records,
    )


def load_student_sections(
    root: Path,
    *,
    students_path: Path | None = None,
    people_path: Path | None = None,
) -> tuple[StudentSection, ...]:
    path = students_data_path(root, students_path=students_path)
    registry_path = (people_path or (root / "site" / "data" / "people.json")).resolve()

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise StudentRecordError(f"missing student registry: {path}") from err
    except StudentRecordError as err:
        raise StudentRecordError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise StudentRecordError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    try:
        registry = load_people_registry(registry_path)
    except PeopleRegistryError as err:
        raise StudentRecordError(str(err)) from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {STUDENTS_ROOT_KEY}:
        unknown = sorted(set(rows) - {STUDENTS_ROOT_KEY})
        if STUDENTS_ROOT_KEY not in rows:
            raise StudentRecordError(f"{path}: missing {STUDENTS_ROOT_KEY}")
        raise StudentRecordError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    sections_raw = rows[STUDENTS_ROOT_KEY]
    if not isinstance(sections_raw, list) or not sections_raw:
        raise StudentRecordError(f"{path}: {STUDENTS_ROOT_KEY} must be a non-empty array")

    sections = tuple(
        _normalize_section(
            item,
            context=f"{path}.sections[{index}]",
            registry=registry,
        )
        for index, item in enumerate(sections_raw)
    )

    seen_section_keys: set[str] = set()
    seen_record_keys: set[str] = set()
    for section in sections:
        if section.key in seen_section_keys:
            raise StudentRecordError(f"{path}: duplicate section key {section.key!r}")
        seen_section_keys.add(section.key)

        for record in section.records:
            if record.key in seen_record_keys:
                raise StudentRecordError(f"{path}: duplicate record key {record.key!r}")
            seen_record_keys.add(record.key)

    return sections


def find_student_record_issues(
    root: Path,
    *,
    students_path: Path | None = None,
    people_path: Path | None = None,
) -> list[str]:
    try:
        load_student_sections(root, students_path=students_path, people_path=people_path)
    except StudentRecordError as err:
        return [str(err)]
    return []
