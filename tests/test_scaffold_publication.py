from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.scaffold_publication import scaffold_publication


class ScaffoldPublicationTests(unittest.TestCase):
    def test_scaffold_defaults_publication_record_to_draft_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            templates_dir = root / "templates"
            pubs_dir = root / "pubs"
            templates_dir.mkdir(parents=True)
            pubs_dir.mkdir(parents=True)

            (templates_dir / "pub-stub.dj").write_text(
                "# TITLE\n\n# DRAFT\n",
                encoding="utf-8",
            )
            (templates_dir / "publication.json").write_text(
                '{\n  "draft": true,\n  "title": "TITLE",\n  "authors": [{"name": "AUTHOR", "ref": "AUTHOR"}],\n  "venue": "CONF",\n  "description": "TODO",\n  "links": {},\n  "talks": []\n}\n',
                encoding="utf-8",
            )

            scaffold_publication(root, "2026-conf-paper")

            record = json.loads(
                (root / "pubs" / "2026-conf-paper" / "publication.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertTrue(record["draft"])
            self.assertTrue((root / "pub-2026-conf-paper.dj").exists())
