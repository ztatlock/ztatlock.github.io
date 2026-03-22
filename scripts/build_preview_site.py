#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.sitebuild.preview_builder import PreviewBuildError, build_preview_site
from scripts.sitebuild.route_model import RouteModelError
from scripts.sitebuild.site_config import load_site_config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the future-oriented preview site into build/."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    config = load_site_config(Path(args.root))
    try:
        build_preview_site(config)
    except (PreviewBuildError, RouteModelError) as err:
        print(err, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
