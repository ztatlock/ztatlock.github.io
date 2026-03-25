#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from scripts.service_record import ServiceRecord, ServiceRecordError, load_service_records


SERVICE_REVIEWING_LIST_PLACEHOLDER = "__SERVICE_REVIEWING_LIST__"
SERVICE_ORGANIZING_LIST_PLACEHOLDER = "__SERVICE_ORGANIZING_LIST__"
SERVICE_MENTORING_LIST_PLACEHOLDER = "__SERVICE_MENTORING_LIST__"
SERVICE_DEPARTMENT_LIST_PLACEHOLDER = "__SERVICE_DEPARTMENT_LIST__"
SERVICE_SECTION_PLACEHOLDERS = {
    "reviewing": SERVICE_REVIEWING_LIST_PLACEHOLDER,
    "organizing": SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    "mentoring": SERVICE_MENTORING_LIST_PLACEHOLDER,
    "department": SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
}


class ServiceIndexError(ValueError):
    pass


def collapse_service_year_label(records: tuple[ServiceRecord, ...]) -> str:
    years = sorted(record.year for record in records)
    first_year = years[0]
    last_year = years[-1]
    if records[-1].ongoing:
        return f"{first_year} - Present"
    if len(years) == 1:
        return str(first_year)
    return f"{first_year} - {last_year}"


def _render_service_lead_text(group_key: str, record: ServiceRecord, *, year_label: str) -> str:
    if group_key == "department":
        label = f"{year_label} : {record.title}"
    else:
        label = f"{year_label} {record.title}"
    if not record.url:
        return label
    return f"[{label}]({record.url})"


def _render_public_service_entry_djot(
    group_key: str,
    records: tuple[ServiceRecord, ...],
) -> str:
    head = records[0]
    lead = _render_service_lead_text(
        group_key,
        head,
        year_label=collapse_service_year_label(records),
    )
    role_suffix = f" {head.role}" if head.role else ""
    line = f"- {lead}{role_suffix}"
    if not head.details:
        return line
    detail_lines = "\n".join(f"  * {detail}" for detail in head.details)
    return f"{line}\n\n{detail_lines}"


def group_service_records_for_view(
    records: tuple[ServiceRecord, ...],
    *,
    group_key: str,
) -> tuple[tuple[ServiceRecord, ...], ...]:
    group_records = [
        record
        for record in records
        if group_key in record.view_groups
    ]
    by_signature: dict[tuple[object, ...], list[ServiceRecord]] = defaultdict(list)
    for record in group_records:
        signature = (
            record.series_key or record.key,
            record.title,
            record.role,
            record.url,
            record.details,
        )
        by_signature[signature].append(record)

    groups: list[tuple[ServiceRecord, ...]] = []
    for signature_records in by_signature.values():
        ordered = sorted(signature_records, key=lambda record: -record.year)
        current_run: list[ServiceRecord] = []
        for record in ordered:
            if not current_run:
                current_run = [record]
                continue
            if record.series_key and current_run[-1].year - 1 == record.year:
                current_run.append(record)
                continue
            groups.append(tuple(sorted(current_run, key=lambda entry: entry.year)))
            current_run = [record]
        if current_run:
            groups.append(tuple(sorted(current_run, key=lambda entry: entry.year)))

    return tuple(
        sorted(
            groups,
            key=lambda grouped_records: (
                -max(record.year for record in grouped_records),
                grouped_records[0].title,
                grouped_records[0].role or "",
            ),
        )
    )

def render_public_service_section_list_djot(
    root: Path,
    group_key: str,
    *,
    service_path: Path | None = None,
) -> str:
    try:
        records = load_service_records(root, service_path=service_path)
    except ServiceRecordError as err:
        raise ServiceIndexError(str(err)) from err

    groups = group_service_records_for_view(records, group_key=group_key)
    chunks = [_render_public_service_entry_djot(group_key, group) for group in groups]
    rendered = "\n".join(chunks)
    return rendered + ("\n" if rendered else "")
