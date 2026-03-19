#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


LINK_RE = re.compile(r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)")
TITLE_RE = re.compile(r"^#\s*(.*)$")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")
SLIDE_SRC_EXTS = (".pptx", ".key")

CURATION_FIELDS = (
    "site_paper_pdf",
    "site_bib",
    "site_abstract_md",
    "site_absimg",
    "site_metaimg",
    "site_slides_pdf",
    "site_poster_pdf",
    "page_talk_link",
    "archive_slides_source",
    "archive_talk_backup",
)
CURATION_ALLOWED_VALUES = ("present", "not-made", "lost", "unknown")
REQUIRED_FIELDS = (
    "site_paper_pdf",
    "site_bib",
    "site_abstract_md",
    "site_absimg",
    "site_metaimg",
)
CURATION_FILE = "manifests/publication-artifact-curation.tsv"
PRESENT_OVERRIDE_FIELDS = (
    "archive_slides_source",
    "archive_talk_backup",
)


@dataclass
class PubRecord:
    slug: str
    title: str
    page: str
    repo_dir: str
    site_paper_pdf_path: str
    site_paper_pdf_status: str
    site_bib_path: str
    site_bib_status: str
    site_abstract_md_path: str
    site_abstract_md_status: str
    site_absimg_path: str
    site_absimg_status: str
    site_metaimg_path: str
    site_metaimg_status: str
    site_slides_pdf_path: str
    site_slides_pdf_status: str
    site_repo_slides_source_path: str
    site_repo_slides_source_status: str
    site_poster_pdf_path: str
    site_poster_pdf_status: str
    page_paper_link: str
    page_paper_link_kind: str
    page_slides_link: str
    page_slides_link_kind: str
    page_poster_link: str
    page_poster_link_kind: str
    page_teaser_link: str
    page_teaser_link_kind: str
    page_talk_link: str
    page_talk_link_kind: str
    page_bib_link: str
    page_bib_link_kind: str
    page_code_link: str
    page_project_link: str
    page_publisher_link: str
    page_arxiv_link: str
    archive_slides_source_candidates: str
    archive_slides_source_status: str
    archive_talk_backup_candidates: str
    archive_talk_backup_status: str
    required_repo_artifacts_status: str
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--webfiles-root",
        default="/Users/ztatlock/Desktop/WEBFILES",
    )
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--curation-file", default=None)
    return parser.parse_args()


def read_title(page: Path) -> str:
    with page.open(encoding="utf-8") as fh:
        for line in fh:
            match = TITLE_RE.match(line.strip())
            if match:
                return match.group(1).strip()
    return page.stem


def read_links(page: Path) -> dict[str, str]:
    links: dict[str, str] = {}
    with page.open(encoding="utf-8") as fh:
        for raw in fh:
            stripped = raw.strip()
            if stripped.startswith("{%"):
                continue
            match = LINK_RE.match(raw)
            if not match:
                continue
            label = match.group(1).strip().lower()
            target = match.group(2).strip()
            links[label] = target
    return links


def first_existing(paths: Iterable[Path]) -> str:
    for path in paths:
        if path.exists():
            return path.name
    return ""


def status_for_path(path_name: str) -> str:
    return "present" if path_name else "missing"


def kind_for_link(target: str) -> str:
    if not target:
        return "missing"
    if target.startswith(("http://", "https://")):
        return "public-external"
    return "local"


def gather_webfiles_candidates(webfiles_root: Path, slug: str) -> tuple[list[Path], list[Path]]:
    year, *rest = slug.split("-")
    system = rest[-1]
    tail = "-".join(rest)

    slide_dir = webfiles_root / "archive" / "pub-slides"
    talk_dirs = [
        webfiles_root / "archive" / "pub-talks",
        webfiles_root / "archive" / "talks",
    ]

    def score(path: Path) -> int:
        name = path.name.lower()
        if slug in name:
            return 100
        if year in name and tail in name:
            return 90
        if year in name and system in name:
            return 70
        return 0

    slide_candidates: list[Path] = []
    if slide_dir.exists():
        for path in slide_dir.iterdir():
            if path.is_file() and score(path) > 0:
                slide_candidates.append(path)

    talk_candidates: list[Path] = []
    for talk_dir in talk_dirs:
        if not talk_dir.exists():
            continue
        for path in talk_dir.iterdir():
            if path.is_file() and score(path) > 0:
                talk_candidates.append(path)

    slide_candidates.sort()
    talk_candidates.sort()
    return slide_candidates, talk_candidates


