# Current Root Layout

This document records the current root-level layout while the repo still
serves as both the authored source tree and the live GitHub Pages site.

It is intentionally conservative: it explains the present structure and the
rules we should follow until a later explicit source/build/deploy migration.

## Goals

- Make the flat root navigable and interpretable.
- Distinguish authored files from intentionally tracked generated outputs.
- Make it clear which new files should avoid landing at the top level.

## Top-Level Directories

- `build/`
  Gitignored route-aware preview output from the new Python preview builder.
- `docs/`
  Human-authored policy, specs, and campaign notes.
- `img/`
  Shared site images that are not publication-specific.
- `manifests/`
  Small versioned structured manifests.
- `pubs/`
  Repo-hosted publication artifacts served directly by the site.
- `scripts/`
  Executable maintenance helpers.
- `site/`
  Staged next-architecture source area for structured site data and related
  redesign prototypes.
- `state/`
  Local generated/runtime state and repo-local previews.
- `templates/`
  Non-executable build and scaffolding inputs.
- `tests/`
  Focused unit tests for the new route/data/build modules.

## Top-Level File Classes

### Authored Page Sources

Top-level `*.dj` files are authored page sources.

- Their page title comes from the first non-empty level-1 heading after any
  optional front matter.
- Public non-publication page metadata is currently sourced from YAML front
  matter in `*.dj`.
- Public publication page metadata is currently sourced from
  `pubs/<slug>/publication.json`.
- For public publication pages, the top-level `pub-<slug>.dj` file
  should stay a minimal transition stub/build anchor rather than a second full
  page body.
- Draft pages may temporarily omit metadata while they remain drafts.
- A source file whose contents include a `# DRAFT` heading is treated as a
  draft page.

### Tracked Generated Public Outputs

Top-level `*.html` files generated from non-draft `*.dj` files are
intentionally tracked in git today.

This is a current-state policy, not an endorsement of the forever design:
these generated outputs are tracked because the repo root is still the live
site served by GitHub Pages.

Tracked generated public outputs currently include:

- generated `*.html` for public pages
- `404.html`
- `sitemap.txt`
- `sitemap.xml`

`404.html` is tracked as a public page but intentionally excluded from the
sitemaps.

### Authored Static Root Files

Some top-level files are authored static assets rather than generated outputs.

Current examples include:

- authored static HTML pages such as `anagram.html`,
  `demo-naive-union-find.html`, and `sundial.html`
- site configuration such as `CNAME` and `robots.txt`
- shared frontend assets such as `style.css` and `zip-longitude.js`
- site verification files such as `9ca38421ba63499eaa1e9c16bfe7be4c.txt`
- repo support files such as `Makefile`, `README.md`, and `TODO.md`

## Root-Level Rules For Now

- New human-authored support material should normally go under `docs/`,
  `scripts/`, `manifests/`, `state/`, or `templates/`, not at the repo root.
- New generated previews, reports, and runtime state should go under `state/`,
  not at the repo root.
- Route-aware preview output should go under `build/`, not at the repo root.
- Draft `*.dj` pages should not have tracked `*.html` outputs.
- Public non-draft `*.dj` pages should continue to have tracked `*.html`
  outputs until the later build/deploy migration happens.
- A top-level `*.html` file without a matching `*.dj` should be treated as an
  intentional authored static page and kept rare.

## Long-Term Direction

This policy is meant to stabilize the current layout, not freeze it forever.

The planned next structural campaign is documented in
`docs/plans/repo-layout.md` and should eventually make the source/build/deploy
split explicit instead of relying on a live served repo root.
