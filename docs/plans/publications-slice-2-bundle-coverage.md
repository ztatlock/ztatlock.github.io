# Publications Slice 2: Bundle Coverage

Status: Implemented

This note details the second implementation slice of the publications
structured-content campaign.

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [publications-slice-1-minimal-bundle-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-1-minimal-bundle-model.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Slice Goal

Finish canonical local bundle coverage for the current publications index
without changing the collection route shape or the hand-authored index wrapper
yet.

This slice should make the following statement true:

- every publication currently listed on the site has a canonical local bundle
  under `site/pubs/<slug>/publication.json`

## Starting State

This slice started from:

- `site/pages/publications.dj` lists `69` publication entries
- `24` of those entries already had local bundles under `site/pubs/`
- `45` entries still did not
- the remaining gap was:
  - `36` main-section publications
  - `9` workshop-section publications

Slice 1 already established the model needed for this work:

- `detail_page: true` for richer local publication pages
- `detail_page: false` for canonical local bundles without local detail pages
- `listing_group`
- `primary_link`

So this slice is mostly about coverage and temporary consistency checks, not
about inventing another new schema split.

## Why This Slice Now

This is the right next step because it gives later publications slices a much
cleaner foundation:

- route cutover should not happen while half the collection is still external-
  only from the repo's point of view
- index projection will be much simpler once every entry has a local bundle
- bundle coverage is now mechanically realistic because the minimal bundle
  model already exists

It also strengthens the current repo immediately by reducing the gap between:

- the hand-authored publications index
- the canonical local publication record set

## Target Invariants

After this slice:

- every `{#slug}` publication entry in `site/pages/publications.dj` has a
  matching `site/pubs/<slug>/publication.json`
- every non-draft publication bundle appears in the current publications index
  exactly once
- every non-draft publication bundle's `listing_group` matches the section
  where it appears in `site/pages/publications.dj`
- `site/pages/publications.dj` remains hand-authored and continues to control
  visible ordering
- index-backed bundles may still point outward via `primary_link`
- local publication detail pages are still only for `detail_page: true`
  publications

This slice should not yet require:

- a local detail page for every publication
- local PDFs/BibTeX/abstracts/images for newly backfilled minimal bundles
- any route change away from `/publications.html`
- any projection macros in the publications index

## Outcome

This slice is now implemented.

The current repo state after this slice is:

- `site/pages/publications.dj` still lists `69` publication entries
- all `69` indexed publications now have canonical non-draft bundles under
  `site/pubs/`
- bundle `listing_group` counts now match the current hand-authored index:
  - `58` `main`
  - `11` `workshop`
- `48` publications are currently in minimal `detail_page: false` mode
- richer existing `detail_page: true` bundles remain intact

The temporary coverage validator is also implemented and now enforces the
pre-projection consistency contract between the hand-authored index and the
bundle set.

## Recommended Scope

### 1. Add Coverage Validation

Add a temporary source-validation check for the current pre-projection state.

It should validate:

- every indexed publication slug has a bundle
- every non-draft bundle appears in the current publications index
- each such bundle appears exactly once
- each such bundle appears in the section matching its `listing_group`

This validation should be intentionally narrow.

It should not try to parse or compare the full rendered publication entry
content yet. In particular, it should not try to compare:

- title text
- author lists
- venue strings
- badge text
- the specific title-link target

Those are future projection concerns.

### 2. Backfill The Remaining Bundles

Add minimal bundles for the remaining `45` indexed publications.

Use the current hand-authored index as the source for:

- slug
- title
- author list
- venue
- section membership
- current title-link destination

For backfilled records:

- default to `detail_page: false`
- set `listing_group` from the current section:
  - `main`
  - `workshop`
- set `primary_link` to whichever `links` key corresponds to the current
  title-link destination

The expected common case is:

- `primary_link: "publisher"`

But use other keys when the current title link is more honest as:

- `arxiv`
- `event`
- or another allowed link key that already matches current behavior

### 3. Keep Rich Bundles Rich

This slice should not downgrade or flatten richer existing bundles.

Existing `detail_page: true` bundles should keep:

- their richer local detail-page semantics
- their current artifacts
- their current links and talk arrays

This is a coverage slice, not a simplification-through-loss slice.

### 4. Keep The Index Hand-Authored

`site/pages/publications.dj` should remain the rendered source for the
collection page in this slice.

That means:

- visible ordering stays hand-authored
- the `Aggregators` section stays hand-authored
- title links stay exactly as they are for now

The point is to finish bundle coverage first, not to mix coverage with route or
projection changes.

## Internal Execution Plan

This slice is large enough to need internal checkpoints.

### Step 1: Coverage Validator

Implement the temporary validation layer first, with focused tests.

Goal:

- make the pre-projection contract explicit before bulk content edits

Checkpoint:

- validator can detect missing bundles
- validator can detect section/listing-group mismatch
- validator can detect orphan non-draft bundles

Result:

- implemented

### Step 2: Workshop Backfill

Backfill the remaining workshop publications first.

Why:

- only `9` remain
- they are a smaller and easier subset
- they exercise the non-`main` classification path early

Checkpoint:

- all workshop entries have bundles
- validator stays green
- inventory still behaves honestly

Result:

- implemented

### Step 3: Main-Section Backfill

Backfill the remaining `36` main-section publications.

Recommended discipline:

- work in reverse chronological order
- preserve current slugs from the hand-authored index
- keep records minimal unless a real richer local page already exists

Checkpoint:

- every indexed publication now has a local bundle

Result:

- implemented

### Step 4: Final Verification

Run the normal repo checks and then stop.

Expected verification:

- `make test`
- `make inventory`
- `make check`
- `git diff --check`

Also verify that there are still no unexpected tracked output diffs in:

- `*.html`
- `sitemap.txt`
- `sitemap.xml`

Result:

- all passed

## Tests

Add focused tests for:

- missing-bundle detection from the publications index
- orphan non-draft bundle detection
- section / `listing_group` mismatch detection
- acceptance of a fully covered minimal-bundle publication set
- continued acceptance of richer `detail_page: true` bundles mixed with
  minimal `detail_page: false` bundles

## Non-Goals

This slice should not:

- move the publications index wrapper to `site/pubs/index.dj`
- change the canonical route to `/pubs/`
- change publication detail-page backlinks
- project repeated publication-entry blocks from bundle data
- recover historical local artifacts from archives
- introduce a more complex venue taxonomy than the current `listing_group`
  needs

## Follow-On Question For The Next Slice

If this slice lands cleanly, the main next decision becomes:

- should route cutover come before projection, or should projection come first?

My current recommendation remains:

- route cutover first
- projection second

because a collection-root wrapper at `site/pubs/index.dj` is the cleaner place
to host future publication-list placeholders.

## Stop And Reassess

After this slice, stop and check:

1. Does full local bundle coverage feel mechanically sustainable?
2. Did the temporary coverage validator catch real drift risks without becoming
   too clever?
3. Does the current hand-authored index still feel manageable long enough to
   support the route-cutover slice?
4. Are there any title-link cases that reveal the current `primary_link`
   design is too narrow?