def build_record(repo_root: Path, webfiles_root: Path, page: Path) -> PubRecord:
    slug = page.stem.removeprefix("pub-")
    title = read_title(page)
    links = read_links(page)
    pub_dir = repo_root / "pubs" / slug

    site_paper_pdf_path = first_existing([pub_dir / f"{slug}.pdf"])
    site_bib_path = first_existing([pub_dir / f"{slug}.bib"])
    site_abstract_md_path = first_existing(
        [pub_dir / f"{slug}-abstract.md", pub_dir / "abstract.md"]
    )
    site_absimg_path = first_existing(pub_dir / f"{slug}-absimg{ext}" for ext in IMAGE_EXTS)
    site_metaimg_path = first_existing(pub_dir / f"{slug}-meta{ext}" for ext in IMAGE_EXTS)
    site_slides_pdf_path = first_existing([pub_dir / f"{slug}-slides.pdf"])
    site_repo_slides_source_path = first_existing(
        pub_dir / f"{slug}-slides{ext}" for ext in SLIDE_SRC_EXTS
    )
    site_poster_pdf_path = first_existing([pub_dir / f"{slug}-poster.pdf"])

    archive_slide_candidates, archive_talk_candidates = gather_webfiles_candidates(
        webfiles_root, slug
    )

    required_missing = [
        label
        for label, path_name in [
            ("paper_pdf", site_paper_pdf_path),
            ("bib", site_bib_path),
            ("abstract_md", site_abstract_md_path),
            ("absimg", site_absimg_path),
            ("metaimg", site_metaimg_path),
        ]
        if not path_name
    ]

    notes: list[str] = []
    if required_missing:
        notes.append("missing required repo artifacts: " + ", ".join(required_missing))
    if not site_slides_pdf_path:
        notes.append("missing repo slides pdf")
    if not site_poster_pdf_path:
        notes.append("missing repo poster pdf")
    if links.get("talk") and not archive_talk_candidates:
        notes.append("public talk link has no WEBFILES backup")
    if archive_talk_candidates and not links.get("talk"):
        notes.append("WEBFILES talk backup exists but page has no talk link")
    if links.get("slides", "").startswith("http"):
        notes.append("slides link is external")
    if site_repo_slides_source_path and not site_slides_pdf_path:
        notes.append("repo slide source exists but repo slides pdf is missing")
    if archive_slide_candidates and not site_slides_pdf_path:
        notes.append("WEBFILES slide source exists but repo slides pdf is missing")

    return PubRecord(
        slug=slug,
        title=title,
        page=page.name,
        repo_dir=str(pub_dir.relative_to(repo_root)),
        site_paper_pdf_path=site_paper_pdf_path,
        site_paper_pdf_status=status_for_path(site_paper_pdf_path),
        site_bib_path=site_bib_path,
        site_bib_status=status_for_path(site_bib_path),
        site_abstract_md_path=site_abstract_md_path,
        site_abstract_md_status=status_for_path(site_abstract_md_path),
        site_absimg_path=site_absimg_path,
        site_absimg_status=status_for_path(site_absimg_path),
        site_metaimg_path=site_metaimg_path,
        site_metaimg_status=status_for_path(site_metaimg_path),
        site_slides_pdf_path=site_slides_pdf_path,
        site_slides_pdf_status=status_for_path(site_slides_pdf_path),
        site_repo_slides_source_path=site_repo_slides_source_path,
        site_repo_slides_source_status=status_for_path(site_repo_slides_source_path),
        site_poster_pdf_path=site_poster_pdf_path,
        site_poster_pdf_status=status_for_path(site_poster_pdf_path),
        page_paper_link=links.get("paper", ""),
        page_paper_link_kind=kind_for_link(links.get("paper", "")),
        page_slides_link=links.get("slides", ""),
        page_slides_link_kind=kind_for_link(links.get("slides", "")),
        page_poster_link=links.get("poster", ""),
        page_poster_link_kind=kind_for_link(links.get("poster", "")),
        page_teaser_link=links.get("teaser", ""),
        page_teaser_link_kind=kind_for_link(links.get("teaser", "")),
        page_talk_link=links.get("talk", ""),
        page_talk_link_kind=kind_for_link(links.get("talk", "")),
        page_bib_link=links.get("bib", ""),
        page_bib_link_kind=kind_for_link(links.get("bib", "")),
        page_code_link=links.get("code", ""),
        page_project_link=links.get("project", ""),
        page_publisher_link=links.get("publisher", ""),
        page_arxiv_link=links.get("arxiv", ""),
        archive_slides_source_candidates="; ".join(
            str(path.relative_to(webfiles_root)) for path in archive_slide_candidates
        ),
        archive_slides_source_status="present" if archive_slide_candidates else "missing",
        archive_talk_backup_candidates="; ".join(
            str(path.relative_to(webfiles_root)) for path in archive_talk_candidates
        ),
        archive_talk_backup_status="present" if archive_talk_candidates else "missing",
        required_repo_artifacts_status="present" if not required_missing else "missing",
        notes="; ".join(notes),
    )


