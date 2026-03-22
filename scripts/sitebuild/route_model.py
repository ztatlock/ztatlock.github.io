"""Route model and validation for the preview build."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Literal

RouteKind = Literal["ordinary_page", "publication_page", "static_file"]


class RouteModelError(ValueError):
    pass


@dataclass(frozen=True)
class Route:
    kind: RouteKind
    key: str
    source_paths: tuple[Path, ...]
    output_relpath: str
    public_url: str
    canonical_url: str
    is_draft: bool = False

    def to_json(self, *, root: Path) -> dict[str, object]:
        data = asdict(self)
        data["source_paths"] = [path.relative_to(root).as_posix() for path in self.source_paths]
        return data


def canonical_url(site_url: str, public_url: str) -> str:
    base = site_url.rstrip("/")
    if public_url == "/":
        return f"{base}/"
    return f"{base}{public_url}"


def normalize_output_relpath(output_relpath: str) -> str:
    candidate = PurePosixPath(output_relpath)
    if candidate.is_absolute():
        raise RouteModelError(f"output_relpath must be relative: {output_relpath}")
    normalized = candidate.as_posix()
    if normalized == ".":
        raise RouteModelError("output_relpath must not be empty")
    if normalized.startswith("../") or "/../" in normalized:
        raise RouteModelError(f"output_relpath escapes build root: {output_relpath}")
    return normalized


def validate_routes(routes: tuple[Route, ...]) -> None:
    seen_kind_key: set[tuple[str, str]] = set()
    output_to_route: dict[str, Route] = {}
    url_to_route: dict[str, Route] = {}
    canon_to_route: dict[str, Route] = {}

    for route in routes:
        kind_key = (route.kind, route.key)
        if kind_key in seen_kind_key:
            raise RouteModelError(f"duplicate route key for kind {route.kind}: {route.key}")
        seen_kind_key.add(kind_key)

        normalized_output = normalize_output_relpath(route.output_relpath)
        if normalized_output != route.output_relpath:
            raise RouteModelError(
                f"route output_relpath not normalized for {route.kind}:{route.key}: {route.output_relpath}"
            )

        if not route.public_url.startswith("/"):
            raise RouteModelError(
                f"route public_url must start with '/': {route.kind}:{route.key}: {route.public_url}"
            )
        if route.public_url != "/" and "//" in route.public_url:
            raise RouteModelError(
                f"route public_url must be normalized: {route.kind}:{route.key}: {route.public_url}"
            )
        if route.canonical_url.endswith("//"):
            raise RouteModelError(
                f"route canonical_url must be normalized: {route.kind}:{route.key}: {route.canonical_url}"
            )

        prior_output = output_to_route.get(route.output_relpath)
        if prior_output is not None:
            raise RouteModelError(
                f"duplicate output_relpath {route.output_relpath}: "
                f"{prior_output.kind}:{prior_output.key} and {route.kind}:{route.key}"
            )
        output_to_route[route.output_relpath] = route

        prior_url = url_to_route.get(route.public_url)
        if prior_url is not None:
            raise RouteModelError(
                f"duplicate public_url {route.public_url}: "
                f"{prior_url.kind}:{prior_url.key} and {route.kind}:{route.key}"
            )
        url_to_route[route.public_url] = route

        prior_canon = canon_to_route.get(route.canonical_url)
        if prior_canon is not None:
            raise RouteModelError(
                f"duplicate canonical_url {route.canonical_url}: "
                f"{prior_canon.kind}:{prior_canon.key} and {route.kind}:{route.key}"
            )
        canon_to_route[route.canonical_url] = route
