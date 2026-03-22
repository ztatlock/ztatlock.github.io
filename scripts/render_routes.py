#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts.sitebuild.route_discovery import discover_routes
from scripts.sitebuild.site_config import load_site_config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the future-oriented preview route table."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    config = load_site_config(Path(args.root))
    routes = discover_routes(config)
    data = [route.to_json(root=config.root) for route in routes]
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
