# Route/Build Engine Slice 2

Status: Initial implementation live in repo

This note defines the next implementation slice after the initial
future-oriented preview builder in
[route-build-engine-slice-1.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/route-build-engine-slice-1.md).

Slice 1 proved the most important architectural point:

- the repo can keep the current source layout temporarily
- the new engine can still use the future output and URL model
- a coherent preview site can be built into `build/`

What slice 1 did **not** do was collapse the duplicated rendering logic.

That has now changed substantially:

- the preview builder no longer carries its own mini renderer
- the legacy Make path and preview path now share one render core
- preview sitemap generation is now route-driven in Python

What remains after this slice is smaller and more specific:

- the legacy root sitemap path is still Makefile/shell based
- preview and legacy validation are still separate entry points

Slice 2 is the first cleanup pass that makes the new engine start earning its
keep structurally rather than just experimentally.

Update:

- the shared render core now exists in
  [page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_renderer.py)
- both the preview builder and the legacy Make path now use it
- route-driven preview sitemaps now exist under:
  - `build/sitemap.txt`
  - `build/sitemap.xml`
- `make check-preview` now validates those sitemap files against the route
  table
- legacy and preview builds now also share HTML artifact-validation helpers in
  [artifact_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/artifact_validate.py)
  while keeping separate validation entrypoints for their genuinely different
  source/output invariants

## Slice Goal

Collapse the most important duplicated build logic without moving source into
`site/` yet.

The right-sized scope is:

1. extract one shared render core for rendered pages
2. then add route-driven sitemap generation for `build/`

The shared render core should include both:

- route-aware metadata rendering
- page HTML document assembly

That is slightly larger than a metadata-only slice, but simpler overall.

## Why This Slice Matters

The current split is workable, but not clean.

### Duplication 1: Page Rendering Assembly

The legacy root build path in
[Makefile](/Users/ztatlock/www/ztatlock.github.io/Makefile)
and the preview builder in
[preview_builder.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/preview_builder.py)
both assemble pages by:

- loading page title/body from [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
- composing site refs
- substituting `__WEBFILES__`
- running `djot`
- wrapping the body with `HEAD.1`, `HEAD.2`, and `FOOT`

The details are not identical, but the shape is clearly the same.

That duplication is already annoying, and it will get worse if both paths keep
evolving independently.

### Duplication 2: Metadata Rendering

The deeper problem had been that
[page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
treated canonical URL computation as fundamentally tied to the old
flat-root page stem model.

That is now partly fixed:

- metadata rendering accepts an explicit canonical URL
- the shared render core uses that route-aware API

The remaining design point is simply to keep that API as the stable center of
gravity rather than letting new rendering branches reappear elsewhere.

### Duplication 3: Sitemap Generation

The preview build now does generate `build/sitemap.txt` and
`build/sitemap.xml`.

The remaining duplication is that the legacy root build still generates
sitemaps via shell loops in
[Makefile](/Users/ztatlock/www/ztatlock.github.io/Makefile),
and those loops are still tied to the legacy root-served output shape.

That is exactly the sort of logic the new route-aware engine should own.

## Core Principle

Slice 2 should extract **shared logic**, not create another layer of preview
special cases.

The target shape is:

- one shared render core for rendered page routes
- one route-driven sitemap builder

with:

- the preview builder calling those modules directly
- the legacy root build calling them through thin wrappers where useful

## Proposed Module Boundaries

These boundaries are deliberately small.

### `scripts/sitebuild/page_renderer.py`

Purpose:

- own HTML document assembly for rendered page routes

Responsibilities:

- accept the route and already-loaded page source context
- render route-aware metadata for:
  - ordinary pages with front matter
  - publication pages with publication-local records
- load `HEAD.1`, `HEAD.2`, and `FOOT`
- combine Djot body plus site refs
- substitute `__WEBFILES__`
- invoke `djot`
- optionally rewrite local HTML targets when the caller supplies alias rules
- return final HTML text

Important constraint:

the caller should no longer need to duplicate either:

- the ordinary/publication metadata decision tree
- the HTML document assembly pipeline

The exact internal helper split matters less than the architectural rule:

- metadata rendering and page assembly should share one stable center of gravity
- canonical/public URL should be caller-controlled, not guessed from the old
  root build layout

Explicit non-responsibilities:

- route discovery
- sitemap generation
- build-directory cleanup

### `scripts/sitebuild/sitemap_builder.py`

Purpose:

- generate `sitemap.txt` and `sitemap.xml` from the route table

Responsibilities:

- choose the public routes that belong in the sitemap
- include copied publication assets that are meant to be public sitemap entries
- render deterministic text and XML outputs
- compute `lastmod` values in a controlled way

For the first cut, it is acceptable for the preview sitemap builder to use the
same last-modification policy as the current Makefile:

- if the output maps to tracked source files, use the latest git modification
  date among those inputs
- otherwise fall back to today

The main architectural win is route-driven generation, not perfect date theory.

## Recommended Implementation Order

This order keeps the slice reviewable without over-splitting it.

### Step 1: Extract The Shared Render Core

Do the render-core extraction in one chunk.

Desired result:

- preview builder stops owning `_render_page_metadata(...)`
- preview builder stops owning its own HTML document assembly path
- legacy root build can call the same renderer through a thin CLI or helper
- the current Makefile recipe loses most of its shell pipeline logic

This is likely to help `make all` / `make check` performance too, because it
reduces repeated process orchestration in the Makefile path.

### Step 2: Add Preview Sitemap Generation

Once route discovery and rendering are shared enough, generate:

- `build/sitemap.txt`
- `build/sitemap.xml`

from the preview route table.

Result:

- `make build-preview` now produces a more complete future-site artifact
- `make check-preview` now validates sitemap presence and correctness

### Step 3: Reassess Before Further Collapse

After these three pieces land, pause and inspect:

- what duplication remains with the root build
- whether the root build should also switch to Python sitemap generation
- whether validation should be partially unified next

Do not force more cleanup into the same slice if the first three steps already
form a clean checkpoint.

## What Slice 2 Should Not Do

Slice 2 should **not**:

- move source into `site/`
- change production deployment
- delete the root build path
- add GitHub Pages workflow
- redesign route discovery
- invent a general plugin system
- migrate all validation at once

This is still a careful consolidation slice, not the full cutover.

## Tests And Checks

Slice 2 should add small focused tests for:

- ordinary-page rendering through the shared render core
- publication-page rendering through the shared render core
- canonical URL handling inside the shared render core
- preview sitemap generation from routes

And the usual integration checks should still pass:

- `make test`
- `make build-preview`
- `make check-preview`
- `make validate-site`
- `make check`

## What Success Looks Like

After slice 2:

- preview builder no longer owns its own metadata logic
- preview builder no longer owns its own HTML assembly logic
- the legacy root build has a path to reuse the same render core
- `build/` includes route-driven sitemaps
- the broader redesign has fewer moving parts and a clearer center of gravity

That would be a good checkpoint before taking on the later source move into
`site/`.
