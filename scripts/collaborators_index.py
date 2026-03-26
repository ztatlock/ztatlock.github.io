#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import string
import unicodedata

from scripts.publication_index import PublicationIndexError, load_publication_index_records
from scripts.student_record import StudentRecordError, load_student_sections
from scripts.teaching_record import TeachingRecordError, load_teaching_groups
from scripts.sitebuild.people_registry import (
    PeopleRegistryError,
    load_people_registry,
)


COLLABORATORS_INDEX_NAME = "index.dj"
RESEARCH_COLLABORATORS_LIST_PLACEHOLDER = "__RESEARCH_COLLABORATORS_LIST__"
TEACHING_COLLABORATORS_LIST_PLACEHOLDER = "__TEACHING_COLLABORATORS_LIST__"
COLLABORATORS_FIRST_INITIAL_GAPS_PLACEHOLDER = "__COLLABORATORS_FIRST_INITIAL_GAPS__"
COLLABORATORS_LAST_INITIAL_GAPS_PLACEHOLDER = "__COLLABORATORS_LAST_INITIAL_GAPS__"
SELF_PERSON_KEY = "zachary-tatlock"
SELF_NAME = "Zachary Tatlock"


class CollaboratorsIndexError(ValueError):
    pass


@dataclass(frozen=True)
class CollaboratorEntry:
    display_name: str
    is_linked: bool


def collaborators_index_path(root: Path, *, collaborators_dir: Path | None = None) -> Path:
    actual_collaborators_dir = collaborators_dir or (root / "site" / "collaborators")
    return (actual_collaborators_dir / COLLABORATORS_INDEX_NAME).resolve()


def _sort_collaborator_entries(
    entries: list[CollaboratorEntry],
) -> tuple[CollaboratorEntry, ...]:
    return tuple(
        sorted(
            entries,
            key=lambda entry: (entry.display_name.casefold(), entry.display_name),
        )
    )


def load_collaborator_entries(
    root: Path,
    *,
    publications_dir: Path | None = None,
    people_path: Path | None = None,
) -> tuple[CollaboratorEntry, ...]:
    actual_people_path = people_path or (root / "site" / "data" / "people.json")
    try:
        records = load_publication_index_records(root, publications_dir=publications_dir)
        registry = load_people_registry(actual_people_path)
    except PublicationIndexError as err:
        raise CollaboratorsIndexError(str(err)) from err
    except PeopleRegistryError as err:
        raise CollaboratorsIndexError(str(err)) from err

    resolved_entries: dict[str, CollaboratorEntry] = {}
    unresolved_names: set[str] = set()
    for record in records:
        for author in record.authors:
            raw_name = author.name.strip()
            try:
                person_key = registry.resolve_alias(raw_name)
            except PeopleRegistryError:
                if raw_name != SELF_NAME:
                    unresolved_names.add(raw_name)
                continue

            if person_key == SELF_PERSON_KEY:
                continue
            if person_key in resolved_entries:
                continue

            person = registry.person(person_key)
            resolved_entries[person_key] = CollaboratorEntry(
                display_name=person.name,
                is_linked=person.primary_url is not None,
            )

    entries = [
        *resolved_entries.values(),
        *(CollaboratorEntry(display_name=name, is_linked=False) for name in unresolved_names),
    ]
    return _sort_collaborator_entries(entries)


def load_research_collaborator_entries(
    root: Path,
    *,
    publications_dir: Path | None = None,
    people_path: Path | None = None,
    students_path: Path | None = None,
) -> tuple[CollaboratorEntry, ...]:
    actual_people_path = people_path or (root / "site" / "data" / "people.json")
    try:
        records = load_publication_index_records(root, publications_dir=publications_dir)
        registry = load_people_registry(actual_people_path)
        sections = load_student_sections(
            root,
            students_path=students_path,
            people_path=actual_people_path,
        )
    except PublicationIndexError as err:
        raise CollaboratorsIndexError(str(err)) from err
    except PeopleRegistryError as err:
        raise CollaboratorsIndexError(str(err)) from err
    except StudentRecordError as err:
        raise CollaboratorsIndexError(str(err)) from err

    resolved_entries: dict[str, CollaboratorEntry] = {}
    unresolved_names: set[str] = set()

    def add_person_key(person_key: str) -> None:
        if person_key == SELF_PERSON_KEY or person_key in resolved_entries:
            return
        person = registry.person(person_key)
        resolved_entries[person_key] = CollaboratorEntry(
            display_name=person.name,
            is_linked=person.primary_url is not None,
        )

    for record in records:
        for author in record.authors:
            raw_name = author.name.strip()
            try:
                person_key = registry.resolve_alias(raw_name)
            except PeopleRegistryError:
                if raw_name != SELF_NAME:
                    unresolved_names.add(raw_name)
                continue
            add_person_key(person_key)

    for section in sections:
        for record in section.records:
            add_person_key(record.person_key)

    resolved_names = {entry.display_name for entry in resolved_entries.values()}
    entries = [
        *resolved_entries.values(),
        *(
            CollaboratorEntry(display_name=name, is_linked=False)
            for name in unresolved_names
            if name not in resolved_names
        ),
    ]
    return _sort_collaborator_entries(entries)


