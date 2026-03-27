# Service Redesign Proposal

Status: draft

It builds on:

- [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [homepage-cv-curated-consumers-slice-3-service-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit-notes.md)

## Recommendation

The cleanest long-horizon design is a **three-level model**:

1. `series`
   optional recurring identity and future higher-level metadata
2. `runs`
   the primary visible grouped units used by `/service/` and homepage links
3. `instances`
   the atomic year-local service facts

This is the first design I think actually resolves most of the current seams
cleanly without forcing renderer code to keep inventing structure.

## Why This Model

The current flat per-year record model made sense as an initial canonicalization
step, but it is now under pressure from too many directions at once:

- recurring identities exist and need stable names
- non-contiguous runs exist and need stable anchors
- homepage wants to link to visible grouped entries, not to arbitrary raw facts
- public `/service/` wants grouped summaries and optional instance expansion
- details and URLs can belong at different levels
- some facts live in more than one rendered section

The proposed model separates those concerns explicitly:

- `instance` is for truth
- `run` is for visible grouped presentation
- `series` is for recurring identity and future higher-level metadata

That means:

- no more pretending that one flat record layer can serve every consumer
- no more forcing renderers to reconstruct runs from implicit conventions
- no more fragile anchor rules based only on `series_key` or year ranges

## Design Principles

### 1. Make The Visible Unit Explicit

The public service page and homepage both need a stable visible unit.

That unit should be `run`, not:

- raw instance
- ad hoc grouped tuple
- or whole recurring series

Why `run`:

- it is anchorable
- it can be rendered in one line
- it can carry section membership
- it can expand into per-instance bullets
- it survives non-contiguous recurring service naturally

### 2. Keep Atomic Facts Atomic

An `instance` remains the smallest intended fact:

- a year-local participation
- optional year-local URL
- optional year-local details
- optional year-local title or role override

That preserves accuracy and future auditability.

### 3. Let Recurring Identity Exist Explicitly

A `series` should exist as an optional first-class object.

This solves the current halfway problem where `series_key` already implies a
real recurring identity but has no explicit home for metadata or validation.

The key point is:

- not every run needs a series
- not every instance needs a series
- but when recurring identity matters, it should be explicit

### 4. Keep The Model Hand-Editable

The redesign should stay understandable in JSON review.

That means:

- no hidden code-generated identifiers
- no deeply nested derived-only structures in canonical data
- no attempt to encode renderer quirks directly into the schema

## Proposed Canonical Shape

```json
{
  "series": [
    {
      "key": "fptalks",
      "title": "FPTalks"
    }
  ],
  "runs": [
    {
      "key": "fptalks-2020-2025",
      "series": "fptalks",
      "title": "FPTalks",
      "role": "Co-Organizer",
      "view_groups": ["organizing"],
      "primary_view_group": "organizing",
      "instances": [
        {
          "key": "fptalks-2025",
          "year": 2025,
          "url": "https://fpbench.org/talks/fptalks25.html"
        },
        {
          "key": "fptalks-2024",
          "year": 2024,
          "url": "https://fpbench.org/talks/fptalks24.html"
        }
      ]
    }
  ]
}
```

The top-level canonical units are:

- `series`
- `runs`

`instances` live inside `runs`, because runs are the grouped visible units that
actually own them.

## `series`

### Purpose

`series` captures recurring identity.

It is the place for facts that are true about the broader recurring lane of
service and not reducible to one run or one instance.

Examples:

- `FPTalks`
- `PNW PLSE`
- `PACMPL Advisory Board`
- `UW CSE Undergraduate Admissions Committee`

### Required Fields

- `key`
- `title`

### Optional Fields

- `url`
  stable higher-level URL when one exists
- `details_djot`
  higher-level notes that belong to the recurring identity as a whole
- `title_short`
  optional future override if a shorter consumer-facing label is ever useful

### Design Notes

- a `series` may have one run or many runs
- a `series` may have no URL
- a `series` does not own `view_groups`
  those belong to visible runs
- a `series` does not need its own role by default
  roles are more naturally run- or instance-local

## `run`

### Purpose

`run` is the primary visible grouped unit.

It is the thing that should map most directly to:

- one visible bullet on `/service/`
- one stable internal anchor
- one homepage recent-service candidate

Examples:

- `FPTalks Co-Organizer, 2020 - 2025`
- `PACMPL Advisory Board Member, 2026 - 2029`
- `PNW PLSE 2023, Co-Organizer`
- `UW CSE Undergraduate Admissions Committee, 2020 - 2021`

### Required Fields

- `key`
  stable visible-unit identity
- `title`
  run-level display title
- `view_groups`
  rendered sections where this run appears
- `primary_view_group`
  canonical section for anchors and internal links
- `instances`
  ordered array of one or more instance objects

### Optional Fields

- `series`
  reference to parent recurring identity
- `role`
  run-level role when uniform across instances
- `url`
  stable run-level URL when one exists
- `details_djot`
  run-level notes/details
- `ongoing`
  marks the latest open-ended run
- `time_basis`
  optional summary-semantics hint such as:
  - `calendar_year`
  - `academic_year`
  - `event_year`

### Why `primary_view_group`

This is one of the main simplifications in the proposal.

Current service data already has multi-view facts such as:

- `2025 PLDI Program Committee Chair`
  in both `reviewing` and `organizing`

So a visible run may appear in multiple rendered sections.

`primary_view_group` gives the model one canonical home for:

- stable anchor attachment
- homepage internal links
- any future reverse links or popups

That avoids ambiguous “which copy on `/service/` should the homepage link to?”
logic.

### Why `key` Lives On Runs

Run keys solve the biggest current anchor problem.

Stable anchors should be based on stable run identity, not on:

- whole-series identity
- or fragile derived `START-END` suffixes

If a future run grows because of backfill, the run key stays the same.
If a future series gets a second or third run, the run keys still stay stable.

### Ordering

`runs` should be in canonical order in the file.

That order becomes the deterministic fallback tie-break for:

- `/service/` section rendering
- homepage recent-service selection
- any future run lists

The repo does not need a numeric `sort_key` until a real case proves it is
necessary.

## `instance`

### Purpose

`instance` is the atomic fact layer.

It records exact service participation facts without forcing the visible page
structure to be flat.

### Required Fields

- `key`
- `year`

### Optional Fields

- `title`
  instance-specific override when the run title is not sufficient
- `role`
  instance-specific override when the run role is not sufficient
- `url`
  instance-specific primary URL
- `details_djot`
  instance-specific supporting details

### Design Notes

- most instances will probably omit `title` and `role` and inherit the run’s
  title/role semantically
- if a run has many per-year URLs, those live here
- if an instance has distinct supporting links, those live here
- instance order inside a run is canonical and should usually be newest first

## Field Ownership Rules

This is the heart of the simplicity story.

### Title

- `series.title`
  broad recurring identity label
- `run.title`
  visible summary label base for that run
- `instance.title`
  only when one instance needs a different label

### Role

- `run.role`
  when the visible run has one stable role
- `instance.role`
  only when that instance differs from the run role

There should be no default `series.role` in the initial redesign.

### URL

- `series.url`
  only for stable series-level landing pages
- `run.url`
  when one URL applies to the whole visible run
- `instance.url`
  when URLs differ year by year or instance by instance

### Details

- `series.details_djot`
  facts true of the whole recurring identity
- `run.details_djot`
  facts true of the whole visible run
- `instance.details_djot`
  facts true only of one instance

This resolves the current ambiguity around things like:

- `UW Faculty Skit`
- `2025 PLDI Program Committee Chair`
- `Dagstuhl Seminar 26022: EGRAPHS`

## Rendering Semantics

### Public `/service/`

The public service page should render from `runs`.

Default behavior:

- filter runs by section membership
- render one summary line per run
- attach the anchor only on the `primary_view_group` occurrence
- if the run has meaningful per-instance variation, render instance sub-bullets

That gives:

- stable sectioned rendering
- stable anchors
- no forced fake flattening of recurring service

### Homepage

The homepage should also render from `runs`.

Recent-service policy can later choose among runs, not raw instances.

Link behavior becomes simple:

- if the selected run has a stable direct URL:
  link directly
- if the run instead contains multiple distinct instance URLs:
  link to the run’s `/service/` anchor
- if no URL exists:
  leave it unlinked

That satisfies the current requirement without special-case derivation hacks.

### CV

The CV can also consume `runs`.

Because runs are already the visible grouped units, the CV can:

- compress them further
- reuse run summary labels
- optionally ignore instance expansion

## How Current Stress Cases Fit

### `FPTalks`

```json
{
  "series": [
    {
      "key": "fptalks",
      "title": "FPTalks"
    }
  ],
  "runs": [
    {
      "key": "fptalks-2020-2025",
      "series": "fptalks",
      "title": "FPTalks",
      "role": "Co-Organizer",
      "view_groups": ["organizing"],
      "primary_view_group": "organizing",
      "instances": [
        { "key": "fptalks-2025", "year": 2025, "url": "..." },
        { "key": "fptalks-2024", "year": 2024, "url": "..." },
        { "key": "fptalks-2023", "year": 2023, "url": "..." }
      ]
    }
  ]
}
```

Benefits:

- one recurring identity
- one visible run
- one stable anchor
- per-instance URLs preserved
- homepage can link to `/service/#fptalks-2020-2025`

### `PNW PLSE`

```json
{
  "series": [
    {
      "key": "pnw-plse",
      "title": "PNW PLSE",
      "url": "http://pnwplse.org/"
    }
  ],
  "runs": [
    {
      "key": "pnw-plse-2023",
      "series": "pnw-plse",
      "title": "PNW PLSE",
      "role": "Co-Organizer",
      "view_groups": ["organizing"],
      "primary_view_group": "organizing",
      "instances": [
        { "key": "pnw-plse-2023-instance", "year": 2023 }
      ]
    },
    {
      "key": "pnw-plse-2018",
      "series": "pnw-plse",
      "title": "PNW PLSE",
      "role": "Organizer",
      "view_groups": ["organizing"],
      "primary_view_group": "organizing",
      "instances": [
        { "key": "pnw-plse-2018-instance", "year": 2018 }
      ]
    }
  ]
}
```

Benefits:

- one recurring identity
- two stable visible runs
- no fake range
- homepage can show latest run and link directly to the shared URL

### `UW CSE Undergraduate Admissions Committee`

```json
{
  "series": [
    {
      "key": "uw-cse-undergraduate-admissions",
      "title": "UW CSE Undergraduate Admissions Committee"
    }
  ],
  "runs": [
    {
      "key": "uw-cse-undergraduate-admissions-2020-2021",
      "series": "uw-cse-undergraduate-admissions",
      "title": "UW CSE Undergraduate Admissions Committee",
      "view_groups": ["department"],
      "primary_view_group": "department",
      "time_basis": "academic_year",
      "instances": [
        { "key": "uw-cse-undergraduate-admissions-2021", "year": 2021 },
        { "key": "uw-cse-undergraduate-admissions-2020", "year": 2020 }
      ]
    },
    {
      "key": "uw-cse-undergraduate-admissions-2017-2018",
      "series": "uw-cse-undergraduate-admissions",
      "title": "UW CSE Undergraduate Admissions Committee",
      "view_groups": ["department"],
      "primary_view_group": "department",
      "time_basis": "academic_year",
      "instances": [
        { "key": "uw-cse-undergraduate-admissions-2018", "year": 2018 },
        { "key": "uw-cse-undergraduate-admissions-2017", "year": 2017 }
      ]
    }
  ]
}
```

Benefits:

- explicit separate runs
- stable anchors even if another future run appears
- explicit academic-year semantics when wanted

### `2025 PLDI Program Committee Chair`

```json
{
  "runs": [
    {
      "key": "pldi-2025-program-committee-chair",
      "title": "PLDI",
      "role": "Program Committee Chair",
      "view_groups": ["reviewing", "organizing"],
      "primary_view_group": "organizing",
      "instances": [
        {
          "key": "pldi-2025-program-committee-chair-instance",
          "year": 2025,
          "url": "https://pldi25.sigplan.org/committee/pldi-2025-organizing-committee",
          "details_djot": [
            "[Review Committee](https://pldi25.sigplan.org/committee/pldi-2025-papers-pldi-review-committee)",
            "[SIGPLAN Announcement](https://www.sigplan.org/announce/2024-09-21-pldi-2025/)"
          ]
        }
      ]
    }
  ]
}
```

Benefits:

- one canonical fact
- multi-view membership explicit
- primary section explicit
- no anchor ambiguity

## Why This Is Simpler Than It Looks

At first glance, three levels look more complex than the current flat model.
I think that is misleading.

The proposed model actually removes complexity from the code by making explicit
what the renderers already need:

- recurring identity
- visible grouped unit
- atomic fact

Right now those concepts exist anyway, but they are smeared across:

- `series_key`
- grouping code
- rendering code
- anchor conventions
- homepage consumer policy

The proposal moves that structure into the data model where it belongs.

## What This Proposal Deliberately Does Not Do

It does not:

- add a giant taxonomy of service kinds
- require every record to belong to a series
- require every level to have all optional metadata
- introduce homepage-specific flags yet
- solve service page styling in the data model
- require month-level timing semantics

## Migration Strategy

If we adopt this design, the migration path should be:

1. write and review the redesign plan
2. introduce new loader/validator alongside the old one
3. backfill the new shape from the current canonical service data
4. write focused tests against current stress cases
5. cut the service page to the new run-based renderer
6. only then revisit homepage recent-service projection

That keeps the redesign explicit and testable rather than half-migrated.

## Bottom Line

If I compress the whole proposal into one sentence:

Make `run` the canonical visible service unit, keep `instance` as the atomic
fact unit, and add an explicit optional `series` layer above runs for recurring
identity and future metadata.

I think that is the cleanest design that is still simple enough to edit by
hand and robust enough not to keep biting the repo for years.
