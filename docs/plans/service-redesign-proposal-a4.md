# Service Redesign Proposal A4

Status: draft

It builds on:

- [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)
- [service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md)
- [service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md)
- [service-redesign-proposal-a3.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a3.md)
- [service-redesign-proposal-a3-residual-issues.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a3-residual-issues.md)

## Purpose

This is the next refinement after A3.

The goal is still the same:

- canonical `series`
- canonical `run`
- atomic `instance`

with a compact authored JSON surface.

Compared to A3, A4 mainly resolves the last three lingering seams:

- top-level record-key uniqueness
- role-normalization contract
- rich `details` validation contract

So A4 is not a new structural proposal.
It is A3 with the remaining specification gaps closed.

## Recommendation

Adopt a progressive-shorthand authored JSON format that normalizes to one
canonical semantic model:

- optional `series`
- one or more canonical `run`s
- one or more atomic `instance`s inside each run

The authored file should be one ordered `records` array, using exactly three
intended authored forms for this redesign:

1. `singleton`
2. `single-run series shorthand`
3. `explicit series with runs`

These three forms are the intended authored surface for this redesign.
Adding further shorthand forms should be treated as a redesign-level change,
not as an ordinary incremental extension.

## Why A4 Still Prefers Canonical Runs

The core design judgment remains unchanged from A1, A2, and A3:

`run` should be canonical because it is the visible unit consumers actually
need.

That solves the hardest requirements directly:

- stable visible identity
- stable internal anchors
- homepage recent-service selection
- non-contiguous service without fake continuous ranges
- run-level section membership
- run-level anchor placement for multi-view rendering

The lighter authored forms exist to improve physical ergonomics, not to retreat
from canonical runs.

## Rehydration Contract

This proposal intentionally distinguishes between:

- the authored JSON source
- the loaded semantic model in Python

The authored JSON is the human-edited source of truth.
The loaded model is the canonical semantic representation used by consumers.

So the contract is:

- authors edit the JSON
- the loader validates and normalizes it
- consumers work only with the loaded model
- consumers should never reason directly from raw JSON shape

This is a real seam, but it is manageable and explicit.
The loader's normalization rules are therefore part of the redesign contract,
not an implementation detail to improvise later.

## Preferred Form Rule

Use the lightest authored form whose constraints are not violated.

That means:

- use `singleton` for true one-off facts
- use `single-run series shorthand` for ordinary recurring identities with one
  current run and no need to separate series-level metadata yet
- use `explicit series with runs` when:
  - there is more than one run
  - series-level metadata differs meaningfully from run-level metadata
  - explicit run keys or explicit run-level semantics need to be stated

This keeps the file compact and diffs small while preserving the richer loaded
model.

## Canonical Semantics After Loading

Regardless of authored form, the loader normalizes the file into the same
semantic model.

### Canonical `series`

`series` is optional recurring identity.

It is the right place for facts that are true of a broader recurring lane of
service rather than one particular visible run or one particular year-local
instance.

Examples:

- `FPTalks`
- `PACMPL Advisory Board`
- `UW CSE Undergraduate Admissions Committee`

### Canonical `run`

`run` is the canonical visible grouped unit.

A canonical run is intended to represent one contiguous span of service years.

It is what consumers should use for:

- `/service/` visible bullets
- stable internal anchors
- homepage recent-service selection
- future grouped summaries

### Canonical `instance`

`instance` is the atomic fact layer.

It preserves:

- exact year-local participation
- instance-specific URLs
- instance-specific details
- instance-level title or role overrides when genuinely needed

## Inheritance

Resolved values follow one universal rule:

- `instance -> run -> series -> absent`

The first level that provides a value wins.

That means:

- omitted fields inherit
- explicit lower-level values override higher-level defaults
- the initial design does not include a null/clear mechanism

Examples:

- resolved `role`
  - `instance.role ?? run.role ?? series.role`
- resolved `url`
  - `instance.url ?? run.url ?? series.url`
- resolved `title`
  - `instance.title ?? run.title ?? series.title`
- resolved `details`
  - `instance.details ?? run.details ?? series.details`

This rule applies uniformly after loading, regardless of which authored form
produced the canonical series/run/instance structure.

## Identifier Model

The redesign uses three identifier layers:

- top-level record keys
- canonical run keys
- optional authored instance keys

### Top-Level Record Keys

Every top-level `records[].key` must be unique across the entire file.

That gives every authored record:

- one stable audit-friendly identity
- one clear review handle
- one unambiguous migration target

### Canonical Run Keys

Every canonical run key must be globally unique across the entire file.

This includes:

- singleton keys reused as canonical run keys
- shorthand record keys reused as implicit run keys
- explicit run keys inside explicit series records

### Relationship Between Record Keys And Run Keys

One deliberate reuse is allowed:

- a canonical run key may equal the top-level record key of its containing
  record

This supports:

- singleton records
- shorthand records
- explicit one-run records
- shorthand-to-explicit promotion where the original run keeps the old key

Outside that parent/contained reuse, run keys and record keys must not collide.

### Authored Instance Keys

`instance.key` remains optional in authored JSON.
It is required only when same-year multiplicity or direct reference needs it.

