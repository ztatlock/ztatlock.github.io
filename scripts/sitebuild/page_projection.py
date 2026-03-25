"""Helpers for rendering projection-backed collection pages."""

from __future__ import annotations

from pathlib import Path

from scripts.publication_index import (
    PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
    PublicationIndexError,
    render_publications_list_djot,
)
from scripts.service_index import (
    SERVICE_DEPARTMENT_LIST_PLACEHOLDER,
    SERVICE_MENTORING_LIST_PLACEHOLDER,
    SERVICE_ORGANIZING_LIST_PLACEHOLDER,
    SERVICE_REVIEWING_LIST_PLACEHOLDER,
    SERVICE_SECTION_PLACEHOLDERS,
    ServiceIndexError,
    render_public_service_section_list_djot,
)
from scripts.service_record import SERVICE_DATA_NAME
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
from scripts.talk_record import TalkRecordError, load_talk_records, render_talk_date
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


def _render_person_ref(*, display_name: str, ref_name: str) -> str:
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
    lines = [f"- {_render_person_ref(display_name=record.name, ref_name=person.name)}, {record.label}"]

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


def _render_uw_course_record(record: TeachingRecord) -> str:
    lines = [f"*{record.code}: {record.title}* \\"]
    if record.audience_label:
        lines.append(record.audience_label)
    if record.description_djot:
        lines.append(f"  {record.description_djot}")
    lines.append("")
    lines.append("{.columns .columns-8rem}")
    lines.extend(f"- {_render_teaching_offering(offering)}" for offering in record.offerings)
    return "\n".join(lines)


def render_teaching_uw_courses_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["uw_courses"]
    chunks = [_render_uw_course_record(record) for record in records]
    if not chunks:
        return ""
    return ("\n\n{.course-vspace}\n".join(chunks)) + "\n"


def _render_special_topics_record(record: TeachingRecord) -> str:
    first_offering = record.offerings[0]
    title = f"{record.code}: {record.title}, \\ {first_offering.year} {first_offering.term}"
    lines = [f"* {_render_title(title, first_offering.url)}"]
    if record.details:
        lines.append("")
        lines.extend(f"  - {detail}" for detail in record.details)
    return "\n".join(lines)


def render_teaching_special_topics_list_djot(
    root: Path,
    *,
    data_dir: Path | None = None,
) -> str:
    records = _teaching_group_records_by_key(root, data_dir=data_dir)["special_topics"]
    chunks = [_render_special_topics_record(record) for record in records]
    return "\n\n".join(chunks) + ("\n" if chunks else "")


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


def render_talks_list_djot(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> str:
    try:
        records = load_talk_records(root, talks_dir=talks_dir)
    except TalkRecordError as err:
        raise PageProjectionError(str(err)) from err

    chunks: list[str] = []
    for record in records:
        title = _render_title(record.title, record.url)
        at_text = ", ".join(_render_segment_text(segment.text, segment.url) for segment in record.at)
        date_text = render_talk_date(record.when)
        chunks.append(f"- {title} \\\n  {at_text}, {date_text}")
    return "\n\n".join(chunks) + ("\n" if chunks else "")


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