def curation_headers() -> list[str]:
    return [
        "slug",
        *[f"{field}_curated_status" for field in CURATION_FIELDS],
        "curation_notes",
    ]


def load_curation(curation_path: Path, known_slugs: set[str]) -> dict[str, dict[str, str]]:
    if not curation_path.exists():
        return {}

    with curation_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        headers = reader.fieldnames or []
        expected_headers = curation_headers()
        if headers != expected_headers:
            raise SystemExit(
                "ERROR: invalid publication artifact curation headers in "
                f"{curation_path}; expected {expected_headers}"
            )

        rows: dict[str, dict[str, str]] = {}
        for raw_row in reader:
            row = {key: (value or "").strip() for key, value in raw_row.items()}
            slug = row["slug"]
            if not slug:
                continue
            if slug not in known_slugs:
                raise SystemExit(
                    f"ERROR: unknown publication slug `{slug}` in {curation_path}"
                )
            if slug in rows:
                raise SystemExit(
                    f"ERROR: duplicate publication slug `{slug}` in {curation_path}"
                )
            for field in CURATION_FIELDS:
                key = f"{field}_curated_status"
                if row[key] and row[key] not in CURATION_ALLOWED_VALUES:
                    raise SystemExit(
                        f"ERROR: invalid curated status `{row[key]}` for `{slug}` "
                        f"field `{key}` in {curation_path}"
                    )
            rows[slug] = row
        return rows


def validate_curation(
    curation: dict[str, dict[str, str]],
    records: list[PubRecord],
    curation_path: Path,
) -> None:
    by_slug = {record.slug: record for record in records}
    for slug, row in curation.items():
        record = by_slug[slug]
        for field in CURATION_FIELDS:
            status = row.get(f"{field}_curated_status", "")
            if not status:
                continue

            observed = observed_status(record, field)
            if observed == "present":
                raise SystemExit(
                    f"ERROR: curated status `{status}` for `{slug}` field `{field}` "
                    f"in {curation_path} is redundant or contradictory because the "
                    "artifact is already observed as present"
                )

            if status == "present" and field not in PRESENT_OVERRIDE_FIELDS:
                raise SystemExit(
                    f"ERROR: curated `present` for `{slug}` field `{field}` in "
                    f"{curation_path} is not allowed; use `present` only for "
                    "archive-presence heuristic misses"
                )


def observed_status(record: PubRecord, field: str) -> str:
    if field == "page_talk_link":
        return "present" if record.page_talk_link else "missing"
    return getattr(record, f"{field}_status")


def curated_status(curation: dict[str, dict[str, str]], record: PubRecord, field: str) -> str:
    return curation.get(record.slug, {}).get(f"{field}_curated_status", "")


def effective_status(curation: dict[str, dict[str, str]], record: PubRecord, field: str) -> str:
    observed = observed_status(record, field)
    if observed == "present":
        return "present"
    return curated_status(curation, record, field) or "missing"


def curation_note(curation: dict[str, dict[str, str]], record: PubRecord) -> str:
    return curation.get(record.slug, {}).get("curation_notes", "")


def required_missing_fields(curation: dict[str, dict[str, str]], record: PubRecord) -> list[str]:
    return [field for field in REQUIRED_FIELDS if effective_status(curation, record, field) == "missing"]


