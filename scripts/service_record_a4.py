#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from scripts.sitebuild.people_registry import (
    PeopleRegistry,
    PeopleRegistryError,
    load_people_registry,
)


SERVICE_DATA_NAME = "service.json"
SERVICE_INDEX_NAME = "index.dj"
SERVICE_ROOT_KEY = "records"
SERVICE_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SERVICE_VIEW_GROUPS = ("reviewing", "organizing", "mentoring", "department")
SERVICE_VIEW_GROUP_SET = frozenset(SERVICE_VIEW_GROUPS)
SYNTHESIZED_INSTANCE_KEY_PREFIX = "__service-instance__:"
PEOPLE_REF_RE = re.compile(r"(?<!!)\[([^\[\]]+)\]\[([^\[\]]*)\]")

SINGLETON_FIELDS = frozenset(
    {
        "key",
        "year",
        "view_groups",
        "anchor_view_group",
        "title",
        "role",
        "url",
        "details",
        "time_basis",
        "ongoing",
    }
)
SHORTHAND_FIELDS = frozenset(
    {
        "key",
        "title",
        "role",
        "url",
        "details",
        "view_groups",
        "anchor_view_group",
        "time_basis",
        "ongoing",
        "instances",
    }
)
EXPLICIT_FIELDS = frozenset(
    {
        "key",
        "title",
        "role",
        "url",
        "details",
        "runs",
    }
)
RUN_FIELDS = frozenset(
    {
        "key",
        "view_groups",
        "anchor_view_group",
        "title",
        "role",
        "url",
        "details",
        "time_basis",
        "ongoing",
        "instances",
    }
)
INSTANCE_FIELDS = frozenset({"key", "year", "title", "role", "url", "details"})


class ServiceRecordA4Error(ValueError):
    pass


@dataclass(frozen=True)
class ServiceSeriesA4:
    key: str
    title: str
    role: str | None = None
    url: str | None = None
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class ServiceInstanceA4:
    key: str
    authored_key: str | None
    year: int
    title: str
    role: str | None = None
    url: str | None = None
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class ServiceRunA4:
    key: str
    parent_record_key: str
    series: ServiceSeriesA4 | None
    view_groups: tuple[str, ...]
    anchor_view_group: str
    title: str
    role: str | None = None
    url: str | None = None
    details: tuple[str, ...] = ()
    time_basis: str | None = None
    ongoing: bool = False
    instances: tuple[ServiceInstanceA4, ...] = ()


@dataclass(frozen=True)
class ServiceRecordA4:
    key: str
    form: str
    series: ServiceSeriesA4 | None
    runs: tuple[ServiceRunA4, ...]


@dataclass(frozen=True)
class ServiceRegistryA4:
    records: tuple[ServiceRecordA4, ...]
    runs: tuple[ServiceRunA4, ...]

    def record(self, key: str) -> ServiceRecordA4:
        for record in self.records:
            if record.key == key:
                return record
        raise KeyError(key)

    def run(self, key: str) -> ServiceRunA4:
        for run in self.runs:
            if run.key == key:
                return run
        raise KeyError(key)


def service_data_path(root: Path, *, service_path: Path | None = None) -> Path:
    return (service_path or (root / "site" / "data" / SERVICE_DATA_NAME)).resolve()


