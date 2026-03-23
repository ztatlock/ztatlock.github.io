from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.scaffold_publication import scaffold_publication
from scripts.sitebuild.site_config import load_site_config


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

    def test_scaffold_uses_layout_config_and_skips_stub_by_default_off_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages_dir = root / "site" / "pages"
            pubs_dir = root / "site" / "pubs"
            templates_dir = root / "site" / "templates"
            data_dir = root / "site" / "data"
            static_dir = root / "site" / "static"
            pages_dir.mkdir(parents=True)
            pubs_dir.mkdir(parents=True)
            templates_dir.mkdir(parents=True)
            data_dir.mkdir(parents=True)
            static_dir.mkdir(parents=True)

            (templates_dir / "pub-stub.dj").write_text(
                "# TITLE\n\n# DRAFT\n",
                encoding="utf-8",
            )
            (templates_dir / "publication.json").write_text(
                '{\n  "draft": true,\n  "title": "TITLE",\n  "authors": [{"name": "AUTHOR", "ref": "AUTHOR"}],\n  "venue": "CONF",\n  "description": "TODO",\n  "links": {},\n  "talks": []\n}\n',
                encoding="utf-8",
            )

            config = load_site_config(
                root,
                page_source_dir=pages_dir,
                publications_dir=pubs_dir,
                templates_dir=templates_dir,
                data_dir=data_dir,
                static_source_dir=static_dir,
            )

            scaffold_publication(root, "2026-conf-paper", config=config)

            self.assertTrue((pubs_dir / "2026-conf-paper" / "publication.json").exists())
            self.assertFalse((pages_dir / "pub-2026-conf-paper.dj").exists())
