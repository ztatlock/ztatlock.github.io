# Service Redesign Slice 4: Homepage Recent Service

Status: draft

It builds on:

- [service-redesign-slice-3-current-consumer-cutover.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-slice-3-current-consumer-cutover.md)
- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)
- [homepage-cv-curated-consumers-slice-3-service-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md)
- [homepage-cv-curated-consumers-slice-3-service-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit-notes.md)

## Goal

Plan and then implement the homepage `## Recent Service / Leadership` block
from canonical service runs now that `/service/` and the CV already consume the
run-native A4 model.

This slice should:

- operate on canonical runs, not raw instances
- reuse the now-landed run-anchor and link policy
- finalize a homepage selection policy over real canonical runs
- only then project the homepage service block itself

It should not:

- reopen the service data-model redesign
- relitigate public `/service/` or CV service rendering
- invent a homepage-specific service labeling style detached from the public
  service surfaces

## What Slice 3 Changed

Slice 3 materially improved the starting point for homepage service:

- `/service/` now exposes canonical run anchors at `/service/#<run.key>`
- recurring multi-URL runs already render as one visible run summary with
  supporting instance bullets
- the CV already uses internal `/service/#<run.key>` links where choosing one
  external instance URL would be lossy
- service-data validation now treats A4 as the direct contract

That means homepage service no longer needs to solve:

- flat-term grouping
- arbitrary per-year URL choice
- or unstable internal targets

Those problems are now already solved upstream.

## Main Consequence For Slice 4

The next unresolved question is now policy, not data shape.

So slice 4 should begin with policy simulation over canonical runs, not with
another structural refactor.

## Selection Invariants

The homepage service consumer should now assume:

- one visible homepage item corresponds to one canonical run
- homepage labels should reuse the same broad run-summary language as
  `/service/` and the CV
- if a selected run resolves to one unambiguous direct URL, link directly
- if multiple distinct instance URLs matter, link to `/service/#<run.key>`
- the trailing authored sentence should remain:
  `Please see my [service page](service/) for more.`

## Policy Questions Still To Resolve

The remaining slice-4 questions are now much narrower:

1. Source scope

Should homepage recent service draw from:

- `organizing` only
- `organizing` plus selected `department` leadership
- or another principled subset over canonical runs

2. Recency anchor rule

Canonical service already contains future years.
The homepage policy needs an explicit anchor rule in the presence of:

- `2026 - 2029 PLDI Steering Committee`
- `2026 - 2029 PACMPL Advisory Board Member`

3. Cap / density

Now that recurring yearly series are already coalesced, the homepage may need
less policy machinery than it would have under the flat-term model.

So slice 4 should explicitly test whether a plain:

- window over canonical runs
- plus a modest cap

is already enough, before adding any `homepage_featured`-style stickiness.

## Updated Recommendation

Because slice 3 already reduced service-list noise substantially, the next step
should be:

1. simulate a few homepage policies over canonical runs
2. review the rendered outcomes
3. only add homepage-specific stickiness metadata if the simulations prove it
   necessary

So the default bias should now be:

- simpler policy first
- metadata later only if justified

## Recommended Slice Shape

### Slice 4A. Policy Simulation / Latch

Use the current canonical runs to compare a few plausible homepage policies.

At minimum compare:

- trailing-window only
- trailing-window plus cap
- trailing-window plus cap plus scoped stickiness

Evaluate them against:

- current canonical run population
- future-facing runs already present in the data
- the current manually curated homepage service block

The goal is to latch one clear homepage policy before implementing the
projection.

### Slice 4B. Homepage Projection

After the policy is latched:

- add the homepage placeholder
- render the selected canonical runs
- use the direct-URL vs `/service/#<run.key>` rule already proven in slice 3
- keep the trailing service-page sentence authored

## Why This Is Better Than The Earlier Trajectory

Before slice 3, homepage service planning was entangled with:

- service grouping semantics
- service-page target availability
- link ambiguity for recurring yearly series

After slice 3, those are no longer the blocking issues.

So slice 4 can now be a much cleaner consumer-policy slice.

## Expected Follow-On

If slice 4 lands cleanly, the remaining service work becomes:

- later service-page presentation polish
- broader homepage/CV cleanup across other canonical domains

not more service data-model upheaval.
