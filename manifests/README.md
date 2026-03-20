# Manifests

This directory holds small human-authored structured manifests that are meant
to be versioned in git.

These are not:

- prose documentation
  That belongs in `docs/`.
- executable helpers
  Those belong in `scripts/`.
- local runtime state
  That belongs in `state/`.
- large archive snapshots
  Those belong in `~/Desktop/WEBFILES/`.

## Current Manifests

- `publication-artifact-curation.tsv`
  Manual curation judgments layered on top of the observational publication
  inventory.
  Use `present` only for archive-presence heuristic misses, not to override a
  missing canonical repo file or page link.
- `publication-metadata.json`
  Structured source of truth for publication page metadata blurbs and rare
  publication-specific overrides such as share descriptions or image-path
  overrides. The build generates publication `<meta>` HTML from this manifest.
