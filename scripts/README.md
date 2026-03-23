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
  It now discovers publications from `pubs/<slug>/publication.json` instead of
  top-level stubs, and emits canonical publication page paths as
  `pubs/<slug>/`.
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
  temporary top-level legacy stub `pub-<slug>.dj` when the current configured
  page source root is still the repo root.
- `page_metadata.py`
  Shared metadata helpers for generated page metadata and metadata source
  validation across both public non-publication pages and publication pages.
  Public publication pages source metadata from
  `pubs/<slug>/publication.json`.
- `page_source.py`
  Shared page-source parser used to strip non-publication front matter from
  Djot input and extract page titles after front matter. It also renders
  public publication pages from per-publication local records, with
  publication-local draft status from `pubs/<slug>/publication.json`.
- `publication_record.py`
  Shared loader and Djot renderer for publication-local records in
  `pubs/<slug>/publication.json`.
- `scaffold_publication.py`
  Creates a new draft publication-local scaffold from templates plus the
  temporary legacy stub used by `mkpub.sh`.
  The default is now layout-aware: root-layout configs create the stub, while
  non-root page-source layouts default to bundle-only scaffolds unless a legacy
  stub is requested explicitly.
- `render_meta.py`
  Emits `<meta>` HTML for a page by rendering non-publication front matter
  plus publication metadata from a publication-local record.
  Draft pages may intentionally emit no metadata while they remain drafts.
- `render_page_html.py`
  Emits a full HTML page using the shared render core.
  The legacy Makefile build now calls this script so page assembly lives in
  Python instead of shell pipelines.
  During the transition it also rewrites canonical publication links like
  `pubs/<slug>/` back to `pub-<slug>.html` for the legacy root build only.
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
  Validates preview source invariants plus the preview site under `build/`
  for unresolved placeholders, broken local links, and route-driven sitemap
  correctness.
  It stays a thin preview-specific entrypoint on top of shared source
  validation, shared artifact validation, preview-only sitemap checks, and the
  temporary publication-stub bridge check that remains during the transition.
- `validate_publication_sources.py`
  Validates publication-local source invariants that must stay true while the
  legacy root build and temporary publication stubs still coexist.
- `validate_site.py`
  Validates generated HTML for unresolved placeholders and broken local links,
  validates canonical source metadata, and enforces the temporary
  publication-stub bridge invariants needed by the legacy root build.
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
