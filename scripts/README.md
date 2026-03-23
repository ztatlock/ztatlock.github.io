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
- `make mkpub YCF=YEAR-CONF-SYS`
- `make index-now`

Optional personal-maintenance helper:

- `make inventory-webfiles`

## Primary CLI Entry Points

- `build_site.py`
  CLI entrypoint behind `make build`.
- `validate_build.py`
  CLI entrypoint behind `make check`.
- `render_routes.py`
  Emits the authoritative route table to `state/routes.json`.
- `build_pub_inventory.py`
  Builds the publication-artifact inventory by merging filesystem observation
  with `manifests/publication-artifact-curation.tsv`.
  `make inventory` writes a repo-local inventory snapshot under `state/inventory/`.
  `make inventory-webfiles` refreshes the personal archive copy under
  `~/Desktop/WEBFILES/inventory/`.
- `mkpub.sh`
  Scaffolds a new publication-local record under `site/pubs/<slug>/`.
- `check_env.sh`
  Verifies local command/tool prerequisites and reports portability
  assumptions.
- `index-now.sh`
  Submits updated pages to IndexNow and stores local run-state under `state/`.

## Shared Build Modules

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
- `page_metadata.py`
  Shared metadata helpers for page metadata rendering and source validation.
- `page_source.py`
  Shared ordinary-page parser plus publication-page source renderer.
- `publication_record.py`
  Shared loader and helpers for publication-local records in
  `site/pubs/<slug>/publication.json`.
- `talk_record.py`
  Shared loader and helpers for talk-local records in
  `site/talks/<slug>/talk.json`.
- `sitebuild/talk_projection.py`
  Talks-page projection helpers that render the bundle-driven talks list.

## Manual / Diagnostic Helpers

- `render_meta.py`
  Emits `<meta>` HTML for one ordinary page or publication page.
- `audit_people_refs.py`
  Audits generated people refs against the manual non-person remainder.
- `render_people_refs.py`
  Manual helper that renders Djot people-reference definitions from
  `site/data/people.json`.
- `render_site_refs.py`
  Manual helper that renders the composed Djot refs bundle used by the build:
  generated people refs from `site/data/people.json` plus the tiny manual
  non-person remainder in `site/templates/REFS`.
- `scaffold_publication.py`
  Underlying Python helper used by `mkpub.sh` to create a new draft
  publication-local scaffold from templates.

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