def service_index_path(root: Path, *, service_dir: Path | None = None) -> Path:
    actual_service_dir = service_dir or (root / "site" / "service")
    return (actual_service_dir / SERVICE_INDEX_NAME).resolve()


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ServiceRecordA4Error(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_object(raw: object, *, context: str) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ServiceRecordA4Error(f"{context}: expected a JSON object")
    return raw


def _require_nonempty_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ServiceRecordA4Error(f"{context}: missing {field}")
    return raw.strip()


def _optional_nonempty_string(raw: object, *, context: str, field: str) -> str | None:
    if raw is None:
        return None
    return _require_nonempty_string(raw, context=context, field=field)


def _require_key(raw: object, *, context: str, field: str) -> str:
    value = _require_nonempty_string(raw, context=context, field=field)
    if value.startswith(SYNTHESIZED_INSTANCE_KEY_PREFIX):
        raise ServiceRecordA4Error(
            f"{context}: {field} must not use reserved synthesized-instance-id namespace"
        )
    if not SERVICE_KEY_RE.fullmatch(value):
        raise ServiceRecordA4Error(f"{context}: invalid {field} {value!r}")
    return value


def _require_year(raw: object, *, context: str, field: str) -> int:
    if not isinstance(raw, int):
        raise ServiceRecordA4Error(f"{context}: {field} must be an integer")
    if raw < 1900 or raw > 2100:
        raise ServiceRecordA4Error(f"{context}: invalid {field} {raw!r}")
    return raw


def _normalize_bool(raw: object, *, context: str, field: str) -> bool:
    if raw is None:
        return False
    if not isinstance(raw, bool):
        raise ServiceRecordA4Error(f"{context}: {field} must be a boolean")
    return raw


def _normalize_role(raw: object, *, context: str, field: str) -> str | None:
    value = _optional_nonempty_string(raw, context=context, field=field)
    if value is None:
        return None
    return re.sub(r"\s+", " ", value)


def _normalize_view_groups(raw: object, *, context: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not raw:
        raise ServiceRecordA4Error(f"{context}: view_groups must be a non-empty array")

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
            raise ServiceRecordA4Error(
                f"{context}: unknown view_group {value!r}; expected one of {allowed}"
            )
        if value in seen:
            raise ServiceRecordA4Error(f"{context}: duplicate view_group {value!r}")
        seen.add(value)
        values.append(value)
    return tuple(values)


def _load_people_registry_if_available(
    root: Path,
    *,
    people_path: Path | None = None,
) -> PeopleRegistry | None:
    path = (people_path or (root / "site" / "data" / "people.json")).resolve()
    if not path.exists():
        return None
    try:
        return load_people_registry(path)
    except PeopleRegistryError as err:
        raise ServiceRecordA4Error(str(err)) from err


def _normalize_details(
    raw: object,
    *,
    context: str,
    people_registry: PeopleRegistry | None,
) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not raw:
        raise ServiceRecordA4Error(f"{context}: details must be a non-empty array")

    values: list[str] = []
    for index, item in enumerate(raw):
        value = _require_nonempty_string(
            item,
            context=f"{context}[{index}]",
            field="value",
        )
        if people_registry is not None:
            for match in PEOPLE_REF_RE.finditer(value):
                display_label, explicit_label = match.groups()
                label = display_label if explicit_label == "" else explicit_label.strip()
                if not label:
                    continue
                person_key = people_registry.alias_to_key.get(label)
                if person_key is None:
                    continue
                if people_registry.person(person_key).primary_url is None:
                    raise ServiceRecordA4Error(
                        f"{context}[{index}]: details must not target linkless person label {label!r}"
                    )
        values.append(value)
    return tuple(values)


def _normalize_time_basis(raw: object, *, context: str, field: str) -> str | None:
    return _optional_nonempty_string(raw, context=context, field=field)


def _normalize_anchor_view_group(
    raw: object,
    *,
    context: str,
    view_groups: tuple[str, ...],
) -> str:
    value = _optional_nonempty_string(raw, context=context, field="anchor_view_group")
    if len(view_groups) == 1:
        if value is None:
            return view_groups[0]
        if value != view_groups[0]:
            raise ServiceRecordA4Error(
                f"{context}: anchor_view_group must equal the sole view_group {view_groups[0]!r}"
            )
        return value
    if value is None:
        raise ServiceRecordA4Error(
            f"{context}: anchor_view_group is required when multiple view_groups are present"
        )
    if value not in view_groups:
        raise ServiceRecordA4Error(
            f"{context}: anchor_view_group {value!r} must be one of the run's view_groups"
        )
    return value


def _check_unknown_fields(
    rows: dict[str, object],
    *,
    allowed_fields: frozenset[str],
    context: str,
) -> None:
    unknown_fields = sorted(set(rows) - allowed_fields)
    if unknown_fields:
        raise ServiceRecordA4Error(f"{context}: unknown fields: {', '.join(unknown_fields)}")


def _synthesized_instance_key(*, run_key: str, index: int) -> str:
    return f"{SYNTHESIZED_INSTANCE_KEY_PREFIX}{run_key}:{index}"


def _validate_run_instance_shape(
    instances: tuple[ServiceInstanceA4, ...],
    *,
    context: str,
) -> None:
    if not instances:
        raise ServiceRecordA4Error(f"{context}: instances must be a non-empty array")

    seen_instance_keys: set[str] = set()
    years_to_authored_keys: dict[int, int] = {}
    unique_years: set[int] = set()
    for instance in instances:
        if instance.key in seen_instance_keys:
            raise ServiceRecordA4Error(f"{context}: duplicate instance key {instance.key!r}")
        seen_instance_keys.add(instance.key)
        unique_years.add(instance.year)
        if instance.authored_key is not None:
            years_to_authored_keys[instance.year] = years_to_authored_keys.get(instance.year, 0) + 1

    year_counts: dict[int, int] = {}
    for instance in instances:
        year_counts[instance.year] = year_counts.get(instance.year, 0) + 1
    for year, count in year_counts.items():
        if count > 1:
            if years_to_authored_keys.get(year, 0) != count:
                raise ServiceRecordA4Error(
                    f"{context}: same-year multiplicity requires explicit instance.key for year {year}"
                )

    years = sorted(unique_years)
    if years and years != list(range(years[0], years[-1] + 1)):
        raise ServiceRecordA4Error(f"{context}: run years must form one contiguous sequence")


def _normalize_instance(
    raw: object,
    *,
    context: str,
    run_key: str,
    index: int,
    default_title: str,
    default_role: str | None,
    default_url: str | None,
    default_details: tuple[str, ...],
    people_registry: PeopleRegistry | None,
) -> ServiceInstanceA4:
    rows = _require_object(raw, context=context)
    _check_unknown_fields(rows, allowed_fields=INSTANCE_FIELDS, context=context)

    authored_key = None
    if rows.get("key") is not None:
        authored_key = _require_key(rows.get("key"), context=context, field="key")
    year = _require_year(rows.get("year"), context=context, field="year")
    title = _optional_nonempty_string(rows.get("title"), context=context, field="title") or default_title
    role = _normalize_role(rows.get("role"), context=context, field="role")
    if role is None:
        role = default_role
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url") or default_url
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        people_registry=people_registry,
    )
    if not details:
        details = default_details

    return ServiceInstanceA4(
        key=authored_key or _synthesized_instance_key(run_key=run_key, index=index),
        authored_key=authored_key,
        year=year,
        title=title,
        role=role,
        url=url,
        details=details,
    )


def _normalize_run(
    raw: object,
    *,
    context: str,
    parent_record_key: str,
    series: ServiceSeriesA4,
    people_registry: PeopleRegistry | None,
) -> ServiceRunA4:
    rows = _require_object(raw, context=context)
    _check_unknown_fields(rows, allowed_fields=RUN_FIELDS, context=context)

    key = _require_key(rows.get("key"), context=context, field="key")
    view_groups = _normalize_view_groups(rows.get("view_groups"), context=f"{context}.view_groups")
    anchor_view_group = _normalize_anchor_view_group(
        rows.get("anchor_view_group"),
        context=context,
        view_groups=view_groups,
    )
    title = _optional_nonempty_string(rows.get("title"), context=context, field="title") or series.title
    role = _normalize_role(rows.get("role"), context=context, field="role")
    if role is None:
        role = series.role
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url") or series.url
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        people_registry=people_registry,
    )
    if not details:
        details = series.details
    time_basis = _normalize_time_basis(rows.get("time_basis"), context=context, field="time_basis")
    ongoing = _normalize_bool(rows.get("ongoing"), context=context, field="ongoing")

    instances_raw = rows.get("instances")
    if not isinstance(instances_raw, list) or not instances_raw:
        raise ServiceRecordA4Error(f"{context}: instances must be a non-empty array")
    instances = tuple(
        _normalize_instance(
            item,
            context=f"{context}.instances[{index}]",
            run_key=key,
            index=index,
            default_title=title,
            default_role=role,
            default_url=url,
            default_details=details,
            people_registry=people_registry,
        )
        for index, item in enumerate(instances_raw)
    )
    _validate_run_instance_shape(instances, context=f"{context}.instances")

    return ServiceRunA4(
        key=key,
        parent_record_key=parent_record_key,
        series=series,
        view_groups=view_groups,
        anchor_view_group=anchor_view_group,
        title=title,
        role=role,
        url=url,
        details=details,
        time_basis=time_basis,
        ongoing=ongoing,
        instances=instances,
    )


