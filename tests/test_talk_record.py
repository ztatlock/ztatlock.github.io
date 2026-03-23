from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.talk_record import (
    TalkRecordError,
    discover_talk_slugs,
    find_talk_record_issues,
    load_talk_record,
    load_talk_records,
    render_talk_date,
)


class TalkRecordTests(unittest.TestCase):
    def test_loads_month_based_talk_record(self) -> None:
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
                        "at": [
                            {"text": "Brown University"},
                            {"text": "PL and Graphics groups"},
                        ],
                        "url": "https://events.brown.edu/demo",
                    }
                ),
                encoding="utf-8",
            )

            record = load_talk_record(root, "2026-02-brown-eqsat", talks_dir=talks_dir)
            self.assertEqual(record.slug, "2026-02-brown-eqsat")
            self.assertEqual(record.title, "Everything is a compiler, try Equality Saturation!")
            self.assertEqual(render_talk_date(record.when), "February 2026")
            self.assertEqual(record.at[1].text, "PL and Graphics groups")
            self.assertEqual(record.url, "https://events.brown.edu/demo")

    def test_loads_season_based_talk_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            talk_dir = talks_dir / "2023-fall-synopsys-egg"
            talk_dir.mkdir(parents=True)
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Relational Equality Saturation in egg",
                        "when": {"year": 2023, "season": "fall"},
                        "at": [{"text": "Synopsys Inc."}],
                    }
                ),
                encoding="utf-8",
            )

            record = load_talk_record(root, "2023-fall-synopsys-egg", talks_dir=talks_dir)
            self.assertEqual(render_talk_date(record.when), "Fall 2023")

    def test_rejects_invalid_date_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            talk_dir = talks_dir / "bad-talk"
            talk_dir.mkdir(parents=True)
            (talk_dir / "talk.json").write_text(
                json.dumps(
                    {
                        "title": "Bad Talk",
                        "when": {"year": 2024, "month": 5, "season": "spring"},
                        "at": [{"text": "Nowhere"}],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(TalkRecordError):
                load_talk_record(root, "bad-talk", talks_dir=talks_dir)

    def test_finds_missing_talk_json_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            talks_dir = root / "site" / "talks"
            (talks_dir / "empty-talk").mkdir(parents=True)

            self.assertEqual(
                find_talk_record_issues(root, talks_dir=talks_dir),
                [f"{talks_dir / 'empty-talk'}: missing talk.json"],
            )

    def test_load_talk_records_sorts_reverse_chronologically(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            talks_dir = root / "site" / "talks"
            entries = {
                "2024-11-cornell-eqsat": {
                    "title": "When You've Got EqSat, Everything Is a Compiler",
                    "when": {"year": 2024, "month": 11},
                    "at": [{"text": "Cornell University"}],
                },
                "2026-02-brown-eqsat": {
                    "title": "Everything is a compiler, try Equality Saturation!",
                    "when": {"year": 2026, "month": 2},
                    "at": [{"text": "Brown University"}],
                },
            }
            for slug, rows in entries.items():
                talk_dir = talks_dir / slug
                talk_dir.mkdir(parents=True)
                (talk_dir / "talk.json").write_text(json.dumps(rows), encoding="utf-8")

            self.assertEqual(discover_talk_slugs(root, talks_dir=talks_dir), tuple(sorted(entries)))
            records = load_talk_records(root, talks_dir=talks_dir)
            self.assertEqual([record.slug for record in records], ["2026-02-brown-eqsat", "2024-11-cornell-eqsat"])
