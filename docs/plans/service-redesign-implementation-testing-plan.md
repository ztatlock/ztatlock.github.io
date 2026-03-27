# Service Redesign Implementation / Testing Plan

Status: draft

It builds on:

- [service-redesign-proposal-a4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a4.md)
- [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [homepage-cv-curated-consumers-slice-3-service-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md)

## Purpose

This note switches the service redesign work from proposal iteration into
implementation and testing planning.

The design question is now considered narrow enough:

- A4 is the leading redesign direction

So the next job is not to keep redesigning.
It is to decide how to land the redesign safely and test it well.

## Goal

Implement the A4 service redesign in a way that:

- preserves canonical service facts
- keeps the site build/check path trustworthy throughout migration
- minimizes accidental public regressions
- and gives later consumers, especially homepage `Recent Service / Leadership`,
  a stronger long-horizon foundation

## Main Execution Principle

Treat the redesign as a **migration plus adapter** problem, not as one giant
renderer rewrite.

That means:

- first make the A4 schema and normalized model executable in code
- then migrate canonical data
- then cut current consumers over to the normalized run model
- only after that revisit richer service-page formatting or homepage recent
  service projection

## Recommended Slice Order

### Slice 1. Loader / Validator Foundation

Implement the A4 schema and normalization logic in code before migrating the
real canonical data file.

Scope:

- add a new loader/validator module for A4-authored service records
- support all three authored forms:
  - `singleton`
  - `single-run series shorthand`
  - `explicit series with runs`
- normalize all forms into one canonical loaded model:
  - optional `series`
  - canonical `run`
  - atomic `instance`
- do not migrate `site/data/service.json` yet
- do not cut any page renderer over yet

Why first:

- it turns the proposal into executable contract
- it gives us focused tests before touching canonical data
- it isolates parser/validation mistakes from migration mistakes

Invariant after slice 1:

- A4 is executable as code
- the repo has tests proving the loader/validator behavior on focused fixtures
- current site output is unchanged

### Slice 2. Canonical Data Migration

Migrate `site/data/service.json` from the current flat term model to the A4
authored schema.

Scope:

- convert current one-offs into `singleton` records
- convert current one-run recurring identities into shorthand records where
  appropriate
- convert current multi-run or metadata-heavy recurring identities into
  explicit series-with-runs records
- preserve current canonical facts, URLs, details, and view-group membership

Important migration discipline:

- prefer the lightest sufficient authored form
- choose stable run keys carefully
- keep old visible-anchor stability in mind whenever a current grouped concept
  already matters downstream

Invariant after slice 2:

- `site/data/service.json` uses the A4 schema
- canonical service facts are preserved
- current renderers may still rely on temporary compatibility helpers, but the
  source of truth is now the redesigned data

### Slice 3. Current Consumer Cutover

Cut the current service consumers over to the normalized A4 loaded model.

Scope:

- update public service-page projection to consume canonical runs
- update CV service projection to consume canonical runs
- preserve the current section structure and authored `Aggregators` handling
- preserve current compressed CV conventions
- do **not** yet broaden the public service-page formatting just because the
  new model now supports richer grouping

Why keep this slice conservative:

- first prove that the redesign can preserve or narrowly improve current public
  behavior
- avoid mixing data-model migration with aesthetic/service-page redesign

Invariant after slice 3:

- all current service consumers run on the redesigned loader/model
- `/service/` and the CV service section remain correct and stable
- remaining service work is no longer blocked on the old flat term model

### Slice 4. Homepage Recent Service Planning / Implementation

Only after slices 1-3 are stable should the repo return to homepage recent
service projection.

At that point:

- the data model question is settled
- the grouped canonical source is stronger
- homepage selection policy can be designed against real canonical runs rather
  than temporary grouping helpers over flat term records

This later slice should explicitly carry forward the open questions from A4 as
test and policy targets rather than reopening the redesign itself.

## Testing Strategy

The redesign should be tested in layers.

### Schema / Validation Tests

Add focused tests for:

- top-level form discrimination:
  - `year`
  - `instances`
  - `runs`
- required/forbidden fields by form
- top-level record-key uniqueness
- canonical run-key uniqueness
- allowed parent-record-key / run-key reuse
- forbidden unrelated record-key / run-key collisions
- `anchor_view_group` rules for single-view and multi-view runs
- shorthand non-contiguity rejection
- same-year multiplicity requiring explicit `instance.key`
- reserved synthesized-instance-id namespace protection

### Normalization Tests

Add focused tests for:

- singleton normalization
- shorthand normalization
- explicit-series normalization
- inheritance:
  - `instance -> run -> series`
- promotion-stable semantics:
  - shorthand-to-explicit with preserved run key
- multi-view runs with one canonical anchor home

### Role / Details Tests

Add focused tests for:

- trivial lexical cleanup only for role strings
- no semantic role normalization in v1
- rich `details` validation at:
  - `series`
  - `run`
  - `instance`
- Djot-bearing `details`
- links inside `details`
- person references inside `details`

### Consumer / Regression Tests

Add focused tests for:

- public service-page grouped rendering over the normalized run model
- CV compressed service rendering over the normalized run model
- anchor placement and duplicate-id avoidance for multi-view service
- homepage/link-target helper behavior if any is introduced during migration

### Build / Diff Review

For migration/cutover slices, review:

- `make build`
- `make check`
- focused unit tests
- rendered diffs for:
  - `/service/`
  - `/cv/`
  - any pages linking into service anchors

The default expectation should be:

- narrow rendered change unless a slice explicitly aims to improve presentation

## Open Questions To Carry Forward

These are no longer redesign blockers, but the implementation should keep them
visible:

- exactly how strict validation should be around partial or uncertain
  historical knowledge
- whether any future consumer will need synthesized instance ids exposed
  publicly
- the best exact style guidance for authored run keys

In implementation planning, these should be treated as:

- explicit test targets
- explicit migration notes
- explicit follow-up decisions if a concrete blocker appears

not as reasons to reopen the A4 model itself.

## Immediate Next Step

The clean first implementation slice is:

- loader / validator foundation over small focused fixtures

That is the safest place to turn the A4 proposal from design into executable
contract before touching `site/data/service.json` or the public renderers.
