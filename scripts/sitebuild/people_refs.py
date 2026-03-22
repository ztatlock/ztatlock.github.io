"""Render Djot reference definitions from the people registry."""

from __future__ import annotations

from pathlib import Path

from .people_registry import PeopleRegistry, load_people_registry


def iter_people_refs(registry: PeopleRegistry) -> tuple[tuple[str, str], ...]:
    entries: list[tuple[str, str]] = []
    for person in registry.people.values():
        for label in (person.name, *person.aliases):
            entries.append((label, person.url))
    return tuple(sorted(entries, key=lambda entry: entry[0]))


def render_people_refs(registry: PeopleRegistry) -> str:
    return "".join(f"[{label}]: {url}\n" for label, url in iter_people_refs(registry))


def load_and_render_people_refs(path: Path) -> str:
    return render_people_refs(load_people_registry(path))
