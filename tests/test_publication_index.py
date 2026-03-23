from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.publication_index import PublicationIndexError, load_publications_index_entries


class PublicationIndexTests(unittest.TestCase):
    def test_loads_entries_from_current_hand_authored_index_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pages.mkdir(parents=True)
            (pages / "publications.dj").write_text(
                "---\n"
                "description: Publications\n"
                "---\n\n"
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "{#2025-test-main}\n"
                "*[Main Paper](https://example.test/main)* \\\n"
                "  [Demo Author][]\n"
                "\\\n"
                "DemoConf 2025\n\n"
                ":::\n\n"
                "## Workshop Papers\n\n"
                "{.pubs}\n"
                ":::\n\n"
                "{#2025-test-workshop}\n"
                "*[Workshop Paper](\n"
                "  https://example.test/workshop\n"
                ")* \\\n"
                "  [First Author][First Author],\n"
                "\\ Second Author,\n"
                "\\ [Third Author][]\n"
                "\\\n"
                "Demo Workshop 2025 \\\n"
                "★ Best Paper\n\n"
                ":::\n\n"
                "## Aggregators\n\n"
                "- [DBLP](https://dblp.org/)\n",
                encoding="utf-8",
            )

            entries = load_publications_index_entries(root, page_source_dir=pages)

            self.assertEqual([entry.slug for entry in entries], ["2025-test-main", "2025-test-workshop"])
            self.assertEqual(entries[0].listing_group, "main")
            self.assertEqual(entries[0].title, "Main Paper")
            self.assertEqual(entries[0].title_url, "https://example.test/main")
            self.assertEqual(entries[0].venue, "DemoConf")
            self.assertEqual(entries[1].listing_group, "workshop")
            self.assertEqual(entries[1].title_url, "https://example.test/workshop")
            self.assertEqual(entries[1].badges, ("★ Best Paper",))
            self.assertEqual(
                [author.name for author in entries[1].authors],
                ["First Author", "Second Author", "Third Author"],
            )
            self.assertEqual(entries[1].authors[0].ref, "First Author")
            self.assertEqual(entries[1].authors[1].ref, "")

    def test_rejects_duplicate_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            pages = root / "site" / "pages"
            pages.mkdir(parents=True)
            (pages / "publications.dj").write_text(
                "# Publications\n\n"
                "## Conference and Journal Papers\n\n"
                "{#2025-test-main}\n"
                "*[Main Paper](https://example.test/main)* \\\n"
                "  Demo Author\n"
                "\\\n"
                "DemoConf 2025\n\n"
                "{#2025-test-main}\n"
                "*[Duplicate](https://example.test/dup)* \\\n"
                "  Demo Author\n"
                "\\\n"
                "DemoConf 2025\n\n"
                "## Workshop Papers\n\n"
                "## Aggregators\n",
                encoding="utf-8",
            )

            with self.assertRaises(PublicationIndexError):
                load_publications_index_entries(root, page_source_dir=pages)
