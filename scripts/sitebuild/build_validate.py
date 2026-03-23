"""Validation helpers for generated build artifacts."""

from __future__ import annotations

from pathlib import Path

SITEMAP_FILENAMES = ("sitemap.txt", "sitemap.xml")


def find_sitemap_file_issues(
    build_root: Path,
    *,
    expected_txt: str | None = None,
    expected_xml: str | None = None,
) -> list[str]:
    issues: list[str] = []
    txt_path = build_root / "sitemap.txt"
    xml_path = build_root / "sitemap.xml"

    for name in SITEMAP_FILENAMES:
        if not (build_root / name).exists():
            issues.append(f"missing {name}")

    if issues:
        return issues

    if expected_txt is not None and txt_path.read_text(encoding="utf-8") != expected_txt:
        issues.append("sitemap.txt does not match route-driven sitemap")
    if expected_xml is not None and xml_path.read_text(encoding="utf-8") != expected_xml:
        issues.append("sitemap.xml does not match route-driven sitemap")
    return issues