def _normalize_singleton_record(
    rows: dict[str, object],
    *,
    context: str,
    people_registry: PeopleRegistry | None,
) -> ServiceRecordA4:
    _check_unknown_fields(rows, allowed_fields=SINGLETON_FIELDS, context=context)

    key = _require_key(rows.get("key"), context=context, field="key")
    year = _require_year(rows.get("year"), context=context, field="year")
    view_groups = _normalize_view_groups(rows.get("view_groups"), context=f"{context}.view_groups")
    anchor_view_group = _normalize_anchor_view_group(
        rows.get("anchor_view_group"),
        context=context,
        view_groups=view_groups,
    )
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    role = _normalize_role(rows.get("role"), context=context, field="role")
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url")
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        people_registry=people_registry,
    )
    time_basis = _normalize_time_basis(rows.get("time_basis"), context=context, field="time_basis")
    ongoing = _normalize_bool(rows.get("ongoing"), context=context, field="ongoing")

    instance = ServiceInstanceA4(
        key=_synthesized_instance_key(run_key=key, index=0),
        authored_key=None,
        year=year,
        title=title,
        role=role,
        url=url,
        details=details,
    )
    run = ServiceRunA4(
        key=key,
        parent_record_key=key,
        series=None,
        view_groups=view_groups,
        anchor_view_group=anchor_view_group,
        title=title,
        role=role,
        url=None,
        details=(),
        time_basis=time_basis,
        ongoing=ongoing,
        instances=(instance,),
    )
    return ServiceRecordA4(
        key=key,
        form="singleton",
        series=None,
        runs=(run,),
    )


