# Publications Slice 3: Collection Index Route Cutover

Status: Implemented

This note defines the next implementation slice of the publications
structured-content campaign.

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [publications-slice-2-bundle-coverage.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-2-bundle-coverage.md)
- [talks-slice-2-collection-index.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-slice-2-collection-index.md)

## Why This Slice Now

Bundle coverage was complete for the current hand-authored publications index
before this slice:

- all `69` indexed publications have canonical local bundles under
  `site/pubs/`
- the temporary coverage validator keeps the index and bundle set from
  drifting

That means the main remaining architectural seam is no longer coverage.
It is collection shape:

- the collection wrapper still lived at `site/pages/publications.dj`
- the canonical collection URL was still `/publications.html`
- generated publication detail pages still backlinked to `publications.html`

This slice should fix that seam before we attempt projection.

## Outcome

This slice is now implemented.

The current repo state after this slice is:

- the hand-authored publications wrapper now lives at `site/pubs/index.dj`
- the canonical collection route is now `/pubs/`
- the route table has an explicit `publications_index_page` route kind
- richer publication detail pages now backlink to `pubs/`
- authored site-source links now point to `pubs/`, not `publications.html`
- the repeated publication list is still hand-authored for now

## Slice Goal

Move the hand-authored publications index wrapper to the collection root,
canonicalize the collection URL at `/pubs/`, and update the route/link
surface so publications reads like a real collection rather than a singleton
page.

## Scope

This slice should do exactly these things:

1. add explicit `publications_index_page` route support
2. move the wrapper from `site/pages/publications.dj` to `site/pubs/index.dj`
3. make the canonical publications collection route `/pubs/`
4. rewrite authored internal links from `publications.html` to `pubs/`
5. update publication detail-page backlinks to point to `pubs/`
6. keep the publication list hand-authored for this slice
7. stop and reassess before projection

## Non-Goals

This slice should not:

- project repeated publication-entry blocks from bundle data
- introduce `__PUBLICATIONS_*__` placeholders yet
- change visible publication ordering
- recover older publication artifacts from archives
- add local detail pages for bundles that are still `detail_page: false`
- generalize talks/publications into a generic collection-index framework

## Final Invariants For This Slice

At the end of this slice:

1. the canonical authored wrapper for the publications index is:
   - `site/pubs/index.dj`
2. the canonical built output for the publications index is:
   - `build/pubs/index.html`
3. the canonical public URL for the publications index is:
   - `/pubs/`
4. the route table contains an explicit `publications_index_page` route kind
5. the publications index route depends on:
   - `site/pubs/index.dj`
6. source validation requires `site/pubs/index.dj` when non-draft publication
   bundles exist
7. `site/pages/publications.dj` is no longer accepted as the canonical wrapper
8. authored source should not contain local links to `publications.html`
9. richer publication detail pages backlink to `pubs/`, not
   `publications.html`
10. repeated publication-entry content remains hand-authored in the wrapper for
    one more slice

## Design Choices

### 1. Use An Explicit Publications Index Route Kind

The cleanest route model for this slice is:

- `ordinary_page`
- `talks_index_page`
- `publications_index_page`
- `publication_page`
- `static_file`

Do not reintroduce a fake-generic collection abstraction here.
Talks was intentionally narrowed to a talks-specific route kind, and
publications should be equally honest.

If talks and publications later prove to share enough real logic, we can
generalize then from a position of evidence instead of speculation.

### 2. Keep The Wrapper Hand-Authored For One More Slice

This slice should move the wrapper, route, and backlinks only.

The publication list should remain hand-authored in the moved wrapper for now.
That keeps the slice focused on route shape and link hygiene instead of mixing
route cutover with projection.

The immediate goal is:

- collection-root wrapper
- canonical `/pubs/`
- clean backlink and authored-link surface

not:

- generated publication index sections

### 3. Treat `pubs/` As The Canonical Authored Collection Link

