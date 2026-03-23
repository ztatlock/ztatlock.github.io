from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.sitebuild.talk_projection import (
    TALKS_LIST_PLACEHOLDER,
    apply_page_projections,
    render_talks_list_djot,
)


class TalkProjectionTests(unittest.TestCase):
    def test_renders_talks_list_from_bundles(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            first = talks_dir / "2026-02-brown-eqsat"
            first.mkdir(parents=True)
            (first / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Everything is a compiler, try Equality Saturation!",
                        "when": {"year": 2026, "month": 2},
                        "at": [
                            {"text": "Brown University"},
                            {"text": "PL and Graphics groups"},
                        ],
                        "url": "https://events.brown.edu/demo",
                    }
                ),
                encoding="utf-8",
            )
            second = talks_dir / "2023-05-uiuc-egg"
            second.mkdir(parents=True)
            (second / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Relational Equality Saturation in egg",
                        "when": {"year": 2023, "month": 5},
                        "at": [
                            {"text": "University of Illinois at Urbana-Champaign"},
                            {
                                "text": "Compilers Seminar",
                                "url": "https://compilerseminar.web.illinois.edu/",
                            },
                        ],
                        "url": "talk-2023-05-egg-uiuc.html",
                    }
                ),
                encoding="utf-8",
            )

            rendered = render_talks_list_djot(root, talks_dir=talks_dir)
            self.assertIn(
                "- [Everything is a compiler, try Equality Saturation!](https://events.brown.edu/demo) \\",
                rendered,
            )
            self.assertIn(
                "Brown University, PL and Graphics groups, February 2026",
                rendered,
            )
            self.assertIn(
                "- [Relational Equality Saturation in egg](talk-2023-05-egg-uiuc.html) \\",
                rendered,
            )
            self.assertIn(
                "University of Illinois at Urbana-Champaign, [Compilers Seminar](https://compilerseminar.web.illinois.edu/), May 2023",
                rendered,
            )
            self.assertLess(rendered.find("February 2026"), rendered.find("May 2023"))

    def test_applies_projection_only_to_talks_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            talk_dir = talks_dir / "2026-02-brown-eqsat"
            talk_dir.mkdir(parents=True)
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Everything is a compiler, try Equality Saturation!",
                        "when": {"year": 2026, "month": 2},
                        "at": [{"text": "Brown University"}],
                    }
                ),
                encoding="utf-8",
            )

            body = "# Talks\n\n" + TALKS_LIST_PLACEHOLDER + "\n"
            rendered = apply_page_projections("talks", body, root=root, talks_dir=talks_dir)
            self.assertNotIn(TALKS_LIST_PLACEHOLDER, rendered)
            self.assertIn("Brown University, February 2026", rendered)

            self.assertEqual(
                apply_page_projections("about", body, root=root, talks_dir=talks_dir),
                body,
            )
