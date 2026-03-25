from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.people_registry import PeopleRegistryError, load_people_registry


ROOT = Path(__file__).resolve().parent.parent
PEOPLE_PATH = ROOT / "site" / "data" / "people.json"


class PeopleRegistryTests(unittest.TestCase):
    def test_seed_registry_loads_and_resolves_aliases(self) -> None:
        registry = load_people_registry(PEOPLE_PATH)

        self.assertEqual(registry.resolve_alias("Gus Henry Smith"), "gus-smith")
        self.assertEqual(registry.resolve_alias("Gus Smith"), "gus-smith")
        self.assertEqual(registry.resolve_alias("Steve Tanimoto"), "steven-tanimoto")
        self.assertEqual(registry.resolve_alias("Steven L. Tanimoto"), "steven-tanimoto")
        self.assertEqual(registry.resolve_alias("Remy Wang"), "remy-wang")
        self.assertEqual(registry.resolve_alias("Yisu Remy Wang"), "remy-wang")
        self.assertEqual(
            registry.person("gilbert-bernstein").name,
            "Gilbert Bernstein",
        )
        self.assertEqual(registry.person("steven-tanimoto").name, "Steve Tanimoto")
        self.assertEqual(registry.person("michael-ernst").name, "Mike Ernst")

    def test_duplicate_alias_is_rejected(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["Shared Alias"],
                },
                "beta-person": {
                    "name": "Beta Person",
                    "url": "https://example.com/beta",
                    "aliases": ["Shared Alias"],
                },
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "Shared Alias"):
                load_people_registry(path)

    def test_duplicate_alias_within_person_is_rejected(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["Repeated Alias", "Repeated Alias"],
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "duplicate aliases value"):
                load_people_registry(path)

    def test_duplicate_name_is_rejected(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Shared Name",
                    "url": "https://example.com/alpha",
                },
                "beta-person": {
                    "name": "Shared Name",
                    "url": "https://example.com/beta",
                },
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "Shared Name"):
                load_people_registry(path)

    def test_alias_must_not_collide_with_another_name(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                },
                "beta-person": {
                    "name": "Beta Person",
                    "url": "https://example.com/beta",
                    "aliases": ["Alpha Person"],
                },
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "Alpha Person"):
                load_people_registry(path)

    def test_alias_must_not_repeat_name(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["Alpha Person"],
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "must not repeat name"):
                load_people_registry(path)

    def test_duplicate_json_key_is_rejected(self) -> None:
        raw = """{
  "people": {
    "alpha-person": {
      "name": "Alpha Person",
      "url": "https://example.com/alpha"
    },
    "alpha-person": {
      "name": "Alpha Person Two",
      "url": "https://example.com/alpha-two"
    }
  }
}
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(raw, encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "duplicate JSON key"):
                load_people_registry(path)

    def test_invalid_key_is_rejected(self) -> None:
        payload = {
            "people": {
                "Bad Key": {
                    "name": "Bad Key",
                    "url": "https://example.com/bad",
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "invalid key"):
                load_people_registry(path)


if __name__ == "__main__":
    unittest.main()
