# Scripts

This directory holds executable helpers for working on the website repo.

Prefer the top-level `make` targets when they exist:

- `make check`
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
  Rebuilds the site and runs structural validation checks.
- `index-now.sh`
  Submits updated pages to IndexNow and stores its local run-state under
  `state/`.
- `mkpub.sh`
  Scaffolds a new publication page and its meta file from the templates.

## Conventions

- Put new executable helpers here, not in `templates/`.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
