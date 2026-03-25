#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
import re
from pathlib import Path

from scripts.service_record import ServiceRecord, ServiceRecordError, load_service_records


SERVICE_PAGE_NAME = "service.dj"
SERVICE_SECTION_KEYS = ("reviewing", "organizing", "mentoring", "department")
SERVICE_SECTION_TITLES = {
    "reviewing": "Reviewing",
    "organizing": "Organizing",
    "mentoring": "Mentoring",
    "department": "Department",
}
SKIT_SERIES_KEY = "uw-faculty-skit"
SKIT_NOTE_RE = re.compile(
    r"annual faculty skit since 2015.*Hank Levy.*Adriana Schulz",
    re.DOTALL,
)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
WHITESPACE_RE = re.compile(r"\s+")


class ServiceIndexError(ValueError):
    pass


def service_page_path(root: Path, *, page_source_dir: Path | None = None) -> Path:
    actual_page_source_dir = page_source_dir or (root / "site" / "pages")
    return (actual_page_source_dir / SERVICE_PAGE_NAME).resolve()


def _normalize_service_entry_text(text: str) -> str:
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    return WHITESPACE_RE.sub(" ", text.strip())


def _collapse_year_label(records: tuple[ServiceRecord, ...]) -> str:
    years = sorted(record.year for record in records)
    first_year = years[0]
    last_year = years[-1]
    if len(years) == 1:
        if records[-1].ongoing:
            return f"{first_year} - Present"
        return str(first_year)
    if records[-1].ongoing:
        return f"{first_year} - Present"
    return f"{first_year} - {last_year}"


def _render_public_service_entry_text(group_key: str, records: tuple[ServiceRecord, ...]) -> str:
    head = records[0]
    year_label = _collapse_year_label(records)
    role_suffix = f" {head.role}" if head.role else ""
    if group_key == "department":
        return f"{year_label} : {head.title}{role_suffix}"
    return f"{year_label} {head.title}{role_suffix}"


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


def public_service_entries_by_group(
    root: Path,
    *,
    service_path: Path | None = None,
) -> dict[str, tuple[str, ...]]:
    try:
        records = load_service_records(root, service_path=service_path)
    except ServiceRecordError as err:
        raise ServiceIndexError(str(err)) from err

    return {
        group_key: tuple(
            _render_public_service_entry_text(group_key, grouped_records)
            for grouped_records in _group_public_service_records(records, group_key=group_key)
        )
        for group_key in SERVICE_SECTION_KEYS
    }


def parse_public_service_page_entries(
    root: Path,
    *,
    page_source_dir: Path | None = None,
) -> dict[str, tuple[str, ...]]:
    path = service_page_path(root, page_source_dir=page_source_dir)
    text = path.read_text(encoding="utf-8")
    section_key_by_title = {title: key for key, title in SERVICE_SECTION_TITLES.items()}
    entries: dict[str, list[str]] = {key: [] for key in SERVICE_SECTION_KEYS}
    current_section: str | None = None

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            current_section = section_key_by_title.get(stripped.removeprefix("## ").strip())
            continue
        if current_section and stripped.startswith("- "):
            entries[current_section].append(_normalize_service_entry_text(stripped.removeprefix("- ")))

    return {key: tuple(values) for key, values in entries.items()}


def find_public_service_drift_issues(
    root: Path,
    *,
    service_path: Path | None = None,
    page_source_dir: Path | None = None,
) -> list[str]:
    page_path = service_page_path(root, page_source_dir=page_source_dir)
    if not page_path.exists():
        return []

    try:
        expected = public_service_entries_by_group(root, service_path=service_path)
    except ServiceIndexError:
        return []

    actual = parse_public_service_page_entries(root, page_source_dir=page_source_dir)
    issues: list[str] = []

    for group_key in SERVICE_SECTION_KEYS:
        expected_entries = set(expected[group_key])
        actual_entries = set(actual[group_key])
        missing = sorted(expected_entries - actual_entries)
        extra = sorted(actual_entries - expected_entries)
        if missing:
            issues.append(
                f"{page_path}: service section {group_key} missing canonical entries: {', '.join(missing)}"
            )
        if extra:
            issues.append(
                f"{page_path}: service section {group_key} has non-canonical entries: {', '.join(extra)}"
            )

    text = page_path.read_text(encoding="utf-8")
    if any(
        record.series_key == SKIT_SERIES_KEY
        for record in load_service_records(root, service_path=service_path)
    ) and not SKIT_NOTE_RE.search(text):
        issues.append(
            f"{page_path}: missing annual faculty skit note for canonical service records"
        )

    return issues
