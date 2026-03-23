#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.publication_record import publication_page_stem
from scripts.sitebuild.site_config import SiteConfig, load_site_config

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


def _default_include_legacy_stub(config: SiteConfig) -> bool:
    return config.page_source_dir == config.repo_root


def scaffold_publication(
    root: Path,
    slug: str,
    *,
    config: SiteConfig | None = None,
    include_legacy_stub: bool | None = None,
) -> None:
    actual_config = config or load_site_config(root)
    actual_include_legacy_stub = (
        _default_include_legacy_stub(actual_config)
        if include_legacy_stub is None
        else include_legacy_stub
    )

    pub_dir = actual_config.publications_dir / slug
    page_stub = actual_config.page_source_dir / f"{publication_page_stem(slug)}.dj"

    if pub_dir.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing directory: {pub_dir}")
    if actual_include_legacy_stub and page_stub.exists():
        raise ScaffoldPublicationError(f"Refusing to overwrite existing file: {page_stub}")

    replacements = {"YEAR-CONF-SYS": slug}

    pub_dir.mkdir(parents=True)
    if actual_include_legacy_stub:
        write_new_file(
            page_stub,
            render_template(actual_config.templates_dir / PUB_STUB_TEMPLATE.name, replacements),
        )
    write_new_file(
        pub_dir / "publication.json",
        render_template(actual_config.templates_dir / PUBLICATION_JSON_TEMPLATE.name, replacements),
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
    stub_group = parser.add_mutually_exclusive_group()
    stub_group.add_argument(
        "--legacy-stub",
        action="store_true",
        help="Force creation of the temporary legacy publication stub.",
    )
    stub_group.add_argument(
        "--no-legacy-stub",
        action="store_true",
        help="Do not create the temporary legacy publication stub.",
    )
    args = parser.parse_args()
    include_legacy_stub: bool | None = None
    if args.legacy_stub:
        include_legacy_stub = True
    if args.no_legacy_stub:
        include_legacy_stub = False

    try:
        scaffold_publication(
            Path(args.root).resolve(),
            args.slug,
            include_legacy_stub=include_legacy_stub,
        )
    except ScaffoldPublicationError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
