from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.people_refs import iter_people_refs, load_and_render_people_refs
from scripts.sitebuild.people_registry import load_people_registry


class PeopleRefsTests(unittest.TestCase):
    def test_iter_people_refs_sorts_labels_deterministically(self) -> None:
        payload = {
            "people": {
                "beta-person": {
                    "name": "Beta Person",
                    "url": "https://example.com/beta",
                    "aliases": ["Bee Person"],
                },
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["A Person"],
                },
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            registry = load_people_registry(path)
            self.assertEqual(
                iter_people_refs(registry),
                (
                    ("A Person", "https://example.com/alpha"),
                    ("Alpha Person", "https://example.com/alpha"),
                    ("Bee Person", "https://example.com/beta"),
                    ("Beta Person", "https://example.com/beta"),
                ),
            )

    def test_rendered_output_is_plain_djot_refs(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["A Person"],
                }
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "people.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                load_and_render_people_refs(path),
                "[A Person]: https://example.com/alpha\n"
                "[Alpha Person]: https://example.com/alpha\n",
            )

    def test_seed_registry_renders_expected_labels(self) -> None:
        root = Path(__file__).resolve().parent.parent
        people_path = root / "site" / "data" / "people.json"
        rendered = load_and_render_people_refs(people_path)

        self.assertIn("[Gus Henry Smith]: https://justg.us/\n", rendered)
        self.assertIn("[Gus Smith]: https://justg.us/\n", rendered)
        self.assertIn("[Steven L. Tanimoto]: https://www.cs.washington.edu/people/faculty/tanimoto\n", rendered)
        self.assertIn("[Steve Tanimoto]: https://www.cs.washington.edu/people/faculty/tanimoto\n", rendered)


if __name__ == "__main__":
    unittest.main()
