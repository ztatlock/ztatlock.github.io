from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.people_refs_audit import audit_people_refs
from scripts.sitebuild.template_refs import parse_template_refs


class PeopleRefsAuditTests(unittest.TestCase):
    def test_parse_template_refs_tracks_duplicate_labels(self) -> None:
        raw = """[Alpha Person]: https://example.com/alpha
[Alpha Person]: https://example.com/alpha
[Beta Person]: https://example.com/beta
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "REFS"
            path.write_text(raw, encoding="utf-8")
            parsed = parse_template_refs(path)

        self.assertEqual(parsed.label_to_url["Alpha Person"], "https://example.com/alpha")
        self.assertEqual(
            parsed.duplicate_labels["Alpha Person"],
            ("https://example.com/alpha", "https://example.com/alpha"),
        )

    def test_audit_classifies_matches_missing_non_people_and_extra(self) -> None:
        people_payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/alpha",
                    "aliases": ["A Person"],
                },
                "beta-person": {
                    "name": "Beta Person",
                    "url": "https://example.com/beta",
                },
            }
        }
        refs_raw = """[Alpha Person]: https://example.com/alpha
[PGAS]: https://www.cs.washington.edu/
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            audit = audit_people_refs(
                people_path=people_path,
                refs_path=refs_path,
            )

        self.assertEqual(audit.overlapping_people_refs, ("Alpha Person",))
        self.assertEqual(audit.manual_remainder_refs, ("PGAS",))

    def test_audit_detects_url_mismatches(self) -> None:
        people_payload = {
            "people": {
                "alpha-person": {
                    "name": "Alpha Person",
                    "url": "https://example.com/generated",
                }
            }
        }
        refs_raw = "[Alpha Person]: https://example.com/template\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            people_path = tmp / "people.json"
            refs_path = tmp / "REFS"
            people_path.write_text(json.dumps(people_payload), encoding="utf-8")
            refs_path.write_text(refs_raw, encoding="utf-8")
            audit = audit_people_refs(
                people_path=people_path,
                refs_path=refs_path,
            )

        self.assertEqual(
            audit.mismatched_urls["Alpha Person"],
            ("https://example.com/template", "https://example.com/generated"),
        )


if __name__ == "__main__":
    unittest.main()
