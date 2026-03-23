#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.page_metadata import (
    MetadataError,
    render_page_meta,
    render_publication_meta,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render page metadata HTML from page-local front matter or publication-local records."
    )
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--page", help="Ordinary page stem without .html")
    selector.add_argument("--publication", help="Publication slug, e.g. 2024-asplos-lakeroad")
    parser.add_argument("--title", required=True, help="Rendered page title")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing source pages and publication records.",
    )
    args = parser.parse_args()

    try:
        root = Path(args.root).resolve()
        if args.page is not None:
            sys.stdout.write(render_page_meta(args.page, args.title, root))
        else:
            sys.stdout.write(render_publication_meta(args.publication, args.title, root))
    except MetadataError as err:
        print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
