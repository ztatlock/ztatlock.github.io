#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.publication_index import PublicationIndexError, load_publication_index_records
from scripts.sitebuild.people_registry import (
    PeopleRegistryError,
    PersonRecord,
    load_people_registry,
)


COLLABORATORS_INDEX_NAME = "index.dj"
COLLABORATORS_LIST_PLACEHOLDER = "__COLLABORATORS_LIST__"
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


def _preferred_label(person: PersonRecord) -> str:
    labels = (person.name, *person.aliases)
    return min(
        labels,
        key=lambda label: (
            len(label),
            0 if label == person.name else 1,
            label.casefold(),
        ),
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
                display_name=_preferred_label(person),
                is_linked=True,
            )

    entries = [
        *resolved_entries.values(),
        *(CollaboratorEntry(display_name=name, is_linked=False) for name in unresolved_names),
    ]
    return tuple(
        sorted(
            entries,
            key=lambda entry: (entry.display_name.casefold(), entry.display_name),
        )
    )


def _render_collaborator_entry_djot(entry: CollaboratorEntry) -> str:
    if entry.is_linked:
        return f"* [{entry.display_name}][]"
    return f"* {entry.display_name}"


def render_public_collaborators_list_djot(
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
    rendered = "\n".join(_render_collaborator_entry_djot(entry) for entry in entries)
    return rendered + ("\n" if rendered else "")
