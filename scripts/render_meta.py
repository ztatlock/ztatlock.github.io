#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from page_metadata import MetadataError, render_page_meta


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render page metadata HTML from front matter or structured metadata manifests."
    )
    parser.add_argument("--page", required=True, help="Page stem without .html")
    parser.add_argument("--title", required=True, help="Rendered page title")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing manifests and source pages.",
    )
    args = parser.parse_args()

    try:
        sys.stdout.write(render_page_meta(args.page, args.title, Path(args.root).resolve()))
    except MetadataError as err:
        print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
