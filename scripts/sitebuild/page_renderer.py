"""Shared HTML page renderer for the route-aware build."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from scripts.page_metadata import MetadataError, render_route_meta_for_url
from scripts.page_source import (
    PageSourceError,
    read_collaborators_index_source,
    read_cv_index_source,
    read_funding_index_source,
    read_news_index_source,
    read_page_source,
    read_publications_index_source,
    read_publication_page_source,
    read_service_index_source,
    read_students_index_source,
    read_teaching_index_source,
    read_talks_index_source,
)

from .page_projection import PageProjectionError, apply_page_projections

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
    route_kind: str,
    route_key: str,
    *,
    canonical_url: str,
    refs_text: str,
    root: Path,
    site_url: str,
    webfiles_url: str,
    aliases: dict[str, str] | None = None,
    page_source_dir: Path | None = None,
    collaborators_dir: Path | None = None,
    cv_dir: Path | None = None,
    funding_dir: Path | None = None,
    news_dir: Path | None = None,
    service_dir: Path | None = None,
    students_dir: Path | None = None,
    teaching_dir: Path | None = None,
    talks_dir: Path | None = None,
    publications_dir: Path | None = None,
    data_dir: Path | None = None,
    templates_dir: Path | None = None,
) -> str:
    actual_templates_dir = templates_dir or (root / "templates")
    head_1 = _read_template(actual_templates_dir / "HEAD.1")
    head_2 = _read_template(actual_templates_dir / "HEAD.2")
    foot = _read_template(actual_templates_dir / "FOOT")

    try:
        if route_kind == "ordinary_page":
            source = read_page_source(
                route_key,
                root,
                page_source_dir=page_source_dir,
            )
        elif route_kind == "collaborators_index_page":
            if route_key != "collaborators":
                raise PageRenderError(f"unsupported collaborators index route key: {route_key}")
            source = read_collaborators_index_source(
                root,
                collaborators_dir=collaborators_dir,
            )
        elif route_kind == "cv_index_page":
            if route_key != "cv":
                raise PageRenderError(f"unsupported CV index route key: {route_key}")
            source = read_cv_index_source(
                root,
                cv_dir=cv_dir,
            )
        elif route_kind == "talks_index_page":
            if route_key != "talks":
                raise PageRenderError(f"unsupported talks index route key: {route_key}")
            source = read_talks_index_source(
                root,
                talks_dir=talks_dir,
            )
        elif route_kind == "students_index_page":
            if route_key != "students":
                raise PageRenderError(f"unsupported students index route key: {route_key}")
            source = read_students_index_source(
                root,
                students_dir=students_dir,
            )
        elif route_kind == "service_index_page":
            if route_key != "service":
                raise PageRenderError(f"unsupported service index route key: {route_key}")
            source = read_service_index_source(
                root,
                service_dir=service_dir,
            )
        elif route_kind == "funding_index_page":
            if route_key != "funding":
                raise PageRenderError(f"unsupported funding index route key: {route_key}")
            source = read_funding_index_source(
                root,
                funding_dir=funding_dir,
            )
        elif route_kind == "news_index_page":
            if route_key != "news":
                raise PageRenderError(f"unsupported news index route key: {route_key}")
            source = read_news_index_source(
                root,
                news_dir=news_dir,
            )
        elif route_kind == "teaching_index_page":
            if route_key != "teaching":
                raise PageRenderError(f"unsupported teaching index route key: {route_key}")
            source = read_teaching_index_source(
                root,
                teaching_dir=teaching_dir,
            )
        elif route_kind == "publications_index_page":
            if route_key != "publications":
                raise PageRenderError(f"unsupported publications index route key: {route_key}")
            source = read_publications_index_source(
                root,
                publications_dir=publications_dir,
            )
        elif route_kind == "publication_page":
            source = read_publication_page_source(
                route_key,
                root,
                publications_dir=publications_dir,
            )
        else:
            raise PageRenderError(f"unsupported route kind for page rendering: {route_kind}")
    except PageSourceError as err:
        raise PageRenderError(str(err)) from err

    try:
        metadata_html = render_route_meta_for_url(
            route_kind,
            route_key,
            source.title,
            canonical_url=canonical_url,
            root=root,
            site_url=site_url,
            page_source_dir=page_source_dir,
            collaborators_dir=collaborators_dir,
            cv_dir=cv_dir,
            funding_dir=funding_dir,
            news_dir=news_dir,
            service_dir=service_dir,
            students_dir=students_dir,
            teaching_dir=teaching_dir,
            talks_dir=talks_dir,
            publications_dir=publications_dir,
        )
    except MetadataError as err:
        raise PageRenderError(str(err)) from err

    try:
        rendered_body = apply_page_projections(
            route_kind,
            route_key,
            source.body,
            root=root,
            data_dir=data_dir,
            talks_dir=talks_dir,
            publications_dir=publications_dir,
        )
    except PageProjectionError as err:
        raise PageRenderError(str(err)) from err

    djot_input = rendered_body.rstrip() + "\n\n" + refs_text
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
