"""Helpers for rendering projection-backed collection pages."""

from __future__ import annotations

from pathlib import Path
import re

from scripts.collaborators_index import (
    COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER,
    COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER,
    CollaboratorsIndexError,
    RESEARCH_COLLABORATORS_LIST_PLACEHOLDER,
    TEACHING_COLLABORATORS_LIST_PLACEHOLDER,
    render_missing_collaborator_first_initials,
    render_missing_collaborator_last_initials,
    render_public_research_collaborators_list_djot,
    render_public_teaching_collaborators_list_djot,
)
from scripts.funding_index import (
    FUNDING_LIST_PLACEHOLDER,
    FundingIndexError,
    render_public_funding_list_djot,
)
from scripts.funding_record import FUNDING_DATA_NAME, FundingRecordError, load_funding_records
from scripts.news_index import (
    NEWS_MONTH_GROUPS_PLACEHOLDER,
    NewsIndexError,
    render_public_news_month_groups_djot,
)
from scripts.news_record import NEWS_DATA_NAME
from scripts.publication_index import (
    PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
    PublicationIndexError,
    load_publication_index_records,
    render_publications_list_djot,
)
from scripts.publication_record import PublicationRecord, publication_year
from scripts.service_index import (
    SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
    SERVICE_MENTORING_LIST_PLACEHOLDER,
    SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    SERVICE_REVIEWING_LIST_PLACEHOLDER,
    SERVICE_SECTION_PLACEHOLDERS,
    ServiceIndexError,
    collapse_service_year_label,
    group_service_records_for_view,
    render_public_service_section_list_djot,
)
from scripts.service_record import (
    SERVICE_DATA_NAME,
    ServiceRecord,
    ServiceRecordError,
    load_service_records,
)
from scripts.student_record import (
    STUDENTS_DATA_NAME,
    StudentRecord,
    StudentRecordError,
    load_student_sections,
)
from scripts.teaching_record import (
    TeachingOffering,
    TeachingRecord,
    TeachingRecordError,
    load_teaching_groups,
)
from scripts.talk_record import TalkRecord, TalkRecordError, load_talk_records, render_talk_date
from .people_registry import PeopleRegistryError, load_people_registry

