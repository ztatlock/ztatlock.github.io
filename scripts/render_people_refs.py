#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sitebuild.people_refs import load_and_render_people_refs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Djot people references from site/data/people.json."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    root = Path(args.root)
    people_path = root / "site" / "data" / "people.json"
    print(load_and_render_people_refs(people_path), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
