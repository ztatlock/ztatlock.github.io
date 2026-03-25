from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse

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

    def test_seed_registry_uses_name_as_default_label_and_aliases_for_resolution(self) -> None:
        registry = load_people_registry(PEOPLE_PATH)

        cases = (
            ("gus-smith", "Gus Smith", ("Gus Henry Smith",)),
            ("gilbert-bernstein", "Gilbert Bernstein", ("Gilbert Louis Bernstein",)),
            ("remy-wang", "Remy Wang", ("Yisu Remy Wang",)),
            ("steven-tanimoto", "Steve Tanimoto", ("Steven L. Tanimoto",)),
            ("michael-ernst", "Mike Ernst", ("Michael Ernst", "Michael D. Ernst")),
        )

        for key, expected_name, expected_aliases in cases:
            person = registry.person(key)
            self.assertEqual(person.name, expected_name)
            self.assertEqual(person.aliases, expected_aliases)

            self.assertEqual(registry.resolve_alias(expected_name), key)
            for alias in expected_aliases:
                self.assertEqual(registry.resolve_alias(alias), key)

    def test_accepts_optional_public_link_fields_and_primary_url_fallback(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "linkedin": "https://linkedin.example/alpha",
                },
                "beta-person": {
                    "name": "Beta Person",
                    "github": "https://github.com/beta",
                },
                "gamma-person": {
                    "name": "Gamma Person",
                    "url": "https://example.com/gamma",
                    "linkedin": "https://linkedin.example/gamma",
                    "github": "https://github.com/gamma",
                },
                "delta-person": {
                    "name": "Delta Person",
                },
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            registry = load_people_registry(path)

        self.assertEqual(
            registry.person("alpha-person").primary_url,
            "https://linkedin.example/alpha",
        )
        self.assertEqual(
            registry.person("beta-person").primary_url,
            "https://github.com/beta",
        )
        self.assertEqual(
            registry.person("gamma-person").primary_url,
            "https://example.com/gamma",
        )
        self.assertIsNone(registry.person("delta-person").primary_url)

    def test_seed_registry_preserves_primary_url_for_social_only_profiles(self) -> None:
        registry = load_people_registry(PEOPLE_PATH)

        cases = (
            (
                "aditya-akhileshwaran",
                None,
                "https://www.linkedin.com/in/adiakhil",
                None,
                "https://www.linkedin.com/in/adiakhil",
            ),
            (
                "andrew-liu",
                None,
                None,
                "https://github.com/hypercubestart/",
                "https://github.com/hypercubestart/",
            ),
            (
                "bill-zorn",
                None,
                "https://www.linkedin.com/in/bill-zorn-265872141",
                None,
                "https://www.linkedin.com/in/bill-zorn-265872141",
            ),
            (
                "justin-adsuara",
                None,
                None,
                "https://github.com/justinads",
                "https://github.com/justinads",
            ),
        )

        for key, expected_url, expected_linkedin, expected_github, expected_primary in cases:
            person = registry.person(key)
            self.assertEqual(person.url, expected_url)
            self.assertEqual(person.linkedin, expected_linkedin)
            self.assertEqual(person.github, expected_github)
            self.assertEqual(person.primary_url, expected_primary)

    def test_seed_registry_has_no_social_hosts_left_in_url_field(self) -> None:
        raw = json.loads(PEOPLE_PATH.read_text(encoding="utf-8"))
        people = raw["people"]

        for key, person in people.items():
            url = person.get("url")
            if url is None:
                continue
            host = urlparse(url).netloc.lower()
            self.assertNotIn(
                host,
                {"linkedin.com", "www.linkedin.com", "github.com", "www.github.com"},
                msg=f"{key} still stores a social-profile URL in url",
            )

    def test_unknown_link_field_is_rejected(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "mastodon": "https://example.social/@alpha",
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(PeopleRegistryError, "unknown fields: mastodon"):
                load_people_registry(path)

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