TALKS_LIST_PLACEHOLDER = "__TALKS_LIST__"
STUDENTS_CURRENT_LIST_PLACEHOLDER = "__STUDENTS_CURRENT_LIST__"
STUDENTS_POSTDOC_LIST_PLACEHOLDER = "__STUDENTS_POSTDOC_LIST__"
STUDENTS_PHD_LIST_PLACEHOLDER = "__STUDENTS_PHD_LIST__"
STUDENTS_MASTERS_LIST_PLACEHOLDER = "__STUDENTS_MASTERS_LIST__"
STUDENTS_BACHELORS_LIST_PLACEHOLDER = "__STUDENTS_BACHELORS_LIST__"
STUDENTS_VISITING_LIST_PLACEHOLDER = "__STUDENTS_VISITING_LIST__"
STUDENT_SECTION_PLACEHOLDERS = {
    "current_students": STUDENTS_CURRENT_LIST_PLACEHOLDER,
    "completed_postdoctoral_mentoring": STUDENTS_POSTDOC_LIST_PLACEHOLDER,
    "graduated_doctoral_students": STUDENTS_PHD_LIST_PLACEHOLDER,
    "graduated_masters_students": STUDENTS_MASTERS_LIST_PLACEHOLDER,
    "graduated_bachelors_students": STUDENTS_BACHELORS_LIST_PLACEHOLDER,
    "visiting_students": STUDENTS_VISITING_LIST_PLACEHOLDER,
}
CV_STUDENTS_CURRENT_LIST_PLACEHOLDER = "__CV_STUDENTS_CURRENT_LIST__"
CV_STUDENTS_POSTDOC_LIST_PLACEHOLDER = "__CV_STUDENTS_POSTDOC_LIST__"
CV_STUDENTS_PHD_LIST_PLACEHOLDER = "__CV_STUDENTS_PHD_LIST__"
CV_STUDENTS_MASTERS_LIST_PLACEHOLDER = "__CV_STUDENTS_MASTERS_LIST__"
CV_STUDENTS_BACHELORS_LIST_PLACEHOLDER = "__CV_STUDENTS_BACHELORS_LIST__"
CV_STUDENTS_VISITING_LIST_PLACEHOLDER = "__CV_STUDENTS_VISITING_LIST__"
CV_STUDENT_SECTION_PLACEHOLDERS = {
    "current_students": CV_STUDENTS_CURRENT_LIST_PLACEHOLDER,
    "completed_postdoctoral_mentoring": CV_STUDENTS_POSTDOC_LIST_PLACEHOLDER,
    "graduated_doctoral_students": CV_STUDENTS_PHD_LIST_PLACEHOLDER,
    "graduated_masters_students": CV_STUDENTS_MASTERS_LIST_PLACEHOLDER,
    "graduated_bachelors_students": CV_STUDENTS_BACHELORS_LIST_PLACEHOLDER,
    "visiting_students": CV_STUDENTS_VISITING_LIST_PLACEHOLDER,
}
CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER = "__CV_TEACHING_INSTRUCTOR_LIST__"
CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER = "__CV_TEACHING_SUMMER_SCHOOL_LIST__"
CV_TEACHING_TA_LIST_PLACEHOLDER = "__CV_TEACHING_TA_LIST__"
CV_SERVICE_REVIEWING_LIST_PLACEHOLDER = "__CV_SERVICE_REVIEWING_LIST__"
CV_SERVICE_ORGANIZING_LIST_PLACEHOLDER = "__CV_SERVICE_ORGANIZING_LIST__"
CV_SERVICE_MENTORING_LIST_PLACEHOLDER = "__CV_SERVICE_MENTORING_LIST__"
CV_SERVICE_DEPARTMENT_LIST_PLACEHOLDER = "__CV_SERVICE_DEPARTMENT_LIST__"
CV_SERVICE_SECTION_PLACEHOLDERS = {
    "reviewing": CV_SERVICE_REVIEWING_LIST_PLACEHOLDER,
    "organizing": CV_SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    "mentoring": CV_SERVICE_MENTORING_LIST_PLACEHOLDER,
    "department": CV_SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
}
CV_PUBLICATIONS_MAIN_LIST_PLACEHOLDER = "__CV_PUBLICATIONS_MAIN_LIST__"
CV_PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER = "__CV_PUBLICATIONS_WORKSHOP_LIST__"
CV_PUBLICATIONS_SECTION_PLACEHOLDERS = {
    "main": CV_PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    "workshop": CV_PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
}
CV_TALKS_LIST_PLACEHOLDER = "__CV_TALKS_LIST__"
CV_FUNDING_LIST_PLACEHOLDER = "__CV_FUNDING_LIST__"
TEACHING_UW_COURSES_LIST_PLACEHOLDER = "__TEACHING_UW_COURSES_LIST__"
TEACHING_SPECIAL_TOPICS_LIST_PLACEHOLDER = "__TEACHING_SPECIAL_TOPICS_LIST__"
TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER = "__TEACHING_SUMMER_SCHOOL_LIST__"
TEACHING_GROUP_PLACEHOLDERS = {
    "uw_courses": TEACHING_UW_COURSES_LIST_PLACEHOLDER,
    "special_topics": TEACHING_SPECIAL_TOPICS_LIST_PLACEHOLDER,
    "summer_school": TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER,
}


class PageProjectionError(ValueError):
    pass


INLINE_LINK_RE = re.compile(r"\[([^\]]+)\](?:\([^)]+\)|\[[^\]]*\])")


def _render_segment_text(text: str, url: str | None) -> str:
    if not url:
        return text
    return f"[{text}]({url})"


