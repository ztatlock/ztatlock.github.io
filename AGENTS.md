# AGENTS.md

This repo is a static website generated from Djot source files. Keep changes source-first and predictable.

## Ground Rules
- This repo is edited from multiple machines. At the start of a session, run
  `git status` and, if the tree is clean, `git pull --ff-only` before making
  changes.
- If the tree is dirty at the start of a session, do not pull until the state
  is understood and resolved explicitly.
- After each coherent commit, `git push` so other machines and future sessions
  do not drift.
- Edit `*.dj` (content) first. For head metadata, edit
  YAML front matter for public non-publication pages and
  publication-local `pubs/<slug>/publication.json` when a page uses the new
  local-record path, otherwise `manifests/publication-metadata.json`.
  Draft pages may omit metadata while they remain drafts.
  Then regenerate matching `*.html` with `make`.
- Do not hand-edit generated `*.html` when a same-named `.dj` file exists.
- Top-level standalone HTML pages without `.dj` sources are `anagram.html`, `demo-naive-union-find.html`, and `sundial.html`.
- If you add `[Name][]` links, add/update the matching reference in `templates/REFS`.
- Publication assets and migrated publication-local records live in
  `pubs/<year-conf-sys>/`.
  Top-level `pub-<year-conf-sys>.dj` files currently remain as build anchors
  and draft/public status stubs during the transition.
- Track actionable backlog items in `ROADMAP.md`.
- Keep broader structural plans and design notes in `TODO.md` and `docs/plans/`.

## Build And Checks
- Build all generated pages and sitemaps: `make all`
- Build one page: `make <page>.html`
- Check local prerequisites and assumptions: `make env-check`
- Run validation checks: `make check`

## Before Committing
- Ensure edited `.dj` pages have regenerated `.html`.
- Ensure `sitemap.txt` and `sitemap.xml` are updated (via `make all`).
- If new TODO markers are added, add/update matching checklist entries in `ROADMAP.md`.
