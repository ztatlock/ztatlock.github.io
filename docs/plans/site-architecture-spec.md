# Site Architecture Spec

Status: Draft 1

This note is the first concrete architecture spec for the next major website
redesign campaign.

It builds on the earlier design notes:

- [build-system-route-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/build-system-route-model.md)
- [publication-output-cutover.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-output-cutover.md)
- [source-build-deploy-redesign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/source-build-deploy-redesign.md)

The goal here is not to finalize every detail immediately.
The goal is to make the target architecture concrete enough that we can judge
it as a system rather than as a collection of individual ideas.

## Design Priorities

The redesign should optimize for:

- dead-simple editing workflows
- rational layout
- explicit route awareness
- hardened single sources of truth
- minimal moving parts
- easy local understanding
- easy extension without hacks
- reliability through strong validation and small tests

## Architecture Commitments

These are explicit commitments, not loose aspirations:

- pure Python modules with narrow responsibilities
- explicit schemas and invariants
- small unit tests for route and data resolution
- thin Make commands on top

This is the intended engineering style for the redesign.

## Target Top-Level Repo Shape

The repo should eventually look roughly like:

```text
repo/
  docs/
  scripts/
  manifests/
  state/
  tests/
  site/
    pages/
    pubs/
    data/
    static/
    templates/
  build/
  Makefile
  README.md
```

Where:

- `site/` is the complete website source root
- `build/` is the generated deployable site
- repo support material stays outside `site/`

## `site/` Layout

### `site/pages/`

Ordinary authored Djot pages.

Examples:

- `site/pages/index.dj`
- `site/pages/about.dj`
- `site/pages/publications.dj`
- `site/pages/news.dj`

These pages remain prose-first and should keep YAML front matter for page-local
metadata.

### `site/pubs/`

Publication-local bundles.

Each publication directory remains the canonical home for:

- `publication.json`
- abstract
- BibTeX
- canonical local assets
- optional `extra.dj`

Example:

```text
site/pubs/2024-asplos-lakeroad/
  publication.json
  2024-asplos-lakeroad-abstract.md
  2024-asplos-lakeroad.bib
  2024-asplos-lakeroad.pdf
  2024-asplos-lakeroad-absimg.png
  2024-asplos-lakeroad-meta.png
```

### `site/data/`

Cross-page structured data for facts that should have a single source of
truth.

This directory should stay small and disciplined.

Likely first-cut records:

- `site/data/people.json`
- `site/data/talks.json`
- `site/data/students.json`
- `site/data/cv/`

The rule is:

- if a fact appears in many places, consider structured data
- if it is mostly local to one page or publication, keep it local
- prose should stay in Djot, not in JSON

### `site/static/`

Files copied into the build output unchanged.

Examples:

- `CNAME`
- `robots.txt`
- `style.css`
- `zip-longitude.js`
- `img/`
- static standalone HTML pages
- verification files

### `site/templates/`

Non-public build inputs.

Examples:

- page head/body fragments
- shared references
- scaffolding templates

Nothing in `site/templates/` should be treated as a public route.

## `build/` Layout

The build output should mirror the final public site:

```text
build/
  index.html
  about.html
  publications.html
  pubs/
    2024-asplos-lakeroad/
      index.html
      2024-asplos-lakeroad.pdf
      ...
  img/
  CNAME
  robots.txt
  sitemap.txt
  sitemap.xml
```

This is the artifact that should eventually be deployed.

## Route Model

The build system should have one explicit route model.

At minimum, each route should know:

- `kind`
- `key`
- `source inputs`
- `output path`
- `public url`
- `canonical url`
- `is_draft`

The route model should be computed in one place and consumed by:

- page rendering
- metadata rendering
- sitemap generation
- validation
- build target selection

## First-Cut Route Classes

### Ordinary Page Route

- source: `site/pages/<stem>.dj`
- output: `build/<stem>.html`
- public URL: `/<stem>.html`, except `index -> /`
- canonical URL: `https://ztatlock.net/<...>`
- draft status: `# DRAFT` in the Djot source

### Publication Page Route

- source: `site/pubs/<slug>/publication.json` and canonical local files
- output: `build/pubs/<slug>/index.html`
- public URL: `/pubs/<slug>/`
- canonical URL: `https://ztatlock.net/pubs/<slug>/`
- draft status: publication-local, likely `draft: true`

### Static File Route

- source: `site/static/...`
- output: `build/...`
- public URL: path-relative to `site/static/`
- canonical URL: only where relevant

Static files are copy routes, not rendered page routes.

## Structured Data Model

The build system should treat shared structured data separately from routes.

That means:

- route resolution decides where pages live
- data resolution decides what shared facts pages can render

These are related but distinct layers.

## First-Cut Shared Data Domains

### People Registry

This should be the highest-priority shared data domain.

Suggested fields:

- stable key
- name
- aliases
- URL

This registry should eventually feed:

- collaborator/coauthor links
- publication author rendering
- talk speaker rendering
- student page links
- the composed site-wide refs bundle, whether or not the future redesign keeps
  the same file layout

Historical audit note:

- before the split, `templates/REFS` had 162 entries and 160 unique labels
- only a tiny handful were clearly non-person references
- there were at least 2 duplicate person entries

That audit justified the split now live in the current repo:

- generated people references from `site/data/people.json`
- a very small hand-maintained remainder for non-person references in
  `templates/REFS`

### Talks

Likely useful if the talks page is generated from shared records.

But this should only be introduced once we know the page really benefits from
it.

