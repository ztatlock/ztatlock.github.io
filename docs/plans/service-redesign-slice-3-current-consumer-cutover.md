# Service Redesign Slice 3: Current Consumer Cutover

Status: implemented

It builds on:

- [service-redesign-proposal-a4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a4.md)
- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)

## Goal

Cut the live service consumers over from the temporary flattened compatibility
path to the canonical A4 loaded model while moving the public and CV service
output closer to the intended run-native design.

This slice should:

- make public `/service/` projection consume canonical runs directly
- make the CV service section consume canonical runs directly
- make service-data validation use the A4 validator directly
- attach canonical run anchors on `/service/`
- preserve current section wrappers and hand-authored prose

It should not:

- start homepage `Recent Service / Leadership` projection
- reopen the A4 data-model question
- attempt a full visual polish pass on `/service/`

## Why This Slice Exists

After slice 2, the repo has a split state:

- [site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json)
  is already A4 canonical data
- [scripts/service_record_a4.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_record_a4.py)
  already loads and validates that model directly
- but the live renderers and source validation still flow through the
  temporary flattened compatibility path in the then-live legacy shim and the
  legacy grouping logic in
  [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)

So the next safe step is not another schema change.
It is to remove the live dependence on term-level flattening and legacy
signature grouping.

The more important design correction is this:

- preserve canonical facts, correctness, and stability
- do **not** preserve legacy flat-term formatting merely because it already
  exists

Trying to preserve the old visible service list too exactly would keep forcing
run-native code to imitate a model we have already replaced.

## Current Compatibility Seams

The current live service path still depends on:

