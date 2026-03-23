# Publications Slice 1: Minimal Bundle Model

Status: Implemented

This note details the first implementation slice of the publications
structured-content campaign.

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Slice Goal

Define the smallest publication bundle model that allows the repo to work
toward "every publication has a local bundle" without forcing every publication
to immediately become a rich local publication page.

This slice should not change the publications index route yet.
It should make full local bundle coverage realistic first.

## Result

This slice is now in place.

It established:

- `detail_page` to distinguish local bundle truth from local detail-page
  readiness
- `listing_group` as the smallest current publications-index classification
- `primary_link` for published bundles that do not yet have a local detail page

It also proved the model on a small real pilot set of published index-backed
bundles:

- `2019-oopsla-troika`
- `2020-pldi-szalinski`
- `2023-farm-twine`

And it aligned the existing richer local publication bundles with the new
model by adding `listing_group` to them.

## Current Constraint

Today the repo effectively has one non-draft publication-bundle mode:

- full local publication page bundle

That mode assumes:

- local PDF
- local BibTeX
- local abstract
- local preview image
- enough metadata to render publication-page meta tags

That assumption currently lives in:

- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
- [route_discovery.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_discovery.py)

So "just add local bundles for the remaining publications" is not actually a
small slice under the current model.

## Target Model

After this slice, non-draft publication bundles should have two explicit modes:

1. local detail page bundle
   Published locally and eligible for a `/pubs/<slug>/` page route.

2. index-backed bundle
   Canonical local structured record, included in the publications collection,
   but not yet eligible for a local publication detail page.

Draft remains separate:

3. draft bundle
   Not yet public in the built site or projected indexes.

### Recommended Field Shape

This slice should add the following publication-record fields:

- `detail_page`
  Optional boolean, default `true`.
  Meaning:
  - `true`: this publication is expected to support a local detail page
  - `false`: this publication is canonical locally but does not yet have a
    local detail page

- `listing_group`
  Required for non-draft publications.
  Initial allowed values:
  - `main`
  - `workshop`

- `primary_link`
  Optional string naming one key in `links`.
  Required when `detail_page: false`.

Why this shape:

- `detail_page` separates local-record truth from local-page readiness
- `listing_group` is the smallest structured field that serves the current
  publications index shape
- `primary_link` avoids duplicating URLs in a second `primary_url` field

When `detail_page: false`, title linking for future projected indexes should
use:

- `links[primary_link]`

When `detail_page: true`, title linking should continue to use:

- the local publication page route

## Core Invariants

After this slice:

- every publication bundle can be one of:
  - draft
  - index-backed
  - local-detail-page-backed
- draft status still controls visibility
- `detail_page: false` never implies draft
- non-draft `detail_page: false` publications must still be fully canonical as
  records
- non-draft `detail_page: false` publications do not require local PDF/BibTeX/
  abstract/preview-image assets
- non-draft `detail_page: true` publications keep the current stronger local
  page invariants

## Validation Split

This slice should split publication validation into two layers.

### Record-Core Validation

Applies to every publication bundle.

Must validate:

- slug shape
- `title`
- `authors`
- `venue`
- `links`
- `detail_page`
- `listing_group` for non-draft records
- `primary_link` when `detail_page: false`

Should reject:

- unknown listing groups
- `primary_link` values not present in `links`
- `detail_page: false` with missing `primary_link`

### Local-Page Validation

Applies only to non-draft `detail_page: true` publications.

Must validate:

- local PDF
- local BibTeX
- local abstract
- local preview image
- metadata description requirements
- metadata image resolution

This preserves the current strong publication-page invariants while letting
index-backed bundles be lighter-weight.

## Recommended Schema Adjustment

The current record model likely needs one careful relaxation:

- `description` should no longer be universally required at record-load time

Instead:

- `description` can be optional at the record-core layer
- `description` is still required for non-draft `detail_page: true`
  publications because publication-page metadata rendering depends on it

Reason:

- index-backed bundles should only need fields that the publications index
  actually uses
- requiring page metadata text for publications that do not yet have a local
  page would make bundle coverage harder than it needs to be

This is the main schema split to implement carefully.

## Route And Build Behavior

This slice should leave the current collection route shape untouched.

Specifically:

- keep `site/pages/publications.dj`
- keep `/publications.html`
- do not add `site/pubs/index.dj` yet

But route discovery should change for publication bundles:

- draft publication:
  no built publication page
- non-draft `detail_page: true` publication:
  current `publication_page` route behavior
- non-draft `detail_page: false` publication:
  no `publication_page` route yet

That means the first slice changes publication truth, not publication routing.

## Downstream Helpers That Must Stay Honest

This slice should update downstream helpers that currently assume every
non-draft publication bundle has a local page.

The most important one is:

- [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)

For index-backed bundles, the inventory should not claim a nonexistent local
page. It should represent the bundle as canonical locally while being honest
about local page readiness.

This slice should explicitly review any helper that assumes:

- `publication_page_path(slug)` always exists for every non-draft publication

## Pilot Backfill

This slice should not try to backfill all missing bundles.

Instead, pick a small pilot set of currently external-only publications, for
example:

- one older conference/journal publication
- one workshop publication
- one publication with a straightforward publisher/arXiv primary target

The pilot is there to prove the model and the validation rules, not to grind
through content migration volume.

## Tests

Add focused tests for:

- loading a non-draft `detail_page: false` publication record
- rejecting `detail_page: false` without `primary_link`
- rejecting unknown `listing_group`
- allowing index-backed bundles without local page assets
- preserving current validation for non-draft `detail_page: true` bundles
- excluding index-backed bundles from publication page routes
- keeping current publication-page routes for existing rich bundles
- inventory output honesty for index-backed bundles

## Explicit Non-Goals

This slice should not:

- move the publications index wrapper
- change publication detail-page backlinks yet
- project the publications index from bundles yet
- recover missing local artifacts from archives yet
- bulk backfill every missing publication bundle

## Stop And Reassess

After this slice, stop and check:

1. Does the split between record-core truth and local-page readiness feel
   simple?
2. Does `detail_page: false` feel like the right published-no-local-page
   representation?
3. Does `primary_link` avoid unnecessary duplication cleanly?
4. Does `listing_group` feel small and sufficient for the current page shape?
5. Are we now set up for an honest bulk bundle-coverage slice next?

Only after that reassessment should the campaign broaden into wider bundle
coverage or route/index cutover.
