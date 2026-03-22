"""Parse simple Djot reference-definition files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


REF_LINE_RE = re.compile(r"^\[(.+?)\]:\s*(\S+)\s*$")


@dataclass(frozen=True)
class TemplateRefs:
    label_to_url: dict[str, str]
    duplicate_labels: dict[str, tuple[str, ...]]


def parse_template_refs(path: Path) -> TemplateRefs:
    label_to_urls: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = REF_LINE_RE.match(line)
        if match is None:
            continue
        label, url = match.groups()
        label_to_urls.setdefault(label, []).append(url)

    label_to_url = {label: urls[0] for label, urls in label_to_urls.items()}
    duplicate_labels = {
        label: tuple(urls) for label, urls in label_to_urls.items() if len(urls) > 1
    }
    return TemplateRefs(label_to_url=label_to_url, duplicate_labels=duplicate_labels)
