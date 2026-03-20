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
  Scaffolds a new publication page directory and adds a placeholder entry to
  `manifests/publication-metadata.json`. It currently assumes BSD/macOS
  `sed -i ''`.
- `add_publication_metadata.py`
  Adds a new placeholder entry to `manifests/publication-metadata.json` for
  `mkpub.sh` and other structured metadata workflows.
- `page_metadata.py`
  Shared metadata helpers for generated page metadata and metadata source
  validation across both public non-publication pages and publication pages.
- `render_meta.py`
  Emits `<meta>` HTML for a page by rendering generated publication metadata
  or non-publication page metadata. Draft pages may intentionally emit no
  metadata while they remain drafts.
- `validate_site.py`
  Validates generated HTML for unresolved placeholders and broken local links,
  validates `manifests/page-metadata.json` and
  `manifests/publication-metadata.json`.
  It also rejects any legacy raw `.meta` sidecars.

## Conventions

- Put new executable helpers here, not in `templates/`.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
- Keep portability assumptions explicit when a script relies on a tool such as
  `wget`, `rsync`, or BSD/macOS `sed`.