Authored Djot should link to the collection as:

- `pubs/`

not:

- `publications.html`

This matches the existing publication-item convention:

- `pubs/<slug>/`

and lets the current route-alias rewrite turn `pubs/` into canonical `/pubs/`
in generated HTML, even from nested pages.

## Implementation Order

### Step 1: Add Publications Index Route Support

Introduce a new route kind for the publications collection index.

Suggested initial rule:

- source: `site/pubs/index.dj`
- output: `build/pubs/index.html`
- public URL: `/pubs/`
- canonical URL: `https://ztatlock.net/pubs/`
- draft status: same `# DRAFT` rule used for other Djot wrappers

Tests to add or update:

- route model accepts `publications_index_page`
- route discovery finds `publications_index_page:publications`
- route discovery gives it the expected output path and public URL
- the route source paths include only `site/pubs/index.dj`

Stop and reflect:

- Is the route kind naming clear and honest?
- Is this getting simpler, not more magical?

### Step 2: Move The Wrapper To `site/pubs/index.dj`

Move the current hand-authored wrapper content from:

- `site/pages/publications.dj`

to:

- `site/pubs/index.dj`

Keep the repeated publication entries and `Aggregators` section hand-authored
for this slice.

This step should also update helper paths that currently assume the wrapper
lives under `site/pages/`.

Likely affected code:

- publication-index parser/helper paths
- source validation
- metadata/source loading for the new route kind

Tests to add or update:

- parser/helper functions read the wrapper from `site/pubs/index.dj`
- source validation requires the new wrapper when publication bundles exist
- source validation rejects coexistence with `site/pages/publications.dj`

Stop and reflect:

- Does the wrapper now read like a real collection-root source file?
- Did we avoid accidentally coupling wrapper parsing to projection work?

### Step 3: Update Link Surface

Rewrite authored local links from:

- `publications.html`

to:

- `pubs/`

This should include:

- singleton pages like `site/pages/index.dj`
- singleton pages like `site/pages/research.dj`
- any other authored Djot sources that still reference the old collection URL

Also update generated publication detail-page backlinks so richer local
publication pages point to:

- `pubs/`

instead of:

- `publications.html`

Add source validation for legacy collection links after the wrapper move.

Tests to add or update:

- legacy `publications.html` link detection
- publication detail-page rendering uses the canonical collection backlink

Stop and reflect:

- Does the site now have one clear collection URL surface for publications?
- Are there any unexpected places still depending on `publications.html`?

### Step 4: Final Verification

Run the normal repo checks and then stop.

Expected verification:

- `make test`
- `make build`
- `make inventory`
- `make check`
- `git diff --check`

Also verify there are no unexpected tracked output diffs in:

- `*.html`
- `sitemap.txt`
- `sitemap.xml`

## Tests

Add focused tests for:

- publications index route discovery
- new wrapper path resolution under `site/pubs/index.dj`
- source-validation requirement for `site/pubs/index.dj`
- rejection of legacy `publications.html` authored links
- publication detail-page backlink rewrite to `pubs/`
- acceptance of the moved wrapper while projection is still hand-authored

## Follow-On Question For The Next Slice

If this slice lands cleanly, the main next decision becomes:

- how should projection be introduced into `site/pubs/index.dj`?

My current recommendation is:

- keep the wrapper hand-authored
- add multiple generated blocks later, likely something like:
  - `__PUBLICATIONS_MAIN_LIST__`
  - `__PUBLICATIONS_WORKSHOP_LIST__`

That should be its own slice.

## Stop And Reassess

After this slice, stop and check:

1. Does `site/pubs/index.dj` feel like the right home for the collection
   wrapper?
2. Does `/pubs/` feel obviously cleaner than `/publications.html` in practice?
3. Did the route cutover stay small enough to review comfortably?
4. Is the wrapper still manageable by hand for one more slice before
   projection?
