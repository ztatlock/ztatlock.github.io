from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.funding_record import (
    FundingRecordError,
    find_funding_record_issues,
    load_funding_records,
)


ROOT = Path(__file__).resolve().parent.parent


def _write_funding(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class FundingRecordTests(unittest.TestCase):
    def test_seed_funding_registry_loads(self) -> None:
        records = load_funding_records(ROOT)
        by_key = {record.key: record for record in records}

        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].key, "2021-comport-software-porting")
        self.assertEqual(by_key["2020-fmitf-retargetable-cam"].award_id, "CCF-2017927")
        self.assertEqual(by_key["2019-rtml-neural-networks"].amount_usd, 2803490)
        self.assertEqual(by_key["2018-career-distributed-systems"].role, "PI")
        self.assertEqual(by_key["2018-ada-jump-center"].sponsor, "Joint SRC & DARPA")

    def test_duplicate_record_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_funding(
                root / "site" / "data" / "funding.json",
                [
                    {
                        "key": "2018-demo-grant",
                        "title": "Demo Grant",
                        "role": "PI",
                        "sponsor": "NSF",
                        "amount_usd": 100000,
                        "start_year": 2018,
                        "end_year": 2020,
                    },
                    {
                        "key": "2018-demo-grant",
                        "title": "Other Grant",
                        "role": "Co-PI",
                        "sponsor": "DARPA",
                        "amount_usd": 200000,
                        "start_year": 2019,
                        "end_year": 2021,
                    },
                ],
            )

            with self.assertRaisesRegex(FundingRecordError, "duplicate record key"):
                load_funding_records(root)

    def test_amount_usd_must_be_positive_integer(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_funding(
                root / "site" / "data" / "funding.json",
                [
                    {
                        "key": "2018-demo-grant",
                        "title": "Demo Grant",
                        "role": "PI",
                        "sponsor": "NSF",
                        "amount_usd": 0,
                        "start_year": 2018,
                        "end_year": 2020,
                    }
                ],
            )

            with self.assertRaisesRegex(FundingRecordError, "amount_usd must be positive"):
                load_funding_records(root)

    def test_start_year_must_not_exceed_end_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_funding(
                root / "site" / "data" / "funding.json",
                [
                    {
                        "key": "2018-demo-grant",
                        "title": "Demo Grant",
                        "role": "PI",
                        "sponsor": "NSF",
                        "amount_usd": 100000,
                        "start_year": 2021,
                        "end_year": 2020,
                    }
                ],
            )

            with self.assertRaisesRegex(FundingRecordError, "must not exceed end_year"):
                load_funding_records(root)

    def test_unknown_fields_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_funding(
                root / "site" / "data" / "funding.json",
                [
                    {
                        "key": "2018-demo-grant",
                        "title": "Demo Grant",
                        "role": "PI",
                        "sponsor": "NSF",
                        "amount_usd": 100000,
                        "start_year": 2018,
                        "end_year": 2020,
                        "related_publications": [],
                    }
                ],
            )

            with self.assertRaisesRegex(FundingRecordError, "unknown fields"):
                load_funding_records(root)

    def test_find_funding_record_issues_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            issues = find_funding_record_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertIn("missing funding registry", issues[0])


if __name__ == "__main__":
    unittest.main()
