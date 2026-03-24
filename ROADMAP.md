# ROADMAP

Last updated: 2026-03-24.

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
- [x] Implement the slice-1 canonical advising-record model for `site/data/students.json`, including required `person_key`, ordered section/record structure, and typed detail items (`docs/plans/students-slice-1-canonical-model.md`, `site/data/students.json`, `scripts/student_record.py`).
- [x] Implement the students index-wrapper/projection slice: move the public wrapper to `site/students/index.dj`, canonicalize `/students/`, and project the repeated section bodies from `site/data/students.json` while preserving authored framing (`docs/plans/students-slice-2-index-projection.md`, `site/data/students.json`, `site/students/index.dj`).
- [x] Implement the slice-1 canonical teaching-record model for `site/data/teaching.json`, including ordered teaching groups, structured course/summer-school records, and offering/event invariants (`docs/plans/teaching-campaign.md`, `docs/plans/teaching-slice-1-canonical-model.md`, `site/data/teaching.json`, `scripts/teaching_record.py`).
- [x] Plan and implement the public teaching wrapper/projection slice so the public teaching page moves to `site/teaching/index.dj`, canonicalizes `/teaching/`, and projects repeated teaching blocks from `site/data/teaching.json` while keeping the award note and related section hand-authored (`docs/plans/teaching-campaign.md`, `site/data/teaching.json`, `site/teaching/index.dj`).
- [x] Capture the missing Marktoberdorf Summer School 2024 teaching entry during the teaching campaign backfill so the canonical teaching record is more complete than the current public teaching page (`site/data/teaching.json`, `site/pages/index.dj`, `site/pages/news.dj`, `site/pages/cv.dj`, `docs/plans/teaching-campaign.md`).
- [x] Move the public teaching wrapper to `site/teaching/index.dj`, canonicalize `/teaching/`, project the repeated public teaching blocks from `site/data/teaching.json`, and rewrite lingering `teaching.html` links to `teaching/` (`docs/plans/teaching-slice-2-index-projection.md`, `site/data/teaching.json`, `site/teaching/index.dj`, `site/pages/index.dj`).
- [ ] Add a later teaching-staffing slice for courses where Zach was the instructor, with offering-level `co_instructors` and `teaching_assistants` fields tied into `site/data/people.json`, without overloading the current `teaching_assistant` history group that records Zach's own prior TA experience (`docs/plans/teaching-campaign.md`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Plan and implement the slice-1 canonical service model in `site/data/service.json`, using flat per-year service terms with multi-group view membership so the service domain has one shared source of truth without assuming the current hand-authored section headings are the full ontology; defer homepage/CV consumer projection to later cross-cutting cleanup work (`docs/plans/service-campaign.md`, `docs/plans/service-slice-1-canonical-model.md`, `site/data/service.json`).
- [ ] Plan and implement the public service wrapper/projection slice so the service page moves to `site/service/index.dj`, canonicalizes `/service/`, and projects repeated public service blocks from `site/data/service.json` while keeping the Aggregators section hand-authored (`docs/plans/service-campaign.md`, `site/data/service.json`, `site/service/index.dj`).
- [ ] Plan and implement the students CV-projection slice so the duplicated advising sections in `site/pages/cv.dj` render from `site/data/students.json` with an intentionally more compressed view (`docs/plans/students-campaign.md`, `site/data/students.json`, `site/pages/cv.dj`).
- [ ] Decide whether the current omission of Ian Briggs from the CV visiting-students section is intentional or drift to remove during the students campaign (`site/students/index.dj`, `site/pages/cv.dj`, `docs/plans/students-campaign.md`).
- [ ] Later projection-layer cleanup: load shared student/teaching-style data once per projected page render and introduce a tiny projection registry if another projection-backed domain lands (`scripts/sitebuild/page_projection.py`).

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
