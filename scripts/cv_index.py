#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

CV_INDEX_NAME = "index.dj"


def default_cv_dir(root: Path) -> Path:
    return root / "site" / "cv"


def cv_index_path(
    root: Path,
    *,
    cv_dir: Path | None = None,
) -> Path:
    return (cv_dir or default_cv_dir(root)) / CV_INDEX_NAME
