"""Helpers for rendering projection-backed collection pages."""

from __future__ import annotations

from pathlib import Path

from scripts.publication_index import (
    PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
    PublicationIndexError,
    render_publications_list_djot,
)
from scripts.student_record import (
    STUDENTS_DATA_NAME,
    StudentRecord,
    StudentRecordError,
    load_student_sections,
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
