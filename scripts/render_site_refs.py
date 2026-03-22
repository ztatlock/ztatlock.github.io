#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sitebuild.djot_refs import load_and_render_site_refs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the composed Djot refs bundle for site builds."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    root = Path(args.root)
    print(
        load_and_render_site_refs(
            people_path=root / "site" / "data" / "people.json",
            refs_path=root / "templates" / "REFS",
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
