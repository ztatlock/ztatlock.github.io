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

    def test_skips_linkless_people_and_uses_public_link_fallbacks(self) -> None:
        payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "linkedin": "https://linkedin.example/alpha",
                    "aliases": ["A Person"],
                },
                "beta-person": {
                    "name": "Beta Person",
                    "github": "https://github.com/beta",
                },
                "gamma-person": {
                    "name": "Gamma Person",
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
                    ("A Person", "https://linkedin.example/alpha"),
                    ("Alpha Person", "https://linkedin.example/alpha"),
                    ("Beta Person", "https://github.com/beta"),
                ),
            )

    def test_seed_registry_renders_expected_labels(self) -> None:
        root = Path(__file__).resolve().parent.parent
        people_path = root / "site" / "data" / "people.json"
        rendered = load_and_render_people_refs(people_path)

        self.assertIn("[Adam Anderson]: https://github.com/AdamEAnderson/\n", rendered)
        self.assertIn("[Aditya Akhileshwaran]: https://www.linkedin.com/in/adiakhil\n", rendered)
        self.assertIn(
            "[Christopher Mackie]: https://www.linkedin.com/in/christopher-mackie-881903b0/\n",
            rendered,
        )
        self.assertIn(
            "[Chris Mackie]: https://www.linkedin.com/in/christopher-mackie-881903b0/\n",
            rendered,
        )
        self.assertIn("[Gus Henry Smith]: https://justg.us/\n", rendered)
        self.assertIn("[Gus Smith]: https://justg.us/\n", rendered)
        self.assertIn("[Kenny Wu]: https://www.linkedin.com/in/anshuowu/\n", rendered)
        self.assertIn(
            "[Anshuo (Kenny) Wu]: https://www.linkedin.com/in/anshuowu/\n",
            rendered,
        )
        self.assertIn(
            "[Jennifer Tao]: https://www.linkedin.com/in/tingjia-jennifer-tao/\n",
            rendered,
        )
        self.assertIn(
            "[Tingjia (Jennifer) Tao]: https://www.linkedin.com/in/tingjia-jennifer-tao/\n",
            rendered,
        )
        self.assertIn(
            "[Sam Gao]: https://www.linkedin.com/in/sam-gao/\n",
            rendered,
        )
        self.assertIn(
            "[Zhengyang Gao]: https://www.linkedin.com/in/sam-gao/\n",
            rendered,
        )
        self.assertIn("[Steven L. Tanimoto]: https://www.cs.washington.edu/people/faculty/tanimoto\n", rendered)
        self.assertIn("[Steve Tanimoto]: https://www.cs.washington.edu/people/faculty/tanimoto\n", rendered)
        self.assertIn(
            "[Taylor Coffman]: https://www.linkedin.com/in/taylor-coffman-bb1626170/\n",
            rendered,
        )
        self.assertIn(
            "[Levi Coffman]: https://www.linkedin.com/in/taylor-coffman-bb1626170/\n",
            rendered,
        )


if __name__ == "__main__":
    unittest.main()
