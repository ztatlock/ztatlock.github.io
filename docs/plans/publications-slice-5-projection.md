# Publications Slice 5: Index Projection

Status: Implemented

This note records the implementation of the projection slice of the
publications structured-content campaign.

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [publications-slice-3-route-cutover.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-3-route-cutover.md)
- [publications-slice-4-pub-date.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-4-pub-date.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)

## Why This Slice Was Needed

The collection shape is now in place:

- the hand-authored publications wrapper lives at `site/pubs/index.dj`
- the canonical collection route is `/pubs/`
- every indexed publication already has a canonical local bundle

That means the main remaining duplication is the repeated publication-entry
text still hand-maintained inside `site/pubs/index.dj`.

This slice should remove that duplication without taking on artifact recovery
or more schema churn.

## Slice Goal

Keep `site/pubs/index.dj` as the authored wrapper, but replace the repeated
publication-entry blocks with generated sections rendered from publication
bundles.

## Ordering

This slice should derive ordering from publication bundle truth:

1. `pub_date` descending
2. `title` ascending as a stable tie-break

That ordering rule should already be established and backfilled by
[publications-slice-4-pub-date.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-4-pub-date.md).

## Landed Scope

This slice did these things:

1. replace the repeated entry blocks in `site/pubs/index.dj` with generated
   placeholders
2. render the main and workshop sections from bundle data ordered by
   `pub_date`
3. retire the temporary parser/validator contract that depended on literal
   hand-authored publication entries
4. keep the wrapper framing and `Aggregators` section hand-authored
5. stop and reassess before any artifact-enrichment work

## Non-Goals

This slice should not:

- change the canonical route away from `/pubs/`
- change publication detail-page routes
- recover missing PDFs/BibTeX/abstracts/images from archives
- introduce a richer venue taxonomy than the existing `listing_group`
- force every publication to become `detail_page: true`
- derive CV/news/collaborators from publication data yet

## Final Invariants For This Slice

At the end of this slice:

1. `site/pubs/index.dj` remains the authored collection wrapper
2. the repeated publication-entry blocks are no longer hand-maintained there
3. the wrapper contains explicit placeholders for generated lists:
   - `__PUBLICATIONS_MAIN_LIST__`
   - `__PUBLICATIONS_WORKSHOP_LIST__`
4. publication facts used in those generated lists come from publication
   bundles, not the wrapper body
5. publication ordering for the collection is derived from bundle `pub_date`
6. source validation ensures:
   - every non-draft bundle has `pub_date`
   - each bundle appears under the section matching `listing_group`
   - the wrapper contains the required placeholders
7. the temporary literal-entry parser/coverage contract is retired
8. the rendered `/pubs/` page keeps the current section split but may change
   visible ordering where bundle `pub_date` truth differs from the old
   hand-authored order
9. the rendered `/pubs/` page may also improve author-link coverage where the
   publication bundles carry richer person refs than the old hand-authored
   wrapper text

## Design Choices

### 1. Derive Order From `pub_date`

Ordering should come from publication-local truth:

- `pub_date`

That is cleaner than introducing a collection-owned order manifest because
publication date is a real fact that will likely help later consumers too.

### 2. Keep The Wrapper Hand-Authored

The wrapper should still own:

- page title and framing
- section headings
- `Aggregators`

Only the repeated list bodies should be projected.

That means the wrapper will likely evolve to something like:

```text
# [Zachary Tatlock][] / Publications

## Conference and Journal Papers

__PUBLICATIONS_MAIN_LIST__

## Workshop Papers

__PUBLICATIONS_WORKSHOP_LIST__

## Aggregators

- [DBLP](https://dblp.org/)
```

### 3. Generalize Page Projections Only As Far As Evidence Requires

Talks already established one projection-backed wrapper.
Publications will be the second.

That is enough evidence to justify a small projection helper generalization,
but not a big framework.

Recommended shape:

- a small shared page-projection module
- route-kind dispatch for:
  - `talks_index_page`
  - `publications_index_page`

Do not generalize beyond those real cases yet.

### 4. Derive Title Links From Bundle Truth

The projected publication title should link as follows:

- if `detail_page: true`, link to `pubs/<slug>/`
- if `detail_page: false`, link to `record.links[record.primary_link]`

This matches the current bundle model and avoids reintroducing duplicated title
link state in the wrapper.

## What Landed

### Step 1: Add Publication Projection Rendering

Add a projection helper that renders a publication list section from:

- publication bundle data
- ordering by `pub_date` descending, then title

It should render:

- title line
- author lines
- venue line
- badges

using the current publication bundle truth.

Recommended output style:

- match the current Djot entry shape closely enough that rendered HTML diffs
  stay minimal and reviewable

Tests added:

- `detail_page: true` entry links locally
- `detail_page: false` entry links via `primary_link`
- badges render correctly
- author references render correctly

### Step 2: Switch The Wrapper To Placeholders

Replace the literal entry blocks in `site/pubs/index.dj` with:

- `__PUBLICATIONS_MAIN_LIST__`
- `__PUBLICATIONS_WORKSHOP_LIST__`

Keep:

- page framing
- section headings
- `Aggregators`

Then update the page-render path so `publications_index_page` fills those
placeholders before Djot rendering.

Tests added:

- wrapper projection applies only to `publications_index_page`
- both placeholders are filled
- wrapper missing placeholders is rejected by source validation

### Step 3: Retire Temporary Hand-Authored Entry Parsing

Once placeholders are live:

- remove the temporary runtime dependence on literal entry parsing from
  `site/pubs/index.dj`
- keep any parsing helper only if still useful for migration/tests

The steady-state validation should now be based on:

- bundle data
- `pub_date`
- wrapper placeholders

not on literal rendered entry text inside the wrapper.

### Step 4: Final Verification

Run the normal repo checks and stop.

Verification run:

- `make test`
- `make build`
- `make inventory`
- `make check`
- `git diff --check`

Also inspect tracked output diffs for:

- `*.html`
- `sitemap.txt`
- `sitemap.xml`

Observed output changes were reviewable and limited to:

- `pub_date`-driven reordering within sections
- richer author linking where bundle refs were more complete
- small formatting differences caused by replacing literal wrapper entries
  with projection

## Tests

Focused tests now cover:

- publication list rendering from bundles
- local vs external title-link behavior
- wrapper placeholder enforcement
- projection application only on `publications_index_page`
- acceptance of the real repo's current main/workshop split through `pub_date`
  ordering

## Outcome

The publications wrapper now reads like authored framing rather than a second
publication database. The collection is ordered from bundle truth, and the
temporary parser/validator contract for literal wrapper entries is gone.

The likely follow-on work is now local artifact enrichment or later downstream
reuse, not more projection plumbing.