def curation_entries(curation: dict[str, dict[str, str]], record: PubRecord) -> list[str]:
    entries = []
    for field in CURATION_FIELDS:
        status = curated_status(curation, record, field)
        if status:
            entries.append(f"{field}={status}")
    return entries


def curation_status_counts(curation: dict[str, dict[str, str]], records: list[PubRecord]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        for field in CURATION_FIELDS:
            status = curated_status(curation, record, field)
            if status:
                counts[status] += 1
    return counts


def tsv_fieldnames() -> list[str]:
    return [
        *PubRecord.__dataclass_fields__.keys(),
        "page_talk_link_status",
        *[
            name
            for field in CURATION_FIELDS
            for name in (f"{field}_curated_status", f"{field}_effective_status")
        ],
        "curation_notes",
    ]


def record_to_row(curation: dict[str, dict[str, str]], record: PubRecord) -> dict[str, str]:
    row = record.__dict__.copy()
    row["page_talk_link_status"] = observed_status(record, "page_talk_link")
    for field in CURATION_FIELDS:
        row[f"{field}_curated_status"] = curated_status(curation, record, field)
        row[f"{field}_effective_status"] = effective_status(curation, record, field)
    row["curation_notes"] = curation_note(curation, record)
    return row


def write_tsv(
    out_path: Path,
    records: list[PubRecord],
    curation: dict[str, dict[str, str]],
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=tsv_fieldnames(),
            delimiter="\t",
        )
        writer.writeheader()
        for record in records:
            writer.writerow(record_to_row(curation, record))


def render_list(records: list[PubRecord], pred, formatter) -> list[str]:
    rows = [formatter(record) for record in records if pred(record)]
    return rows or ["- none"]


def write_summary(
    out_path: Path,
    records: list[PubRecord],
    curation: dict[str, dict[str, str]],
    curation_path: Path,
) -> None:
    required_missing = [r for r in records if required_missing_fields(curation, r)]
    missing_slides_pdf = [
        r for r in records if effective_status(curation, r, "site_slides_pdf") == "missing"
    ]
    missing_poster_pdf = [
        r for r in records if effective_status(curation, r, "site_poster_pdf") == "missing"
    ]
    external_slides_link = [r for r in records if r.page_slides_link_kind == "public-external"]
    no_public_talk_link = [r for r in records if observed_status(r, "page_talk_link") == "missing"]
    talk_link_without_backup = [
        r
        for r in records
        if r.page_talk_link_kind == "public-external"
        and effective_status(curation, r, "archive_talk_backup") == "missing"
    ]
    backup_without_talk_link = [
        r
        for r in records
        if effective_status(curation, r, "page_talk_link") == "missing"
        and r.archive_talk_backup_status == "present"
    ]
    slide_source_without_pdf = [
        r
        for r in records
        if effective_status(curation, r, "site_slides_pdf") == "missing"
        and (
            r.site_repo_slides_source_status == "present"
            or r.archive_slides_source_status == "present"
        )
    ]
    curated_rows = [
        r
        for r in records
        if curation_entries(curation, r) or curation_note(curation, r)
    ]
    curated_counts = curation_status_counts(curation, records)

    lines = [
        "# Publication Artifact Inventory",
        "",
        "This inventory merges filesystem observation with manual curation.",
        "Observed statuses here mean only `present` or `missing`.",
        "Effective statuses may also be `not-made`, `lost`, or `unknown`",
        "when manual curation has been added.",
        f"Manual curation file: `{curation_path}`",
        "A page without a public talk link is informational by itself, not an error.",
        "",
        f"- Total publications: {len(records)}",
        f"- Required repo artifacts still missing: {len(required_missing)}",
        f"- Expected repo slide PDFs still missing: {len(missing_slides_pdf)}",
        f"- Expected repo poster PDFs still missing: {len(missing_poster_pdf)}",
        f"- Pages with external slides links: {len(external_slides_link)}",
        f"- Pages without public talk links: {len(no_public_talk_link)}",
        f"- Public talk links without WEBFILES backup: {len(talk_link_without_backup)}",
        f"- WEBFILES talk backups without page talk links: {len(backup_without_talk_link)}",
        f"- Manual curation judgments: {sum(curated_counts.values())}",
        f"- Missing artifacts marked `present`: {curated_counts['present']}",
        f"- Missing artifacts marked `not-made`: {curated_counts['not-made']}",
        f"- Missing artifacts marked `lost`: {curated_counts['lost']}",
        f"- Missing artifacts marked `unknown`: {curated_counts['unknown']}",
        "",
        "## Required Repo Artifacts Still Missing",
        "",
        *render_list(
            records,
            lambda r: bool(required_missing_fields(curation, r)),
            lambda r: (
                f"- `{r.slug}`: "
                + ", ".join(f"`{field}=missing`" for field in required_missing_fields(curation, r))
                + (f"; observed=`{r.notes}`" if r.notes else "")
            ),
        ),
        "",
        "## Manual Curation Entries",
        "",
        *render_list(
            records,
            lambda r: bool(curation_entries(curation, r) or curation_note(curation, r)),
            lambda r: (
                f"- `{r.slug}`: "
                + (
                    ", ".join(f"`{entry}`" for entry in curation_entries(curation, r))
                    if curation_entries(curation, r)
                    else "notes only"
                )
                + (
                    f"; notes=`{curation_note(curation, r)}`"
                    if curation_note(curation, r)
                    else ""
                )
            ),
        ),
        "",
        "## Expected Repo Slide PDFs Still Missing",
        "",
        *render_list(
            records,
            lambda r: effective_status(curation, r, "site_slides_pdf") == "missing",
            lambda r: f"- `{r.slug}`: page slides link=`{r.page_slides_link or '-'}`",
        ),
        "",
        "## Expected Repo Poster PDFs Still Missing",
        "",
        *render_list(
            records,
            lambda r: effective_status(curation, r, "site_poster_pdf") == "missing",
            lambda r: f"- `{r.slug}`: page poster link=`{r.page_poster_link or '-'}`",
        ),
        "",
        "## External Slides Links",
        "",
        *render_list(
            records,
            lambda r: r.page_slides_link_kind == "public-external",
            lambda r: f"- `{r.slug}`: `{r.page_slides_link}`",
        ),
        "",
        "## Pages Without Public Talk Links",
        "",
        *render_list(
            records,
            lambda r: observed_status(r, "page_talk_link") == "missing",
            lambda r: (
                f"- `{r.slug}`"
                + (
                    f": WEBFILES backup=`{r.archive_talk_backup_candidates}`"
                    if r.archive_talk_backup_status == "present"
                    else ""
                )
            ),
        ),
        "",
        "## Public Talk Links Without WEBFILES Backup",
        "",
        *render_list(
            records,
            lambda r: (
                r.page_talk_link_kind == "public-external"
                and effective_status(curation, r, "archive_talk_backup") == "missing"
            ),
            lambda r: f"- `{r.slug}`: `{r.page_talk_link}`",
        ),
        "",
        "## WEBFILES Talk Backups Without Page Talk Links",
        "",
        *render_list(
            records,
            lambda r: (
                effective_status(curation, r, "page_talk_link") == "missing"
                and r.archive_talk_backup_status == "present"
            ),
            lambda r: f"- `{r.slug}`: `{r.archive_talk_backup_candidates}`",
        ),
        "",
        "## Slide Source Backups Without Repo Slide PDFs",
        "",
        *render_list(
            records,
            lambda r: (
                effective_status(curation, r, "site_slides_pdf") == "missing"
                and (
                    r.site_repo_slides_source_status == "present"
                    or r.archive_slides_source_status == "present"
                )
            ),
            lambda r: (
                f"- `{r.slug}`:"
                f" repo_source=`{r.site_repo_slides_source_path or '-'}`,"
                f" webfiles_source=`{r.archive_slides_source_candidates or '-'}`"
            ),
        ),
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    webfiles_root = Path(args.webfiles_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    curation_path = (
        Path(args.curation_file).resolve()
        if args.curation_file
        else (repo_root / CURATION_FILE)
    )

    pages = sorted(repo_root.glob("pub-*.dj"))
    records = [build_record(repo_root, webfiles_root, page) for page in pages]
    curation = load_curation(curation_path, {record.slug for record in records})
    validate_curation(curation, records, curation_path)

    write_tsv(out_dir / "publication-artifact-inventory.tsv", records, curation)
    write_summary(out_dir / "publication-artifact-inventory.md", records, curation, curation_path)


if __name__ == "__main__":
    main()
