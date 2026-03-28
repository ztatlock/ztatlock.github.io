#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.sitebuild.site_config import SiteConfig, load_site_config

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


def scaffold_publication(
    root: Path,
    slug: str,
    *,
    config: SiteConfig | None = None,
) -> None:
    actual_config = config or load_site_config(root)

    pub_dir = actual_config.publications_dir / slug

    if pub_dir.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing directory: {pub_dir}")

    year, _, _ = slug.partition("-")
    if len(year) != 4 or not year.isdigit():
        raise ScaffoldPublicationError(
            f"Invalid publication slug {slug!r}; expected YEAR-..."
        )

    replacements = {
        "YEAR-CONF-SYS": slug,
        "YEAR": year,
    }

    pub_dir.mkdir(parents=True)
    write_new_file(
        pub_dir / "publication.json",
        render_template(actual_config.templates_dir / PUBLICATION_JSON_TEMPLATE.name, replacements),
    )
    write_new_file(pub_dir / f"{slug}-abstract.md", "TODO\n")
    write_new_file(pub_dir / f"{slug}.bib", "TODO\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new draft publication-local record."
    )
    parser.add_argument("--slug", required=True, help="Publication slug, e.g. 2026-conf-paper")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing site/templates/ and site/pubs/.",
    )
    args = parser.parse_args()

    try:
        scaffold_publication(
            Path(args.root).resolve(),
            args.slug,
        )
    except ScaffoldPublicationError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