## Role Normalization Contract

Role strings are canonical authored text.

This redesign does **not** attempt semantic role normalization in v1.

That means:

- no automatic case normalization
- no automatic punctuation normalization
- no automatic "Organizer" vs "Co-Organizer" family reasoning

Validation may apply only trivial lexical cleanup such as:

- trimming outer whitespace
- rejecting empty strings
- optionally collapsing accidental repeated internal whitespace

But for ownership, inheritance, and uniformity reasoning, role equality should
be treated as exact authored equality after that trivial lexical cleanup.

Consequences:

- `Co-chair` and `Co-Chair` may coexist in the broader corpus
- if a recurring identity wants a uniform role at the series or run level, the
  authored data should be made literally uniform
- broader role cleanup can remain a separate future data-quality campaign

This keeps the redesign simple and explicit while tolerating the known drift in
the current corpus.

## Details Contract

`details` remain rich authored content, not opaque strings.

At any ownership level:

- `series.details`
- `run.details`
- `instance.details`

the field should be an ordered array of Djot-bearing detail items.

Those items may include:

- ordinary Djot text
- links
- person references

The redesign therefore preserves the current source-validation discipline:

- Djot-bearing details remain parsed/validated as authored markup
- links inside details remain subject to link validation
- person references inside details remain subject to people-reference validation
- renderers preserve the authored item order at whatever level owns the detail

This is important because the redesign should not accidentally make `details`
look like unstructured plain-text comments.

## Field Ownership Summary

General rule:

- place a fact at the highest level where it remains true
- lower levels override only when the higher-level fact stops being true

### Title

- `series.title`
  recurring identity label
- `run.title`
  only when one run needs a different visible label
- `instance.title`
  only when one instance needs a different label

### Role

- `series.role`
  when one role remains true across the whole recurring identity
- `run.role`
  when one run has a stable role that is not uniform across the whole series
- `instance.role`
  only when one instance differs from the resolved run/series role

### URL

- `series.url`
  only for stable series-level landing pages
- `run.url`
  when one URL applies to the whole run
- `instance.url`
  when URLs differ year by year or instance by instance

### Details

- `series.details`
  facts true of the whole recurring identity
- `run.details`
  facts true of the whole visible run
- `instance.details`
  facts true only of one instance

## Authored Top-Level Shape

The authored file should be:

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
It is for true one-off service facts with no separate recurring identity
currently modeled.

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
  becomes the canonical run key and public anchor id
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

### `ongoing` On Singletons

`ongoing` is allowed on a singleton.

In this case it means:

- the record describes one open-ended run
- but no broader recurring identity is currently being modeled

If a broader recurring identity later becomes important, the record can be
promoted.

## Authored Form 2: Single-Run Series Shorthand

This is the common recurring case.

It is for a recurring identity that currently has one canonical run and does
not yet need an explicitly separate series metadata block.

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

A shorthand record is shorthand for:

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

### Why This Form Exists

This form deliberately merges:

- recurring series identity
- and sole-run authoring concerns

into one compact authored block.

That means the distinction between series-level and run-level ownership is
being intentionally collapsed where it does not matter yet.

If that distinction later starts to matter, the record should be promoted to
explicit form.

### Important Constraint

This form is only valid for one current canonical run.

So a shorthand record must not be used when:

- the identity has more than one run
- the years are non-contiguous
- series-level metadata needs to be separated cleanly from run-level metadata
- explicit run keys beyond the series key are needed

## Authored Form 3: Explicit Series With Runs

This is the fully explicit form.

It is for recurring identities that need:

- multiple runs
- explicit separation between series-level and run-level metadata
- authored run keys beyond the series key
- or more complex run-level semantics

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

## Run Keys And Anchor Semantics

### Run-Key Rules

- every canonical run has a stable authored key
- singleton records reuse the top-level record key as the run key
- shorthand records reuse the top-level record key as the implicit run key
- explicit additional runs must have explicit authored keys
- all canonical run keys must be globally unique across the entire file
- run keys should not encode exact year boundaries
- run keys should not be renamed merely because:
  - a run grows under backfill
  - an older year is added to an existing run
  - a new additional run appears later

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

### `anchor_view_group`

`anchor_view_group` is narrowly about anchor placement.

For any canonical run:

- if resolved `view_groups` length is `1`, `anchor_view_group` is implied
- if resolved `view_groups` length is greater than `1`,
  `anchor_view_group` is required
- `anchor_view_group` must be one of the run's `view_groups`

## Instance Keys

`instance.key` should be optional in authored JSON.

It should be required only when the record really needs it.

### Explicit `instance.key` Is Required When

- same-year multiplicity exists within one run
- a future consumer needs to reference a specific instance directly
- a migration/import path needs durable authored instance identity for a
  specific case

### Internal Synthesis

If a run has unique years across its instances and an instance omits `key`,
the loader may synthesize a deterministic internal instance id.

Those synthesized ids are:

- internal loader artifacts
- not part of the public authored schema
- generated in a reserved namespace that cannot collide with authored keys

If same-year multiplicity exists, explicit authored instance keys become
required for those ambiguous instances.

