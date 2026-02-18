# AGENTS.md

This repo is a static website generated from Djot source files. Keep changes source-first and predictable.

## Ground Rules
- Edit `*.dj` (content) and `*.meta` (head metadata), then regenerate matching `*.html` with `make`.
- Do not hand-edit generated `*.html` when a same-named `.dj` file exists.
- Top-level standalone HTML pages without `.dj` sources are `anagram.html`, `demo-naive-union-find.html`, and `sundial.html`.
- If you add `[Name][]` links, add/update the matching reference in `templates/REFS`.
- Publication assets live in `pubs/<year-conf-sys>/`, with page source in `pub-<year-conf-sys>.dj`.
- Track pending work in `ROADMAP.md` so the backlog stays centralized.

## Build And Checks
- Build all generated pages and sitemaps: `make all`
- Build one page: `make <page>.html`
- Run placeholder checks: `bash templates/check.sh`

## Before Committing
- Ensure edited `.dj` pages have regenerated `.html`.
- Ensure `sitemap.txt` and `sitemap.xml` are updated (via `make all`).
- If new TODO markers are added, add/update matching checklist entries in `ROADMAP.md`.
