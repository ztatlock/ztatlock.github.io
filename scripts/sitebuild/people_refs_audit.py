"""Audit the manual REFS remainder against generated people refs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .people_registry import load_people_registry
from .template_refs import parse_template_refs


@dataclass(frozen=True)
class PeopleRefsAudit:
    overlapping_people_refs: tuple[str, ...]
    mismatched_urls: dict[str, tuple[str, str]]
    manual_remainder_refs: tuple[str, ...]
    duplicate_template_labels: dict[str, tuple[str, ...]]


def audit_people_refs(
    *,
    people_path: Path,
    refs_path: Path,
) -> PeopleRefsAudit:
    registry = load_people_registry(people_path)
    template_refs = parse_template_refs(refs_path)

    overlapping_people_refs = []
    mismatched_urls: dict[str, tuple[str, str]] = {}
    for label in sorted(template_refs.label_to_url):
        person_key = registry.alias_to_key.get(label)
        if person_key is None:
            continue
        template_url = template_refs.label_to_url[label]
        generated_url = registry.person(person_key).url
        if template_url == generated_url:
            overlapping_people_refs.append(label)
        else:
            mismatched_urls[label] = (template_url, generated_url)

    manual_remainder_refs = tuple(
        sorted(label for label in template_refs.label_to_url if label not in registry.alias_to_key)
    )

    return PeopleRefsAudit(
        overlapping_people_refs=tuple(overlapping_people_refs),
        mismatched_urls=mismatched_urls,
        manual_remainder_refs=manual_remainder_refs,
        duplicate_template_labels=template_refs.duplicate_labels,
    )
