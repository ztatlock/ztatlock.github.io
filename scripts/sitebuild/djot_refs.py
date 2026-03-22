"""Compose the site-wide Djot reference definitions."""

from __future__ import annotations

from pathlib import Path

from .people_refs import render_people_refs
from .people_registry import load_people_registry
from .template_refs import parse_template_refs


class DjotRefsError(ValueError):
    pass


def render_ref_entries(entries: tuple[tuple[str, str], ...]) -> str:
    return "".join(f"[{label}]: {url}\n" for label, url in entries)


def load_and_render_site_refs(*, people_path: Path, refs_path: Path) -> str:
    registry = load_people_registry(people_path)
    template_refs = parse_template_refs(refs_path)

    if template_refs.duplicate_labels:
        labels = ", ".join(sorted(template_refs.duplicate_labels))
        raise DjotRefsError(f"templates/REFS contains duplicate labels: {labels}")

    overlapping_labels = sorted(
        label for label in template_refs.label_to_url if label in registry.alias_to_key
    )
    if overlapping_labels:
        labels = ", ".join(overlapping_labels)
        raise DjotRefsError(
            "templates/REFS still contains person refs owned by people.json for: "
            f"{labels}"
        )

    manual_entries = tuple(sorted(template_refs.label_to_url.items(), key=lambda entry: entry[0]))

    rendered_people = render_people_refs(registry)
    rendered_manual = render_ref_entries(manual_entries)
    if rendered_manual:
        return f"{rendered_people}\n{rendered_manual}"
    return rendered_people
