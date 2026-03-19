# Docs

This directory is the home for human-authored repository documentation that is
meant to be read, maintained, and extended over time.

## Layout

- `policy/`
  Long-lived policy and specification documents.
- `plans/`
  Active work notes and resumable campaign docs.

## What Belongs Here

- storage/linking policy
- repository layout decisions
- work-in-progress campaign notes
- future migration plans

## What Does Not Belong Here

- executable helpers
  These belong in `scripts/`.
- versioned structured manifests
  These belong in `manifests/`.
- page/build template inputs
  These belong in `templates/`.
- local generated/runtime state
  This belongs in `state/`.
- generated state snapshots
  These generally should not live in git unless we explicitly decide they are
  versioned artifacts.

## Current Conventions

- Human-authored policy/spec docs should go under `docs/policy/`.
- Resumable work notes should go under `docs/plans/`.
- Executable utilities should go under `scripts/`.
- Versioned structured manifests should go under `manifests/`.
- `templates/` should hold non-executable site template assets.
- Local generated/runtime state should go under `state/` and should usually be
  ignored by git.
- Repo-local generated previews can live under `state/`.
- Canonical generated archive-state snapshots should live outside the repo in
  `~/Desktop/WEBFILES/inventory/`.

## Current Docs

- `policy/publication-artifacts.md`
  Publication storage and linking policy.
- `policy/root-layout.md`
  Current root-level file classes and tracked generated outputs.
- `plans/publication-artifact-followup.md`
  Resume point for the current publication-artifact cleanup.
- `plans/repo-layout.md`
  Staged direction for making the repo less flat and more modular.

## Near-Term Cleanup

- Keep `templates/HEAD.*`, `templates/FOOT`, `templates/REFS`,
  `templates/meta.html`, and `templates/pub.dj` in `templates/`.
- Keep `docs/policy/root-layout.md` current as the root-level file mix changes.
- Revisit whether any versioned generated artifacts deserve a separate home
  beyond `manifests/`.
