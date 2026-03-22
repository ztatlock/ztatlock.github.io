#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.sitebuild.djot_refs import load_and_render_site_refs
from scripts.sitebuild.page_renderer import PageRenderError, render_page_html
from scripts.sitebuild.site_config import load_site_config


def _load_refs_text(root: Path, refs_file: Path | None) -> str:
    if refs_file is not None:
        return refs_file.read_text(encoding="utf-8")
    return load_and_render_site_refs(
        people_path=root / "site" / "data" / "people.json",
        refs_path=root / "templates" / "REFS",
    )


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
    refs_text = _load_refs_text(root, refs_file)
    webfiles_url = args.webfiles_url or config.webfiles_url

    try:
        sys.stdout.write(
            render_page_html(
                args.page,
                canonical_url=args.canonical_url,
                refs_text=refs_text,
                root=root,
                webfiles_url=webfiles_url,
            )
        )
    except PageRenderError as err:
        print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
