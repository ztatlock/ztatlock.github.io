"""Shared HTML page renderer for legacy and preview builds."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from scripts.page_metadata import MetadataError, render_page_meta_for_url
from scripts.page_source import PageSourceError, read_page_source

HTML_TARGET_RE = re.compile(r'((?:href|src)=["\'])([^"\']+)(["\'])')
IGNORED_TARGET_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "data:",
    "javascript:",
)


class PageRenderError(ValueError):
    pass


def _read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _render_head_1(template: str, *, title: str, canonical_url: str) -> str:
    return template.replace("__TITLE__", title).replace("__CANON__", canonical_url)


def _run_djot(djot_text: str) -> str:
    completed = subprocess.run(
        ["djot"],
        input=djot_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise PageRenderError(completed.stderr.strip() or "djot failed")
    return completed.stdout


def rewrite_local_html_targets(html_text: str, *, aliases: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        if target.startswith(IGNORED_TARGET_PREFIXES) or target.startswith("/"):
            return match.group(0)

        fragment = ""
        query = ""
        base = target
        if "#" in base:
            base, hash_part = base.split("#", 1)
            fragment = f"#{hash_part}"
        if "?" in base:
            base, query_part = base.split("?", 1)
            query = f"?{query_part}"

        rewritten = aliases.get(base)
        if rewritten is None:
            return match.group(0)
        return f"{prefix}{rewritten}{query}{fragment}{suffix}"

    return HTML_TARGET_RE.sub(replace, html_text)


def render_page_html(
    page_stem: str,
    *,
    canonical_url: str,
    refs_text: str,
    root: Path,
    webfiles_url: str,
    aliases: dict[str, str] | None = None,
) -> str:
    templates_dir = root / "templates"
    head_1 = _read_template(templates_dir / "HEAD.1")
    head_2 = _read_template(templates_dir / "HEAD.2")
    foot = _read_template(templates_dir / "FOOT")

    try:
        source = read_page_source(page_stem, root)
    except PageSourceError as err:
        raise PageRenderError(str(err)) from err

    try:
        metadata_html = render_page_meta_for_url(
            page_stem,
            source.title,
            canonical_url=canonical_url,
            root=root,
        )
    except MetadataError as err:
        raise PageRenderError(str(err)) from err

    djot_input = source.body.rstrip() + "\n\n" + refs_text
    djot_input = djot_input.replace("__WEBFILES__", webfiles_url)
    body_html = _run_djot(djot_input)

    html_text = "".join(
        [
            _render_head_1(head_1, title=source.title, canonical_url=canonical_url),
            metadata_html,
            head_2,
            body_html,
            foot,
        ]
    )
    if aliases:
        return rewrite_local_html_targets(html_text, aliases=aliases)
    return html_text