- the legacy flattened compatibility loader
- [group_service_records_for_view(...) in service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)
- [render_public_service_section_list_djot(...) in service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)
- [render_cv_service_section_list_djot(...) in page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- the legacy flattened validation helper

That means:

- live public/CV output is still determined by flattened term records
- live grouping is still driven by legacy `(series_key, title, role, url, details)`
  signatures rather than canonical runs
- source validation still does not treat A4 as the direct service-data contract

Slice 3 should remove that from the live path.

## Scope

### In Scope

- new run-based service grouping/render helpers
- public `/service/` cutover to canonical runs
- CV service cutover to canonical runs
- direct A4 service-data validation cutover
- canonical run-anchor attachment on `/service/`
- tests proving the compatibility bridge is no longer in the live build/check
  path

### Out Of Scope

- homepage recent-service projection
- homepage service policy
- service-page CSS/presentation polish beyond what the run-native cutover
  naturally changes
- deleting every legacy helper immediately if a small isolated compatibility
  shim is still useful during transition

## Canonical Rendering Policy For Slice 3

This slice should consume canonical runs directly and should stop trying to
preserve legacy flat-term presentation merely because it is old.

The conservative part of the slice is:

- preserve canonical facts
- preserve section membership
- preserve build/check trustworthiness
- preserve anchor stability and link correctness

The slice should **not** preserve:

- year-first labels just because they are inherited
- repeated yearly top-level bullets when a canonical run is the real visible
  unit
- old grouping quirks that only existed because URLs differed per year

### Section Membership

Visible service sections should be driven by resolved `run.view_groups`.

The existing section structure remains:

- `reviewing`
- `organizing`
- `mentoring`
- `department`

The authored wrappers remain in:

- [site/service/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/service/index.dj)
- [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)

### Run Ordering

Within a section, canonical runs should be ordered by:

1. latest instance year descending
2. resolved title
3. resolved role
4. canonical file order as final tie-break

This keeps the live surface deterministic without depending on flattened term
order.

### Visible Entry Policy

The public service page should now treat the canonical run as the visible
top-level unit.

That means:

- one summary block per canonical run
- explicit multi-run series still render once per run
- repeated yearly instance bullets appear only as substructure under a run,
  not as separate top-level entries

#### Uniform Runs

If all instances in a canonical run resolve to the same visible:

- `title`
- `role`
- `url`
- `details`

then the run renders as:

- one summary line
- no instance sub-bullets

#### Runs With Meaningful Instance Variation

If instance-level variation materially matters, the canonical run should still
render as one top-level summary block, but it may include instance sub-bullets.

The main current trigger is:

- multiple distinct instance URLs that matter to readers

This applies to the bounded current cases:

- `fptalks`
- `pldi-workshops`
- `egraphs-workshop`

For those runs, slice 3 should render:

- one run summary line
- then contextual instance bullets underneath

So slice 3 becomes run-native immediately instead of preserving the legacy flat
list.

### Explicit Multi-Run Series

Explicit multi-run series should render once per canonical run.

That means current non-contiguous cases remain separate visible blocks:

- `pnw-plse-return`
- `pnw-plse-foundation`
- `uw-cse-undergraduate-admissions-recent`
- `uw-cse-undergraduate-admissions-early`

Slice 3 should not invent higher-level umbrella headers for them.

## Public `/service/` Rendering Policy

Slice 3 should move the public service page toward the rendering direction
already supported by the redesign and audit work.

Recommended public shape:

- one grouped summary line per run
- summary labels use year-last formatting
- summary labels prefer:
  - multi-year: `Title Role, Years`
  - multi-year without role: `Title, Years`
  - single-year: `Title Year, Role`
  - single-year without role: `Title Year`
- when a run has meaningful instance-level links or variation, render
  contextual instance sub-bullets underneath
- instance bullets should never be bare years
- instance bullets should use contextual year-last labels such as:
  - `[FPTalks 2025](...)`, `Co-Organizer`

Examples of the intended direction:

- `FPTalks Co-Organizer, 2020 - 2025`
  - `[FPTalks 2025](...)`, `Co-Organizer`
  - `[FPTalks 2024](...)`, `Co-Organizer`
- `PACMPL Advisory Board Member, 2026 - 2029`
- `PNW PLSE 2023, Co-Organizer`

The hand-authored `Aggregators` section remains untouched.

## CV Rendering Policy

The CV should also become run-native in this slice, but remain more compressed
than the public service page.

Recommended CV shape:

- one summary line per canonical run
- no instance sub-bullets
- use the same year-last summary language as the public run summaries
- keep the current section headings
- keep the department omission of `UW Faculty Skit`
- keep the hand-authored skit prose note below the projected department block

Link policy for the CV:

- if a run resolves to one unambiguous direct URL, link the summary there
- if multiple distinct instance URLs matter, prefer linking to
  `/service/#<run.key>` rather than choosing one misleading external URL
- if there is no useful resolved URL, leave the summary unlinked

So the CV can stay compact without pretending recurring yearly series are just
one arbitrary instance.

## Anchor Policy

Slice 3 should honor the A4 run-anchor contract on the public service page.

The rule should be:

- every canonical run owns exactly one canonical internal anchor
- the anchor id is always the canonical run key
- the anchor appears only on the run's `anchor_view_group` occurrence, or on
  its sole section occurrence when the anchor view is implied
- the CV does not attach these anchors

For runs with instance sub-bullets, the anchor should attach to the run
summary line in the anchor-owning section.

That gives later homepage service consumers a stable `/service/#<run.key>`
target without forcing another redesign pass first.

## Concrete Code Surfaces

Primary code surfaces for slice 3:

- [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [scripts/sitebuild/source_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/source_validate.py)

Expected code-direction changes:

1. `service_index.py`
   - stop driving public rendering from flattened `ServiceRecord`
   - add run-based section selection and rendering helpers over
     `ServiceRegistryA4`
2. `page_projection.py`
   - stop CV service rendering from flattened `ServiceRecord`
   - reuse the run-based helpers or equivalent run-based logic
   - support CV internal links to `/service/#<run.key>` where direct external
     links would be lossy
3. `source_validate.py`
   - stop validating service data through `find_service_record_issues(...)`
   - validate service data directly through the A4 loader/validator

The temporary compatibility API may remain briefly as isolated migration
scaffolding, but it should no longer be part of the live build/check path
after this slice. That scaffolding has since been removed.

## Proposed Invariant After Slice 3

After slice 3:

- live public/CV service rendering consumes canonical A4 runs directly
- live service-data validation consumes the A4 validator directly
- `/service/` exposes canonical run anchors
- public/CV visible behavior is intentionally closer to the run-native target
- the temporary flat-model compatibility bridge is no longer on the live path
- later homepage service work can target real `/service/#<run.key>` anchors
  and canonical runs

## Test Plan For This Slice

### Public Service Rendering Tests

Add or update focused tests for:

- grouped rendering of a uniform run
- grouped rendering of a run with instance sub-bullets
- year-last summary formatting
- contextual year-last instance bullets
- nested detail bullets
- explicit multi-run rendering remaining separate

### CV Service Rendering Tests

Add or update focused tests for:

- grouped run summary rendering under CV conventions
- direct external linking for unambiguous runs
- internal `/service/#<run.key>` linking for ambiguous multi-url runs
- department omission of `UW Faculty Skit`

### Anchor Tests

Add focused tests for:

- canonical run anchor attached on the sole-section occurrence
- canonical run anchor attached only on `anchor_view_group` for multi-view runs
- no duplicate ids across repeated run appearances
- run-summary anchors for runs with instance sub-bullets

### Validation / Live-Path Tests

Add focused tests for:

- source validation using the A4 validator directly
- current service projection helpers no longer requiring
  `load_service_records(...)`
- current service projection helpers no longer requiring
  `group_service_records_for_view(...)`

### Rendered Diff Review

Review diffs for:

- `/service/`
- `/cv/`
- any pages that will later link into `/service/#...`

Default expectation:

- rendered diffs are expected
- the important requirement is that they are intentional and aligned with the
  run-native target rather than accidental regressions

## Why The Risk Is Bounded

The current canonical data has a small number of cutover-stress cases:

- `64` top-level A4 records
- `66` canonical runs
- `2` explicit multi-run records
- `1` multi-view run
- `3` heterogeneous runs that need sub-bullets or internal service-anchor
  linking

So slice 3 is not a giant open-ended renderer rewrite.
It is a bounded consumer cutover with a small, known set of special cases.

## Next Follow-On

Only after this slice lands should the repo return to homepage
`Recent Service / Leadership`.

That later work can then depend on:

- canonical runs
- stable `/service/#<run.key>` anchors
- and the public/CV service pages no longer being blocked on the temporary
  flattening bridge
