#!/usr/bin/env python3

from __future__ import annotations

from datetime import date
from pathlib import Path

from scripts.service_record_a4 import (
    ServiceRecordA4Error,
    ServiceRegistryA4,
    ServiceRunA4,
    load_service_registry_a4,
)


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
CV_SERVICE_HREF_PREFIX = "/service/#"
HOMEPAGE_RECENT_SERVICE_GROUPS = frozenset({"organizing", "reviewing", "mentoring"})
HOMEPAGE_RECENT_SERVICE_WINDOW_YEARS = 3
HOMEPAGE_RECENT_SERVICE_CAP: int | None = None


class ServiceIndexError(ValueError):
    pass


def _load_service_registry(
    root: Path,
    *,
    service_path: Path | None = None,
) -> ServiceRegistryA4:
    try:
        return load_service_registry_a4(root, service_path=service_path)
    except ServiceRecordA4Error as err:
        raise ServiceIndexError(str(err)) from err


def collapse_service_run_year_label(run: ServiceRunA4) -> str:
    years = sorted(instance.year for instance in run.instances)
    first_year = years[0]
    last_year = years[-1]
    if run.ongoing:
        return f"{first_year} - Present"
    if len(years) == 1:
        return str(first_year)
    return f"{first_year} - {last_year}"


def _is_single_year_label(year_label: str) -> bool:
    return year_label.isdigit()


def _format_run_summary_label(run: ServiceRunA4) -> str:
    year_label = collapse_service_run_year_label(run)
    if _is_single_year_label(year_label):
        summary = f"{run.title} {year_label}"
        if run.role:
            summary += f", {run.role}"
        return summary
    summary = run.title
    if run.role:
        summary += f" {run.role}"
    return f"{summary}, {year_label}"


def _format_instance_label(title: str, year: int, role: str | None) -> str:
    label = f"{title} {year}"
    if role:
        label += f", {role}"
    return label


def _nonempty_unique_urls(run: ServiceRunA4) -> set[str]:
    return {instance.url for instance in run.instances if instance.url}


def _resolved_single_url(run: ServiceRunA4) -> str | None:
    urls = _nonempty_unique_urls(run)
    if len(urls) == 1:
        return next(iter(urls))
    return None


def _latest_run_year_not_later_than(run: ServiceRunA4, current_year: int) -> int | None:
    years = [instance.year for instance in run.instances if instance.year <= current_year]
    if not years:
        return None
    return max(years)


def _summary_details(run: ServiceRunA4) -> tuple[str, ...]:
    if run.details:
        return run.details
    detail_sets = {instance.details for instance in run.instances}
    if len(detail_sets) == 1:
        return next(iter(detail_sets))
    return ()


def _has_meaningful_instance_variation(run: ServiceRunA4) -> bool:
    titles = {instance.title for instance in run.instances}
    roles = {instance.role for instance in run.instances}
    urls = {instance.url for instance in run.instances}
    details = {instance.details for instance in run.instances}
    return any(len(values) > 1 for values in (titles, roles, urls, details))


def _service_runs_for_view(
    registry: ServiceRegistryA4,
    *,
    group_key: str,
) -> tuple[ServiceRunA4, ...]:
    order_by_key = {run.key: index for index, run in enumerate(registry.runs)}
    runs = [run for run in registry.runs if group_key in run.view_groups]
    return tuple(
        sorted(
            runs,
            key=lambda run: (
                -max(instance.year for instance in run.instances),
                run.title,
                run.role or "",
                order_by_key[run.key],
            ),
        )
    )


def _homepage_recent_service_runs(
    registry: ServiceRegistryA4,
    *,
    current_year: int,
) -> tuple[ServiceRunA4, ...]:
    earliest_year = current_year - (HOMEPAGE_RECENT_SERVICE_WINDOW_YEARS - 1)
    order_by_key = {run.key: index for index, run in enumerate(registry.runs)}
    selected: list[tuple[int, ServiceRunA4]] = []
    for run in registry.runs:
        if not HOMEPAGE_RECENT_SERVICE_GROUPS.intersection(run.view_groups):
            continue
        years = {instance.year for instance in run.instances if instance.year <= current_year}
        if not years:
            continue
        if not any(earliest_year <= year <= current_year for year in years):
            continue
        selected.append((max(years), run))

    selected.sort(
        key=lambda item: (
            -item[0],
            item[1].title,
            item[1].role or "",
            order_by_key[item[1].key],
        )
    )
    runs = tuple(run for _, run in selected)
    if HOMEPAGE_RECENT_SERVICE_CAP is None:
        return runs
    return runs[:HOMEPAGE_RECENT_SERVICE_CAP]


