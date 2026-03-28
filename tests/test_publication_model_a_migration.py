from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


MANIFEST_PATH = Path("manifests") / "publication-model-a-migration.tsv"
PUBLICATIONS_DIR = Path("site") / "pubs"
ALLOWED_PUB_TYPES = {"conference", "journal", "workshop"}


def _load_manifest_rows() -> list[dict[str, str]]:
    with MANIFEST_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _load_current_publications() -> dict[str, dict[str, object]]:
    publications: dict[str, dict[str, object]] = {}
    for path in sorted(PUBLICATIONS_DIR.glob("*/publication.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("draft"):
            continue
        publications[path.parent.name] = data
    return publications


class PublicationModelAMigrationManifestTests(unittest.TestCase):
    def test_manifest_covers_every_indexed_publication_once(self) -> None:
        rows = _load_manifest_rows()
        current = _load_current_publications()

        manifest_slugs = [row["slug"] for row in rows]
        self.assertEqual(len(manifest_slugs), len(set(manifest_slugs)))
        self.assertEqual(set(manifest_slugs), set(current))
        self.assertEqual(len(rows), 69)

    def test_manifest_current_columns_match_current_corpus(self) -> None:
        rows = _load_manifest_rows()
        current = _load_current_publications()

        for row in rows:
            slug = row["slug"]
            data = current[slug]
            self.assertEqual(row["title"], data["title"])
            self.assertEqual(row["current_listing_group"], data["listing_group"])
            self.assertEqual(
                row["current_detail_page"],
                str(data.get("detail_page", True)).lower(),
            )
            self.assertEqual(row["current_primary_link"], data.get("primary_link", ""))
            self.assertEqual(row["current_pub_date"], data.get("pub_date", ""))
            self.assertEqual(row["current_venue"], data["venue"])

    def test_manifest_proposed_columns_are_valid(self) -> None:
        rows = _load_manifest_rows()

        pub_type_counts = {key: 0 for key in ALLOWED_PUB_TYPES}
        for row in rows:
            slug_year = int(row["slug"].split("-", 1)[0])
            self.assertEqual(int(row["proposed_pub_year"]), slug_year)
            self.assertIn(row["proposed_local_page"], {"true", "false"})
            self.assertTrue(row["proposed_venue"])
            self.assertTrue(row["proposed_venue_short"])
            self.assertIn(row["proposed_pub_type"], ALLOWED_PUB_TYPES)
            pub_type_counts[row["proposed_pub_type"]] += 1

        self.assertEqual(pub_type_counts["conference"], 49)
        self.assertEqual(pub_type_counts["journal"], 7)
        self.assertEqual(pub_type_counts["workshop"], 13)

    def test_manifest_preserves_named_special_cases(self) -> None:
        rows = {row["slug"]: row for row in _load_manifest_rows()}

        self.assertEqual(
            rows["2016-netpl-bagpipe"]["notes"],
            "listing_group-main-but-semantic-workshop",
        )
        self.assertEqual(rows["2016-netpl-bagpipe"]["current_listing_group"], "main")
        self.assertEqual(rows["2016-netpl-bagpipe"]["proposed_pub_type"], "workshop")

        self.assertEqual(
            rows["2018-mapl-relay"]["notes"],
            "listing_group-main-but-semantic-workshop",
        )
        self.assertEqual(rows["2018-mapl-relay"]["current_listing_group"], "main")
        self.assertEqual(rows["2018-mapl-relay"]["proposed_pub_type"], "workshop")

        self.assertEqual(rows["2016-nsv-fpbench"]["notes"], "pub_date-year-2017")
        self.assertEqual(rows["2017-icalepcs-neutrons"]["notes"], "pub_date-year-2018")
        self.assertEqual(rows["2018-popl-disel"]["notes"], "pub_date-year-2017")

        self.assertEqual(
            rows["2024-programming-magicmarkup"]["notes"],
            "venue_short-equals-venue",
        )
        self.assertEqual(
            rows["2024-programming-magicmarkup"]["proposed_venue"],
            rows["2024-programming-magicmarkup"]["proposed_venue_short"],
        )

        self.assertEqual(
            rows["2019-siga-carpentry"]["notes"],
            "mixed-event-journal-container-seam",
        )
