#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sitebuild.preview_validate import (
    find_broken_link_issues,
    find_placeholder_issues,
)


def _print_section(title: str, issues: list[str]) -> None:
    if not issues:
        return
    print(title)
    for issue in issues:
        print(issue)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the preview site built under build/."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    build_root = Path(args.root).resolve() / "build"
    placeholder_issues = find_placeholder_issues(build_root)
    broken_link_issues = find_broken_link_issues(build_root)

    if placeholder_issues:
        _print_section(
            "ERROR: found unresolved placeholders in preview HTML",
            placeholder_issues,
        )
    if broken_link_issues:
        _print_section(
            "ERROR: found broken local links in preview HTML",
            broken_link_issues,
        )

    return 1 if placeholder_issues or broken_link_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