def _anchor_prefix(run: ServiceRunA4, *, group_key: str) -> str:
    if group_key != run.anchor_view_group:
        return ""
    return f"{{#{run.key}}}\n"


def _render_optional_link(label: str, href: str | None) -> str:
    if not href:
        return label
    return f"[{label}]({href})"


def _render_detail_bullets(details: tuple[str, ...], *, indent: str) -> list[str]:
    return [f"{indent}* {detail}" for detail in details]


def _render_instance_block_lines(
    instance,
    *,
    indent: str,
    inherited_details: tuple[str, ...],
) -> list[str]:
    label = _format_instance_label(instance.title, instance.year, instance.role)
    lines = [f"{indent}* {_render_optional_link(label, instance.url)}"]
    if instance.details and instance.details != inherited_details:
        lines.extend(_render_detail_bullets(instance.details, indent=indent + "  "))
    return lines


def _render_public_service_entry_djot(
    run: ServiceRunA4,
    *,
    group_key: str,
) -> str:
    lines = []
    anchor = _anchor_prefix(run, group_key=group_key)
    if anchor:
        lines.append(anchor.rstrip("\n"))

    summary = _render_optional_link(_format_run_summary_label(run), _resolved_single_url(run))
    lines.append(f"- {summary}")

    summary_details = _summary_details(run)
    if summary_details:
        lines.extend(_render_detail_bullets(summary_details, indent="  "))

    if _has_meaningful_instance_variation(run):
        ordered_instances = sorted(run.instances, key=lambda instance: -instance.year)
        for instance in ordered_instances:
            lines.extend(
                _render_instance_block_lines(
                    instance,
                    indent="  ",
                    inherited_details=summary_details,
                )
            )

    return "\n".join(lines)


def render_public_service_section_list_djot(
    root: Path,
    group_key: str,
    *,
    service_path: Path | None = None,
) -> str:
    registry = _load_service_registry(root, service_path=service_path)
    runs = _service_runs_for_view(registry, group_key=group_key)
    chunks = [_render_public_service_entry_djot(run, group_key=group_key) for run in runs]
    rendered = "\n\n".join(chunks)
    return rendered + ("\n" if rendered else "")


def _summary_href(run: ServiceRunA4) -> str | None:
    direct = _resolved_single_url(run)
    if direct:
        return direct
    if len(_nonempty_unique_urls(run)) > 1:
        return f"{CV_SERVICE_HREF_PREFIX}{run.key}"
    return None


def _render_cv_service_entry_djot(
    run: ServiceRunA4,
    *,
    group_key: str,
) -> str:
    label = _format_run_summary_label(run)
    line = f"- {_render_optional_link(label, _summary_href(run))}"
    if group_key == "department" and run.key == "uw-faculty-skit":
        return ""
    summary_details = _summary_details(run)
    if not summary_details:
        return line
    detail_lines = "\n".join(f"  * {detail}" for detail in summary_details)
    return f"{line}\n\n{detail_lines}"


def render_cv_service_section_list_djot(
    root: Path,
    group_key: str,
    *,
    service_path: Path | None = None,
) -> str:
    registry = _load_service_registry(root, service_path=service_path)
    runs = _service_runs_for_view(registry, group_key=group_key)
    chunks = [
        rendered
        for run in runs
        if (rendered := _render_cv_service_entry_djot(run, group_key=group_key))
    ]
    rendered = "\n\n".join(chunks)
    return rendered + ("\n" if rendered else "")


def render_homepage_recent_service_list_djot(
    root: Path,
    *,
    service_path: Path | None = None,
    current_year: int | None = None,
) -> str:
    registry = _load_service_registry(root, service_path=service_path)
    anchor_year = current_year if current_year is not None else date.today().year
    runs = _homepage_recent_service_runs(registry, current_year=anchor_year)
    chunks = [
        f"- {_render_optional_link(_format_run_summary_label(run), _summary_href(run))}"
        for run in runs
    ]
    rendered = "\n\n".join(chunks)
    return rendered + ("\n" if rendered else "")
