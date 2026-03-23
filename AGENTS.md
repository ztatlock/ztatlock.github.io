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
  publication-local `pubs/<slug>/publication.json` for public publication
  pages.
  Draft pages may omit metadata while they remain drafts.
  Then regenerate matching `*.html` with `make`.
- Do not hand-edit generated `*.html` when a same-named `.dj` file exists.
- Top-level standalone HTML pages without `.dj` sources are `anagram.html`, `demo-naive-union-find.html`, and `sundial.html`.
- If you add a person reference link like `[Name][]`, add/update the matching
  entry in `site/data/people.json`.
  Keep `templates/REFS` only for the tiny non-person manual remainder.
- Publication assets and migrated publication-local records live in
  `pubs/<year-conf-sys>/`.
  For public publication pages, top-level `pub-<year-conf-sys>.dj` files should
  stay minimal temporary legacy-build stubs; the preview engine now treats
  `pubs/<slug>/publication.json` as the source of truth for publication
  existence, status, body, and metadata.
- Authored publication page links in Djot should use `pubs/<slug>/`, not
  `pub-<slug>.html`.
  The legacy root build rewrites those canonical links temporarily while the
  transition remains in progress.
- Track actionable backlog items in `ROADMAP.md`.
- Keep broader structural plans and design notes in `TODO.md` and `docs/plans/`.

## Build And Checks
- Build all generated pages and sitemaps: `make all`
- Build one page: `make <page>.html`
- Build the route-aware preview site: `make build-preview`
- Validate the route-aware preview site: `make check-preview`
- Run focused unit tests for route/data/build helpers: `make test`
- Check local prerequisites and assumptions: `make env-check`
- Run validation checks: `make check`

## Before Committing
- Ensure edited `.dj` pages have regenerated `.html`.
- Ensure `sitemap.txt` and `sitemap.xml` are updated (via `make all`).
- Run `make check`.
- If new TODO markers are added, add/update matching checklist entries in `ROADMAP.md`.
