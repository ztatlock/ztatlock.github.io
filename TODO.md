# TODO

## Near Term

- Keep the current root-level file classes documented in
  `docs/policy/root-layout.md`.
- Keep small self-describing docs current when support directories change.
- Keep the post-cutover command surface, repo layout, and docs coherent as the
  new architecture settles.
- Trim lingering historical naming and stale migration-era assumptions when
  they no longer earn their keep.

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

- Introduce a small shared data model for cross-page facts such as people,
  talks, students, and selected CV records, while keeping prose near prose and
  publication-local facts near publication bundles.
- Reduce repeated per-page build subprocess overhead so `make build` and
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
