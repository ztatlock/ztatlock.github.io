from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_pub_inventory import build_record, discover_publication_slugs, write_summary
from scripts.publication_record import publication_page_path


class BuildPubInventoryTests(unittest.TestCase):
    def test_discovers_publications_from_records_without_stubs(self) -> None:
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

            self.assertEqual(discover_publication_slugs(root), ["2025-test-demo"])

    def test_build_record_uses_publication_record_and_local_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            webfiles_root = root / "WEBFILES"
            webfiles_root.mkdir()

            slug = "2025-test-demo"
            pub_dir = root / "site" / "pubs" / slug
            pub_dir.mkdir(parents=True)

            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
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

    def test_build_record_supports_non_root_publications_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            webfiles_root = root / "WEBFILES"
            webfiles_root.mkdir()

            slug = "2025-test-demo"
            pubs_dir = root / "site" / "pubs"
            pub_dir = pubs_dir / slug
            pub_dir.mkdir(parents=True)

            (pub_dir / "publication.json").write_text(
                json.dumps(
                    {
                        "title": "Demo Paper",
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )
            (pub_dir / f"{slug}.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / f"{slug}.bib").write_text("@inproceedings{demo}\n", encoding="utf-8")
            (pub_dir / f"{slug}-abstract.md").write_text("Demo abstract.\n", encoding="utf-8")
            (pub_dir / f"{slug}-absimg.png").write_bytes(b"PNG")
            (pub_dir / f"{slug}-meta.png").write_bytes(b"PNG")

            self.assertEqual(
                discover_publication_slugs(root, publications_dir=pubs_dir),
                [slug],
            )

            record = build_record(
                root,
                webfiles_root,
                slug,
                publications_dir=pubs_dir,
            )

            self.assertEqual(record.page, publication_page_path(slug))
            self.assertEqual(record.repo_dir, f"site/pubs/{slug}")

    def test_build_record_supports_index_only_publication_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            webfiles_root = root / "WEBFILES"
            webfiles_root.mkdir()

            slug = "2025-test-demo"
            pub_dir = root / "site" / "pubs" / slug
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
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {
                            "publisher": "https://example.test/paper",
                            "project": "https://example.test/project",
                        },
                        "talks": [],
                    }
                ),
                encoding="utf-8",
            )

            record = build_record(root, webfiles_root, slug)

            self.assertEqual(record.page, "")
            self.assertEqual(record.local_detail_page_status, "missing")
            self.assertEqual(record.page_publisher_link, "https://example.test/paper")
            self.assertEqual(record.page_project_link, "https://example.test/project")
            self.assertEqual(record.page_paper_link, "")
            self.assertEqual(record.required_repo_artifacts_status, "present")
            self.assertIn("no local detail page", record.notes)

    def test_summary_expected_slide_and_poster_lists_match_local_detail_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            out_path = root / "publication-artifact-inventory.md"

            detail_record = build_record(
                root,
                root / "WEBFILES",
                "2025-detail-paper",
                publications_dir=self._write_publication_fixture(
                    root,
                    "2025-detail-paper",
                    {
                        "title": "Detail Paper",
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    },
                    local_page=True,
                ),
            )
            index_only_record = build_record(
                root,
                root / "WEBFILES",
                "2025-index-only-paper",
                publications_dir=self._write_publication_fixture(
                    root,
                    "2025-index-only-paper",
                    {
                        "title": "Index Only Paper",
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {},
                        "talks": [],
                    },
                    local_page=False,
                ),
            )

            write_summary(out_path, [detail_record, index_only_record], {}, root / "curation.tsv")
            summary = out_path.read_text(encoding="utf-8")

            self.assertIn("- Expected repo slide PDFs still missing: 1", summary)
            self.assertIn("- Expected repo poster PDFs still missing: 1", summary)
            self.assertIn("## Expected Repo Slide PDFs Still Missing", summary)
            self.assertIn("## Expected Repo Poster PDFs Still Missing", summary)
            self.assertIn("`2025-detail-paper`", summary)
            self.assertNotIn("`2025-index-only-paper`: page slides link=`-`", summary)
            self.assertNotIn("`2025-index-only-paper`: page poster link=`-`", summary)

    def test_summary_pages_without_public_talk_links_matches_local_detail_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            out_path = root / "publication-artifact-inventory.md"

            detail_record = build_record(
                root,
                root / "WEBFILES",
                "2025-detail-paper",
                publications_dir=self._write_publication_fixture(
                    root,
                    "2025-detail-paper",
                    {
                        "title": "Detail Paper",
                        "listing_group": "main",
                        "pub_type": "conference",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "description": "Demo description",
                        "links": {},
                        "talks": [],
                    },
                    local_page=True,
                ),
            )
            index_only_record = build_record(
                root,
                root / "WEBFILES",
                "2025-index-only-paper",
                publications_dir=self._write_publication_fixture(
                    root,
                    "2025-index-only-paper",
                    {
                        "title": "Index Only Paper",
                        "listing_group": "workshop",
                        "pub_type": "workshop",
                        "pub_year": 2025,
                        "pub_date": "2025-01-01",
                        "authors": [{"name": "Demo Author", "ref": ""}],
                        "venue": "DemoConf",
                        "venue_short": "DemoConf",
                        "links": {},
                        "talks": [],
                    },
                    local_page=False,
                ),
            )

            write_summary(out_path, [detail_record, index_only_record], {}, root / "curation.tsv")
            summary = out_path.read_text(encoding="utf-8")

            self.assertIn("- Pages without public talk links: 1", summary)
            self.assertIn("## Pages Without Public Talk Links", summary)
            self.assertIn("`2025-detail-paper`", summary)
            self.assertNotIn("`2025-index-only-paper`", summary)

    def _write_publication_fixture(
        self,
        root: Path,
        slug: str,
        record: dict[str, object],
        *,
        local_page: bool,
    ) -> Path:
        pubs_dir = root / "site" / "pubs"
        pub_dir = pubs_dir / slug
        pub_dir.mkdir(parents=True, exist_ok=True)
        payload = dict(record)
        if not local_page:
            payload["local_page"] = False
            payload["primary_link"] = "publisher"
            payload["links"] = {"publisher": "https://example.test/paper"}
        (pub_dir / "publication.json").write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        if local_page:
            (pub_dir / f"{slug}.pdf").write_bytes(b"%PDF-1.4\n")
            (pub_dir / f"{slug}.bib").write_text("@inproceedings{demo}\n", encoding="utf-8")
            (pub_dir / f"{slug}-abstract.md").write_text("Demo abstract.\n", encoding="utf-8")
            (pub_dir / f"{slug}-absimg.png").write_bytes(b"PNG")
            (pub_dir / f"{slug}-meta.png").write_bytes(b"PNG")
        return pubs_dir
