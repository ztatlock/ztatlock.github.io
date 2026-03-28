#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from scripts.collaborators_index import collaborators_index_path
from scripts.cv_index import cv_index_path
from scripts.funding_record import funding_index_path
from scripts.news_index import news_index_path
from scripts.publication_index import publications_index_path
from scripts.publication_record import (
    PublicationRecord,
    PublicationRecordError,
    load_publication_record,
    render_publication_body,
)
from scripts.service_record_a4 import service_index_path
from scripts.student_record import students_index_path
from scripts.teaching_record import teaching_index_path
from scripts.talk_record import talks_index_path

DRAFT_HEADING_RE = re.compile(r"^# DRAFT$", re.MULTILINE)
TITLE_HEADING_RE = re.compile(r"^#\s+(.*\S)\s*$")
FRONT_MATTER_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


class PageSourceError(ValueError):
    pass


@dataclass(frozen=True)
class PageSource:
    front_matter: dict[str, str]
    body: str
    title: str
    is_draft: bool


def page_path(page_stem: str, root: Path) -> Path:
    return root / f"{page_stem}.dj"


def talks_index_source_path(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> Path:
    return talks_index_path(root, talks_dir=talks_dir)


def cv_index_source_path(
    root: Path,
    *,
    cv_dir: Path | None = None,
) -> Path:
    return cv_index_path(root, cv_dir=cv_dir)


def collaborators_index_source_path(
    root: Path,
    *,
    collaborators_dir: Path | None = None,
) -> Path:
    return collaborators_index_path(root, collaborators_dir=collaborators_dir)


def students_index_source_path(
    root: Path,
    *,
    students_dir: Path | None = None,
) -> Path:
    return students_index_path(root, students_dir=students_dir)


def service_index_source_path(
    root: Path,
    *,
    service_dir: Path | None = None,
) -> Path:
    return service_index_path(root, service_dir=service_dir)


def funding_index_source_path(
    root: Path,
    *,
    funding_dir: Path | None = None,
) -> Path:
    return funding_index_path(root, funding_dir=funding_dir)


def news_index_source_path(
    root: Path,
    *,
    news_dir: Path | None = None,
) -> Path:
    return news_index_path(root, news_dir=news_dir)


def publications_index_source_path(
    root: Path,
    *,
    publications_dir: Path | None = None,
) -> Path:
    return publications_index_path(root, publications_dir=publications_dir)


def teaching_index_source_path(
    root: Path,
    *,
    teaching_dir: Path | None = None,
) -> Path:
    return teaching_index_path(root, teaching_dir=teaching_dir)


def normalize_front_matter_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_front_matter(block: str, path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for lineno, line in enumerate(block.splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        match = FRONT_MATTER_KEY_RE.match(line)
        if match is None:
            raise PageSourceError(f"{path}:{lineno}: invalid front matter line")

        key, raw_value = match.groups()
        if key in rows:
            raise PageSourceError(f"{path}:{lineno}: duplicate front matter key {key}")
        rows[key] = normalize_front_matter_value(raw_value)

    return rows


def split_front_matter(text: str, path: Path) -> tuple[dict[str, str], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    block_lines: list[str] = []
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return parse_front_matter("".join(block_lines), path), "".join(lines[i + 1 :])
        block_lines.append(line)

    raise PageSourceError(f"{path}: unterminated front matter block")


def extract_title(body: str, path: Path) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        match = TITLE_HEADING_RE.match(stripped)
        if match is None:
            raise PageSourceError(
                f"{path}: first non-empty line after front matter must be a level-1 heading"
            )

        title = match.group(1).translate(str.maketrans("", "", "#[]")).strip()
        if not title:
            raise PageSourceError(f"{path}: page title heading is empty")
        return title

    raise PageSourceError(f"{path}: missing level-1 heading")


def read_page_source(
    page_stem: str,
    root: Path,
    *,
    page_source_dir: Path | None = None,
) -> PageSource:
    actual_page_source_dir = page_source_dir or root
    path = page_path(page_stem, actual_page_source_dir)
    return read_source_path(path)


def read_source_path(path: Path) -> PageSource:
    if not path.exists():
        raise PageSourceError(f"Missing source page: {path}")
    text = path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(text, path)
    return PageSource(
        front_matter=front_matter,
        body=body,
        title=extract_title(body, path),
        is_draft=bool(DRAFT_HEADING_RE.search(text)),
    )


def read_talks_index_source(
    root: Path,
    *,
    talks_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        talks_index_source_path(
            root,
            talks_dir=talks_dir,
        )
    )


def read_cv_index_source(
    root: Path,
    *,
    cv_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        cv_index_source_path(
            root,
            cv_dir=cv_dir,
        )
    )


def read_collaborators_index_source(
    root: Path,
    *,
    collaborators_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        collaborators_index_source_path(
            root,
            collaborators_dir=collaborators_dir,
        )
    )


def read_students_index_source(
    root: Path,
    *,
    students_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        students_index_source_path(
            root,
            students_dir=students_dir,
        )
    )


def read_service_index_source(
    root: Path,
    *,
    service_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        service_index_source_path(
            root,
            service_dir=service_dir,
        )
    )


def read_funding_index_source(
    root: Path,
    *,
    funding_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        funding_index_source_path(
            root,
            funding_dir=funding_dir,
        )
    )


def read_news_index_source(
    root: Path,
    *,
    news_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        news_index_source_path(
            root,
            news_dir=news_dir,
        )
    )


def read_publications_index_source(
    root: Path,
    *,
    publications_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        publications_index_source_path(
            root,
            publications_dir=publications_dir,
        )
    )


def read_teaching_index_source(
    root: Path,
    *,
    teaching_dir: Path | None = None,
) -> PageSource:
    return read_source_path(
        teaching_index_source_path(
            root,
            teaching_dir=teaching_dir,
        )
    )


def publication_page_source(record: PublicationRecord, root: Path, *, publications_dir: Path | None = None) -> PageSource:
    if record.draft:
        return PageSource(
            front_matter={},
            body="",
            title=record.title,
            is_draft=True,
        )
    if not record.local_page:
        raise PageSourceError(
            f"{record.slug}: publication has no local detail page source"
        )
    return PageSource(
        front_matter={},
        body=render_publication_body(
            root,
            record,
            publications_dir=publications_dir,
        ),
        title=record.title,
        is_draft=False,
    )


def read_publication_page_source(
    slug: str,
    root: Path,
    *,
    publications_dir: Path | None = None,
) -> PageSource:
    try:
        record = load_publication_record(
            root,
            slug,
            publications_dir=publications_dir,
        )
    except PublicationRecordError as err:
        raise PageSourceError(str(err)) from err
    return publication_page_source(
        record,
        root,
        publications_dir=publications_dir,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract normalized title or Djot body from a page source."
    )
    parser.add_argument("action", choices={"title", "body"})
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--page", help="Ordinary page stem without .dj")
    selector.add_argument("--publication", help="Publication slug, e.g. 2024-asplos-lakeroad")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing Djot page sources.",
    )
    args = parser.parse_args()

    try:
        root = Path(args.root).resolve()
        if args.page is not None:
            source = read_page_source(args.page, root)
        else:
            source = read_publication_page_source(args.publication, root)
    except PageSourceError as err:
        print(err, file=sys.stderr)
        return 1

    if args.action == "title":
        sys.stdout.write(source.title)
        return 0

    sys.stdout.write(source.body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
