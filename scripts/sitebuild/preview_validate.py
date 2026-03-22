"""Validate the preview build under build/."""

from __future__ import annotations

import re
from pathlib import Path

IGNORED_TARGET_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "data:",
    "javascript:",
)
PLACEHOLDER_RE = re.compile(
    r'YOUTUBEID|href="TODO"|content="TITLE"|content="DESCRIPTION"|CONF YEAR'
)
PUBLICATION_TODO_RE = re.compile(r"\bTODO\b")
HTML_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def _all_html_files(build_root: Path) -> list[Path]:
    return sorted(path for path in build_root.rglob("*.html") if path.is_file())


def find_placeholder_issues(build_root: Path) -> list[str]:
    issues: list[str] = []
    for path in _all_html_files(build_root):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                issues.append(f"{path.relative_to(build_root)}:{lineno}: {line.strip()}")
            if path.relative_to(build_root).as_posix().startswith("pubs/") and PUBLICATION_TODO_RE.search(line):
                issues.append(f"{path.relative_to(build_root)}:{lineno}: {line.strip()}")
    return issues


def _resolve_target_path(build_root: Path, source_html: Path, target: str) -> Path | None:
    relpath = target.split("#", 1)[0].split("?", 1)[0]
    if not relpath:
        return build_root / "index.html"

    if target.startswith("/"):
        candidate = build_root / relpath.lstrip("/")
    else:
        candidate = source_html.parent / relpath

    resolved = candidate.resolve()
    try:
        resolved.relative_to(build_root.resolve())
    except ValueError:
        return None

    if relpath.endswith("/") or resolved.is_dir():
        return resolved / "index.html"
    return resolved


def find_broken_link_issues(build_root: Path) -> list[str]:
    issues: list[str] = []
    for path in _all_html_files(build_root):
        text = path.read_text(encoding="utf-8")
        for target in HTML_LINK_RE.findall(text):
            if target.startswith(IGNORED_TARGET_PREFIXES):
                continue
            resolved = _resolve_target_path(build_root, path, target)
            if resolved is None or not resolved.exists():
                issues.append(f"{path.relative_to(build_root)}: {target}")
    return issues
