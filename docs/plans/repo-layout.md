# Repository Layout Plan

This note captures the intended direction for making the repo less flat and
more interpretable without forcing a risky large-bang reorganization.

## Goals

- Separate human-authored documentation from executable helpers.
- Separate template assets from scripts.
- Make generated state and archival state explicit.
- Move gradually toward a clearer authored-source -> build -> deploy model.

## Current Pain Points

- The repo root is extremely flat.
- Authored sources and generated outputs live together.
- `templates/` currently mixes template assets and executable shell helpers.
- Documentation and policy notes have no obvious home.
- Some important state snapshots live outside the repo, but that convention was
  not previously documented.

## Proposed Boundaries

- `docs/`
  Human-authored policy, specs, plans, and migration notes.
- `manifests/`
  Small human-authored structured manifests that should be versioned in git.
- `scripts/`
  Executable utilities, validators, migration helpers, and inventory builders.
- `state/`
  Local repo-adjacent generated/runtime state that should not normally be
  committed.
- `templates/`
  Non-executable page/build template assets only.
- `pubs/`
  Repo-hosted publication artifacts that the site serves directly.
- `~/Desktop/WEBFILES/`
  Large archival backups and generated inventory/state snapshots that should
  not normally be committed to git.

## Staged Direction

### Stage 1

- Keep the current page-source layout at the top level.
- Put policy/spec docs under `docs/`.
- Put executable helpers under `scripts/`.
- Stop adding new shell helpers to `templates/`.

### Stage 2

- Decide whether any repo-versioned generated artifacts belong in `manifests/`
  or deserve a separate home.
- Document which generated outputs are intentionally tracked and which are not.

### Stage 3

- Consider separating authored content from built output more aggressively.
- Possible future shape:
  - authored sources in `content/` or `pages/`
  - generated site output in `build/` or `dist/`
  - deployment from built artifacts rather than serving the repo root directly

That future step should be treated as an explicit migration, not an incidental
cleanup.

## Next Structural Campaign

The next likely structural campaign after the current morning cleanup is:

- make the authored-source vs built-output split explicit
- move toward an intentional build/deploy pipeline instead of treating the repo
  root as both source tree and live site

That work is intentionally deferred for a later dedicated pass.

## Guidance For Now

- Add new human-readable policy/spec docs under `docs/`.
- Add new versioned structured manifests under `manifests/`.
- Add new executable helpers under `scripts/`.
- Put local generated/runtime state under `state/`.
- Treat `templates/` as data, not as the default home for new scripts.
- Keep canonical large archival state in `WEBFILES` unless there is a clear
  reason to version it in git.
