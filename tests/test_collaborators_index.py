from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.collaborators_index import (
    load_collaborator_entries,
    render_public_collaborators_list_djot,
)


def _write_publication(
    pubs_dir: Path,
    slug: str,
    *,
    title: str,
    pub_date: str,
    authors: list[dict[str, str]],
) -> None:
    pub_dir = pubs_dir / slug
    pub_dir.mkdir(parents=True)
    (pub_dir / "publication.json").write_text(
        json.dumps(
            {
                "detail_page": False,
                "listing_group": "main",
                "pub_date": pub_date,
                "primary_link": "publisher",
                "title": title,
                "authors": authors,
                "venue": "DemoConf",
                "links": {"publisher": f"https://example.test/{slug}"},
                "talks": [],
            }
        ),
        encoding="utf-8",
    )


class CollaboratorsIndexTests(unittest.TestCase):
    def test_load_collaborator_entries_prefers_shortest_label_and_excludes_self(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "james-wilcox": {
                                "name": "James Wilcox",
                                "url": "https://example.test/james",
                                "aliases": ["James R. Wilcox"],
                            },
                            "michael-ernst": {
                                "name": "Michael Ernst",
                                "url": "https://example.test/michael",
                                "aliases": ["Mike Ernst", "Michael D. Ernst"],
                            },
                            "remy-wang": {
                                "name": "Yisu Remy Wang",
                                "url": "https://example.test/remy",
                                "aliases": ["Remy Wang"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "James R. Wilcox", "ref": "James Wilcox"},
                    {"name": "Michael D. Ernst", "ref": "Mike Ernst"},
                    {"name": "Robert Rabe", "ref": ""},
                ],
            )
            _write_publication(
                pubs_dir,
                "2024-demo-two",
                title="Second Paper",
                pub_date="2024-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "James Wilcox", "ref": "James Wilcox"},
                    {"name": "Mike Ernst", "ref": "Mike Ernst"},
                    {"name": "Remy Wang", "ref": "Remy Wang"},
                ],
            )

            entries = load_collaborator_entries(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
            )

            self.assertEqual(
                [(entry.display_name, entry.is_linked) for entry in entries],
                [
                    ("James Wilcox", True),
                    ("Mike Ernst", True),
                    ("Remy Wang", True),
                    ("Robert Rabe", False),
                ],
            )

    def test_render_public_collaborators_list_links_resolved_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            data_dir = root / "site" / "data"
            pubs_dir = root / "site" / "pubs"
            data_dir.mkdir(parents=True)

            (data_dir / "people.json").write_text(
                json.dumps(
                    {
                        "people": {
                            "zachary-tatlock": {
                                "name": "Zachary Tatlock",
                                "url": "https://ztatlock.net/",
                            },
                            "adam-geller": {
                                "name": "Adam Geller",
                                "url": "https://example.test/adam",
                                "aliases": ["Adam T. Geller"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            _write_publication(
                pubs_dir,
                "2025-demo-one",
                title="First Paper",
                pub_date="2025-01-01",
                authors=[
                    {"name": "Zachary Tatlock", "ref": "Zachary Tatlock"},
                    {"name": "Adam T. Geller", "ref": "Adam Geller"},
                    {"name": "Robert Rabe", "ref": ""},
                ],
            )

            rendered = render_public_collaborators_list_djot(
                root,
                publications_dir=pubs_dir,
                people_path=data_dir / "people.json",
            )

            self.assertEqual(
                rendered,
                "* [Adam Geller][]\n"
                "* Robert Rabe\n",
            )


if __name__ == "__main__":
    unittest.main()