def _render_title(title: str, url: str | None) -> str:
    if not url:
        return title
    return f"[{title}]({url})"


def _render_teaching_offering(offering: TeachingOffering) -> str:
    label = f"{offering.year} {offering.term}"
    if not offering.url:
        return label
    return f"[{label}]({offering.url})"


def _load_projection_people_registry(root: Path, *, data_dir: Path | None = None):
    people_path = (data_dir / "people.json") if data_dir is not None else None
    try:
        return load_people_registry(people_path or (root / "site" / "data" / "people.json"))
    except PeopleRegistryError as err:
        raise PageProjectionError(str(err)) from err


def _render_person_key_ref(person_key: str, *, registry) -> str:
    person = registry.person(person_key)
    return _render_person_ref(
        display_name=person.name,
        ref_name=person.name,
        is_linked=person.primary_url is not None,
    )


def _render_staffing_line(
    label: str,
    person_keys: tuple[str, ...],
    *,
    registry,
) -> str | None:
    if not person_keys:
        return None
    rendered_people = tuple(
        _render_person_key_ref(person_key, registry=registry) for person_key in person_keys
    )
    return f"  - {label}: {_join_people_refs(rendered_people)}"


def _render_offering_with_staffing_lines(
    offering: TeachingOffering,
    *,
    registry,
) -> tuple[str, ...]:
    lines = [f"- {_render_teaching_offering(offering)}"]
    staffing_lines = tuple(
        line
        for line in (
            _render_staffing_line(
                "Co-Instructors",
                offering.co_instructors,
                registry=registry,
            ),
            _render_staffing_line(
                "Teaching Assistants",
                offering.teaching_assistants,
                registry=registry,
            ),
            _render_staffing_line(
                "Tutors",
                offering.tutors,
                registry=registry,
            ),
        )
        if line is not None
    )
    if staffing_lines:
        lines.append("")
        lines.extend(staffing_lines)
    return tuple(lines)


def _flatten_cv_djot_text(text: str) -> str:
    return INLINE_LINK_RE.sub(r"\1", text).replace("\\ ", " ")


def _render_cv_teaching_offering(offering: TeachingOffering) -> str:
    return f"{offering.year} {offering.term}"


def _render_person_ref(*, display_name: str, ref_name: str, is_linked: bool) -> str:
    if not is_linked:
        return display_name
    if display_name == ref_name:
        return f"[{display_name}][]"
    return f"[{display_name}][{ref_name}]"


def _join_people_refs(people_refs: tuple[str, ...]) -> str:
    if len(people_refs) == 1:
        return people_refs[0]
    if len(people_refs) == 2:
        return f"{people_refs[0]} and {people_refs[1]}"
    return ", ".join(people_refs[:-1]) + f", and {people_refs[-1]}"


def _render_student_record(record: StudentRecord, *, registry) -> str:
    person = registry.person(record.person_key)
    lines = [
        f"- {_render_person_ref(display_name=record.name, ref_name=person.name, is_linked=person.primary_url is not None)}, {record.label}"
    ]

    if record.details:
        lines.append("")
    for detail in record.details:
        if detail.kind == "thesis":
            lines.append(f"  * Thesis: [{detail.title}]({detail.url})")
            continue
        if detail.kind == "coadvisor":
            people_refs = tuple(
                _render_person_ref(
                    display_name=registry.person(person_key).name,
                    ref_name=registry.person(person_key).name,
                    is_linked=registry.person(person_key).primary_url is not None,
                )
                for person_key in detail.person_keys
            )
            lines.append(f"  * co-advised with {_join_people_refs(people_refs)}")
            continue
        lines.append(f"  * {detail.djot}")

    return "\n".join(lines)


