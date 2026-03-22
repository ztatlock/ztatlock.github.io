#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from scripts.publication_record import (
    PublicationRecordError,
    load_optional_publication_record,
    publication_slug,
    render_publication_body,
)

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


def read_page_source(page_stem: str, root: Path) -> PageSource:
    path = page_path(page_stem, root)
    slug = publication_slug(page_stem)
    if slug is not None:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            front_matter, body = split_front_matter(text, path)
            is_draft = bool(DRAFT_HEADING_RE.search(text))
        else:
            text = ""
            front_matter = {}
            body = ""
            is_draft = False

        if is_draft:
            return PageSource(
                front_matter=front_matter,
                body=body,
                title=extract_title(body, path),
                is_draft=True,
            )

        try:
            record = load_optional_publication_record(root, slug)
        except PublicationRecordError as err:
            raise PageSourceError(str(err)) from err
        if record is not None:
            return PageSource(
                front_matter=front_matter,
                body=render_publication_body(root, record),
                title=record.title,
                is_draft=is_draft,
            )

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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract normalized title or Djot body from a page source."
    )
    parser.add_argument("action", choices={"title", "body"})
    parser.add_argument("--page", required=True, help="Page stem without .dj")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing Djot page sources.",
    )
    args = parser.parse_args()

    try:
        source = read_page_source(args.page, Path(args.root).resolve())
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