def load_teaching_collaborator_entries(
    root: Path,
    *,
    people_path: Path | None = None,
    teaching_path: Path | None = None,
) -> tuple[CollaboratorEntry, ...]:
    actual_people_path = people_path or (root / "site" / "data" / "people.json")
    try:
        registry = load_people_registry(actual_people_path)
        groups = load_teaching_groups(
            root,
            teaching_path=teaching_path,
        )
    except PeopleRegistryError as err:
        raise CollaboratorsIndexError(str(err)) from err
    except TeachingRecordError as err:
        raise CollaboratorsIndexError(str(err)) from err

    resolved_entries: dict[str, CollaboratorEntry] = {}

    def add_person_key(person_key: str) -> None:
        if person_key == SELF_PERSON_KEY or person_key in resolved_entries:
            return
        person = registry.person(person_key)
        resolved_entries[person_key] = CollaboratorEntry(
            display_name=person.name,
            is_linked=person.primary_url is not None,
        )

    for group in groups:
        for record in group.records:
            for offering in record.offerings:
                for person_key in (
                    *offering.co_instructors,
                    *offering.teaching_assistants,
                    *offering.tutors,
                ):
                    add_person_key(person_key)

    return _sort_collaborator_entries(list(resolved_entries.values()))


def _normalized_ascii_initial(token: str) -> str | None:
    for char in unicodedata.normalize("NFKD", token):
        if not char.isalpha():
            continue
        upper = char.upper()
        if upper in string.ascii_uppercase:
            return upper
    return None


def _missing_collaborator_initials(
    entries: tuple[CollaboratorEntry, ...],
    *,
    pick_token,
) -> tuple[str, ...]:
    present: set[str] = set()
    for entry in entries:
        tokens = entry.display_name.split()
        if not tokens:
            continue
        token = pick_token(tokens)
        initial = _normalized_ascii_initial(token)
        if initial is not None:
            present.add(initial)
    return tuple(letter for letter in string.ascii_uppercase if letter not in present)


def render_missing_collaborator_first_initials(
    root: Path,
    *,
    publications_dir: Path | None = None,
    people_path: Path | None = None,
) -> str:
    entries = load_collaborator_entries(
        root,
        publications_dir=publications_dir,
        people_path=people_path,
    )
    missing = _missing_collaborator_initials(entries, pick_token=lambda tokens: tokens[0])
    return ", ".join(missing)


def render_missing_collaborator_last_initials(
    root: Path,
    *,
    publications_dir: Path | None = None,
    people_path: Path | None = None,
) -> str:
    entries = load_collaborator_entries(
        root,
        publications_dir=publications_dir,
        people_path=people_path,
    )
    missing = _missing_collaborator_initials(entries, pick_token=lambda tokens: tokens[-1])
    return ", ".join(missing)


def _render_collaborator_entry_djot(entry: CollaboratorEntry) -> str:
    if entry.is_linked:
        return f"* [{entry.display_name}][]"
    return f"* {entry.display_name}"


def _render_collaborator_entries_djot(entries: tuple[CollaboratorEntry, ...]) -> str:
    rendered = "\n".join(_render_collaborator_entry_djot(entry) for entry in entries)
    return rendered + ("\n" if rendered else "")


def render_public_research_collaborators_list_djot(
    root: Path,
    *,
    publications_dir: Path | None = None,
    people_path: Path | None = None,
    students_path: Path | None = None,
) -> str:
    entries = load_research_collaborator_entries(
        root,
        publications_dir=publications_dir,
        people_path=people_path,
        students_path=students_path,
    )
    return _render_collaborator_entries_djot(entries)


def render_public_teaching_collaborators_list_djot(
    root: Path,
    *,
    people_path: Path | None = None,
    teaching_path: Path | None = None,
) -> str:
    entries = load_teaching_collaborator_entries(
        root,
        people_path=people_path,
        teaching_path=teaching_path,
    )
    return _render_collaborator_entries_djot(entries)
