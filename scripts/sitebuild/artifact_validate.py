"""Shared HTML artifact validation helpers for built site output."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Pattern

IGNORED_TARGET_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "data:",
    "javascript:",
)
HTML_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
PUBLICATION_TODO_RE = re.compile(r"\bTODO\b")


def recursive_html_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.html") if path.is_file())


def find_placeholder_issues(
    *,
    html_files: Iterable[Path],
    relative_to: Path,
    placeholder_re: Pattern[str],
    publication_todo_prefixes: tuple[str, ...] = (),
) -> list[str]:
    issues: list[str] = []
    for path in html_files:
        relpath = path.relative_to(relative_to)
        relpath_text = relpath.as_posix()
        check_publication_todo = any(
            relpath_text.startswith(prefix) for prefix in publication_todo_prefixes
        )
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if placeholder_re.search(line):
                issues.append(f"{relpath_text}:{lineno}: {line.strip()}")
            if check_publication_todo and PUBLICATION_TODO_RE.search(line):
                issues.append(f"{relpath_text}:{lineno}: {line.strip()}")
    return issues


def _resolve_target_path(artifact_root: Path, source_html: Path, target: str) -> Path | None:
    relpath = target.split("#", 1)[0].split("?", 1)[0]
    if not relpath:
        return artifact_root / "index.html"

    if target.startswith("/"):
        candidate = artifact_root / relpath.lstrip("/")
    else:
        candidate = source_html.parent / relpath

    resolved = candidate.resolve()
    try:
        resolved.relative_to(artifact_root.resolve())
    except ValueError:
        return None

    if relpath.endswith("/") or resolved.is_dir():
        return resolved / "index.html"
    return resolved


def find_broken_link_issues(
    *,
    html_files: Iterable[Path],
    artifact_root: Path,
    relative_to: Path,
) -> list[str]:
    issues: list[str] = []
    for path in html_files:
        relpath = path.relative_to(relative_to).as_posix()
        text = path.read_text(encoding="utf-8")
        for target in HTML_LINK_RE.findall(text):
            if target.startswith(IGNORED_TARGET_PREFIXES):
                continue
            resolved = _resolve_target_path(artifact_root, path, target)
            if resolved is None or not resolved.exists():
                issues.append(f"{relpath}: {target}")
    return issues
