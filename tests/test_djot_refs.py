from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.djot_refs import DjotRefsError, load_and_render_site_refs


class DjotRefsTests(unittest.TestCase):
    def test_composed_refs_use_generated_people_and_manual_remainder(self) -> None:
        people_payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["A Person"],
                }
            }
        }
        refs_raw = "[UW]: https://example.com/uw\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            rendered = load_and_render_site_refs(
                people_path=people_path,
                refs_path=refs_path,
            )

        self.assertEqual(
            rendered,
            "[A Person]: https://example.com/alpha\n"
            "[Alpha Person]: https://example.com/alpha\n"
            "\n"
            "[UW]: https://example.com/uw\n",
        )

    def test_composed_refs_rejects_duplicate_manual_labels(self) -> None:
        people_payload = {"people": {}}
        refs_raw = """[UW]: https://example.com/uw
[UW]: https://example.com/uw
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            with self.assertRaisesRegex(
                DjotRefsError,
                "templates/REFS contains duplicate labels",
            ):
                load_and_render_site_refs(
                    people_path=people_path,
                    refs_path=refs_path,
                )

    def test_composed_refs_rejects_person_labels_in_manual_remainder(self) -> None:
        people_payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                }
            }
        }
        refs_raw = "[Alpha Person]: https://example.com/alpha\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            with self.assertRaisesRegex(
                DjotRefsError,
                "templates/REFS still contains person refs owned by people.json",
            ):
                load_and_render_site_refs(
                    people_path=people_path,
                    refs_path=refs_path,
                )

    def test_composed_refs_allows_new_manual_non_person_label(self) -> None:
        people_payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                }
            }
        }
        refs_raw = "[Unexpected Label]: https://example.com/unexpected\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            rendered = load_and_render_site_refs(
                people_path=people_path,
                refs_path=refs_path,
            )

        self.assertEqual(
            rendered,
            "[Alpha Person]: https://example.com/alpha\n"
            "\n"
            "[Unexpected Label]: https://example.com/unexpected\n",
        )


if __name__ == "__main__":
    unittest.main()
