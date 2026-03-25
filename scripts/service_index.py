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
SKIT_SERIES_KEY = "uw-faculty-skit"


class ServiceIndexError(ValueError):
    pass


def _collapse_year_label(records: tuple[ServiceRecord, ...]) -> str:
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
        year_label=_collapse_year_label(records),
    )
    role_suffix = f" {head.role}" if head.role else ""
    return f"- {lead}{role_suffix}"


def _group_public_service_records(
    records: tuple[ServiceRecord, ...],
    *,
    group_key: str,
) -> tuple[tuple[ServiceRecord, ...], ...]:
    group_records = [
        record
        for record in records
        if group_key in record.view_groups and record.series_key != SKIT_SERIES_KEY
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


def _render_skit_note_djot(records: tuple[ServiceRecord, ...]) -> str:
    skit_records = tuple(
        sorted(
            (
                record
                for record in records
                if record.series_key == SKIT_SERIES_KEY
            ),
            key=lambda record: record.year,
        )
    )
    if not skit_records:
        return ""

    first_year = skit_records[0].year
    last_record = skit_records[-1]
    if last_record.ongoing:
        years_text = f"since {first_year}"
    elif first_year == last_record.year:
        years_text = f"in {first_year}"
    else:
        years_text = f"from {first_year} to {last_record.year}"

    suffix = ""
    if last_record.details:
        suffix = f"\n  {last_record.details[0].rstrip('.')}."

    return (
        "I have also helped\n"
        "  write, produce, and direct\n"
        f"  UW's annual faculty skit {years_text}"
        f"{suffix}"
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

    groups = _group_public_service_records(records, group_key=group_key)
    chunks = [_render_public_service_entry_djot(group_key, group) for group in groups]
    rendered = "\n".join(chunks)
    if group_key == "department":
        skit_note = _render_skit_note_djot(records)
        if rendered and skit_note:
            return rendered + "\n\n" + skit_note + "\n"
        if skit_note:
            return skit_note + "\n"
    return rendered + ("\n" if rendered else "")
