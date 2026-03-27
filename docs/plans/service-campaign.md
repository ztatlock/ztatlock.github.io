# Service Campaign

Status: public-page core and CV service projection implemented; A4 redesign and
migration planning are now the leading direction; later homepage cleanup
remains deferred

## Goal

Establish a canonical service data source that removes repeated service facts
from the public service page first, while also giving later cross-cutting
homepage/CV cleanup a clean shared foundation.

## Why Service Next

Service is now the strongest next major shared-data domain because:

- the facts are already duplicated across three consumers:
  - `site/pages/service.dj`
  - `site/cv/index.dj`
  - `site/pages/index.dj`
- the domain is still fairly flat and regular even though it is more varied
  than teaching
- it already shows real cross-page drift, so canonicalization will improve
  correctness as well as maintenance
- it fits the same shared-data-first pattern that worked for students and
  teaching

That public-page core is now implemented:

- canonical service terms live in `site/data/service.json`
- the public service wrapper lives at `site/service/index.dj`
- the canonical public route is `/service/`

## Historical Pre-Slice-2 Surface Audit

### Public Service Page

`site/pages/service.dj` currently contains:

- 32 reviewing entries
- 21 organizing entries
- 8 mentoring entries
- 12 department entries
- 1 hand-authored Aggregators section

Important characteristics:

- reviewing and mentoring are mostly single-year flat entries
- department entries are mostly year ranges
- organizing mixes annual items, longer appointments, and externally linked
  events
- the page is almost entirely repeated structured content

### CV Service Section

Before the CV service projection slice, `site/cv/index.dj` duplicated the same
broad service surface, but not perfectly:

- 32 reviewing entries
- 22 organizing entries
- 8 mentoring entries
- 12 department entries

Important pre-CV-projection characteristics:

- the CV is slightly richer for some entries, especially links and supporting
  references
- the CV currently contains service facts missing from the public page
- the public page currently contains at least one service fact missing from the
  CV

Known pre-CV-projection drift:

- public page only: `2024 FPTalks Co-Organizer`
- CV only: `2022 - Present EGRAPHS Community Advisory Board`
- CV only: `2026 Dagstuhl Seminar 26022: EGRAPHS`

### Homepage Recent Service / Leadership

`site/pages/index.dj` currently contains:

- 6 curated recent service / leadership entries

Important characteristics:

- this view is not just “all recent service”
- it is a curated subset spanning multiple categories
- it should eventually derive from the same canonical service terms, but that
  consumer cleanup does not need to be part of the near-term service campaign

### Important Audit Constraint

The current service section headings are useful public views, but they are not
the whole ontology.

At least one service record currently belongs in more than one bucket:

- `2025 PLDI Program Committee Chair`
  - appears under `Reviewing`
  - also appears under `Organizing`

That means the canonical model should not be “top-level groups with one record
living in exactly one group.” It needs to support multi-group membership.

## Design Recommendation

Service should follow the students/teaching pattern more than the
talks/publications pattern:

- canonical truth in shared data under `site/data/`
- a thin public service wrapper at `site/service/index.dj`
- later cross-cutting renderers for the homepage and CV once more domains are
  canonicalized

Recommended target shape:

- canonical data: `site/data/service.json`
- public wrapper: `site/service/index.dj`
- canonical public route: `/service/`

This is intentionally not a bundle-root campaign.
Service records do not currently need per-record local prose, assets, or
detail routes.

## Historical Canonical Model Recommendation

This section is preserved as the historical model that originally powered the
implemented public/CV service projections.

It is now superseded as forward-looking redesign guidance by:

- [service-redesign-proposal-a4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a4.md)
- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)

So the flat per-year term model below is historical context, not the current
recommended destination.

## Historical Flat-Term Model Recommendation

The canonical model should be a flat ordered list of service terms rather than
top-level section buckets.

Recommended high-level shape:

- top-level ordered `records`
- each record is one service term for one year

Recommended record fields:

- `key`
  stable unique key for this exact term record
- optional `series_key`
  shared key for records that represent a longer appointment or recurring role
- `year`
  four-digit integer
- optional `ongoing`
  marks the latest currently open-ended term within a series so later renderers
  can collapse it to `Present`
- ordered `view_groups`
  current public/CV grouping buckets, drawn from:
  - `reviewing`
  - `organizing`
  - `mentoring`
  - `department`
