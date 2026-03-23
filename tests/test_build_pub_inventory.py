from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_pub_inventory import build_record, discover_publication_slugs
from scripts.publication_record import publication_page_path


class BuildPubInventoryTests(unittest.TestCase):
    def test_discovers_publications_from_records_without_stubs(self) -> None:
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

            self.assertEqual(discover_publication_slugs(root), ["2025-test-demo"])

    def test_build_record_uses_publication_record_and_local_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            webfiles_root = root / "WEBFILES"
            webfiles_root.mkdir()

            slug = "2025-test-demo"
            pub_dir = root / "pubs" / slug
            pub_dir.mkdir(parents=True)

            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "description": "Demo description",
                        "links": {
                            "code": "https://example.test/code",
                            "project": "https://example.test/project",
                        },
                        "talks": [
                            {
                                "event": "Demo Talk",
                                "speakers": [{"name": "Demo Author", "ref": ""}],
                                "url": "https://example.test/talk",
                                "embed": "https://example.test/embed",
                                "title": "Demo Talk",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (pub_dir / f"{slug}.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / f"{slug}.bib").write_text("@inproceedings{demo}\n", encoding="utf-8")
            (pub_dir / f"{slug}-abstract.md").write_text("Demo abstract.\n", encoding="utf-8")
            (pub_dir / f"{slug}-absimg.png").write_bytes(b"PNG")
            (pub_dir / f"{slug}-meta.png").write_bytes(b"PNG")
            (pub_dir / f"{slug}-slides.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / f"{slug}-poster.pdf").write_bytes(b"%PDF-1.4\n")

            record = build_record(root, webfiles_root, slug)

            self.assertEqual(record.title, "Demo Paper")
            self.assertEqual(record.page, publication_page_path(slug))
            self.assertEqual(record.page_paper_link, f"pubs/{slug}/{slug}.pdf")
            self.assertEqual(record.page_bib_link, f"pubs/{slug}/{slug}.bib")
            self.assertEqual(record.page_slides_link, f"pubs/{slug}/{slug}-slides.pdf")
            self.assertEqual(record.page_poster_link, f"pubs/{slug}/{slug}-poster.pdf")
            self.assertEqual(record.page_talk_link, "https://example.test/talk")
            self.assertEqual(record.page_code_link, "https://example.test/code")
            self.assertEqual(record.page_project_link, "https://example.test/project")
