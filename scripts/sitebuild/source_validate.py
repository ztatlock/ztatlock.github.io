"""Config-driven source validation for the new build path."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.publication_index import (
    publications_index_path,
    PUBLICATIONS_MAIN_LIST_PLACEHOLDER,
    PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER,
)
from scripts.publication_record import (
    EXTRA_CONTENT_NAME,
    PUBLICATION_RECORD_NAME,
    PublicationRecordError,
    load_publication_record,
    publication_page_path,
)
from scripts.student_record import (
    STUDENTS_DATA_NAME,
    StudentRecordError,
    find_student_record_issues,
    load_student_sections,
    students_index_path,
)
from scripts.talk_record import TALKS_INDEX_NAME, find_talk_record_issues, talks_index_path
from scripts.page_metadata import (
    validate_general_source_metadata_path,
    validate_general_page_metadata,
    validate_publication_record_metadata,
)

from .site_config import SiteConfig
from .page_projection import STUDENT_SECTION_PLACEHOLDERS, TALKS_LIST_PLACEHOLDER

LEGACY_PUBLICATION_LINK_RE = re.compile(r"\b(pub-\d{4}[-a-z0-9]*\.html)\b")
LEGACY_PUBLICATIONS_INDEX_LINK_RE = re.compile(r"\b(publications\.html)\b")
LEGACY_STUDENTS_LINK_RE = re.compile(r"\b(students\.html)\b")
LEGACY_TALKS_LINK_RE = re.compile(r"\b(talks\.html)\b")
LITERAL_STUDENT_ENTRY_RE = re.compile(
    r"^- \[[^\]]+\](?:\[[^\]]*\]|\([^)]+\)),\s",
    re.MULTILINE,
)
ROOT_STATIC_SOURCE_NAMES = (
    "CNAME",
    "robots.txt",
    "style.css",
    "zip-longitude.js",
)
STUDENT_CONSUMER_PAGE_NAMES = ("students.dj", "cv.dj")


def _legacy_publication_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    seen = sorted(set(LEGACY_PUBLICATION_LINK_RE.findall(text)))
    for target in seen:
        slug = target.removeprefix("pub-").removesuffix(".html")
        issues.append(
            f"{path}: legacy publication link should use canonical publication path: "
            f"{target} -> {publication_page_path(slug)}"
        )
    return issues


def _legacy_talks_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not LEGACY_TALKS_LINK_RE.search(text):
        return []
    return [f"{path}: legacy talks link should use canonical collection path: talks.html -> talks/"]


def _legacy_publications_index_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not LEGACY_PUBLICATIONS_INDEX_LINK_RE.search(text):
        return []
    return [
        f"{path}: legacy publications index link should use canonical collection path: "
        "publications.html -> pubs/"
    ]


def _legacy_students_link_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not LEGACY_STUDENTS_LINK_RE.search(text):
        return []
    return [f"{path}: legacy students link should use canonical collection path: students.html -> students/"]


def _all_authored_djot_sources(config: SiteConfig) -> list[Path]:
    paths = list(sorted(config.page_source_dir.glob("*.dj")))
    talks_index = talks_index_path(config.repo_root, talks_dir=config.talks_dir)
    if talks_index.exists():
        paths.append(talks_index)
    students_index = students_index_path(config.repo_root, students_dir=config.students_dir)
    if students_index.exists():
        paths.append(students_index)
    publications_index = publications_index_path(
        config.repo_root,
        publications_dir=config.publications_dir,
    )
    if publications_index.exists():
        paths.append(publications_index)
    paths.extend(sorted(config.publications_dir.glob(f"*/{EXTRA_CONTENT_NAME}")))
    paths.extend(sorted(config.talks_dir.glob(f"*/{EXTRA_CONTENT_NAME}")))
    return paths


def _find_legacy_publication_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_publication_link_issues(path))
    return issues


def _find_legacy_talks_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_talks_link_issues(path))
    return issues


def _find_legacy_publications_index_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_publications_index_link_issues(path))
    return issues


def _find_legacy_students_link_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in _all_authored_djot_sources(config):
        issues.extend(_legacy_students_link_issues(path))
    return issues


def _find_root_layout_drift_issues(config: SiteConfig) -> list[str]:
    issues: list[str] = []
    for path in sorted(config.repo_root.glob("*.dj")):
        issues.append(f"{path}: authored Djot source must live under site/pages/")
    for path in sorted(config.repo_root.glob("*.html")):
        issues.append(f"{path}: authored static HTML must live under site/static/")
    for path in sorted(config.repo_root.glob("*.txt")):
        if path.name == "sitemap.txt":
            issues.append(f"{path}: generated sitemap belongs only under build/")
            continue
        if path.name in ROOT_STATIC_SOURCE_NAMES:
            continue
        issues.append(f"{path}: static text assets must live under site/static/")
    if (config.repo_root / "sitemap.xml").exists():
        issues.append(f"{config.repo_root / 'sitemap.xml'}: generated sitemap belongs only under build/")
    for name in ROOT_STATIC_SOURCE_NAMES:
        path = config.repo_root / name
        if path.exists():
            issues.append(f"{path}: static assets must live under site/static/")
    if (config.repo_root / "img").exists():
        issues.append(f"{config.repo_root / 'img'}: shared images must live under site/static/img/")
    if (config.repo_root / "pubs").exists():
        issues.append(f"{config.repo_root / 'pubs'}: publication bundles must live under site/pubs/")
    if (config.repo_root / "templates").exists():
        issues.append(f"{config.repo_root / 'templates'}: templates must live under site/templates/")
    return issues


def _find_talk_projection_issues(config: SiteConfig) -> list[str]:
    if not config.talks_dir.exists():
        return []

    talk_dirs = [path for path in sorted(config.talks_dir.iterdir()) if path.is_dir()]
    if not talk_dirs:
        return []

    talks_page = talks_index_path(config.repo_root, talks_dir=config.talks_dir)
    issues: list[str] = []
    if not talks_page.exists():
        return [f"{talks_page}: talks index page is required when talk bundles exist"]

    legacy_talks_page = config.page_source_dir / "talks.dj"
    if legacy_talks_page.exists():
        issues.append(f"{legacy_talks_page}: talks index wrapper must move to {talks_page}")

    text = talks_page.read_text(encoding="utf-8")
    if TALKS_LIST_PLACEHOLDER not in text:
        issues.append(f"{talks_page}: talks index page must contain {TALKS_LIST_PLACEHOLDER}")

    issues.extend(
        validate_general_source_metadata_path(
            talks_page,
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
    )
    return issues


def _find_publications_index_projection_issues(config: SiteConfig) -> list[str]:
    index_path = publications_index_path(
        config.repo_root,
        publications_dir=config.publications_dir,
    )
    legacy_index_path = config.page_source_dir / "publications.dj"
    has_non_draft_records = False
    for path in sorted(config.publications_dir.glob(f"*/{PUBLICATION_RECORD_NAME}")):
        try:
            record = load_publication_record(
                config.repo_root,
                path.parent.name,
                publications_dir=config.publications_dir,
            )
        except PublicationRecordError:
            continue
        if not record.draft:
            has_non_draft_records = True

    issues: list[str] = []
    if legacy_index_path.exists():
        issues.append(
            f"{legacy_index_path}: publications index wrapper must move to {index_path}"
        )

    if not has_non_draft_records and not index_path.exists():
        return issues

    if not index_path.exists():
        issues.append(
            f"{index_path}: publications index page is required when publication bundles exist"
        )
        return issues

    issues.extend(
        validate_general_source_metadata_path(
            index_path,
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
    )

    text = index_path.read_text(encoding="utf-8")
    if PUBLICATIONS_MAIN_LIST_PLACEHOLDER not in text:
        issues.append(
            f"{index_path}: publications index page must contain {PUBLICATIONS_MAIN_LIST_PLACEHOLDER}"
        )
    if PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER not in text:
        issues.append(
            f"{index_path}: publications index page must contain {PUBLICATIONS_WORKSHOP_LIST_PLACEHOLDER}"
        )
    if re.search(r"^\{#\d{4}[-a-z0-9]+\}$", text, flags=re.MULTILINE):
        issues.append(
            f"{index_path}: publications index page must not contain literal publication entry blocks"
        )
    return issues


def _find_student_projection_issues(config: SiteConfig) -> list[str]:
    index_path = students_index_path(config.repo_root, students_dir=config.students_dir)
    legacy_index_path = config.page_source_dir / "students.dj"
    students_path = config.data_dir / STUDENTS_DATA_NAME

    issues: list[str] = []
    if legacy_index_path.exists():
        issues.append(f"{legacy_index_path}: students index wrapper must move to {index_path}")

    if not students_path.exists() and not index_path.exists():
        return issues

    if not index_path.exists():
        issues.append(
            f"{index_path}: students index page is required when canonical student records exist"
        )
        return issues

    issues.extend(
        validate_general_source_metadata_path(
            index_path,
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
    )

    text = index_path.read_text(encoding="utf-8")
    for placeholder in STUDENT_SECTION_PLACEHOLDERS.values():
        if placeholder not in text:
            issues.append(f"{index_path}: students index page must contain {placeholder}")
    if LITERAL_STUDENT_ENTRY_RE.search(text):
        issues.append(
            f"{index_path}: students index page must not contain literal student entry blocks"
        )

    if students_path.exists():
        try:
            sections = load_student_sections(
                config.repo_root,
                students_path=students_path,
                people_path=config.people_data_path,
            )
        except StudentRecordError:
            return issues
        section_keys = {section.key for section in sections}
        missing = [key for key in STUDENT_SECTION_PLACEHOLDERS if key not in section_keys]
        if missing:
            issues.append(
                f"{students_path}: missing section keys required by students page projection: {', '.join(missing)}"
            )
    return issues


def _find_student_data_issues(config: SiteConfig) -> list[str]:
    students_path = config.data_dir / STUDENTS_DATA_NAME
    students_index = students_index_path(config.repo_root, students_dir=config.students_dir)
    has_student_consumers = any(
        (config.page_source_dir / name).exists()
        for name in STUDENT_CONSUMER_PAGE_NAMES
    ) or students_index.exists()
    if not students_path.exists() and not has_student_consumers:
        return []
    return find_student_record_issues(
        config.repo_root,
        students_path=students_path,
        people_path=config.people_data_path,
    )


def find_source_issues(config: SiteConfig) -> list[str]:
    return (
        validate_general_page_metadata(
            config.repo_root,
            page_source_dir=config.page_source_dir,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
        + validate_publication_record_metadata(
            config.repo_root,
            publications_dir=config.publications_dir,
            static_source_dir=config.static_source_dir,
        )
        + _find_student_data_issues(config)
        + _find_student_projection_issues(config)
        + find_talk_record_issues(
            config.repo_root,
            talks_dir=config.talks_dir,
        )
        + _find_talk_projection_issues(config)
        + _find_publications_index_projection_issues(config)
        + _find_legacy_publication_link_issues(config)
        + _find_legacy_publications_index_link_issues(config)
        + _find_legacy_students_link_issues(config)
        + _find_legacy_talks_link_issues(config)
        + _find_root_layout_drift_issues(config)
    )
