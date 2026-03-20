#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from page_metadata import MetadataError, add_publication_metadata_entry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add a new publication metadata placeholder entry."
    )
    parser.add_argument("--slug", required=True, help="Publication slug, e.g. 2026-conf-paper")
    parser.add_argument(
        "--description",
        default="TODO",
        help='Initial description placeholder (default: "TODO").',
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing manifests/publication-metadata.json.",
    )
    args = parser.parse_args()

    try:
        add_publication_metadata_entry(Path(args.root).resolve(), args.slug, args.description)
    except MetadataError as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
