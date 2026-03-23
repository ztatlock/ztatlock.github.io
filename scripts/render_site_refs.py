#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.sitebuild.djot_refs import load_and_render_site_refs
from scripts.sitebuild.site_config import load_site_config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the composed Djot refs bundle for site builds."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    config = load_site_config(Path(args.root))
    print(
        load_and_render_site_refs(
            people_path=config.people_data_path,
            refs_path=config.manual_refs_path,
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
