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
  Rebuilds the site in an isolated scratch copy and runs structural validation
  checks without dirtying tracked site outputs in the live repo.
- `index-now.sh`
  Submits updated pages to IndexNow and stores its local run-state under
  `state/`. It currently assumes `wget`.
- `mkpub.sh`
  Scaffolds a new publication page and its current raw HTML meta sidecar from
  the templates. It currently assumes BSD/macOS `sed -i ''`.

## Conventions

- Put new executable helpers here, not in `templates/`.
- Keep local generated/runtime state under `state/`.
- Keep larger archival state outside the repo in `~/Desktop/WEBFILES/` unless
  there is a clear reason to version it in git.
- Keep portability assumptions explicit when a script relies on a tool such as
  `wget`, `rsync`, or BSD/macOS `sed`.
