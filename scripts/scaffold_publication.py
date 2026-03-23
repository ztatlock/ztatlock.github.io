#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.publication_record import publication_page_stem

PUB_STUB_TEMPLATE = Path("templates/pub-stub.dj")
PUBLICATION_JSON_TEMPLATE = Path("templates/publication.json")


class ScaffoldPublicationError(ValueError):
    pass


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def write_new_file(path: Path, contents: str) -> None:
    if path.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing file: {path}")
    path.write_text(contents, encoding="utf-8")


def scaffold_publication(root: Path, slug: str) -> None:
    pub_dir = root / "pubs" / slug
    page_stub = root / f"{publication_page_stem(slug)}.dj"

    if pub_dir.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing directory: {pub_dir}")
    if page_stub.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing file: {page_stub}")

    replacements = {"YEAR-CONF-SYS": slug}

    pub_dir.mkdir(parents=True)
    write_new_file(
        page_stub,
        render_template(root / PUB_STUB_TEMPLATE, replacements),
    )
    write_new_file(
        pub_dir / "publication.json",
        render_template(root / PUBLICATION_JSON_TEMPLATE, replacements),
    )
    write_new_file(pub_dir / f"{slug}-abstract.md", "TODO\n")
    write_new_file(pub_dir / f"{slug}.bib", "TODO\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Scaffold a new draft publication-local record plus the temporary "
            "legacy publication stub."
        )
    )
    parser.add_argument("--slug", required=True, help="Publication slug, e.g. 2026-conf-paper")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing templates/ and pubs/.",
    )
    args = parser.parse_args()

    try:
        scaffold_publication(Path(args.root).resolve(), args.slug)
    except ScaffoldPublicationError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