def render_students_section_list_djot(
    root: Path,
    section_key: str,
    *,
    data_dir: Path | None = None,
) -> str:
    students_path = (data_dir / STUDENTS_DATA_NAME) if data_dir is not None else None
    people_path = (data_dir / "people.json") if data_dir is not None else None
    try:
        sections = load_student_sections(
            root,
            students_path=students_path,
            people_path=people_path,
        )
        registry = load_people_registry(people_path or (root / "site" / "data" / "people.json"))
    except StudentRecordError as err:
        raise PageProjectionError(str(err)) from err
    except PeopleRegistryError as err:
        raise PageProjectionError(str(err)) from err

    try:
        section = next(section for section in sections if section.key == section_key)
    except StopIteration as err:
        raise PageProjectionError(f"missing student section for projection: {section_key}") from err

    chunks = [
        _render_student_record(record, registry=registry)
        for record in section.records
    ]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def _render_cv_student_record(record: StudentRecord) -> str:
    lines = [f"- {record.name}, {record.label}"]

    rendered_details: list[str] = []
    for detail in record.details:
        if detail.kind == "thesis":
            rendered_details.append(f"  * Thesis: {detail.title}")
            continue
        if detail.kind == "coadvisor":
            continue
        rendered_details.append(f"  * {detail.djot}")
    if rendered_details:
        lines.append("")
        lines.extend(rendered_details)
    return "\n".join(lines)


def render_cv_students_section_list_djot(
    root: Path,
    section_key: str,
    *,
    data_dir: Path | None = None,
) -> str:
    students_path = (data_dir / STUDENTS_DATA_NAME) if data_dir is not None else None
    people_path = (data_dir / "people.json") if data_dir is not None else None
    try:
        sections = load_student_sections(
            root,
            students_path=students_path,
            people_path=people_path,
        )
    except StudentRecordError as err:
        raise PageProjectionError(str(err)) from err

    try:
        section = next(section for section in sections if section.key == section_key)
    except StopIteration as err:
        raise PageProjectionError(f"missing student section for projection: {section_key}") from err

    chunks = [_render_cv_student_record(record) for record in section.records]
    return "\n".join(chunks) + ("\n" if chunks else "")


def _teaching_group_records_by_key(root: Path, *, data_dir: Path | None = None) -> dict[str, tuple[TeachingRecord, ...]]:
    teaching_path = (data_dir / "teaching.json") if data_dir is not None else None
    try:
        groups = load_teaching_groups(root, teaching_path=teaching_path)
    except TeachingRecordError as err:
        raise PageProjectionError(str(err)) from err
    return {group.key: group.records for group in groups}


def _service_records(root: Path, *, data_dir: Path | None = None) -> tuple[ServiceRecord, ...]:
    service_path = (data_dir / SERVICE_DATA_NAME) if data_dir is not None else None
    try:
        return load_service_records(root, service_path=service_path)
    except ServiceRecordError as err:
        raise PageProjectionError(str(err)) from err


def _render_cv_publication_entry(record: PublicationRecord) -> str:
    parts = [
        f"*{record.title}*",
        ", ".join(author.name for author in record.authors),
        f"{record.venue} {publication_year(record.slug)}",
        *record.badges,
    ]
    return " \\\n".join(parts)


def render_cv_publications_list_djot(
    root: Path,
    listing_group: str,
    *,
    publications_dir: Path | None = None,
) -> str:
    try:
        records = load_publication_index_records(root, publications_dir=publications_dir)
    except PublicationIndexError as err:
        raise PageProjectionError(str(err)) from err
    chunks = [
        _render_cv_publication_entry(record)
        for record in records
        if record.listing_group == listing_group
    ]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def _render_cv_service_lead_text(group_key: str, record: ServiceRecord, *, year_label: str) -> str:
    if group_key == "department":
        label = f"{year_label} : {record.title}"
    else:
        label = f"{year_label} {record.title}"
    role_suffix = f" {record.role}" if record.role else ""
    visible_text = f"{label}{role_suffix}"
    if not record.url:
        return visible_text
    return f"[{visible_text}]({record.url})"


