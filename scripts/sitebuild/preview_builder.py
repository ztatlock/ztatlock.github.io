"""Build a future-oriented preview site into build/."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from page_metadata import (
    MetadataError,
    default_page_image_path,
    load_front_matter_general_metadata,
    render_metadata_block,
)
from page_source import PageSourceError, read_page_source
from publication_record import (
    PublicationRecordError,
    load_publication_record,
    publication_metadata_image_path,
    publication_page_stem,
)

from .djot_refs import load_and_render_site_refs
from .route_discovery import discover_routes
from .route_model import Route, normalize_output_relpath
from .site_config import SiteConfig

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


class PreviewBuildError(ValueError):
    pass


def _read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _render_head_1(template: str, *, title: str, canonical: str) -> str:
    return template.replace("__TITLE__", title).replace("__CANON__", canonical)


def _render_page_metadata(route: Route, *, title: str, config: SiteConfig) -> str:
    root = config.root
    if route.kind == "ordinary_page":
        try:
            row = load_front_matter_general_metadata(route.key, root)
        except MetadataError as err:
            raise PreviewBuildError(str(err)) from err
        if row is None:
            return ""
        description = row["description"]
        share_description = row["share_description"] or description
        image_path = row["image_path"] or default_page_image_path()
        rendered_title = row["title"] or title
        return render_metadata_block(
            title=rendered_title,
            description=description,
            share_description=share_description,
            image_path=image_path,
            url=route.canonical_url,
        )

    if route.kind == "publication_page":
        try:
            record = load_publication_record(root, route.key)
        except PublicationRecordError as err:
            raise PreviewBuildError(str(err)) from err
        description = record.description
        share_description = record.share_description or description
        image_path = publication_metadata_image_path(root, record)
        return render_metadata_block(
            title=title,
            description=description,
            share_description=share_description,
            image_path=image_path,
            url=route.canonical_url,
        )

    return ""


def _run_djot(djot_text: str) -> str:
    completed = subprocess.run(
        ["djot"],
        input=djot_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise PreviewBuildError(completed.stderr.strip() or "djot failed")
    return completed.stdout


def _route_aliases(routes: tuple[Route, ...]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for route in routes:
        aliases[route.output_relpath] = route.public_url
        if route.kind == "ordinary_page" and route.key == "index":
            aliases["index.html"] = route.public_url
        if route.kind == "publication_page":
            aliases[f"pub-{route.key}.html"] = route.public_url
    return aliases


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


def _render_page_html(route: Route, *, refs_text: str, aliases: dict[str, str], config: SiteConfig) -> str:
    templates_dir = config.root / "templates"
    head_1 = _read_template(templates_dir / "HEAD.1")
    head_2 = _read_template(templates_dir / "HEAD.2")
    foot = _read_template(templates_dir / "FOOT")

    page_stem = route.key if route.kind == "ordinary_page" else publication_page_stem(route.key)
    try:
        source = read_page_source(page_stem, config.root)
    except PageSourceError as err:
        raise PreviewBuildError(str(err)) from err
    except PublicationRecordError as err:
        raise PreviewBuildError(str(err)) from err

    djot_input = source.body.rstrip() + "\n\n" + refs_text
    djot_input = djot_input.replace("__WEBFILES__", config.webfiles_url)
    body_html = _run_djot(djot_input)
    html_text = "".join(
        [
            _render_head_1(head_1, title=source.title, canonical=route.canonical_url),
            _render_page_metadata(route, title=source.title, config=config),
            head_2,
            body_html,
            foot,
        ]
    )
    return rewrite_local_html_targets(html_text, aliases=aliases)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _copy_static_route(route: Route, *, config: SiteConfig) -> None:
    destination = config.build_dir / normalize_output_relpath(route.output_relpath)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(route.source_paths[0], destination)


def build_preview_site(config: SiteConfig) -> tuple[Route, ...]:
    routes = discover_routes(config)

    if config.build_dir.exists():
        shutil.rmtree(config.build_dir)
    config.build_dir.mkdir(parents=True)

    refs_text = load_and_render_site_refs(
        people_path=config.root / "site" / "data" / "people.json",
        refs_path=config.root / "templates" / "REFS",
    )
    aliases = _route_aliases(routes)

    for route in routes:
        if route.kind == "static_file":
            _copy_static_route(route, config=config)
            continue
        if route.is_draft:
            continue
        html_text = _render_page_html(route, refs_text=refs_text, aliases=aliases, config=config)
        _write_text(config.build_dir / route.output_relpath, html_text)

    return routes