def _normalize_shorthand_record(
    rows: dict[str, object],
    *,
    context: str,
    people_registry: PeopleRegistry | None,
) -> ServiceRecordA4:
    _check_unknown_fields(rows, allowed_fields=SHORTHAND_FIELDS, context=context)

    key = _require_key(rows.get("key"), context=context, field="key")
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    view_groups = _normalize_view_groups(rows.get("view_groups"), context=f"{context}.view_groups")
    anchor_view_group = _normalize_anchor_view_group(
        rows.get("anchor_view_group"),
        context=context,
        view_groups=view_groups,
    )
    role = _normalize_role(rows.get("role"), context=context, field="role")
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url")
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        people_registry=people_registry,
    )
    time_basis = _normalize_time_basis(rows.get("time_basis"), context=context, field="time_basis")
    ongoing = _normalize_bool(rows.get("ongoing"), context=context, field="ongoing")

    instances_raw = rows.get("instances")
    if not isinstance(instances_raw, list) or not instances_raw:
        raise ServiceRecordA4Error(f"{context}: instances must be a non-empty array")

    series = ServiceSeriesA4(
        key=key,
        title=title,
    )
    instances = tuple(
        _normalize_instance(
            item,
            context=f"{context}.instances[{index}]",
            run_key=key,
            index=index,
            default_title=title,
            default_role=role,
            default_url=url,
            default_details=details,
            people_registry=people_registry,
        )
        for index, item in enumerate(instances_raw)
    )
    _validate_run_instance_shape(instances, context=f"{context}.instances")

    run = ServiceRunA4(
        key=key,
        parent_record_key=key,
        series=series,
        view_groups=view_groups,
        anchor_view_group=anchor_view_group,
        title=title,
        role=role,
        url=url,
        details=details,
        time_basis=time_basis,
        ongoing=ongoing,
        instances=instances,
    )
    return ServiceRecordA4(
        key=key,
        form="shorthand",
        series=series,
        runs=(run,),
    )


