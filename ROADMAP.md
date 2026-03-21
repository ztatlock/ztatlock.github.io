# ROADMAP

Last updated: 2026-03-20.

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

- [ ] Make a publication page for each publication (migrated from legacy `TODO.md`).
- [ ] Make a talk page for each talk (migrated from legacy `TODO.md`).

## Open TODOs In Source Files

### General Site Content

- [ ] Decide what the August 2017 Neutrons news item should link to now that
  the historical project page is gone (`news.dj:117`).
- [ ] Decide what the stale Neutrons project link on the research page should
  point to until a replacement page exists (`research.dj:80`).
- [ ] Implement or remove `canon` TODO in the union-find demo (`demo-naive-union-find.html:147`).
- [ ] Refactor union-find demo state/history for easier "back" behavior (`demo-naive-union-find.html:381`).

### Publication Pages

- [ ] Fill arXiv TODO for `pub-2008-oopsla-dtar` (`pub-2008-oopsla-dtar.dj:20`).
- [ ] Decide whether `2009-pldi-pec` should expose an arXiv link and, if so, add it to the canonical publication record (`pubs/2009-pldi-pec/publication.json:10`).
- [ ] Resolve TODO-tagged project/code/arXiv items for `pub-2012-security-quark` (`pub-2012-security-quark.dj:26`, `pub-2012-security-quark.dj:27`, `pub-2012-security-quark.dj:28`).
- [ ] Fill arXiv TODOs for `pub-2019-conga-sinkingpoint` (`pub-2019-conga-sinkingpoint.dj:18`, `pub-2019-conga-sinkingpoint.dj:29`).
- [ ] Fill arXiv TODO for `pub-2021-arith-herbie` (`pub-2021-arith-herbie.dj:29`).
- [ ] Fill project TODO for `pub-2021-oopsla-ruler` (`pub-2021-oopsla-ruler.dj:34`).
- [ ] Fill arXiv TODO for `pub-2021-sff-3dp` (`pub-2021-sff-3dp.dj:33`).
- [ ] Fill talk/arXiv TODOs for `pub-2022-ecoop-cakemlfp` (`pub-2022-ecoop-cakemlfp.dj:31`, `pub-2022-ecoop-cakemlfp.dj:32`).
- [ ] Resolve TODO-tagged poster item for `pub-2022-tog-carpentry` (`pub-2022-tog-carpentry.dj:33`).
- [ ] Resolve TODO-tagged `poster` link for `pub-2023-plarch-lakeroad` (`pub-2023-plarch-lakeroad.dj:30`).
- [ ] Resolve TODO-tagged `talk` link for `pub-2023-pldi-egglog` (`pub-2023-pldi-egglog.dj:33`).
- [ ] Resolve TODO-tagged `project` link for `pub-2023-popl-babble` (`pub-2023-popl-babble.dj:30`).
- [ ] Resolve TODO-tagged `poster` link for `pub-2023-popl-babble` (`pub-2023-popl-babble.dj:31`).

### Template Placeholders (Intentional Scaffolding)

- [ ] Keep or revise template TODO placeholders for new publication scaffolds (`templates/pub-stub.dj:1`, `templates/pub-stub.dj:8`, `templates/publication.json:2`, `templates/publication.json:4`, `templates/publication.json:6`, `templates/publication.json:7`).
- [ ] Confirm required publication placeholder checks still match policy (`scripts/validate_site.py:22`).

## Known Non-TODO Follow-Ups From Review

- [x] Fix broken publication link target missing `.html` suffix (`publications.dj:620`).
- [ ] Decide whether hidden template TODO blocks in publication source files should keep shipping to production or be treated as release blockers.
