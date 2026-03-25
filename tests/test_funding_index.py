from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.funding_index import render_public_funding_list_djot


ROOT = Path(__file__).resolve().parent.parent


def _write_funding(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"records": records}), encoding="utf-8")


class FundingIndexTests(unittest.TestCase):
    def test_seed_public_funding_render_includes_expected_fields(self) -> None:
        rendered = render_public_funding_list_djot(ROOT)
        self.assertIn(
            "- ComPort: Rigorous Testing Methods to Safeguard Software Porting \\",
            rendered,
        )
        self.assertIn("Co-PI; NSF CCF-2017927; $749,913; 2020 - 2023", rendered)

    def test_render_public_funding_list_from_temp_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _write_funding(
                root / "site" / "data" / "funding.json",
                [
                    {
                        "key": "2020-demo-grant",
                        "title": "Demo Grant",
                        "role": "PI",
                        "sponsor": "NSF",
                        "award_id": "CCF-1234567",
                        "amount_usd": 100000,
                        "start_year": 2020,
                        "end_year": 2023,
                    }
                ],
            )

            rendered = render_public_funding_list_djot(root)
            self.assertEqual(
                rendered,
                "- Demo Grant \\\n"
                "  PI; NSF CCF-1234567; $100,000; 2020 - 2023\n",
            )


if __name__ == "__main__":
    unittest.main()
