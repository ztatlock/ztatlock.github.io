"""Shared people-registry loading and validation helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

PEOPLE_ROOT_KEY = "people"
PERSON_ALLOWED_FIELDS = {"name", "url", "aliases"}
PERSON_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PeopleRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class PersonRecord:
    key: str
    name: str
    url: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class PeopleRegistry:
    people: dict[str, PersonRecord]
    alias_to_key: dict[str, str]

    def person(self, key: str) -> PersonRecord:
        try:
            return self.people[key]
        except KeyError as err:
            raise PeopleRegistryError(f"unknown person key: {key}") from err

    def resolve_alias(self, alias: str) -> str:
        try:
            return self.alias_to_key[alias]
        except KeyError as err:
            raise PeopleRegistryError(f"unknown person alias: {alias}") from err


def _require_string(raw: object, *, context: str, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise PeopleRegistryError(f"{context}: missing {field}")
    return raw.strip()


def _optional_string_list(raw: object, *, context: str, field: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise PeopleRegistryError(f"{context}: {field} must be an array or null")

    values: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(raw):
        value = _require_string(entry, context=f"{context}.{field}[{index}]", field="value")
        if value in seen:
            raise PeopleRegistryError(f"{context}: duplicate {field} value {value!r}")
        seen.add(value)
        values.append(value)
    return tuple(values)


def _normalize_person(key: str, raw: object, *, context: str) -> PersonRecord:
    if not PERSON_KEY_RE.fullmatch(key):
        raise PeopleRegistryError(
            f"{context}: invalid key {key!r}; expected lowercase words joined by hyphens"
        )
    if not isinstance(raw, dict):
        raise PeopleRegistryError(f"{context}: expected a JSON object")

    unknown_fields = sorted(set(raw) - PERSON_ALLOWED_FIELDS)
    if unknown_fields:
        raise PeopleRegistryError(f"{context}: unknown fields: {', '.join(unknown_fields)}")

    name = _require_string(raw.get("name"), context=context, field="name")
    url = _require_string(raw.get("url"), context=context, field="url")
    aliases = _optional_string_list(raw.get("aliases"), context=context, field="aliases")
    if name in aliases:
        raise PeopleRegistryError(
            f"{context}: aliases must not repeat name {name!r}"
        )

    return PersonRecord(
        key=key,
        name=name,
        url=url,
        aliases=aliases,
    )


def _load_json_object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise PeopleRegistryError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_people_registry(path: Path) -> PeopleRegistry:
    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_load_json_object_pairs,
        )
    except FileNotFoundError as err:
        raise PeopleRegistryError(f"missing people registry: {path}") from err
    except PeopleRegistryError as err:
        raise PeopleRegistryError(f"{path}: {err}") from err
    except json.JSONDecodeError as err:
        raise PeopleRegistryError(f"{path}:{err.lineno}: invalid JSON: {err.msg}") from err

    if not isinstance(raw, dict):
        raise PeopleRegistryError(f"{path}: expected a JSON object")
    if set(raw) != {PEOPLE_ROOT_KEY}:
        unknown = sorted(set(raw) - {PEOPLE_ROOT_KEY})
        if PEOPLE_ROOT_KEY not in raw:
            raise PeopleRegistryError(f"{path}: missing {PEOPLE_ROOT_KEY}")
        raise PeopleRegistryError(f"{path}: unknown top-level fields: {', '.join(unknown)}")

    people_raw = raw[PEOPLE_ROOT_KEY]
    if not isinstance(people_raw, dict):
        raise PeopleRegistryError(f"{path}: {PEOPLE_ROOT_KEY} must be a JSON object")

    people: dict[str, PersonRecord] = {}
    alias_to_key: dict[str, str] = {}
    for key in sorted(people_raw):
        person = _normalize_person(key, people_raw[key], context=f"{path}:{key}")
        people[key] = person

        # Names and aliases share one namespace on purpose: every human-facing
        # string should resolve to exactly one person key.
        for alias in (person.name, *person.aliases):
            prior = alias_to_key.get(alias)
            if prior is not None and prior != key:
                raise PeopleRegistryError(
                    f"{path}:{key}: alias {alias!r} already claimed by {prior}"
                )
            alias_to_key[alias] = key

    return PeopleRegistry(
        people=people,
        alias_to_key=alias_to_key,
    )
