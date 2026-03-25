# Funding Campaign

Status: planning

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

Current explicit funding surface:

- `site/cv/index.dj`
  currently contains `10` funding entries under `## Funding`

Current funding-entry shape in the CV:

- title
- role
- sponsor
- optional award identifier embedded in sponsor text
- dollar amount
- year range

Current related surfaces:

- `site/pages/research.dj`
  mentions projects that may later benefit from funding associations
- `site/pubs/`
  already contains canonical publication bundles that may later benefit from
  related-grant links

Important current constraint:

- there is no public funding page yet
- there is no canonical funding data file yet
- there is no current structured association between grants and projects or
  publications

## Design Recommendation

Funding should follow the shared-data pattern used for students, teaching, and
service:

- canonical shared data under `site/data/funding.json`
- a thin public wrapper at `site/funding/index.dj`
- later downstream CV/homepage consumers only if they clearly earn their keep

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

Planned.

- add `site/data/funding.json`
- add loader and validator tests
- backfill the current intended funding facts from the CV
- stop before any public rendering cutover

Invariant after slice 1:

- `site/data/funding.json` is the canonical funding fact source
- every intended current funding fact is represented exactly once
- no public page or CV rendering has switched yet
- no grant-output associations are modeled yet

### Slice 2. Public Funding Wrapper / Route Cutover

Planned.

- add `site/funding/index.dj`
- canonicalize `/funding/`
- project repeated funding records from `site/data/funding.json`
- keep page framing hand-authored

Invariant after slice 2:

- the public funding page is a thin wrapper over canonical funding records
- the canonical public route is `/funding/`
- no second funding fact source exists in the wrapper
- CV funding remains hand-authored for now

## Deferred Work

The following should remain explicitly out of the first funding campaign
checkpoint:

- CV funding projection
- homepage funding/highlights consumers
- grant-to-publication associations
- grant-to-project associations
- sponsor normalization or a funder registry
- funding totals, charts, or analytics views

Those may become worthwhile later, but they should not complicate the base
funding architecture.

## Recommendation

Start funding with the smallest real architecture:

1. canonical data
2. public wrapper
3. stop and reassess

If later grant-output mapping clearly earns its complexity, it should land as a
separate follow-on campaign slice rather than being smuggled into the first
funding model.
