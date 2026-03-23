#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.publication_record import (
    PUBLICATION_RECORD_NAME,
    publication_page_path,
    publication_page_stem,
)
from scripts.sitebuild.djot_refs import load_and_render_site_refs
from scripts.sitebuild.page_renderer import PageRenderError, render_page_html
from scripts.sitebuild.site_config import SiteConfig, load_site_config


def _load_refs_text(config: SiteConfig, refs_file: Path | None) -> str:
    if refs_file is not None:
        return refs_file.read_text(encoding="utf-8")
    return load_and_render_site_refs(
        people_path=config.people_data_path,
        refs_path=config.manual_refs_path,
    )


def _legacy_publication_aliases(config: SiteConfig) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for record_path in sorted(config.publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}")):
        slug = record_path.parent.name
        legacy_page = f"{publication_page_stem(slug)}.html"
        canonical_page = publication_page_path(slug)
        aliases[canonical_page] = legacy_page
        aliases[f"{canonical_page}index.html"] = legacy_page
    return aliases


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a full HTML page using the shared site render core."
    )
    parser.add_argument("--page", required=True, help="page stem without .dj")
    parser.add_argument("--canonical-url", required=True, help="canonical URL for this render")
    parser.add_argument("--root", default=".", help="repo root")
    parser.add_argument("--refs-file", help="pre-rendered Djot refs bundle to append")
    parser.add_argument(
        "--webfiles-url",
        help="replacement URL for __WEBFILES__ placeholders",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = load_site_config(root)
    refs_file = Path(args.refs_file).resolve() if args.refs_file else None
    refs_text = _load_refs_text(config, refs_file)
    webfiles_url = args.webfiles_url or config.webfiles_url

    try:
        sys.stdout.write(
            render_page_html(
                args.page,
                canonical_url=args.canonical_url,
                refs_text=refs_text,
                root=config.repo_root,
                site_url=config.site_url,
                webfiles_url=webfiles_url,
                aliases=_legacy_publication_aliases(config),
                page_source_dir=config.page_source_dir,
                publications_dir=config.publications_dir,
                templates_dir=config.templates_dir,
            )
        )
    except PageRenderError as err:
        print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
