# Funding Campaign

Status: canonical data, public wrapper, and CV funding projection implemented;
later grant-output enrichment remains important but deferred

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)

## Goal

Establish a canonical funding data source and a public funding wrapper so the
site has one clear home for grant facts before any richer cross-domain
association work begins.

This campaign is not about building a full grant-output graph on day one.
It is about making funding a first-class structured domain with an obvious
source of truth and a clean public route.

## Why Funding Next

Funding is now the strongest next new shared-data campaign because:

- it has a clear product outcome: a public `/funding/` page
- the current funding facts are already structured enough to canonicalize
- the domain matters strategically beyond simple deduplication
- later grant-to-paper and grant-to-project associations are valuable, but
  they can be deferred until the base architecture is in place

This is a better next move than inventing another curated CV slice by inertia.

## Current Audit

Current explicit funding surfaces:

- `site/data/funding.json`
  canonical funding records for the current grant list
- `site/funding/index.dj`
  thin public funding wrapper at the canonical `/funding/` route
- `site/cv/index.dj`
  contains the authored `## Funding` heading plus the projected funding list

Current funding-entry shape:

- title
- role
- sponsor
- optional award identifier
- dollar amount
- year range

Current related surfaces:

- `site/pages/research.dj`
  mentions projects that may later benefit from funding associations
- `site/pubs/`
  already contains canonical publication bundles that may later benefit from
  related-grant links

Important current constraint:

- there is still no structured association between grants and projects or
  publications
- the public funding page and the CV now share canonical funding data, while
  keeping separate consumer renderers

## Design Recommendation

Funding should follow the shared-data pattern used for students, teaching, and
service:

- canonical shared data under `site/data/funding.json`
- a thin public wrapper at `site/funding/index.dj`
- a narrow CV consumer where the duplicated funding list clearly earns its keep
- later homepage consumers only if they clearly earn their keep

Funding should not start as:

- a bundle-root domain under `site/funding/<slug>/`
- a new cross-domain mega-schema
- a grant/publication/project graph

The first campaign slices should keep the model flat, explicit, and easy to
edit by hand.

## Canonical Model Recommendation

The first funding model should be a flat ordered list of grant records.

Recommended top-level shape:

- ordered `records`

Recommended slice-1 fields per record:

- `key`
  stable unique identifier for the grant record
- `title`
- `role`
  short role text such as `PI` or `Co-PI`
- `sponsor`
- optional `award_id`
- `amount_usd`
  integer dollar amount
- `start_year`
- `end_year`

Important design notes:

- preserve file order as canonical in slice 1
- use a plain string for `sponsor`; do not normalize funders into a separate
  registry yet
- keep `amount_usd` as a simple integer; do not add multi-currency machinery
- keep award identifiers optional
- do not add `related_publications`, `related_projects`, or cross-links yet

## What Should Stay Hand-Authored

The funding campaign should not move everything into JSON.

The following should stay in wrappers unless a later slice clearly proves
otherwise:

- the funding-page heading
- any editorial framing about research direction or impact
- any later curated grant highlights if those ever appear on the homepage or
  elsewhere

## Recommended Slice Order

### Slice 1. Canonical Funding Model

Implemented.

- add `site/data/funding.json`
- add loader and validator tests
- backfill the current intended funding facts from the CV
- stop before any public rendering cutover

Invariant after slice 1:

- `site/data/funding.json` is the canonical funding fact source
- every intended current funding fact is represented exactly once
- no public page or CV rendering has switched yet
- no grant-output associations are modeled yet

What landed:

- canonical funding records in `site/data/funding.json`
- strict loading and validation in `scripts/funding_record.py`
- source-validation integration so the existing CV funding section now
  requires the canonical funding registry to exist
- focused loader and source-validation tests

### Slice 2. Public Funding Wrapper / Route Cutover

Implemented.

- add `site/funding/index.dj`
- canonicalize `/funding/`
- project repeated funding records from `site/data/funding.json`
- keep page framing hand-authored

Invariant after slice 2:

- the public funding page is a thin wrapper over canonical funding records
- the canonical public route is `/funding/`
- no second funding fact source exists in the wrapper
- CV funding remains hand-authored for now

What landed:

- the public funding wrapper at `site/funding/index.dj`
- canonical `/funding/` route support in the explicit route-aware build
- public funding-list projection from `site/data/funding.json`
- source validation for the placeholder-backed funding wrapper

### Slice 3. CV Funding Projection

Implemented.

- replace only the duplicated funding list body in `site/cv/index.dj`
- preserve the `## Funding` heading hand-authored
- define an explicit CV-specific funding renderer over canonical funding data
- keep the rendered diff focused on the funding section and explain any
  visible policy changes

Invariant after slice 3:

- the CV funding list derives from canonical funding records
- the public funding page and the CV now share one canonical funding source
  while still allowing separate consumer renderers
- no grant-output associations are modeled yet

What landed:

- the duplicated funding list body in `site/cv/index.dj`
  now uses `__CV_FUNDING_LIST__`
- an explicit CV funding renderer in `scripts/sitebuild/page_projection.py`
- source validation requiring the CV funding placeholder and rejecting
  literal copied funding-entry blocks
- focused projection and source-validation tests
- a rendered HTML diff review showing the built CV Funding section remained
  byte-identical after projection

## Deferred Work

The following should remain explicitly out of the first funding campaign
checkpoint:

- homepage funding/highlights consumers
- grant-to-publication associations
- grant-to-project associations
- sponsor normalization or a funder registry
- funding totals, charts, or analytics views

Those may become worthwhile later, but they should not complicate the base
funding architecture.

That deferred enrichment is strategically important, especially eventual
grant-to-paper and grant-to-project mapping across funding, research, and
publication views, but it should remain a deliberate later campaign rather
than a same-day follow-on from the flat funding model.

## Recommendation

Funding has now landed the smallest real architecture that clearly earned its
keep:

1. canonical data
2. public wrapper
3. CV consumer
4. stop and reassess

If later grant-output mapping clearly earns its complexity, it should land as a
separate follow-on campaign slice rather than being smuggled into the first
funding model.
