from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.news_record import (
    NewsRecordError,
    find_news_record_issues,
    load_news_records,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_news(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"records": records}, ensure_ascii=False),
        encoding="utf-8",
    )


class NewsRecordTests(unittest.TestCase):
    def test_seed_news_registry_loads(self) -> None:
        records = load_news_records(ROOT)
        by_key = {record.key: record for record in records}

        self.assertEqual(len(records), 23)
        self.assertEqual(records[0].key, "2026-02-brown-talk")
        self.assertEqual(records[-1].key, "2017-08-neutrons-feature")
        self.assertEqual(by_key["2025-02-sigplan-research-highlights-egg"].kind, "recognition")
        self.assertEqual(by_key["2023-10-haploid-release"].kind, "release")
        self.assertEqual(by_key["2023-09-cse-507-teaching"].emoji, "🧑‍🏫")
        self.assertFalse(by_key["2026-02-brown-talk"].homepage_featured)
        self.assertIn("[Anjali][Anjali Pal]", by_key["2023-10-enumo-oopsla"].body_djot)

    def test_duplicate_record_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 2,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Demo.",
                    },
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 1,
                        "kind": "other",
                        "emoji": "🧰",
                        "body_djot": "Other demo.",
                    },
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "duplicate record key"):
                load_news_records(root)

    def test_unknown_kind_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 2,
                        "kind": "awardish",
                        "emoji": "🗣️",
                        "body_djot": "Demo.",
                    }
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "unknown kind"):
                load_news_records(root)

    def test_invalid_month_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-13-demo",
                        "year": 2026,
                        "month": 13,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Demo.",
                    }
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "invalid month"):
                load_news_records(root)

    def test_non_increasing_year_month_order_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2025-01-demo",
                        "year": 2025,
                        "month": 1,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Older.",
                    },
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 2,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Newer.",
                    },
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "non-increasing \\(year, month\\) order"):
                load_news_records(root)

    def test_sort_day_order_is_enforced_within_same_month(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-02-demo-one",
                        "year": 2026,
                        "month": 2,
                        "sort_day": 10,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Earlier in file.",
                    },
                    {
                        "key": "2026-02-demo-two",
                        "year": 2026,
                        "month": 2,
                        "sort_day": 15,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Should not sort ahead.",
                    },
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "non-increasing sort_day order"):
                load_news_records(root)

    def test_find_news_record_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            issues = find_news_record_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing news registry", issues[0])

    def test_accepts_optional_homepage_featured_boolean(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 2,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Demo.",
                        "homepage_featured": True,
                    }
                ],
            )

            records = load_news_records(root)
            self.assertTrue(records[0].homepage_featured)

    def test_invalid_homepage_featured_type_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_news(
                root / "site" / "data" / "news.json",
                [
                    {
                        "key": "2026-02-demo",
                        "year": 2026,
                        "month": 2,
                        "kind": "talk",
                        "emoji": "🗣️",
                        "body_djot": "Demo.",
                        "homepage_featured": "yes",
                    }
                ],
            )

            with self.assertRaisesRegex(NewsRecordError, "homepage_featured must be a boolean"):
                load_news_records(root)


if __name__ == "__main__":
    unittest.main()
