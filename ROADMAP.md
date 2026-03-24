# ROADMAP

Last updated: 2026-03-23.

This is the working checklist for maintenance and collaboration.
Use this file as the actionable backlog for concrete repo tasks.
Use `TODO.md` and `docs/plans/` for broader strategy and longer-horizon design
notes.

## How To Use This File

- Add new work as unchecked items (`- [ ]`).
- Mark done work as checked (`- [x]`) and keep file references.
- When a source file keeps a `TODO` marker intentionally, track it here too.

## Collaboration Foundation

- [x] Add minimal collaboration guide (`AGENTS.md`).
- [x] Update README with real workflow and structure (`README.md`).
- [x] Document multi-machine pull/push workflow in `AGENTS.md` and `README.md`.

## Migrated Backlog From TODO.md

- [x] Establish the canonical publication-bundle pattern under `site/pubs/` for publication pages that have local records today.
- [ ] Decide which talks actually need talk-local detail pages instead of index-only bundles (`site/talks/`, `site/pages/talk-2023-05-egg-uiuc.dj`).
- [ ] Define the canonical advising-record schema and projection policy for `site/data/students.json`, `site/pages/students.dj`, and the duplicated students sections in `site/pages/cv.dj`.

## Open TODOs In Source Files

### General Site Content

- [ ] Decide what the August 2017 Neutrons news item should link to now that
  the historical project page is gone (`site/pages/news.dj`).
- [ ] Decide what the stale Neutrons project link on the research page should
  point to until a replacement page exists (`site/pages/research.dj`).
- [ ] Implement or remove `canon` TODO in the union-find demo (`site/static/demo-naive-union-find.html`).
- [ ] Refactor union-find demo state/history for easier "back" behavior (`site/static/demo-naive-union-find.html`).

### Publication Pages

- [ ] Decide whether `2008-oopsla-dtar` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2008-oopsla-dtar/publication.json`).
- [ ] Decide whether `2009-pldi-pec` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2009-pldi-pec/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose a code link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2019-conga-sinkingpoint` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2019-conga-sinkingpoint/publication.json`).
- [ ] Decide whether `2021-arith-herbie` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2021-arith-herbie/publication.json`).
- [ ] Decide whether `2021-oopsla-ruler` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2021-oopsla-ruler/publication.json`).
- [ ] Decide whether `2021-sff-3dp` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2021-sff-3dp/publication.json`).
- [ ] Decide whether `2022-ecoop-cakemlfp` should expose a public talk link and, if so, add it to the canonical publication record (`site/pubs/2022-ecoop-cakemlfp/publication.json`).
- [ ] Decide whether `2022-ecoop-cakemlfp` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2022-ecoop-cakemlfp/publication.json`).
- [ ] Decide whether `2022-tog-carpentry` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2022-tog-carpentry/publication.json`).
- [ ] Decide whether `2023-plarch-lakeroad` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2023-plarch-lakeroad/publication.json`).
- [ ] Decide whether `2023-pldi-egglog` should expose a public talk link and, if so, add it to the canonical publication record (`site/pubs/2023-pldi-egglog/publication.json`).
- [ ] Decide whether `2023-popl-babble` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2023-popl-babble/publication.json`).
- [ ] Decide whether `2023-popl-babble` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2023-popl-babble/publication.json`).

### Template Placeholders (Intentional Scaffolding)

- [ ] Keep or revise placeholder values for new publication scaffolds (`site/templates/publication.json`).
- [ ] Confirm unresolved placeholder policy still matches the authoritative validator (`scripts/validate_build.py`, `scripts/sitebuild/artifact_validate.py`).

## Known Non-TODO Follow-Ups From Review

- [x] Canonicalize authored publication links to `pubs/<slug>/` paths (`site/pages/index.dj`, `site/pages/news.dj`, `site/pages/publications.dj`).
- [x] Mirror the publications collection under `site/pubs/index.dj` with canonical `/pubs/`, and update publication detail backlinks accordingly (`site/pubs/index.dj`, `scripts/publication_record.py`, `docs/plans/structured-content-roadmap.md`).
- [ ] Decide whether unresolved scaffold placeholders in draft publication records should remain acceptable until publication (`site/templates/publication.json`, `scripts/validate_build.py`, `scripts/sitebuild/artifact_validate.py`).
