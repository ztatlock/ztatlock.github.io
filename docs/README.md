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
- `plans/page-metadata-and-ssg.md`
  Design direction for replacing raw page `*.meta` files and deciding whether
  the site should ever migrate to Jekyll or another SSG.
- `plans/metadata-source-comparison.md`
  Controlled comparison of shared manifests, page-local sidecars, and YAML
  front matter as metadata sources.
- `plans/repo-layout.md`
  Staged direction for making the repo less flat and more modular.
- `plans/build-system-route-model.md`
  Why the current flat-root build model is straining and what a minimal
  route-aware model would need to represent.
- `plans/publication-output-cutover.md`
  Focused design note on whether publication pages should move from
  root-level outputs into their own directories.
- `plans/source-build-deploy-redesign.md`
  Broader redesign direction for introducing `site/`, `build/`, and explicit
  deployment.
- `plans/site-architecture-spec.md`
  Draft concrete architecture spec for the next source/build/data/deploy
  redesign campaign.
- `plans/route-build-engine-slice-1.md`
  Initial implementation slice for the redesign: a future-oriented
  preview builder that writes to `build/` while still reading from the current
  source layout.
- `plans/route-build-engine-slice-2.md`
  Consolidation slice for collapsing duplicated rendering and metadata logic
  and adding route-driven sitemap generation for `build/`, followed by shared
  artifact-validation helpers for legacy and preview builds.
- `plans/route-build-engine-slice-3.md`
  Source-layout-awareness slice for making the preview engine read from
  configured source roots before any real source-file move into `site/`.

## Near-Term Cleanup

- Keep `templates/HEAD.*`, `templates/FOOT`, `templates/REFS`,
  `templates/pub-stub.dj`, and `templates/publication.json` in `templates/`.
- Keep `docs/policy/root-layout.md` current as the root-level file mix changes.
- Revisit whether any versioned generated artifacts deserve a separate home
  beyond `manifests/`.