## Promotion Rules

### Shorthand -> Explicit Promotion

When a shorthand single-run series is promoted to explicit form:

- the original run should usually keep the old series/record key as its run key
- new later runs get new authored run keys

This preserves existing `/service/#...` links.

### Singleton -> Recurring Promotion

If a singleton later becomes part of a broader recurring identity:

- the old singleton key may remain the first run key
- a cleaner new recurring `series.key` may be introduced if needed
- when preserving existing anchors matters, promoting directly to explicit form
  is usually the safer path

## Validation Rules

### Top-Level Shape

A top-level record must have exactly one of:

- `year`
- `instances`
- `runs`

Interpretation:

- `year` => singleton
- `instances` => shorthand
- `runs` => explicit series with runs

### Required Top-Level Fields

All top-level records require:

- `key`
- `title`

Additional requirements by form:

- singleton:
  - `year`
  - `view_groups`
- shorthand:
  - `instances`
  - `view_groups`
- explicit:
  - `runs`

### Identifier Validation

The validator should enforce:

- unique top-level `records[].key` values across the entire file
- unique canonical run keys across all canonical runs
- no collision between a run key and any unrelated top-level record key
- no authored collision with the reserved synthesized-instance-id namespace

The intentional exception is:

- a run key may equal the top-level record key of its own containing record

### Field Restrictions By Form

If a top-level record has `runs`:

- top-level `view_groups` is forbidden
- top-level `anchor_view_group` is forbidden
- top-level `time_basis` is forbidden
- top-level `ongoing` is forbidden

Those belong on explicit runs instead.

### Role Validation

The validator should treat role strings as canonical authored text.

That means:

- enforce trivial lexical cleanup rules
- do not attempt semantic normalization
- only treat roles as equal when they are literally equal after the allowed
  lexical cleanup

### Rich `details` Validation

At every ownership level, `details` should validate as rich authored Djot
content rather than as opaque strings.

So validation should continue to include:

- Djot-bearing content validation
- link validation inside details
- person-reference validation inside details

### Contiguity

A canonical run is intended to represent one contiguous span of service years.

So:

- shorthand records with non-contiguous years are invalid
- non-contiguous service should be promoted to explicit multiple runs
- explicit multi-instance runs are also expected to be contiguous unless a
  future uncertainty-aware design says otherwise

### Ordering

- top-level record order is canonical
- explicit run order inside a series is canonical
- instance order inside a run is canonical
- these array orders are the final tie-break wherever stronger semantic rules
  do not already decide the result

Newest-first is the normal authoring convention, but strict descending order is
not itself the foundational validity rule.

## Consumer Semantics

### Public `/service/`

The public service page should consume canonical `run`s.

That means:

- section filtering works over run-level membership
- anchors attach at run level
- grouped summary labels come from runs
- instance sub-bullets expand only where they materially help

The service page should not need to care which authored form produced the run.

### Homepage `Recent Service / Leadership`

The homepage should also select from canonical `run`s, not raw instances.

That preserves the desired behavior:

- one visible unit per run
- stable internal link targets when needed
- no fake flattening of recurring service

Link rule:

- if the selected run resolves to one unambiguous direct URL, link directly
- if direct linking would be lossy or ambiguous because multiple distinct
  instance URLs matter, link to the run's `/service/` anchor instead
- if there is no resolved URL, render the summary unlinked

### CV

The CV can also consume canonical runs.

Because the loaded run model is stable, the CV can stay simple even though the
authored JSON uses several compact forms.

## Worked Examples

### Multi-View Singleton

```json
{
  "key": "2025-pldi-program-committee-chair",
  "year": 2025,
  "title": "PLDI",
  "role": "Program Committee Chair",
  "view_groups": ["organizing", "reviewing"],
  "anchor_view_group": "organizing",
  "url": "https://pldi25.sigplan.org/track/pldi-2025-papers",
  "details": [
    "[Proceedings](https://dl.acm.org/doi/proceedings/10.1145/3729317)"
  ]
}
```

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

## Migration Sketch

From the current flat record model:

1. Leave true one-offs as singleton records.
2. Collapse single-run recurring identities into shorthand records.
3. Expand non-contiguous or metadata-heavy identities into explicit
   series-with-runs records.
4. Keep consumer code working only over the normalized canonical run model.

So the migration cost is mainly:

- moving canonical facts into better local blocks
- choosing stable run keys where explicit runs are needed
- documenting the loader contract clearly

## Why A4 Is Better Than A3

A4 keeps everything good about A3:

- compact physical JSON
- self-contained common cases
- canonical runs after loading

But it resolves the last three remaining specification seams:

- top-level key uniqueness is now explicit
- role normalization stance is now explicit
- rich `details` validation contract is now explicit

So A4 is still the same design, but it is closer to an implementation-ready
spec.

## Remaining Open Questions

The remaining open questions are now narrow:

- exactly how strict validation should become around partial or uncertain
  historical knowledge
- whether any future consumer will need synthesized instance ids exposed
  publicly
- the best exact style guidance for authored run keys

Those are implementation-tightening questions, not model-choice questions.
