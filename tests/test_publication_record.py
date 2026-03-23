from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.publication_record import PublicationRecordError, load_publication_record


class PublicationRecordTests(unittest.TestCase):
    def test_draft_defaults_false_when_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
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

            record = load_publication_record(root, "2025-test-demo")
            self.assertFalse(record.draft)

    def test_rejects_non_boolean_draft_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pub_dir = root / "pubs" / "2025-test-demo"
            pub_dir.mkdir(parents=True)
            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "draft": "yes",
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
