#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from scripts.publication_index import load_publication_index_records
from scripts.student_record import StudentSection, load_student_sections
from scripts.teaching_record import TeachingGroup, TeachingOffering, TeachingRecord, load_teaching_groups

CURRENT_STUDENTS_SECTION_KEY = "current_students"
COMPLETED_POSTDOC_SECTION_KEY = "completed_postdoctoral_mentoring"
GRADUATED_DOCTORAL_SECTION_KEY = "graduated_doctoral_students"
GRADUATED_MASTERS_SECTION_KEY = "graduated_masters_students"
GRADUATED_BACHELORS_SECTION_KEY = "graduated_bachelors_students"
VISITING_STUDENTS_SECTION_KEY = "visiting_students"
TEACHING_IN_SCOPE_GROUP_KEYS = frozenset({"uw_courses", "special_topics"})
CURRENT_CATEGORY_ORDER = ("PhD", "postdoc", "MS", "BS", "HS")
GRADUATED_CATEGORY_ORDER = ("PhD", "MS", "BS")


@dataclass(frozen=True)
class ScaleStats:
    current_advisees_total: int
    current_advisees_breakdown: tuple[tuple[str, int], ...]
    graduated_advisees_total: int
    graduated_advisees_breakdown: tuple[tuple[str, int], ...]
    completed_postdoctoral_mentoring: int
    visiting_students: int
    indexed_publications: int
    completed_uw_offerings_with_enrollment: int
    uw_students_taught: int
    excluded_teaching_offerings: tuple[str, ...]


def _student_sections_by_key(sections: tuple[StudentSection, ...]) -> dict[str, StudentSection]:
    return {section.key: section for section in sections}


def _section_count(sections_by_key: dict[str, StudentSection], key: str) -> int:
    section = sections_by_key.get(key)
    if section is None:
        return 0
    return len(section.records)


def _normalize_current_student_label(label: str) -> str:
    mapping = {
        "PhD Student": "PhD",
        "MS Student": "MS",
        "BS Student": "BS",
        "HS Student": "HS",
        "Postdoctoral Scholar": "postdoc",
    }
    return mapping.get(label, label)


def _ordered_breakdown(
    counts: Counter[str],
    preferred_order: tuple[str, ...],
) -> tuple[tuple[str, int], ...]:
    ordered: list[tuple[str, int]] = []
    seen: set[str] = set()
    for label in preferred_order:
        count = counts.get(label)
        if count:
            ordered.append((label, count))
            seen.add(label)
    for label in sorted(counts):
        if label in seen:
            continue
        ordered.append((label, counts[label]))
    return tuple(ordered)


def _current_advisee_breakdown(sections_by_key: dict[str, StudentSection]) -> tuple[tuple[str, int], ...]:
    current = sections_by_key.get(CURRENT_STUDENTS_SECTION_KEY)
    if current is None:
        return ()
    counts = Counter(_normalize_current_student_label(record.label) for record in current.records)
    return _ordered_breakdown(counts, CURRENT_CATEGORY_ORDER)


def _graduated_advisee_breakdown(sections_by_key: dict[str, StudentSection]) -> tuple[tuple[str, int], ...]:
    counts = Counter(
        {
            "PhD": _section_count(sections_by_key, GRADUATED_DOCTORAL_SECTION_KEY),
            "MS": _section_count(sections_by_key, GRADUATED_MASTERS_SECTION_KEY),
            "BS": _section_count(sections_by_key, GRADUATED_BACHELORS_SECTION_KEY),
        }
    )
    return _ordered_breakdown(counts, GRADUATED_CATEGORY_ORDER)


def _format_breakdown(breakdown: tuple[tuple[str, int], ...]) -> str:
    return ", ".join(f"{count} {label}" for label, count in breakdown)


def _format_offering_label(record: TeachingRecord, offering: TeachingOffering) -> str:
    heading = record.code or record.title
    return f"{heading} {offering.term} {offering.year}"


def build_scale_stats(root: Path) -> ScaleStats:
    resolved_root = root.resolve()
    student_sections = load_student_sections(resolved_root)
    teaching_groups = load_teaching_groups(resolved_root)
    publication_records = load_publication_index_records(resolved_root)

    sections_by_key = _student_sections_by_key(student_sections)
    current_breakdown = _current_advisee_breakdown(sections_by_key)
    current_total = sum(count for _, count in current_breakdown)
    graduated_breakdown = _graduated_advisee_breakdown(sections_by_key)
    graduated_total = sum(count for _, count in graduated_breakdown)

    completed_uw_offerings_with_enrollment = 0
    uw_students_taught = 0
    excluded_teaching_offerings: list[str] = []
    for group in teaching_groups:
        if group.key not in TEACHING_IN_SCOPE_GROUP_KEYS:
            continue
        for record in group.records:
            for offering in record.offerings:
                if offering.enrollment is None:
                    excluded_teaching_offerings.append(_format_offering_label(record, offering))
                    continue
                completed_uw_offerings_with_enrollment += 1
                uw_students_taught += offering.enrollment.students

    return ScaleStats(
        current_advisees_total=current_total,
        current_advisees_breakdown=current_breakdown,
        graduated_advisees_total=graduated_total,
        graduated_advisees_breakdown=graduated_breakdown,
        completed_postdoctoral_mentoring=_section_count(
            sections_by_key,
            COMPLETED_POSTDOC_SECTION_KEY,
        ),
        visiting_students=_section_count(sections_by_key, VISITING_STUDENTS_SECTION_KEY),
        indexed_publications=len(publication_records),
        completed_uw_offerings_with_enrollment=completed_uw_offerings_with_enrollment,
        uw_students_taught=uw_students_taught,
        excluded_teaching_offerings=tuple(excluded_teaching_offerings),
    )


def render_scale_stats(stats: ScaleStats) -> str:
    lines = [
        "Scale stats",
        "===========",
        "Generated from canonical site data.",
        "",
        "Students",
        f"- Current advisees: {stats.current_advisees_total:,} total ({_format_breakdown(stats.current_advisees_breakdown)})",
        f"- Graduated advisees: {stats.graduated_advisees_total:,} total ({_format_breakdown(stats.graduated_advisees_breakdown)})",
        f"- Completed postdoctoral mentoring: {stats.completed_postdoctoral_mentoring:,}",
        f"- Visiting students: {stats.visiting_students:,}",
        "",
        "Publications",
        f"- Indexed publications: {stats.indexed_publications:,}",
        "",
        "Teaching",
        f"- Completed UW instructor-led offerings with enrollment present: {stats.completed_uw_offerings_with_enrollment:,}",
        f"- UW students taught across those offerings: {stats.uw_students_taught:,}",
    ]
    if stats.excluded_teaching_offerings:
        suffix = "offering" if len(stats.excluded_teaching_offerings) == 1 else "offerings"
        lines.append(
            f"- Excludes {len(stats.excluded_teaching_offerings):,} {suffix} without enrollment: "
            + ", ".join(stats.excluded_teaching_offerings)
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print compact scale stats derived from canonical site data."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root (defaults to current directory).",
    )
    args = parser.parse_args()
    print(render_scale_stats(build_scale_stats(args.root)), end="")


if __name__ == "__main__":
    main()
