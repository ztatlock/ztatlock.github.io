#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.page_metadata import validate_publication_metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate publication-local source invariants before legacy builds."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Site root containing publication stubs and pubs/.",
    )
    args = parser.parse_args()

    issues = validate_publication_metadata(Path(args.root).resolve())
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
