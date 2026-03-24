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

- Follow the structured-content campaign sequence in
  `docs/plans/structured-content-roadmap.md`:
  service likely next, with teaching homepage/CV reuse, publication artifact
  enrichment, students CV reuse, and later collaborators/funding/CV/news work
  only where structured data clearly earns its keep.
- Keep the new `site/data/students.json` model small and canonical, and defer
  richer student follow-ons such as advising dates and student-to-publication
  linkage until a later slice clearly needs them.
- Keep the public students wrapper at `site/students/index.dj` with canonical
  `/students/`, and treat CV reuse as one likely follow-on rather than
  reopening the route/wrapper decision prematurely.
- Keep the teaching campaign shared-data-first:
  canonical records in `site/data/teaching.json`, a thin public teaching
  wrapper at `site/teaching/index.dj`, and later homepage/CV renderers over
  the same records.
- Keep publication-local facts in `site/pubs/<slug>/publication.json`, keep
  the `site/pubs/index.dj` wrapper hand-authored, and treat later publication
  work as artifact enrichment or downstream reuse rather than a return to
  hand-maintained repeated index entries.
- Introduce small shared data models only for cross-page facts that are
  actually reused, while keeping prose near prose and publication-local facts
  near publication bundles.
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
