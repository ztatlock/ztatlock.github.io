# Scripts

This directory holds executable helpers for working on the website repo.
It also now holds the small reusable Python modules for the staged
source/build/data redesign under `scripts/sitebuild/`.

Prefer the top-level `make` targets when they exist:

- `make check`
- `make check-preview`
- `make build-preview`
- `make env-check`
- `make routes-preview`
- `make test`
- `make validate-site`
- `make inventory`
- `make inventory-webfiles`
- `make mkpub YCF=YEAR-CONF-SYS`
- `make index-now`

## Current Scripts

- `sitebuild/artifact_validate.py`
  Shared HTML artifact-validation helpers for both the legacy root build and
  the future-oriented preview build.
- `build_pub_inventory.py`
  Builds the publication-artifact inventory by merging filesystem observation
  with `manifests/publication-artifact-curation.tsv`.
  `make inventory` writes a repo-local preview under `state/inventory/`.
  `make inventory-webfiles` refreshes the canonical archive copy under
  `~/Desktop/WEBFILES/inventory/`.
- `build_preview_site.py`
  Builds the future-oriented preview site into `build/` while still reading
  from the current source layout by default.
  The preview path is now source-layout-aware through `SiteConfig`, and the
  preview build includes route-driven `build/sitemap.txt` and
  `build/sitemap.xml`.
- `audit_people_refs.py`
  Audit script for the post-cutover steady state.
  It checks the manual `templates/REFS` remainder for duplicate labels and
  accidental overlap with person refs owned by `site/data/people.json`.
- `check.sh`
  Rebuilds the site in an isolated scratch copy and runs structural validation
  checks without dirtying tracked site outputs in the live repo. It also
  checks that draft outputs stay out of the public build and sitemaps.
- `check_env.sh`
  Verifies the local command/tool prerequisites and reports current
  portability assumptions for optional workflows.
- `index-now.sh`
  Submits updated pages to IndexNow and stores its local run-state under
  `state/`. It currently assumes `wget`.
- `mkpub.sh`
  Scaffolds a new publication-local record under `pubs/<slug>/` plus a
  top-level draft-status stub `pub-<slug>.dj`.
- `page_metadata.py`
  Shared metadata helpers for generated page metadata and metadata source
  validation across both public non-publication pages and publication pages.
  Public publication pages source metadata from
  `pubs/<slug>/publication.json`.
- `page_source.py`
  Shared page-source parser used to strip non-publication front matter from
  Djot input and extract page titles after front matter. It also renders
  public publication pages from per-publication local records.
- `publication_record.py`
  Shared loader and Djot renderer for publication-local records in
  `pubs/<slug>/publication.json`.
- `scaffold_publication.py`
  Creates a new publication-local scaffold from templates plus a top-level
  draft-status stub for `mkpub.sh`.
- `render_meta.py`
  Emits `<meta>` HTML for a page by rendering non-publication front matter
  plus publication metadata from a publication-local record.
  Draft pages may intentionally emit no metadata while they remain drafts.
- `render_page_html.py`
  Emits a full HTML page using the shared render core.
  The legacy Makefile build now calls this script so page assembly lives in
  Python instead of shell pipelines.
- `render_people_refs.py`
  Prototype preview script that renders Djot people-reference definitions from
  `site/data/people.json`.
- `render_routes.py`
  Emits the deterministic route table for the preview builder to
  `state/routes-preview.json`.
- `render_site_refs.py`
  Renders the composed Djot ref bundle used by the live site build:
  generated people refs from `site/data/people.json` plus the tiny manual
  non-person remainder in `templates/REFS`.
- `validate_preview_build.py`
  Validates the preview site under `build/` for unresolved placeholders,
  broken local links, and route-driven sitemap correctness.
  It stays a thin preview-specific entrypoint on top of shared artifact
  validation helpers plus preview-only sitemap checks.
- `validate_site.py`
  Validates generated HTML for unresolved placeholders and broken local links,
  validates non-publication front matter and publication-local metadata
  sources.
  It also rejects any legacy raw `.meta` sidecars.
  It stays a thin legacy-build entrypoint on top of shared artifact
  validation helpers plus metadata-source validation.

## Conventions

- Put new executable helpers here, not in `templates/`.
- Prefer running Python helpers as modules, for example
  `python3 -m scripts.validate_site`, so imports stay package-clean and do not
  depend on `sys.path` hacks.
- Keep reusable build/data logic in small Python modules under
  `scripts/sitebuild/`.
- Keep the new preview builder route/build logic there too:
  route discovery, route validation, preview building, and preview
  validation.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
- Keep portability assumptions explicit when a script relies on a tool such as
  `wget` or `rsync`.
