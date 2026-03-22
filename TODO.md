# TODO

## Near Term

- Keep improving repo structure and discoverability without doing a risky
  source/build/deploy migration yet.
- Keep the current root-level file classes documented in
  `docs/policy/root-layout.md`.
- Keep small self-describing docs current when support directories change.
- Keep the current root-served production build and the route-aware preview
  build coherent while the broader source/build/deploy migration is still in
  progress.
- Revisit which generated outputs are intentionally tracked in git and which
  eventually deserve a better home than the repo root.

## Publication Artifacts

- Do not try to grind through full publication-artifact curation in one pass.
- Chip away at `manifests/publication-artifact-curation.tsv` incrementally over
  time.
- Start with the highest-signal cases:
  - `2023-plarch-lakeroad` missing repo meta image
  - public talk links without `WEBFILES` backups
  - `WEBFILES` talk backups without corresponding page talk links
- Treat missing slide PDFs and poster PDFs as cleanup work, not as a same-day
  fire drill, until manually curated.

## Future Campaigns

- Make the authored-source vs built-output split explicit.
- Move toward an intentional route-aware source/build/deploy pipeline instead
  of serving the repo root directly.
- Introduce a small shared data model for cross-page facts such as people,
  talks, students, and selected CV records, while keeping prose near prose and
  publication-local facts near publication bundles.
- Reduce repeated per-page build subprocess overhead so `make all` and
  `make check` stay fast enough to run routinely, likely by consolidating
  title/body/meta work into fewer Python entry points and revisiting safe
  parallelism.
- Keep the redesign implementation disciplined:
  pure Python modules with narrow responsibilities, explicit
  schemas/invariants, small unit tests for route/data resolution, and thin
  Make commands on top.
- Revisit whether the eventual source/build/deploy split should stay custom or
  migrate to Jekyll or another more conventional SSG.
- Create and integrate a replacement first-party Neutrons project page, since
  the historical external site is gone.
- Search older website copies and personal archives for missing publication
  artifacts.
