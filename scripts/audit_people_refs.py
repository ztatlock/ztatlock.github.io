#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.sitebuild.people_refs_audit import audit_people_refs


def _print_section(title: str, labels: tuple[str, ...]) -> None:
    print(f"{title} ({len(labels)})")
    for label in labels:
        print(f"  {label}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit templates/REFS against generated people refs."
    )
    parser.add_argument("--root", default=".", help="repo root")
    args = parser.parse_args()

    root = Path(args.root)
    audit = audit_people_refs(
        people_path=root / "site" / "data" / "people.json",
        refs_path=root / "templates" / "REFS",
    )

    print(f"duplicate template labels: {len(audit.duplicate_template_labels)}")
    for label, urls in sorted(audit.duplicate_template_labels.items()):
        print(f"  {label}: {', '.join(urls)}")
    _print_section("overlapping people refs", audit.overlapping_people_refs)
    for label, (template_url, generated_url) in sorted(audit.mismatched_urls.items()):
        print(f"url mismatch: {label}")
        print(f"  template : {template_url}")
        print(f"  generated: {generated_url}")
    _print_section("manual remainder refs", audit.manual_remainder_refs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
