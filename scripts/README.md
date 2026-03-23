# Scripts

This directory holds executable helpers for working on the website repo.
It also holds the small reusable Python modules for the route-aware build
engine under `scripts/sitebuild/`.

Prefer the top-level `make` targets when they exist:

- `make build`
- `make check`
- `make routes`
- `make test`
- `make env-check`
- `make inventory`
- `make inventory-webfiles`
- `make mkpub YCF=YEAR-CONF-SYS`
- `make index-now`

## Current Scripts

- `sitebuild/artifact_validate.py`
  Shared HTML artifact-validation helpers for the authoritative `build/`
  output.
- `sitebuild/page_renderer.py`
  Shared HTML page renderer used by the route-aware build.
- `sitebuild/site_builder.py`
  Core builder that generates the site into `build/`.
- `sitebuild/route_discovery.py`
  Route discovery from the configured source layout.
- `sitebuild/route_model.py`
  Small route dataclasses and route invariants.
- `sitebuild/sitemap_builder.py`
  Route-driven sitemap generation.
- `sitebuild/site_config.py`
  Shared source/build configuration.
- `sitebuild/source_validate.py`
  Config-driven source validation for the authoritative path.
- `build_site.py`
  CLI entrypoint behind `make build`.
- `build_pub_inventory.py`
  Builds the publication-artifact inventory by merging filesystem observation
  with `manifests/publication-artifact-curation.tsv`.
  `make inventory` writes a repo-local inventory snapshot under `state/inventory/`.
  `make inventory-webfiles` refreshes the archive copy under
  `~/Desktop/WEBFILES/inventory/`.
- `check_env.sh`
  Verifies local command/tool prerequisites and reports portability
  assumptions.
- `index-now.sh`
  Submits updated pages to IndexNow and stores local run-state under `state/`.
- `mkpub.sh`
  Scaffolds a new publication-local record under `site/pubs/<slug>/`.
- `page_metadata.py`
  Shared metadata helpers for page metadata rendering and source validation.
- `page_source.py`
  Shared Djot page-source parser and publication-page source loader.
- `publication_record.py`
  Shared loader and helpers for publication-local records in
  `site/pubs/<slug>/publication.json`.
- `render_meta.py`
  Emits `<meta>` HTML for a page by rendering non-publication front matter and
  publication metadata.
- `render_people_refs.py`
  Prototype helper that renders Djot people-reference definitions from
  `site/data/people.json`.
- `render_routes.py`
  Emits the authoritative route table to `state/routes.json`.
- `render_site_refs.py`
  Renders the composed Djot refs bundle used by the build:
  generated people refs from `site/data/people.json` plus the tiny manual
  non-person remainder in `site/templates/REFS`.
- `scaffold_publication.py`
  Creates a new draft publication-local scaffold from templates.
- `validate_build.py`
  Validates authoritative source invariants plus the built site under `build/`
  for unresolved placeholders, broken local links, and route-driven sitemap
  correctness.

## Conventions

- Put new executable helpers here, not in `site/templates/`.
- Prefer running Python helpers as modules, for example
  `python3 -m scripts.build_site`, so imports stay package-clean.
- Keep reusable build/data logic in small Python modules under
  `scripts/sitebuild/`.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
- Keep portability assumptions explicit when a script relies on a tool such as
  `wget`.
