# Publications Campaign

This note captures the publications structured-content campaign, the current
architectural seams that motivate it, and the recommended initial slice order.

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)

## Goal

Make publication-local bundles the real single source of truth for the
publications collection, then project that structured truth back into the
publications index and later downstream views where it clearly pays off.

The goal is not to invent a second publication database.
The goal is to finish the architectural shift already started under
`site/pubs/<slug>/publication.json` and remove repeated publication-list
structure from hand-authored pages.

## Why Publications Now

The publications campaign now deserves to move ahead of students.

Why:

- publication bundles are already the most important structured content root
  after people
- the current architecture still has a visible asymmetry between
  `site/pubs/<slug>/publication.json` and `site/pages/publications.dj`
- publication detail pages still backlink to `publications.html`, which is a
  sign that the collection/index shape has not caught up with the bundle model
- talks already proved that bundle-local records plus a collection index
  wrapper can be clean and reviewable

Students still matters, but publications now has more direct architectural
payoff.

## Current Status

Slice 1 of this campaign is now implemented.

That means:

- the repo now supports a minimal published publication-bundle mode for
  canonical local records without local detail pages
- existing richer publication bundles have been aligned to that model
- a small pilot set of formerly external-only publications now has local
  bundles under `site/pubs/`

The next likely slice is therefore Slice 2: expand bundle coverage.

## Current Audit

Current relevant sources:

- `site/pubs/<slug>/publication.json`
  Canonical local publication records for the subset of publications that
  currently have bundles.
- `site/pages/publications.dj`
  Current hand-authored publication index page.
- `scripts/publication_record.py`
  Canonical publication loading and page rendering helpers.

Current observed facts:

- `site/pages/publications.dj` is `811` lines long
- it currently lists `69` publication entries
- it has `2` repeated listing sections:
  - `Conference and Journal Papers`
  - `Workshop Papers`
- it has `1` clearly hand-authored section:
  - `Aggregators`
- only `21` entries currently have canonical local bundles under `site/pubs/`
- `21` title links currently point to local `pubs/<slug>/`
- `48` title links currently point directly to external URLs

### Consequences Of The Audit

These facts imply:

- publications is not a one-slice "flip the page over" campaign
- if we want a truly clean index, every publication should eventually have a
  local bundle
- but the current non-draft publication-page model is too rich to backfill all
  missing bundles in one step
- we need a cleaner minimal bundle model before bulk bundle coverage and index
  projection will be simple
- route shape, bundle coverage, and projection should be treated as related but
  separable subproblems

## Desired End State

The intended long-term shape is:

- every publication has a local bundle under `site/pubs/<slug>/`
- every publication has a local `publication.json`
- publisher pages and external artifact URLs are fallback destinations, not the
  primary source of truth for whether the publication exists on the site
- the publications index projects repeated listing structure from publication
  bundles
- the collection index likely lives with the collection:
  - `site/pubs/index.dj`
  - canonical route `/pubs/`

That does not mean every bundle must become fully rich on the same day.
It means the architecture should clearly work toward local bundle truth while
allowing some bundles to start as minimal index-backed records before richer
local artifact curation happens later.

## Boundary Of The Campaign

This campaign should include:

- the publications collection index route and wrapper location
- canonical publication bundle coverage
- repeated listing projection for the publications index
- backlink/index-link cleanup for publication detail pages
- the smallest structured classification needed to support the index

This campaign should not initially include:

- a full artifact-curation pass for every old publication
- large CV rewrites
- publication-derived collaborator generation
- funding/grants modeling
- any attempt to unify publication-local `"talks"` arrays with invited/public
  talks bundles

## First Architectural Decision

Before the implementation slices broaden, the campaign should make one explicit
route decision:

- should the publications collection mirror talks with:
  - `site/pubs/index.dj`
  - canonical `/pubs/`

My current recommendation is yes.

Why:

- it matches the cleaner talks collection pattern
- it keeps collection framing with the collection root
- it lets publication detail pages backlink to the collection naturally
- it removes one of the most obvious remaining asymmetries in the repo

This decision should be made deliberately rather than drift in via ad hoc link
fixes.

## First Data Decision

The first campaign slices should define a minimal publication bundle model that
supports full bundle coverage without forcing full local artifact richness.

The key idea is to distinguish:

- publication bundles that are canonical enough to appear in the publications
  index
- publication bundles that are rich enough to support a full local publication
  detail page