def _normalize_explicit_record(
    rows: dict[str, object],
    *,
    context: str,
    people_registry: PeopleRegistry | None,
) -> ServiceRecordA4:
    _check_unknown_fields(rows, allowed_fields=EXPLICIT_FIELDS, context=context)

    key = _require_key(rows.get("key"), context=context, field="key")
    title = _require_nonempty_string(rows.get("title"), context=context, field="title")
    role = _normalize_role(rows.get("role"), context=context, field="role")
    url = _optional_nonempty_string(rows.get("url"), context=context, field="url")
    details = _normalize_details(
        rows.get("details"),
        context=f"{context}.details",
        people_registry=people_registry,
    )
    runs_raw = rows.get("runs")
    if not isinstance(runs_raw, list) or not runs_raw:
        raise ServiceRecordA4Error(f"{context}: runs must be a non-empty array")

    series = ServiceSeriesA4(
        key=key,
        title=title,
        role=role,
        url=url,
        details=details,
    )
    runs = tuple(
        _normalize_run(
            item,
            context=f"{context}.runs[{index}]",
            parent_record_key=key,
            series=series,
            people_registry=people_registry,
        )
        for index, item in enumerate(runs_raw)
    )
    return ServiceRecordA4(
        key=key,
        form="explicit",
        series=series,
        runs=runs,
    )


def _normalize_record(
    raw: object,
    *,
    context: str,
    people_registry: PeopleRegistry | None,
) -> ServiceRecordA4:
    rows = _require_object(raw, context=context)

    present_form_fields = [field for field in ("year", "instances", "runs") if field in rows]
    if len(present_form_fields) != 1:
        raise ServiceRecordA4Error(
            f"{context}: exactly one of year, instances, or runs is required"
        )

    if "year" in rows:
        return _normalize_singleton_record(rows, context=context, people_registry=people_registry)
    if "instances" in rows:
        return _normalize_shorthand_record(rows, context=context, people_registry=people_registry)
    return _normalize_explicit_record(rows, context=context, people_registry=people_registry)


def load_service_registry_a4(
    root: Path,
    *,
    service_path: Path | None = None,
    people_path: Path | None = None,
) -> ServiceRegistryA4:
    path = service_data_path(root, service_path=service_path)

    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise ServiceRecordA4Error(f"missing service registry: {path}") from err
    except ServiceRecordA4Error as err:
        raise ServiceRecordA4Error(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise ServiceRecordA4Error(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    rows = _require_object(raw, context=str(path))
    if set(rows) != {SERVICE_ROOT_KEY}:
        unknown = sorted(set(rows) - {SERVICE_ROOT_KEY})
        if SERVICE_ROOT_KEY not in rows:
            raise ServiceRecordA4Error(f"{path}: missing {SERVICE_ROOT_KEY}")
        raise ServiceRecordA4Error(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    records_raw = rows[SERVICE_ROOT_KEY]
    if not isinstance(records_raw, list) or not records_raw:
        raise ServiceRecordA4Error(f"{path}: {SERVICE_ROOT_KEY} must be a non-empty array")

    people_registry = _load_people_registry_if_available(root, people_path=people_path)
    records = tuple(
        _normalize_record(
            item,
            context=f"{path}.records[{index}]",
            people_registry=people_registry,
        )
        for index, item in enumerate(records_raw)
    )

    seen_record_keys: set[str] = set()
    run_key_to_record_key: dict[str, str] = {}
    runs: list[ServiceRunA4] = []

    for record in records:
        if record.key in seen_record_keys:
            raise ServiceRecordA4Error(f"{path}: duplicate top-level record key {record.key!r}")
        seen_record_keys.add(record.key)

    for record in records:
        for run in record.runs:
            owner = run_key_to_record_key.get(run.key)
            if owner is not None:
                raise ServiceRecordA4Error(f"{path}: duplicate canonical run key {run.key!r}")
            run_key_to_record_key[run.key] = record.key
            runs.append(run)

    for run in runs:
        owner = run_key_to_record_key.get(run.key)
        if run.key in seen_record_keys and run.key != run.parent_record_key:
            raise ServiceRecordA4Error(
                f"{path}: run key {run.key!r} collides with unrelated top-level record key"
            )
        if owner is not None and owner != run.parent_record_key:
            raise ServiceRecordA4Error(
                f"{path}: run key {run.key!r} collides with unrelated top-level record key"
            )

    return ServiceRegistryA4(records=records, runs=tuple(runs))


def find_service_record_a4_issues(
    root: Path,
    *,
    service_path: Path | None = None,
    people_path: Path | None = None,
) -> list[str]:
    try:
        load_service_registry_a4(root, service_path=service_path, people_path=people_path)
    except ServiceRecordA4Error as err:
        return [str(err)]
    return []
