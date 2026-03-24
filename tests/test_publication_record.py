from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.publication_record import PublicationRecordError, load_publication_record


class PublicationRecordTests(unittest.TestCase):
    def test_draft_defaults_false_when_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = load_publication_record(root, "2025-test-demo")
            self.assertFalse(record.draft)
            self.assertEqual(record.pub_date, date(2025, 1, 1))

    def test_rejects_non_boolean_draft_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "draft": "yes",
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")

    def test_loads_published_index_only_publication_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "workshop",
                        "pub_date": "2025-01-01",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = load_publication_record(root, "2025-test-demo")
            self.assertFalse(record.draft)
            self.assertFalse(record.detail_page)
            self.assertEqual(record.listing_group, "workshop")
            self.assertEqual(record.pub_date, date(2025, 1, 1))
            self.assertEqual(record.primary_link, "publisher")
            self.assertEqual(record.description, "")

    def test_rejects_published_publication_without_pub_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")

    def test_rejects_malformed_pub_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-1-1",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")

    def test_rejects_impossible_pub_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-02-30",
                        "primary_link": "publisher",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")

    def test_rejects_index_only_publication_without_primary_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "detail_page": False,
                        "listing_group": "main",
                        "pub_date": "2025-01-01",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")

    def test_rejects_unknown_listing_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "site" / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "listing_group": "journal",
                        "pub_date": "2025-01-01",
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(PublicationRecordError):
                load_publication_record(root, "2025-test-demo")
