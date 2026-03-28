from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.publication_record_a import (
    PublicationClassificationA,
    PublicationPersonA,
    PublicationRecordA,
    PublicationRecordAError,
    PublicationTimeA,
    PublicationVenueA,
    load_publication_index_records_a,
    load_publication_record_a,
    publication_display_year,
    publication_index_title_url_a,
    publication_order_key_a,
)


def _write_publication(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")


class PublicationRecordATests(unittest.TestCase):
    def test_loads_published_thin_bundle_and_normalizes_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            record_path = root / "site" / "pubs" / "2025-demo-paper" / "publication.json"
            _write_publication(
                record_path,
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "pub_date": "2025-03-30",
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [
                        {"name": "Demo Author", "ref": "Demo Author"},
                        {"name": "Second Author"},
                    ],
                    "venue": "Architectural Support for Programming Languages and Operating Systems",
                    "venue_short": "ASPLOS",
                    "identifiers": {"doi": "10.1145/demo"},
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [
                        {
                            "event": "DemoConf 2025",
                            "speakers": [{"name": "Demo Student"}],
                            "url": "https://example.test/talk",
                            "embed": "https://example.test/embed",
                            "title": "Demo Student Talk",
                        }
                    ],
                },
            )

            record = load_publication_record_a(root, "2025-demo-paper")
            self.assertFalse(record.draft)
            self.assertFalse(record.local_page)
            self.assertEqual(record.classification.listing_group, "main")
            self.assertEqual(record.classification.pub_type, "conference")
            self.assertEqual(record.time.pub_year, 2025)
            self.assertEqual(record.time.pub_date, date(2025, 3, 30))
            self.assertEqual(record.venue.full, "Architectural Support for Programming Languages and Operating Systems")
            self.assertEqual(record.venue.short, "ASPLOS")
            self.assertEqual(record.identifiers["doi"], "10.1145/demo")
            self.assertEqual(record.authors[0].ref, "Demo Author")
            self.assertIsNone(record.authors[1].ref)
            self.assertEqual(record.talks[0].title, "Demo Student Talk")
            self.assertEqual(publication_display_year(record), "2025")
            self.assertEqual(
                publication_index_title_url_a(record),
                "https://example.test/paper",
            )

    def test_loads_published_local_page_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            record_path = root / "site" / "pubs" / "2024-demo-journal" / "publication.json"
            _write_publication(
                record_path,
                {
                    "local_page": True,
                    "listing_group": "main",
                    "pub_type": "journal",
                    "pub_year": 2024,
                    "title": "Journal Paper",
                    "authors": [{"name": "Solo Author"}],
                    "venue": "<Programming>",
                    "venue_short": "<Programming>",
                    "description": "Local page description.",
                    "links": {"publisher": "https://example.test/journal"},
                    "talks": [],
                },
            )

            record = load_publication_record_a(root, "2024-demo-journal")
            self.assertTrue(record.local_page)
            self.assertIsNone(record.primary_link)
            self.assertEqual(record.classification.pub_type, "journal")
            self.assertEqual(record.venue.short, "<Programming>")
            self.assertEqual(
                publication_index_title_url_a(record),
                "pubs/2024-demo-journal/",
            )

    def test_draft_can_omit_indexed_only_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            record_path = root / "site" / "pubs" / "2026-draft-demo" / "publication.json"
            _write_publication(
                record_path,
                {
                    "draft": True,
                    "title": "Draft Paper",
                    "authors": [{"name": "Draft Author"}],
                    "venue": "Draft Venue",
                    "links": {},
                    "talks": [],
                },
            )

            record = load_publication_record_a(root, "2026-draft-demo")
            self.assertTrue(record.draft)
            self.assertIsNone(record.time.pub_year)
            self.assertIsNone(record.classification.listing_group)
            self.assertIsNone(record.classification.pub_type)
            self.assertTrue(record.local_page)

    def test_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            path = root / "site" / "pubs" / "2025-demo-paper" / "publication.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                '{"title":"Demo","title":"Again","authors":[{"name":"Author"}],"venue":"Venue"}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(PublicationRecordAError, "duplicate JSON key"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_rejects_published_bundle_without_pub_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "missing pub_year"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_rejects_pub_year_slug_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2024,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "pub_year must match slug year 2025"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_allows_pub_year_to_differ_from_pub_date_year(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "pub_date": "2024-12-20",
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            record = load_publication_record_a(root, "2025-demo-paper")
            self.assertEqual(record.time.pub_year, 2025)
            self.assertEqual(record.time.pub_date, date(2024, 12, 20))

    def test_rejects_published_bundle_without_venue_short(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "missing venue_short"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_rejects_unknown_pub_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "survey",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "pub_type must be one of"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_rejects_primary_link_for_local_page_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": True,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "description": "Local page description.",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "primary_link is only valid"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_requires_primary_link_for_thin_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "missing primary_link"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_rejects_unknown_identifier_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            _write_publication(
                root / "site" / "pubs" / "2025-demo-paper" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Demo Paper",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "identifiers": {"pmid": "123"},
                    "links": {"publisher": "https://example.test/paper"},
                    "talks": [],
                },
            )

            with self.assertRaisesRegex(PublicationRecordAError, "unknown identifier keys"):
                load_publication_record_a(root, "2025-demo-paper")

    def test_index_loader_sorts_by_pub_year_then_exact_pub_date_then_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pubs = root / "site" / "pubs"
            _write_publication(
                pubs / "2025-late-date" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "pub_date": "2025-05-01",
                    "primary_link": "publisher",
                    "title": "Late Date",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/late"},
                    "talks": [],
                },
            )
            _write_publication(
                pubs / "2025-year-only" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2025,
                    "primary_link": "publisher",
                    "title": "Year Only",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/year-only"},
                    "talks": [],
                },
            )
            _write_publication(
                pubs / "2024-exact-date" / "publication.json",
                {
                    "local_page": False,
                    "listing_group": "main",
                    "pub_type": "conference",
                    "pub_year": 2024,
                    "pub_date": "2024-12-31",
                    "primary_link": "publisher",
                    "title": "Older Exact",
                    "authors": [{"name": "Author"}],
                    "venue": "DemoConf",
                    "venue_short": "DemoConf",
                    "links": {"publisher": "https://example.test/older"},
                    "talks": [],
                },
            )

            records = load_publication_index_records_a(root, publications_dir=pubs)
            self.assertEqual(
                tuple(record.slug for record in records),
                ("2025-late-date", "2025-year-only", "2024-exact-date"),
            )

    def test_publication_order_key_handles_year_only_records(self) -> None:
        no_date = PublicationRecordA(
            slug="2025-year-only",
            draft=False,
            local_page=False,
            primary_link="publisher",
            title="Year Only",
            authors=(PublicationPersonA(name="Author"),),
            time=PublicationTimeA(pub_year=2025),
            venue=PublicationVenueA(full="DemoConf", short="DemoConf"),
            classification=PublicationClassificationA(
                listing_group="main",
                pub_type="conference",
            ),
            links={"publisher": "https://example.test/year-only"},
        )
        with_date = PublicationRecordA(
            slug="2025-with-date",
            draft=False,
            local_page=False,
            primary_link="publisher",
            title="With Date",
            authors=(PublicationPersonA(name="Author"),),
            time=PublicationTimeA(pub_year=2025, pub_date=date(2025, 1, 1)),
            venue=PublicationVenueA(full="DemoConf", short="DemoConf"),
            classification=PublicationClassificationA(
                listing_group="main",
                pub_type="conference",
            ),
            links={"publisher": "https://example.test/with-date"},
        )

        self.assertLess(publication_order_key_a(with_date), publication_order_key_a(no_date))