- `title`
  event, committee, workshop, or role title without the year prefix
- optional `role`
  short role text such as `Co-Organizer`, `Program Committee`, or
  `Advisory Board Member`
- optional `url`
  primary public URL for the term
- optional ordered `details`
  small strings for richer CV/public renderers if needed later

Important design notes:

- `view_groups` are current view buckets, not a grand universal ontology
- a record may belong to multiple `view_groups`
- longer year ranges should be exploded into one record per year
- future renderers may collapse contiguous records with the same `series_key`
  back into ranges like `2026 - 2029`
- ongoing appointments can use a small explicit `ongoing` marker on the latest
  known term if a renderer wants to show `Present`
- homepage-selection metadata should be deferred until a later cross-cutting
  consumer phase unless slice-1 backfill proves it is unavoidable sooner

This keeps the model:

- queryable by year
- flexible across views
- simple enough to edit by hand
- extensible without overcommitting to a rigid taxonomy too early

## What Should Stay Hand-Authored

The campaign should not move everything into JSON.

The following should stay in wrappers unless a later slice clearly proves
otherwise:

- the service-page heading
- the public section headings
- the Aggregators section on the public page
- any future editorial commentary about service philosophy or leadership

## Recommended Slice Order

### Slice 1. Canonical Service Term Model

Implemented.

- add `site/data/service.json`
- add loader/validator tests
- backfill canonical term records for the current public service page, CV
  service section, and homepage recent-service slice as audit inputs
- stop before any projection

Invariant after slice 1:

- every intended service fact has one canonical per-year term record
- multi-group membership is explicit
- public/CV drift is captured and corrected in canonical data
- no public rendering has switched yet

### Slice 2. Public Service Wrapper / Route Cutover

Implemented.

- move the public wrapper to `site/service/index.dj`
- canonicalize `/service/`
- project the repeated public service blocks from `site/data/service.json`
- keep the Aggregators section hand-authored

Invariant after slice 2:

- `site/data/service.json` is the canonical service truth
- `/service/` is the canonical public service page
- repeated public service entries are no longer hand-maintained
- the public wrapper owns only framing and section structure

### Checkpoint After Slice 2

Stop and reassess after the public service page is canonicalized.

At that point:

- the service domain itself has a clean shared truth
- the public service page is no longer a second source of truth
- later homepage/CV reuse can be evaluated together with the other domains that
  are also approaching consumer-projection readiness

### Slice 3. CV Service Projection

- project the duplicated service subsection bodies in `site/cv/index.dj`
- preserve the intentionally more compressed CV view
- reuse canonical service range/ongoing semantics
- keep the faculty-skit prose note hand-authored in the CV

Implemented in:

- [cv-slice-4-service-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-slice-4-service-projection.md)

Implemented outcomes so far:

- the duplicated service subsection bodies in `site/cv/index.dj` now project
  from `site/data/service.json`
- the CV reuses canonical service range collapse and `Present` semantics
- the CV service section now includes the canonical `2024 FPTalks
  Co-Organizer` entry that was previously missing from the literal CV block
- the faculty-skit prose note remains hand-authored in the CV wrapper

## Deferred Follow-On Work

These should likely be treated as later cross-cutting consumer work rather
than part of the near-term service campaign:

- homepage recent-service projection from redesigned canonical service runs
- broader homepage/CV cleanup across multiple canonical domains once enough of
  the underlying sources of truth are in place
- implement the latched A4 service redesign before homepage recent-service
  projection depends more heavily on the current flat term model

The current redesign checkpoint is now:

- [service-redesign-proposal-a4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a4.md)

The current implementation/testing checkpoint is:

- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)

The next planned move is:

- slice 2 canonical data migration onto the A4 authored schema, after the
  slice-1 loader/validator foundation

If those later consumers land, the invariant should be:

- remaining variation is renderer policy and curation, not duplicated facts

## Deferred Questions

These are real possibilities, but they should not shape slice 1:

- richer taxonomy beyond the current `view_groups`
- explicit `leadership` or other cross-cutting tags
- people-linked co-organizers or committees tied into `site/data/people.json`
- academic-year versus calendar-year nuance beyond plain integer `year`
- explicit homepage-selection metadata if and when homepage projection becomes
  part of a later cross-cutting consumer phase
- service-specific detail pages or local assets
