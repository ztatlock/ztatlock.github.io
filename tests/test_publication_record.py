from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.publication_record import (
    PublicationRecordError,
    load_publication_record,
    publication_compact_venue_label,
    publication_display_year,
    publication_full_venue_label,
    publication_index_title_url,
    publication_listing_group,
    publication_pub_year,
)


class PublicationRecordTests(unittest.TestCase):
    def test_loads_published_thin_bundle_with_proposal_a_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Demo Workshop",
                        "venue_short": "Workshop",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = load_publication_record(root, "2025-test-demo")
            self.assertFalse(record.draft)
            self.assertFalse(record.local_page)
            self.assertEqual(publication_listing_group(record), "workshop")
            self.assertEqual(record.classification.pub_type, "workshop")
            self.assertEqual(publication_pub_year(record), 2025)
            self.assertEqual(record.time.pub_date, date(2025, 1, 1))
            self.assertEqual(publication_full_venue_label(record), "Demo Workshop")
            self.assertEqual(publication_compact_venue_label(record), "Workshop")
            self.assertEqual(publication_display_year(record), "2025")
            self.assertEqual(
                publication_index_title_url(record),
                "https://example.test/paper",
            )
            self.assertIsNone(record.authors[0].ref)

    def test_loads_local_page_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2024-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "listing_group": "main",
                        "pub_type": "journal",
                        "pub_year": 2024,
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author"}],
                        "venue": "<Programming>",
                        "venue_short": "<Programming>",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = load_publication_record(root, "2024-test-demo")
            self.assertTrue(record.local_page)
            self.assertIsNone(record.primary_link)
            self.assertEqual(publication_index_title_url(record), "pubs/2024-test-demo/")

    def test_draft_can_omit_published_only_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2026-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "draft": True,
                        "title": "Draft Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "Draft Venue",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = load_publication_record(root, "2026-test-demo")
            self.assertTrue(record.draft)
            self.assertIsNone(record.time.pub_year)
            self.assertIsNone(record.classification.pub_type)
            self.assertTrue(record.local_page)

    def test_rejects_published_bundle_without_pub_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": False,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author"}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(PublicationRecordError, "missing pub_year"):
                load_publication_record(root, "2025-test-demo")

    def test_rejects_primary_link_for_local_page_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "local_page": True,
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author"}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "description": "Demo description",
                        "links": {"publisher": "https://example.test/paper"},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(PublicationRecordError, "primary_link is only valid"):
                load_publication_record(root, "2025-test-demo")
