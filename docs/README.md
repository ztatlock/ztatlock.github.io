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
  These belong in `site/templates/`.
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
- `site/templates/` should hold non-executable site template assets.
- Local generated/runtime state should go under `state/` and should usually be
  ignored by git.
- Repo-local generated snapshots can live under `state/`.
- Canonical generated archive-state snapshots should live outside the repo in
  `~/Desktop/WEBFILES/inventory/`.

## Current Docs

### Current Reference Docs

- `policy/publication-artifacts.md`
  Publication storage and linking policy.
- `policy/root-layout.md`
  Current root-level layout now that authored source lives under `site/` and
  generated site output lives under `build/`.
- `plans/source-build-deploy-redesign.md`
  Big-picture redesign narrative from flat-root site to the current
  source/build split.
- `plans/site-architecture-spec.md`
  The concrete architecture spec for the current site/build/data layout.
- `plans/source-move-cutover-plan.md`
  The implemented cutover campaign that moved authored source into `site/` and
  made the route-aware build authoritative.
- `plans/publication-artifact-followup.md`
  Resume point for the current publication-artifact cleanup.

### Historical Design / Campaign Notes

- `plans/route-build-engine-slice-1.md`
  Initial route-aware builder slice before the full cutover.
- `plans/route-build-engine-slice-2.md`
  Rendering/sitemap consolidation slice.
- `plans/route-build-engine-slice-3.md`
  Source-layout-awareness slice before files moved into `site/`.
- `plans/route-build-engine-slice-4.md`
  Publication-source-model cleanup before the source move.
- `plans/route-build-engine-slice-5.md`
  Final source-move-readiness slice.
- `plans/build-system-route-model.md`
  Early route-model design note from the flat-root build era.
- `plans/publication-output-cutover.md`
  Early publication-route cutover exploration.
- `plans/repo-layout.md`
  Earlier staged repo-layout exploration.
- `plans/page-metadata-and-ssg.md`
  Metadata and SSG exploration note.
- `plans/metadata-source-comparison.md`
  Comparison of metadata-source alternatives.

## Near-Term Cleanup

- Keep `site/templates/HEAD.*`, `site/templates/FOOT`,
  `site/templates/REFS`, and `site/templates/publication.json` in
  `site/templates/`.
- Keep `docs/policy/root-layout.md` current as the root-level file mix changes.
- Revisit whether any versioned generated artifacts deserve a separate home
  beyond `manifests/`.