The cleanest likely rule is:

- every publication eventually gets a local `publication.json`
- local detail-page readiness is inferred from richer canonical assets and
  files, not from a second separate publication database

This lets bundle coverage happen before full artifact recovery.

### Minimal Classification

The first projection slices should also avoid a grand venue ontology.

The current index only needs a small amount of listing classification, such as:

- `main`
- `workshop`

or similarly named categories.

That is probably better than immediately forcing a perfect global taxonomy like:

- conference
- journal
- workshop
- magazine
- survey

because some venues blur those lines and the first campaign slices do not need
that full complexity yet.

The first structured field should therefore be the smallest classification that
supports the current page shape.

## Recommended Slice Order

### Slice 1: Minimal Publication Bundle Model

Goal:

- define what the smallest acceptable local publication bundle is
- prove that external-only publications can be represented canonically without
  pretending they already have full local artifacts

Likely scope:

- decide the invariant for a minimal index-backed publication bundle
- decide how an external-first publication chooses its primary outbound link
- add the smallest listing-classification field needed for future index
  grouping
- update loaders/validators/tests to recognize that model
- create a small pilot set of new local bundles for currently external-only
  publications
- keep the current publications index route and page structure unchanged

Why this first:

- it makes "every publication has a local bundle" a realistic campaign goal
- it avoids mixing a large content backfill with route-shape changes in one
  slice
- it gives later collection-index and projection slices a cleaner foundation

Stop and reassess after this slice.

Status:

- implemented

### Slice 2: Expand Bundle Coverage

Goal:

- move from the pilot model toward full local bundle coverage for the current
  publications index

Likely scope:

- scaffold minimal bundles for the remaining currently external-only
  publications
- keep using external destinations where richer local artifacts are not yet
  available
- avoid turning this slice into a full artifact-curation campaign

Stop and reassess after this slice.

### Slice 3: Collection Index Route Cutover

Goal:

- decide the canonical publications collection route shape
- move only the wrapper/index location and backlinks

Likely scope:

- add a publications collection index wrapper at `site/pubs/index.dj`
- decide whether the canonical route becomes `/pubs/`
- update publication detail page backlinks away from `publications.html`
- update authored internal links accordingly
- keep the repeated publication list body hand-authored for this slice

Why here:

- by this point the collection index will sit on top of much broader local
  bundle coverage
- it mirrors the talks collection-index slice cleanly
- it gives the campaign a stable public/index shape before classification or
  projection work

Stop and reassess after this slice.

### Slice 4: Publication Index Projection

Goal:

- replace repeated listing blocks with projection from publication bundles

Likely scope:

- add a projection helper for publication entries and sections
- support multiple generated blocks in the index wrapper, for example:
  - `__PUBLICATIONS_MAIN_LIST__`
  - `__PUBLICATIONS_WORKSHOP_LIST__`
- keep hand-authored framing and aggregator links in Djot

Stop and reassess after this slice.

### Slice 5+: Local Artifact Enrichment

Goal:

- keep strengthening local publication pages over time

Likely scope:

- recover richer local artifacts from older site copies and WEBFILES-like
  archives
- upgrade minimal index-backed bundles into richer local publication bundles
- keep this work incremental and separate from route/index correctness

## Key Invariants

As this campaign proceeds, we want:

- publication-local bundles to become more authoritative over time, not less
- every publication in the index to gain a canonical local bundle
- the publications index route shape to stay simple and unsurprising
- full local publication-page richness to remain a later enrichment concern,
  not a blocker to canonical bundle coverage
- hand-authored framing to stay in Djot
- repeated entry structure to move into structured projection
- no giant publication mega-schema unless repeated real needs justify it
- strong tests around classification, route shape, and projection behavior

## Current Recommendation

The next publications slice should be:

- minimal publication bundle model

Concretely, that means:

1. define the smallest acceptable local bundle for currently external-only
   publications
2. decide how title links or primary outbound links should work for those
   minimal bundles
3. add the smallest listing-classification field needed for future projection
4. implement focused validation/tests and a small pilot backfill
5. stop and reassess before large-scale bundle coverage or route cutover

That is the cleanest next move because it makes full local bundle coverage a
realistic, reviewable goal before we try to build a cleaner collection index on
top of it.

The detailed planning note for that first slice is:

- [publications-slice-1-minimal-bundle-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-1-minimal-bundle-model.md)
