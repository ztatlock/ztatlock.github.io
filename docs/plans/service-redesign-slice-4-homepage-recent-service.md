# Service Redesign Slice 4: Homepage Recent Service

Status: implemented

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
- if a selected run has no URL at all, leave it unlinked
- the trailing authored sentence should remain:
  `Please see my [service page](service/) for more.`

## Latched Policy For Slice 4A

The current best policy is now:

- anchor to the current calendar year, not the latest canonical future year
- use a trailing 3-year window over canonical runs
- scope to everything except `department`:
  - `organizing`
  - `reviewing`
  - `mentoring`
- use no cap for now
- keep the policy simple and parameterized so a later cap can be introduced if
  future backfill makes the homepage too dense

Why this is the current recommendation:

- `organizing` only was appealing, but the actual current corpus shows that the
  broader non-`department` scope only adds one additional reviewing run under
  the current 3-year window:
  - `ICFP 2026, Program Committee`
- `department` still adds visibly different institutional/service material that
  should not be mixed into the homepage block without a stronger later policy
- run coalescing has already reduced density enough that the plain 3-year
  window currently stays small without a cap

This policy is intentionally simple first.

If later backfill makes the block too dense, the expected first follow-ons are:

- re-evaluate whether `organizing` should outrank or replace broader
  `reviewing` / `mentoring`
- introduce a cap only if the plain window stops reading well

## Additional Content-Policy Decision

The current `Dagstuhl Seminar 26022: EGRAPHS` service record should not drive
homepage recent-service policy.

The repo should instead treat that as a separate content cleanup:

- remove the Dagstuhl entry from the service domain
- preserve the information through the existing news item and any later more
  appropriate CV/site category
- do not let homepage service policy contort itself around one entry that is
  better understood as research/community participation than service

So slice 4 should proceed assuming the service domain will no longer claim that
entry.

## Narrow Remaining Questions

The remaining slice-4 questions are now much narrower:

1. Multi-URL internal links

For runs like `FPTalks` and `PLDI Workshops`, the current preferred rule is:

- link the homepage summary line to `/service/#<run.key>`

This is now a positive design choice, not just a fallback compromise.

2. Future density handling

The current policy intentionally has no cap.

The slice should keep the implementation parameterized enough that a later cap
can be added cleanly if broader backfill materially changes density.

## Updated Recommendation

Because slice 3 already reduced service-list noise substantially, the next step
should be:

1. simulate a few homepage policies over canonical runs
2. review the rendered outcomes
3. only add homepage-specific stickiness metadata if the simulations prove it
   necessary

That simulation work is now effectively settled.

So the default bias should now be:

- simpler policy first
- metadata later only if justified

## Recommended Slice Shape

### Slice 4A. Policy Simulation / Latch

Implemented in planning.

The current latched direction is:

- current-year anchor
- trailing 3-year window
- all service except `department`
- no cap
- direct link for unambiguous single-URL runs
- internal `/service/#<run.key>` link for multi-URL runs
- no link for no-URL runs
- service-page link sentence retained beneath the section

### Slice 4B. Homepage Projection

Implemented.

- add the homepage placeholder
- render the selected canonical runs
- use the direct-URL vs `/service/#<run.key>` rule now chosen for homepage
  service
- leave no-URL runs unlinked
- keep the trailing service-page sentence authored
- remove the current literal repeated list
- add tests proving the chosen non-`department` window policy over canonical
  runs

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
