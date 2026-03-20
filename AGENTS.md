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
- Edit `*.dj` (content) first. For head metadata, edit legacy `*.meta` files
  for non-publication pages and `manifests/publication-metadata.json` for
  publication pages. Then regenerate matching `*.html` with `make`.
- Do not hand-edit generated `*.html` when a same-named `.dj` file exists.
- Top-level standalone HTML pages without `.dj` sources are `anagram.html`, `demo-naive-union-find.html`, and `sundial.html`.
- If you add `[Name][]` links, add/update the matching reference in `templates/REFS`.
- Publication assets live in `pubs/<year-conf-sys>/`, with page source in `pub-<year-conf-sys>.dj`.
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
