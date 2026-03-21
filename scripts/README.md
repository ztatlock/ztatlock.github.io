# Scripts

This directory holds executable helpers for working on the website repo.

Prefer the top-level `make` targets when they exist:

- `make check`
- `make env-check`
- `make validate-site`
- `make inventory`
- `make inventory-webfiles`
- `make mkpub YCF=YEAR-CONF-SYS`
- `make index-now`

## Current Scripts

- `build_pub_inventory.py`
  Builds the publication-artifact inventory by merging filesystem observation
  with `manifests/publication-artifact-curation.tsv`.
  `make inventory` writes a repo-local preview under `state/inventory/`.
  `make inventory-webfiles` refreshes the canonical archive copy under
  `~/Desktop/WEBFILES/inventory/`.
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
  Djot input and extract page titles after front matter. It also supports the
  current publication-record transition by rendering migrated publication
  pages from per-publication local records.
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
- `validate_site.py`
  Validates generated HTML for unresolved placeholders and broken local links,
  validates non-publication front matter and publication-local metadata
  sources.
  It also rejects any legacy raw `.meta` sidecars.

## Conventions

- Put new executable helpers here, not in `templates/`.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
- Keep portability assumptions explicit when a script relies on a tool such as
  `wget` or `rsync`.