### Students

Likely useful because student facts are cross-cutting and structured.

### CV Records

Likely useful for sections like:

- positions
- education
- awards
- service
- teaching

But the CV should not become one giant JSON blob if a few smaller structured
sections are cleaner.

## Build Phases

The Python build engine should conceptually run in these phases:

1. load source configuration
2. load structured data
3. validate structured data
4. resolve shared references
5. compute the route table
6. build rendered pages
7. copy static files
8. generate sitemaps
9. run validation on the built output

These phases should be explicit in code, even if they are implemented with
small helper functions.

## Python Module Boundaries

The implementation should prefer small focused modules, for example:

- `site_config.py`
- `data_loader.py`
- `people_registry.py`
- `route_model.py`
- `page_loader.py`
- `publication_renderer.py`
- `page_renderer.py`
- `meta_renderer.py`
- `static_copy.py`
- `sitemap.py`
- `validator.py`

The exact filenames can change, but the principle should not:

- one module, one clear responsibility

## Schemas And Invariants

The redesign should validate structured data explicitly.

Examples of invariants:

- every person key is unique
- aliases resolve unambiguously
- every route has exactly one output path
- every route has exactly one canonical URL
- public publication records satisfy the canonical asset contract
- copied static routes do not collide with rendered routes

These invariants should be documented and tested.

## Testing Strategy

We should not rely only on full-site builds for confidence.

The redesign should add small unit tests for:

- route derivation
- canonical URL computation
- publication route generation
- ordinary route generation
- draft filtering
- people alias resolution
- schema validation failures
- output-path collision detection

Then keep a smaller number of higher-level integration checks for:

- full build
- sitemap correctness
- broken local links
- publication asset validation

## Make Command Surface

Make should remain the public command surface, but stay thin.

Likely commands:

- `make build`
- `make check`
- `make clean`
- `make env-check`
- `make serve`
- `make page PAGE=index`
- `make route ROUTE=pubs/2024-asplos-lakeroad`

The exact names can still change, but the important rule is:

- Make delegates
- Python decides

## Deployment Model

The target deployment model should be:

- build into `build/`
- deploy `build/` via GitHub Pages Actions

That means:

- source and build artifacts stop being mixed
- generated HTML no longer needs to be committed
- Pages deployment becomes explicit and reproducible

## Migration Shape

This should be a staged migration, not a big-bang rewrite.

### Phase 1

Freeze the architecture and invariants.

### Phase 2

Build the new Python route/data/build engine against the current repo, but
target the future output layout immediately:

- keep current source locations for now
- build a real preview site into `build/`
- use the future publication output shape in that preview build
- validate the route model and preview build together
- then collapse duplicated build logic by extracting:
  - one shared render core
    - route-aware metadata rendering
    - page HTML document assembly
  - route-driven sitemap generation for `build/`

### Phase 3

Finalize the new engine's publication source model before any real source move:

- publication discovery from `site/pubs/*/publication.json`
- publication-local draft status
- no architectural dependence on top-level publication stubs
- no redirect/compatibility layer for old `pub-*.html` URLs

### Phase 4

Finish source-move readiness in the new engine before moving real files:

- make the new path authoritative for source validation
- make `static_source_dir` behave like a true recursive static copy tree
- keep only sharply isolated bridge behavior for the current repo-root layout

### Phase 5

Move source into `site/` once the new engine is ready enough that the move is
mostly mechanical.
This phase must also include command-surface cutover or retirement of the
legacy root-only build/check path.

Phase 5 is not complete unless it also does the following:

- flip the default source roots in the new engine from the repo root to:
  - `site/pages/`
  - `site/pubs/`
  - `site/static/`
  - `site/templates/`
- cut over or retire the legacy root-only commands that still define the old
  architecture:
  - `make all`
  - `make <page>.html`
  - `make check`
- remove preview-validator dependence on the temporary publication-stub bridge
  once top-level `pub-*.dj` stubs are gone
- remove the remaining legacy-only reverse-rewrite bridge for canonical
  publication links in the root build path
- stop defaulting new publication scaffolds to create legacy stubs
- flip contributor-facing docs so the normal workflow describes the new
  authoritative build/check path rather than the legacy root build

Immediate cleanup after Phase 5, if not folded into the phase itself, should
delete the remaining bridge-only branches:

- repo-root static-route bridge behavior
- publication-stub bridge validation
- legacy publication-link reverse-rewrite glue
- legacy-stub scaffolding defaults

### Phase 6

Add GitHub Pages workflow for deploying `build/`.

### Phase 7

Remove old committed generated outputs, publication stubs, and the legacy
root-served build path.

### Phase 8

Clean up remaining transitional assumptions and docs.

## Explicit Non-Goals For The First Implementation

- solving every possible future page class immediately
- inventing a giant central site database
- replacing Djot
- migrating to Jekyll
- building a plugin system

## Open Questions

These still need deliberate decisions:

1. whether the people registry should stay at the current minimal
   `name` / `url` / `aliases` schema or grow additional fields later
2. exact Make command names for building one page/route
3. whether some CV data should remain prose-first longer
4. whether copied static standalone HTML pages should stay under `static/` or
   get their own small convention
5. whether one focused static-source cleanup slice should happen before the
   real source move, or whether that cleanup should land as part of the move

## Recommendation

This spec points toward a redesign that is:

- route-aware
- source/build separated
- structured where structure pays off
- still plain, explicit, and homegrown

That is the direction I would currently recommend pursuing.
