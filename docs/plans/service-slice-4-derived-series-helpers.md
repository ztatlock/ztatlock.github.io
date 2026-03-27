# Service Slice 4: Derived Series Helpers

Status: draft alternative

It builds on:

- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [homepage-cv-curated-consumers-slice-3-service-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md)
- [homepage-cv-curated-consumers-slice-3-service-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit-notes.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

This note records the strongest current-model-preserving alternative.
The cleaner long-horizon redesign candidate is now documented separately in
[service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md).

## Goal

Keep canonical service data as flat per-year instance records in
[site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json),
but add a richer **derived series view** in code so service consumers no longer
have to choose between:

- over-collapsing recurring service into one lossy summary line
- or over-splitting recurring service only because instance URLs differ

This slice should:

- preserve the current canonical service instance model
- add a cleaner derived series/helper layer over those instances
- support richer grouped rendering on `/service/`
- give later homepage service projection a stable derived input

It should not:

- add an explicit top-level `series` registry to `site/data/service.json`
- require every service record to belong to a series
- change homepage service yet
- solve all service styling/polish questions

## Design Direction

The current canonical model already gives us the right unit of truth:

- one service **instance** per year-term-like fact

The current design pressure comes from recurring service where a series clearly
exists, but only implicitly through `series_key`.

This slice therefore keeps:

- canonical `ServiceRecord` instances as the only data-layer truth

and adds:

- a derived `ServiceSeriesView` layer in code
- a derived contiguous-run layer inside each series

That keeps the data model simple while making series-like structure explicit
where consumers actually need it.

## Why This Instead Of An Explicit Series Registry

The audit has already surfaced legitimate unease about the halfway status of
`series_key`.

But an explicit series registry would immediately introduce more abstraction:

- another layer of identifiers
- optional per-series metadata rules
- edge cases for one-off entries
- questions about what belongs on the series vs the instances

The current recommendation is to stop one step short of that and try a richer
derived helper first.

If that helper proves insufficient later, the repo can still add an explicit
series layer from a more informed position.

## Recommended Derived Shape

Keep the existing canonical dataclass:

- `ServiceRecord`

Add a derived series-oriented structure in code, for example:

- `ServiceSeriesView`
- `ServiceSeriesRunView`
- `ServiceSeriesInstanceView`

Recommended series-view fields:

- `series_identity`
  - derived from `series_key` when present
  - otherwise singleton identity from the instance key
- `title`
  series-facing title
- `view_groups`
  union or stable shared set for the series in the requested view
- `instances`
  ordered instance views
- `is_singleton`
- `runs`
  ordered contiguous runs inside the series

Recommended run-view fields:

- `series_identity`
- `run_start_year`
- `run_end_year`
- `is_ongoing`
- `instances`
  ordered instance views inside the run
- `has_uniform_role`
- optional `uniform_role`
- `has_uniform_url`
- optional `uniform_url`
- `year_summary`
  renderer-facing date summary such as:
  - `2020 - 2025`
  - `2022 - Present`
  - `2025`
- `summary_anchor`
  stable renderer-facing anchor id:
  - single-run series -> likely `series_key`
  - multi-run series -> likely `series_key--START-END`
  - singleton non-series record -> record `key`

Recommended instance-view fields:

- `key`
- `year`
- `title`
- optional `role`
- optional `url`
- `details`

This keeps the exact per-instance facts intact while making derived series and
run summary properties explicit and testable.

## Grouping Rules

Recommended grouping rules for the derived series helper:

1. If `series_key` is present, all matching records belong to the same derived
   series.
2. If `series_key` is absent, the instance becomes a singleton series.
3. Do **not** split a derived series only because instance `url` differs.
4. Do **not** split a derived series only because instance `role` differs.
5. Preserve exact per-instance URL/role variation inside `instances`.
6. Partition each derived series into contiguous year runs.

This is the key difference from the current grouped public view helper, which
effectively splits on `url`, `role`, and `details`.

## Summary Rules

The derived helper should compute summary fields conservatively, primarily at
the run level.

Recommended rules:

- if all run instances share the same role, expose `uniform_role`
- otherwise leave summary role unset and rely on instance roles
- if all run instances share the same URL, expose `uniform_url`
- otherwise leave summary URL unset and rely on instance URLs
- if run years are contiguous:
  - show a normal range summary
- if the latest run is ongoing:
  - allow `Present`
- do not fabricate a whole-series summary range across non-contiguous runs

This avoids generating misleading whole-series summaries.

One important interpretation note:

- a displayed year range such as `2020 - 2021` is sometimes best understood as
  an academic-year span rather than literal full-calendar-year coverage
- this is especially true for Allen School and similar academic service

This slice should therefore treat `year_summary` as a renderer-facing summary
label, not as a promise of exact month-level temporal semantics.

Recommended summary-label rules:

- if the run has a uniform role and a useful year summary:
  - render `title role, year_summary`
- if the run has no uniform role but a useful year summary:
  - render `title, year_summary`
- if the run is a single instance with a role:
  - render `title year, role`
- if the run is a single instance without a role:
  - render `title year`

Examples:

- `FPTalks Co-Organizer, 2020 - 2025`
- `PACMPL Advisory Board Member, 2026 - 2029`
- `PLDI Steering Committee, 2026 - 2029`
- `PNW PLSE 2023, Co-Organizer`

## Rendering Implications

### Public Service Page

The current leading design candidate is:

- one grouped summary line per visible run
- plus instance sub-bullets when the run has meaningful per-instance variation
  or year-specific URLs

Important render rules:

- prefer year-last phrasing:
  - `FPTalks 2025`
  - `PLDI Workshops 2024`
  - not `2025 FPTalks`
- do not use bare years as sub-bullets
- repeat enough context for each instance bullet to read well on its own
- when role matters, repeat it in each instance bullet
- use the grouped summary line for run-level context
- if a visible run has multiple distinct instance URLs, keep the grouped
  summary line unlinked on `/service/` and let instance bullets carry the
  external links
- if a visible run has one uniform URL, the grouped summary line may link
  directly to that URL

Preferred instance-bullet shape:

- `[FPTalks 2025](...)`, `Co-Organizer`
- `[FPTalks 2024](...)`, `Co-Organizer`
- `[PLDI Workshops 2024](...)`, `Co-chair`
- `[PNW PLSE 2023](...)`, `Co-Organizer`

Representative future public-service shape:

- `FPTalks Co-Organizer, 2020 - 2025`
  - `[FPTalks 2025](...)`, `Co-Organizer`
  - `[FPTalks 2024](...)`, `Co-Organizer`
  - `[FPTalks 2023](...)`, `Co-Organizer`

- `PLDI Workshops Co-chair, 2023 - 2024`
  - `[PLDI Workshops 2024](...)`, `Co-chair`
  - `[PLDI Workshops 2023](...)`, `Co-chair`

Stable long-running appointments with no per-instance URL pressure could remain
simple single-line summaries, such as:

- `PLDI Steering Committee, 2026 - 2029`
- `EGRAPHS Community Advisory Board, 2022 - Present`

Non-contiguous series with meaningful instance variation could instead render
as:

- `PNW PLSE`
  - `PNW PLSE 2023, Co-Organizer`
  - `PNW PLSE 2018, Organizer`

### Homepage

The homepage should consume the same derived series/run view differently.

The likely later policy is:

- select one item per derived series
- no instance sub-bullets
- select a specific visible run for each included series
- if the included series has multiple distinct instance URLs:
  - link the homepage entry to the corresponding `/service/` run anchor
- if the included series is a singleton or all of its instances share one URL:
  - link directly to that URL when present
- otherwise leave the entry unlinked
- for contiguous long-running appointments, show the selected run summary line
- for non-contiguous series, prefer the latest run or latest instance instead
  of a misleading fake range

That keeps the homepage compact while letting the public service page be richer.

Recommended homepage examples:

- `PLDI Steering Committee, 2026 - 2029`
- `PACMPL Advisory Board Member, 2026 - 2029`
- `FPTalks Co-Organizer, 2020 - 2025`
  links to `/service/#fptalks`
- `PNW PLSE 2023, Co-Organizer`
  links directly to `http://pnwplse.org/`

## What This Slice Establishes

After this slice:

- canonical service truth still lives only in per-instance records
- the repo has an explicit derived series layer in code
- service renderers no longer need to smuggle series semantics through ad hoc
  grouping signatures
- later homepage service projection can depend on one stable derived input

## Code Shape

I would recommend introducing a new dedicated helper module rather than stuffing
more semantics into
[scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py).

Likely surfaces:

- new module, likely:
  - `scripts/service_series.py`
  or
  - `scripts/service_view.py`
- [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)
  updated to consume the new helper
- [tests/test_service_index.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_service_index.py)
- likely new focused tests such as:
  - `tests/test_service_series.py`

I would prefer `scripts/service_series.py` because the series idea is exactly
what we are trying to make explicit.

## Test Strategy

This slice should add focused tests for:

- singleton entries remaining valid series views
- recurring series with:
  - uniform role and varying URL
  - varying role and uniform URL
  - contiguous years
  - non-contiguous years
  - ongoing latest instance
- run partitioning:
  - one-run series
  - multi-run series
- summary field derivation:
  - `uniform_role`
  - `uniform_url`
  - run-level year summary behavior
- public-service renderer consuming the new helper without losing facts
- anchor derivation:
  - one-run series -> `series_key`
  - multi-run series -> `series_key--START-END`
  - singleton entry -> record `key`
- homepage link policy:
  - varying URLs across included series -> internal `/service/` run anchor target
  - singleton or series-uniform URL -> direct external target

## Deliberate Non-Goals

This slice should not:

- redesign `/service/` styling yet
- decide the final homepage recent-service selection policy
- add explicit series metadata to `site/data/service.json`
- force every recurring title into one unified summary line
- introduce month- or term-level service timing semantics
- normalize every role string proactively

## Follow-On Slices

If this works, the next slices become much clearer:

1. service-page rendering follow-on
   - use the derived series helper for grouped summary + instance sub-bullets
2. homepage recent-service projection
   - select from derived series rather than from raw service records
3. later styling/polish
   - make the richer service rendering easier to scan visually
