# Service Redesign Proposal A2

Status: draft

It builds on:

- [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)
- [service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [homepage-cv-curated-consumers-slice-3-service-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit-notes.md)

## Purpose

This is a refinement of Proposal A, not a different conceptual direction.

The goal is:

- keep Proposal A's winning semantics:
  - canonical `series`
  - canonical `run`
  - atomic `instance`
- while making the authored JSON materially:
  - more compact
  - more self-contained
  - easier to diff
  - easier to review
  - less cross-referential in the common cases

The main idea is:

- keep one rich normalized in-memory model
- allow several lighter authored shorthand forms
- have the loader/validator rehydrate all of them into the same canonical
  semantic model

So A2 changes the **physical JSON representation** much more than the
underlying **conceptual model**.

## Recommendation

Adopt a **progressive-shorthand physical JSON format**.

The top-level file would be one ordered `records` array.

Each top-level record may use one of three authored forms:

1. `singleton`
2. `single-run series shorthand`
3. `explicit series with runs`

All three forms normalize to the same canonical semantic model:

- optional `series`
- one or more `run`s
- one or more atomic `instance`s inside each run

This preserves the part of Proposal A that matters most:

- runs are still canonical visible units
- run anchors are still stable and authored
- recurring identity is still explicit
- non-contiguous runs are still explicit
- multi-view placement is still explicit

But it avoids forcing every simple case to spell all three layers out
independently.

## Why A2 Is Better Than A1

Proposal A1 was strongest on semantics, but weakest on physical ergonomics.

Its main practical costs were:

- separate top-level `series` and `runs` arrays
- more cross-referencing during review
- singletons paying too much ceremony
- single-run series looking heavier than they need to
- explicit `instance.key` on every ordinary case

A2 keeps the same long-horizon semantic bets, but fixes most of those costs:

- singletons stay flat
- ordinary recurring service looks much closer to
  [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- only genuinely multi-run or metadata-heavy cases pay the full explicit cost
- common edits become "find the block, add the year" again
- the loader still produces the same richer semantic model for consumers

## Canonical Semantics After Loading

Regardless of authored form, the loader normalizes the file into the same
semantic model.

### Canonical `series`

`series` is optional recurring identity.

It exists when a record represents a recurring service lane such as:

- `FPTalks`
- `PLDI Workshops`
- `PACMPL Advisory Board`
- `UW CSE Undergraduate Admissions Committee`

### Canonical `run`

`run` is the canonical visible grouped unit.

It is what consumers should use for:

- `/service/` visible bullets
- stable internal anchors
- homepage recent-service selection
- any future grouped summaries

### Canonical `instance`

`instance` is the atomic fact layer.

It preserves:

- exact year-local participation
- instance-specific URLs
- instance-specific details
- instance-level title or role overrides when they are genuinely needed

## Authored Top-Level Shape

The authored file should be one ordered array:

```json
{
  "records": [
    { "...": "singleton or series record" }
  ]
}
```

Top-level record order is canonical and meaningful.
It is the final deterministic tie-break when more semantic ordering rules do
not decide a result.

## Authored Form 1: Singleton

This is the lightest form.
It is for true one-off service facts that do not belong to a recurring series.

### Example

```json
{
  "key": "2026-dagstuhl-seminar-26022-egraphs",
  "year": 2026,
  "view_groups": ["organizing"],
  "title": "Dagstuhl Seminar 26022: EGRAPHS",
  "url": "https://www.dagstuhl.de/26022",
  "details": [
    "[Seminar Details](https://www.dagstuhl.de/en/seminars/seminar-calendar/seminar-details/26022)",
    "[Dagstuhl News](https://www.dagstuhl.de/en/institute/news/2026/dagstuhl-egraphs-2026)"
  ]
}
```

### Intended Semantics

A singleton record is shorthand for:

- no explicit `series`
- one implicit canonical `run`
- one implicit canonical `instance`

### Field Meaning In This Form

- `key`
  becomes the canonical run key and the public anchor id
- `year`
  belongs to the implicit atomic instance
- `view_groups`
  belong to the implicit run
- `anchor_view_group`
  if present, belongs to the implicit run
- `title`
  belongs to the implicit run
- `role`
  if present, belongs to the implicit run
- `url`
  belongs to the implicit instance
- `details`
  belong to the implicit instance
- `time_basis`
  if present, belongs to the implicit run
- `ongoing`
  if present, belongs to the implicit run

This keeps one-off records physically flat while still preserving the richer
run/instance split after loading.

## Authored Form 2: Single-Run Series Shorthand

This is the common recurring case.

It is for a recurring identity that currently has one canonical run and does
not need an explicitly separate series metadata block yet.

### Example

```json
{
  "key": "fptalks",
  "title": "FPTalks",
  "role": "Co-Organizer",
  "view_groups": ["organizing"],
  "instances": [
    { "year": 2025, "url": "https://fpbench.org/talks/fptalks25.html" },
    { "year": 2024, "url": "https://fpbench.org/talks/fptalks24.html" },
    { "year": 2023, "url": "https://fpbench.org/talks/fptalks23.html" }
  ]
}
```

### Intended Semantics

A single-run series shorthand record is shorthand for:

- one canonical `series`
- one implicit canonical `run`
- one or more canonical `instance`s inside that run

### Field Meaning In This Form

- `key`
  becomes the canonical `series.key`
  and also the implicit run key
- `title`
  becomes the canonical `series.title`
- `view_groups`
  belong to the implicit run
- `anchor_view_group`
  if present, belongs to the implicit run
- `time_basis`
  if present, belongs to the implicit run
- `ongoing`
  if present, belongs to the implicit run
- `role`
  if present, belongs to the implicit run
- `url`
  if present, belongs to the implicit run
- `details`
  if present, belong to the implicit run
- `instances`
  become the canonical instance list inside that implicit run

### Why This Split

This form is intentionally opinionated:

- it gives the record an explicit recurring identity
- but it keeps the physical JSON close to the lived editing experience
- it avoids forcing the common one-run recurring case to spell both a series
  block and a run block separately

It also keeps the top-level record self-contained, which produces cleaner diffs
and simpler reviews.

### Important Constraint

In this shorthand form, only `title` is treated as true series metadata.

If a recurring identity needs:

- distinct series-level `url`
- distinct series-level `role`
- distinct series-level `details`
- more than one run
- or an explicit run title separate from the series title

then the record should expand into the explicit series form below.

That is a feature, not a bug:

- ordinary cases stay compact
- more complex cases pay for more structure only when they truly need it

## Authored Form 3: Explicit Series With Runs

This is the fully explicit form.

It is for any recurring identity that needs:

- multiple runs
- explicit separation between series-level and run-level metadata
- stable authored run keys beyond the series key
- or more complex multi-view / run-level semantics

It is also allowed for single-run recurring identities when the shorthand form
would hide real structure or metadata ownership.

### Example

```json
{
  "key": "pnw-plse",
  "title": "PNW PLSE",
  "url": "http://pnwplse.org/",
  "runs": [
    {
      "key": "pnw-plse-return",
      "view_groups": ["organizing"],
      "role": "Co-Organizer",
      "instances": [
        { "year": 2023 }
      ]
    },
    {
      "key": "pnw-plse-foundation",
      "view_groups": ["organizing"],
      "role": "Organizer",
      "instances": [
        { "year": 2018 }
      ]
    }
  ]
}
```

### Intended Semantics

This form maps almost directly onto the canonical loaded model:

- one explicit canonical `series`
- one or more explicit canonical `run`s
- one or more canonical `instance`s inside each run

### Field Meaning In This Form

Top-level fields belong to the canonical `series`:

- `key`
- `title`
- optional `url`
- optional `role`
- optional `details`

Nested run fields belong to each canonical `run`:

- `key`
- `view_groups`
- optional `anchor_view_group`
- optional `title`
- optional `role`
- optional `url`
- optional `details`
- optional `time_basis`
- optional `ongoing`
- `instances`

Nested instance fields belong to the canonical `instance`:

- `year`
- optional `key`
- optional `title`
- optional `role`
- optional `url`
- optional `details`

## Why Runs Are Still Canonical In A2

This is the part A2 does **not** compromise.

Runs remain canonical because they solve the hardest requirements directly:

- stable visible-unit identity
- stable homepage internal targets
- non-contiguous service without fake continuous ranges
- run-level metadata when it is real
- per-run section membership
- per-run anchor placement for multi-view rendering

A2 only changes how the authored JSON gets there.
It does not retreat to derived runs.

## Run Keys And Anchor Semantics

Proposal A's refined run-key discipline still applies unchanged in A2.

### Run Key Rules

- every canonical run has a stable authored key
- singleton runs reuse the top-level record key
- single-run series shorthand records reuse the top-level series key as their
  implicit run key
- explicit additional runs must have explicit authored keys
- run keys should not encode exact year boundaries
- run keys should not be renamed merely because a run grows under backfill

Recommended style:

- `fptalks`
- `pnw-plse-return`
- `uw-cse-undergraduate-admissions-early`
- `uw-cse-undergraduate-admissions-recent`

Avoid:

- `fptalks-2020-2025`
- `pnw-plse-2018`
- `undergrad-admissions-2020-2021`

### Anchor Rules

- every canonical run owns exactly one canonical internal anchor
- that anchor id is always the canonical run key
- `/service/` attaches the id only on that run's `anchor_view_group`
  occurrence, or on its sole section occurrence when the anchor view is
  implied
- other rendered copies of the same run in other sections do not get duplicate
  ids
- homepage and other internal consumers link to `/service/#<run.key>`

This preserves the strongest part of Proposal A while letting the common JSON
shapes stay compact.

## Instance Keys In A2

A2 relaxes Proposal A1 here.

### Recommendation

`instance.key` should be optional in authored JSON.

It should be required only when the record really needs it.

### When Explicit `instance.key` Is Required

- same-year multiplicity within one run
- a future consumer needs to reference one specific instance directly
- a future migration/import tool needs durable authored instance identity for a
  specific case

### When It Can Be Omitted

Ordinary cases like:

```json
{ "year": 2025, "url": "..." }
```

should stay that simple.

### Loader Rule

If a run has unique years across its instances and an instance omits `key`,
the loader may synthesize a deterministic internal instance id from:

- the containing canonical run key
- the instance year

If a run contains multiple instances with the same year, explicit instance keys
become required for those ambiguous instances.

This keeps the authored JSON light while still preserving deterministic loaded
identity.

## Validation Rules

The loader/validator should enforce a small number of strong shape rules.

### Top-Level Record Shape

A top-level record must have exactly one of:

- `year`
- `instances`
- `runs`

Interpretation:

- `year` => singleton
- `instances` => single-run series shorthand
- `runs` => explicit series with runs

### Required Top-Level Fields

All top-level records require:

- `key`
- `title`

Additional requirements by form:

- singleton:
  - `year`
  - `view_groups`
- single-run series shorthand:
  - `instances`
  - `view_groups`
- explicit series:
  - `runs`

### Field Restrictions By Form

If a top-level record has `runs`:

- top-level `view_groups` is forbidden
- top-level `anchor_view_group` is forbidden
- top-level `time_basis` is forbidden
- top-level `ongoing` is forbidden

Those belong on explicit runs instead.

### Multi-View Rule

For any canonical run:

- if resolved `view_groups` length is `1`, `anchor_view_group` is implied
- if resolved `view_groups` length is greater than `1`,
  `anchor_view_group` is required
- `anchor_view_group` must be one of that run's `view_groups`

### Ordering Rules

- top-level record order is canonical
- explicit run order inside a series is canonical
- instance order inside a run is canonical
- those array orders are the final tie-break wherever stronger semantic
  ordering rules do not already decide the result

## Consumer Semantics

### Public `/service/`

After normalization, the public service page should consume canonical `run`s.

That means:

- section filtering works over run-level membership
- anchors attach at run level
- grouped summary labels come from runs
- instance sub-bullets can expand only where they materially help

The service page should never need to care which authored shorthand form
produced the canonical run.

### Homepage `Recent Service / Leadership`

The homepage should also select from canonical `run`s, not raw instances.

That preserves the behavior we want:

- one visible unit per appointment/run
- stable internal link targets when needed
- no fake flattening of recurring service

Link rule remains:

- if the selected run resolves to one unambiguous direct URL, link directly
- if linking directly would be lossy or ambiguous because multiple distinct
  instance URLs matter, link to the run's `/service/` anchor instead
- if there is no resolved URL, render the summary unlinked

### CV

The CV can also consume canonical runs.

That keeps the CV logic simple even though the physical JSON can stay compact.

## Worked Examples

### Multi-View Singleton

```json
{
  "key": "2025-pldi-program-committee-chair",
  "year": 2025,
  "title": "PLDI Program Committee Chair",
  "view_groups": ["organizing", "reviewing"],
  "anchor_view_group": "organizing",
  "url": "https://pldi25.sigplan.org/track/pldi-2025-papers",
  "details": [
    "[Proceedings](https://dl.acm.org/doi/proceedings/10.1145/3729317)"
  ]
}
```

Why singleton form is enough:

- it is a one-off fact
- it needs multi-view anchor placement
- it does not need recurring identity or multiple runs

### Single-Run Series Shorthand

```json
{
  "key": "uw-faculty-skit",
  "title": "UW Faculty Skit",
  "role": "Writer, Producer, and Director",
  "view_groups": ["department"],
  "details": [
    "Collaborated with [Dan Grossman][], [Maggie Delano][], [Yoshi Kohno][], [James Fogarty][], and others."
  ],
  "instances": [
    { "year": 2025 },
    { "year": 2024 },
    { "year": 2023 }
  ]
}
```

Why shorthand is good here:

- one run
- clear recurring identity
- run-level role/details shared across instances
- no need yet for separate series-level metadata

### Explicit Series With One Run

```json
{
  "key": "pacmpl-advisory-board",
  "title": "PACMPL Advisory Board",
  "url": "https://www.sigplan.org/OpenTOC/pacmpl/",
  "role": "Member",
  "runs": [
    {
      "key": "pacmpl-advisory-board",
      "view_groups": ["reviewing"],
      "ongoing": true,
      "instances": [
        { "year": 2029 },
        { "year": 2028 },
        { "year": 2027 },
        { "year": 2026 }
      ]
    }
  ]
}
```

Why explicit form is justified even with one run:

- the series-level landing page is real metadata
- the recurring role is truly series-level
- keeping that separate from the run is cleaner than overloading the shorthand

### Explicit Multi-Run Series

```json
{
  "key": "uw-cse-undergraduate-admissions-committee",
  "title": "UW CSE Undergraduate Admissions Committee",
  "runs": [
    {
      "key": "uw-cse-undergraduate-admissions-recent",
      "view_groups": ["department"],
      "instances": [
        { "year": 2021 },
        { "year": 2020 }
      ]
    },
    {
      "key": "uw-cse-undergraduate-admissions-early",
      "view_groups": ["department"],
      "instances": [
        { "year": 2018 },
        { "year": 2017 }
      ]
    }
  ]
}
```

Why explicit runs matter:

- the service is non-contiguous
- the visible runs should remain stable under backfill
- homepage/internal links may need to target one run, not the whole series

## Migration Sketch

From the current flat record model:

1. Leave true one-offs as singleton records.
2. Collapse single-run `series_key` groups into shorthand series records.
3. Expand non-contiguous or metadata-heavy recurring identities into explicit
   series-with-runs records.
4. Keep all consumer code working over the normalized canonical run model.

So the migration cost is mostly:

- moving canonical facts into better local blocks
- choosing stable run keys where explicit runs are needed
- not inventing a wholly different consumer model

## Why A2 Is The Best Current Candidate

It preserves the strongest part of Proposal A:

- canonical visible runs

while borrowing the best physical-JSON instincts from the lighter alternatives:

- self-contained records
- compact common cases
- teaching-like co-location for recurring identities
- less ceremony for singletons

So A2 is not a compromise that weakens the model.
It is Proposal A with a better authored surface.

## Open Questions

This proposal is much tighter than A1, but a few choices still deserve review
before implementation:

- whether shorthand single-run series should ever allow explicit series-level
  metadata beyond `title`, or whether requiring expansion is the cleaner rule
- the best exact style guidance for authored run keys
- whether the loader should expose synthesized instance keys publicly anywhere,
  or keep them entirely internal

Those are now narrow questions.
They do not change the main recommendation.
