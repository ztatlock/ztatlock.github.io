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
  Legacy publication metadata fallback retained temporarily during transition
  cleanup.
  It is currently empty because all public detailed publication pages now
  source metadata from `pubs/<slug>/publication.json`.
