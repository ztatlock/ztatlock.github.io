# AGENTS.md

This repo is a static website generated from Djot source files. Keep changes
source-first and predictable.

For the broader working rhythm and design philosophy, read
`docs/policy/working-style.md`.
The short version:

- keep designs simple, explicit, and narrow
- work campaign-by-campaign and slice-by-slice
- follow the rhythm: review, plan, reflect, implement, verify, sober review,
  align docs, stop and reassess
- prefer small canonical sources of truth plus thin wrappers over duplicated
  hand-maintained facts
- do not introduce clever abstractions unless they have clearly earned their
  keep

## Ground Rules

- This repo is edited from multiple machines. At the start of a session, run
  `git status` and, if the tree is clean, `git pull --ff-only` before making
  changes.
- If the tree is dirty at the start of a session, do not pull until the state
  is understood and resolved explicitly.
- After each coherent commit, `git push` so other machines and future sessions
  do not drift.
- Edit authored site source under `site/`, not at the repo root.
- For public non-publication pages, edit YAML front matter in
  `site/pages/*.dj`.
- For public publication pages, edit
  `site/pubs/<slug>/publication.json`.
- Draft pages may omit metadata while they remain drafts.
- Do not hand-edit generated files under `build/`.
- Standalone authored static HTML pages live under `site/static/`.
- If you add a person reference link like `[Name][]`, add or update the
  matching entry in `site/data/people.json`.
  Keep `site/templates/REFS` only for the tiny non-person manual remainder.
- Publication assets and publication-local records live in
  `site/pubs/<slug>/`.
- Authored publication page links in Djot should use `pubs/<slug>/`, not
  `pub-<slug>.html`.
- Track actionable backlog items in `ROADMAP.md`.
- Keep broader structural plans and design notes in `TODO.md` and `docs/plans/`.

## Build And Checks

- Build the authoritative site: `make build`
- Validate authoritative source plus the built site: `make check`
- Render the authoritative route table: `make routes`
- Auto-discover and run focused unit tests under `tests/`: `make test`
- Check local prerequisites and assumptions: `make env-check`
- Build publication inventory snapshots: `make inventory`

## Before Committing

- Ensure the authoritative build/check path passes:
  - `make build`
  - `make check`
- Ensure the changed authored source lives under `site/`.
- If new TODO markers are added, add/update matching checklist entries in
  `ROADMAP.md`.