def _render_cv_service_entry_djot(
    group_key: str,
    records: tuple[ServiceRecord, ...],
) -> str:
    head = records[0]
    lead = _render_cv_service_lead_text(
        group_key,
        head,
        year_label=collapse_service_year_label(records),
    )
    line = f"- {lead}"
    if not head.details:
        return line
    detail_lines = "\n".join(f"  * {detail}" for detail in head.details)
    return f"{line}\n\n{detail_lines}"


def render_cv_service_section_list_djot(
    root: Path,
    group_key: str,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _service_records(root, data_dir=data_dir)
    if group_key == "department":
        records = tuple(
            record
            for record in records
            if record.series_key != "uw-faculty-skit" and record.title != "UW Faculty Skit"
        )
    groups = group_service_records_for_view(records, group_key=group_key)
    chunks = [_render_cv_service_entry_djot(group_key, group) for group in groups]
    rendered = "\n".join(chunks)
    return rendered + ("\n" if rendered else "")


def _render_cv_course_record(record: TeachingRecord) -> str:
    lines = [f"- *{record.code}: {record.title}* \\"]
    description_parts: list[str] = []
    if record.audience_label:
        description_parts.append(_flatten_cv_djot_text(record.audience_label))
    if record.description_djot:
        description_parts.append(_flatten_cv_djot_text(record.description_djot))
    if description_parts:
        lines.append(f"  {' '.join(description_parts)}")
    lines.append("")
    lines.append("  {.columns .columns-8rem}")
    lines.extend(f"  *  {_render_cv_teaching_offering(offering)}" for offering in record.offerings)
    return "\n".join(lines)


def _render_cv_special_topics_record(record: TeachingRecord) -> str:
    first_offering = record.offerings[0]
    lines = [f"  * {record.code}: {record.title}, {first_offering.year} {first_offering.term}"]
    if record.details:
        lines.append("")
        lines.extend(f"    - {_flatten_cv_djot_text(detail)}" for detail in record.details)
    return "\n".join(lines)


def render_cv_teaching_instructor_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    groups = _teaching_group_records_by_key(root, data_dir=data_dir)
    chunks = [_render_cv_course_record(record) for record in groups["uw_courses"]]
    special_topics = groups["special_topics"]
    if special_topics:
        special_topics_lines = ["- *Special Topics Graduate Courses*", ""]
        special_topics_lines.extend(
            _render_cv_special_topics_record(record)
            for record in special_topics
        )
        chunks.append("\n".join(special_topics_lines))
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def _render_uw_course_record(record: TeachingRecord, *, registry) -> str:
    lines = [f"*{record.code}: {record.title}* \\"]
    if record.audience_label:
        lines.append(record.audience_label)
    if record.description_djot:
        lines.append(f"  {record.description_djot}")
    lines.append("")
    for offering in record.offerings:
        lines.extend(_render_offering_with_staffing_lines(offering, registry=registry))
    return "\n".join(lines)


def render_teaching_uw_courses_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["uw_courses"]
    registry = _load_projection_people_registry(root, data_dir=data_dir)
    chunks = [_render_uw_course_record(record, registry=registry) for record in records]
    if not chunks:
        return ""
    return ("\n\n{.course-vspace}\n".join(chunks)) + "\n"


def _render_special_topics_record(record: TeachingRecord, *, registry) -> str:
    lines = [f"*{record.code}: {record.title}* \\"]
    if len(record.details) == 1:
        lines.append(f"  {record.details[0]}")
    elif record.details:
        lines.append("")
        lines.extend(f"  - {detail}" for detail in record.details)
    lines.append("")
    for offering in record.offerings:
        lines.extend(_render_offering_with_staffing_lines(offering, registry=registry))
    return "\n".join(lines)


def render_teaching_special_topics_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["special_topics"]
    registry = _load_projection_people_registry(root, data_dir=data_dir)
    chunks = [_render_special_topics_record(record, registry=registry) for record in records]
    if not chunks:
        return ""
    return ("\n\n{.course-vspace}\n".join(chunks)) + "\n"


def _render_cv_summer_school_record(record: TeachingRecord) -> str:
    chunks: list[str] = []
    for event in record.events:
        chunks.append(f"- *{event.label}* \\\n  {record.title}")
    return "\n\n".join(chunks)


def _render_supplemental_links_djot(record) -> str:
    if not record.links:
        return ""
    return ",\n    \\ ".join(
        f"[{link.label}]({link.url})"
        for link in record.links
    )


def _render_summer_school_record(record: TeachingRecord) -> str:
    lines = [f"- {record.title}", ""]
    for event in record.events:
        event_line = f"  * [{event.label}]({event.url})"
        supplemental = _render_supplemental_links_djot(event)
        if supplemental:
            event_line += f":\n    \\ {supplemental}"
        lines.append(event_line)
    return "\n".join(lines)


def render_teaching_summer_school_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["summer_school"]
    chunks = [_render_summer_school_record(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def render_cv_teaching_summer_school_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["summer_school"]
    chunks = [_render_cv_summer_school_record(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def render_cv_teaching_assistant_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["teaching_assistant"]
    chunks = [_render_cv_course_record(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def _talk_records(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> tuple[TalkRecord, ...]:
    try:
        return load_talk_records(root, talks_dir=talks_dir)
    except TalkRecordError as err:
        raise PageProjectionError(str(err)) from err


def _render_talk_entry_djot(record: TalkRecord) -> str:
    title = _render_title(record.title, record.url)
    at_text = ", ".join(_render_segment_text(segment.text, segment.url) for segment in record.at)
    date_text = render_talk_date(record.when)
    return f"- {title} \\\n  {at_text}, {date_text}"


def render_talks_list_djot(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> str:
    records = _talk_records(root, talks_dir=talks_dir)
    chunks = [_render_talk_entry_djot(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def render_cv_talks_list_djot(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> str:
    records = _talk_records(root, talks_dir=talks_dir)
    chunks = [_render_talk_entry_djot(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


def _render_cv_funding_sponsor_label(sponsor: str, award_id: str | None) -> str:
    if not award_id:
        return sponsor
    return f"{sponsor} {award_id}"


def _render_cv_funding_year_range(start_year: int, end_year: int) -> str:
    if start_year == end_year:
        return str(start_year)
    return f"{start_year} – {end_year}"


def _render_cv_funding_entry_djot(record) -> str:
    amount_label = f"${record.amount_usd:,}"
    sponsor_label = _render_cv_funding_sponsor_label(record.sponsor, record.award_id)
    return (
        f"- {record.title} \\\n"
        f"  {record.role}; {sponsor_label}; {amount_label}; "
        f"{_render_cv_funding_year_range(record.start_year, record.end_year)}"
    )


def render_cv_funding_list_djot(
    root: Path,
    *,
    funding_path: Path | None = None,
) -> str:
    try:
        records = load_funding_records(root, funding_path=funding_path)
    except FundingRecordError as err:
        raise PageProjectionError(str(err)) from err

    rendered = "\n\n".join(_render_cv_funding_entry_djot(record) for record in records)
    return rendered + ("\n" if rendered else "")


def apply_page_projections(
    route_kind: str,
    route_key: str,
    body: str,
    *,
    root: Path,
    data_dir: Path | None = None,
    talks_dir: Path | None = None,
    publications_dir: Path | None = None,
) -> str:
    if (
        route_kind == "ordinary_page"
        and route_key == "about"
        and (
            COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER in body
            or COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER in body
        )
    ):
        people_path = (data_dir / "people.json") if data_dir is not None else None
        rendered = body
        try:
            replacements = {
                COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER: render_missing_collaborator_first_initials(
                    root,
                    publications_dir=publications_dir,
                    people_path=people_path,
                ),
                COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER: render_missing_collaborator_last_initials(
                    root,
                    publications_dir=publications_dir,
                    people_path=people_path,
                ),
            }
        except CollaboratorsIndexError as err:
            raise PageProjectionError(str(err)) from err
        for placeholder, replacement in replacements.items():
            rendered = rendered.replace(placeholder, replacement)
        return rendered

    if route_kind == "collaborators_index_page" and route_key == "collaborators":
        people_path = (data_dir / "people.json") if data_dir is not None else None
        students_path = (data_dir / STUDENTS_DATA_NAME) if data_dir is not None else None
        teaching_path = (data_dir / "teaching.json") if data_dir is not None else None
        try:
            research = render_public_research_collaborators_list_djot(
                root,
                publications_dir=publications_dir,
                people_path=people_path,
                students_path=students_path,
            ).rstrip()
            teaching = render_public_teaching_collaborators_list_djot(
                root,
                people_path=people_path,
                teaching_path=teaching_path,
            ).rstrip()
        except CollaboratorsIndexError as err:
            raise PageProjectionError(str(err)) from err
        return (
            body.replace(RESEARCH_COLLABORATORS_LIST_PLACEHOLDER, research)
            .replace(TEACHING_COLLABORATORS_LIST_PLACEHOLDER, teaching)
        )

    if route_kind == "talks_index_page" and route_key == "talks" and TALKS_LIST_PLACEHOLDER in body:
        rendered = render_talks_list_djot(root, talks_dir=talks_dir).rstrip()
        return body.replace(TALKS_LIST_PLACEHOLDER, rendered)

    if route_kind == "service_index_page" and route_key == "service":
        rendered = body
        service_path = (data_dir / SERVICE_DATA_NAME) if data_dir is not None else None
        try:
            for section_key, placeholder in SERVICE_SECTION_PLACEHOLDERS.items():
                section_body = render_public_service_section_list_djot(
                    root,
                    section_key,
                    service_path=service_path,
                ).rstrip()
                rendered = rendered.replace(placeholder, section_body)
        except ServiceIndexError as err:
            raise PageProjectionError(str(err)) from err
        return rendered

    if route_kind == "funding_index_page" and route_key == "funding":
        funding_path = (data_dir / FUNDING_DATA_NAME) if data_dir is not None else None
        try:
            rendered = render_public_funding_list_djot(
                root,
                funding_path=funding_path,
            ).rstrip()
        except FundingIndexError as err:
            raise PageProjectionError(str(err)) from err
        return body.replace(FUNDING_LIST_PLACEHOLDER, rendered)

    if route_kind == "news_index_page" and route_key == "news":
        news_path = (data_dir / NEWS_DATA_NAME) if data_dir is not None else None
        try:
            rendered = render_public_news_month_groups_djot(
                root,
                news_path=news_path,
            ).rstrip()
        except NewsIndexError as err:
            raise PageProjectionError(str(err)) from err
        return body.replace(NEWS_MONTH_GROUPS_PLACEHOLDER, rendered)

    if route_kind == "students_index_page" and route_key == "students":
        rendered = body
        for section_key, placeholder in STUDENT_SECTION_PLACEHOLDERS.items():
            section_body = render_students_section_list_djot(
                root,
                section_key,
                data_dir=data_dir,
            ).rstrip()
            rendered = rendered.replace(placeholder, section_body)
        return rendered

    if route_kind == "cv_index_page" and route_key == "cv":
        rendered = body
        for section_key, placeholder in CV_STUDENT_SECTION_PLACEHOLDERS.items():
            if placeholder not in rendered:
                continue
            section_body = render_cv_students_section_list_djot(
                root,
                section_key,
                data_dir=data_dir,
            ).rstrip()
            rendered = rendered.replace(placeholder, section_body)
        if any(
            placeholder in rendered
            for placeholder in (
                CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER,
                CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER,
                CV_TEACHING_TA_LIST_PLACEHOLDER,
            )
        ):
            teaching_replacements = {
                CV_TEACHING_INSTRUCTOR_LIST_PLACEHOLDER: render_cv_teaching_instructor_list_djot(
                    root,
                    data_dir=data_dir,
                ).rstrip(),
                CV_TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER: render_cv_teaching_summer_school_list_djot(
                    root,
                    data_dir=data_dir,
                ).rstrip(),
                CV_TEACHING_TA_LIST_PLACEHOLDER: render_cv_teaching_assistant_list_djot(
                    root,
                    data_dir=data_dir,
                ).rstrip(),
            }
            for placeholder, replacement in teaching_replacements.items():
                rendered = rendered.replace(placeholder, replacement)
        if any(
            placeholder in rendered
            for placeholder in CV_SERVICE_SECTION_PLACEHOLDERS.values()
        ):
            service_replacements = {
                placeholder: render_cv_service_section_list_djot(
                    root,
                    section_key,
                    data_dir=data_dir,
                ).rstrip()
                for section_key, placeholder in CV_SERVICE_SECTION_PLACEHOLDERS.items()
            }
            for placeholder, replacement in service_replacements.items():
                rendered = rendered.replace(placeholder, replacement)
        if any(
            placeholder in rendered
            for placeholder in CV_PUBLICATIONS_SECTION_PLACEHOLDERS.values()
        ):
            publication_replacements = {
                placeholder: render_cv_publications_list_djot(
                    root,
                    listing_group,
                    publications_dir=publications_dir,
                ).rstrip()
                for listing_group, placeholder in CV_PUBLICATIONS_SECTION_PLACEHOLDERS.items()
            }
            for placeholder, replacement in publication_replacements.items():
                rendered = rendered.replace(placeholder, replacement)
        if CV_TALKS_LIST_PLACEHOLDER in rendered:
            rendered = rendered.replace(
                CV_TALKS_LIST_PLACEHOLDER,
                render_cv_talks_list_djot(
                    root,
                    talks_dir=talks_dir,
                ).rstrip(),
            )
        if CV_FUNDING_LIST_PLACEHOLDER in rendered:
            funding_path = (data_dir / FUNDING_DATA_NAME) if data_dir is not None else None
            rendered = rendered.replace(
                CV_FUNDING_LIST_PLACEHOLDER,
                render_cv_funding_list_djot(
                    root,
                    funding_path=funding_path,
                ).rstrip(),
            )
        return rendered

    if route_kind == "teaching_index_page" and route_key == "teaching":
        rendered = body
        replacements = {
            TEACHING_UW_COURSES_LIST_PLACEHOLDER: render_teaching_uw_courses_list_djot(
                root,
                data_dir=data_dir,
            ).rstrip(),
            TEACHING_SPECIAL_TOPICS_LIST_PLACEHOLDER: render_teaching_special_topics_list_djot(
                root,
                data_dir=data_dir,
            ).rstrip(),
            TEACHING_SUMMER_SCHOOL_LIST_PLACEHOLDER: render_teaching_summer_school_list_djot(
                root,
                data_dir=data_dir,
            ).rstrip(),
        }
        for placeholder, replacement in replacements.items():
            rendered = rendered.replace(placeholder, replacement)
        return rendered

    if route_kind == "publications_index_page" and route_key == "publications":
        try:
            rendered_main = render_publications_list_djot(
                root,
                "main",
                publications_dir=publications_dir,
            ).rstrip()
            rendered_workshop = render_publications_list_djot(
                root,
                "workshop",
                publications_dir=publications_dir,
            ).rstrip()
        except PublicationIndexError as err:
            raise PageProjectionError(str(err)) from err
        return (
            body.replace(PUBLICATIONS_MAIN_LIST_PLACEHOLDER, rendered_main).replace(
                PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
                rendered_workshop,
            )
        )

    return body
