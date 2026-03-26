# Homepage / CV Curated Consumers Slice 2: Homepage Recent Teaching

Status: planned

It builds on:

- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Turn the homepage `## Recent Teaching` block into a tiny derived consumer of
[site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json),
while keeping the section heading and trailing "teaching page" sentence
authored in the homepage wrapper.

This slice should:

- stop hand-maintaining the repeated recent-teaching bullets on the homepage
- preserve the current compact flattened offering style
- make homepage teaching selection and ordering explicit

It should not:

- change the public `/teaching/` page
- change the CV teaching section
- surface staffing details on the homepage
- include Zach's historical `teaching_assistant` group
- redesign homepage layout generally

## Why This Slice Looks Safe

The current homepage block already behaves like a tiny derived view.

Current authored block in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj):

- contains 7 bullets
- every bullet is one flattened instructor offering with a direct offering URL
- all 7 bullets correspond to canonical offerings in the `uw_courses` group of
  [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- the block does not currently try to show staffing, descriptions, or broader
  teaching context

So the main job is not to invent a new homepage teaching design.
It is to stop keeping a second copy of a small canonical recent-teaching
subset while broadening the consumer just enough to include recent special
topics and summer-school teaching when they fall inside the same recent
window.

## Current Behavior

Today:

- the homepage keeps a literal 7-bullet `## Recent Teaching` list
- each bullet is one link of the form:
  `YEAR TERM, CODE: Title`
- the trailing sentence remains authored:
  `Please see my [teaching page](teaching/) for more.`

This is already a consumer shape.
It is just hand-maintained instead of projected.

## Proposed Behavior

After this slice:

- `## Recent Teaching` stays authored in
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- the trailing "teaching page" sentence stays authored
- only the repeated list body is projected from canonical teaching data

Recommended placeholder:

- `__HOMEPAGE_RECENT_TEACHING_LIST__`

## Recommended Selection And Ordering Policy

The homepage should remain intentionally slim, but the recent-teaching
consumer should now cover the full recent teaching surface rather than only
recurring UW course offerings.

Recommended source scope:

- `uw_courses` offerings
- `special_topics` offerings
- `summer_school` events

Recommended exclusion scope:

- no historical `teaching_assistant` records

Recommended recency window:

- anchor to the most recent canonical teaching year
- include only items from that year and the previous `2` years

Recommended recency order:

- sort by `year` descending
- then by derived month descending using:
  - `Autumn = 9`
  - `Summer = 7`
  - `Spring = 4`
  - `Winter = 1`
- treat summer-school events as month `7`
- preserve canonical file order as the tie-break if two items would otherwise
  compare equal

This policy keeps the homepage honest as "recent teaching" while still
allowing items like Marktoberdorf Summer School 2024 to appear naturally
within the same chronological stream.

## Render Policy

Recommended homepage render policy:

- render each selected item as one bullet
- render the whole bullet as one link when a URL exists
- for course offerings, use display text:
  `YEAR TERM, CODE: Title`
- for summer-school events, use display text:
  `YEAR Summer, EVENT: TITLE`
- if an item lacks URL, render the same display text as plain text
- do not show staffing lines
- do not show course descriptions

This keeps the homepage recent-teaching block explicitly compressed and
homepage-specific.

## Invariant

After this slice:

- the homepage recent-teaching body can no longer drift from the canonical
  teaching records in `site/data/teaching.json`
- the homepage remains a compressed recent-teaching consumer rather than a
  second mini `/teaching/` page
- no new homepage-only teaching-selection metadata is introduced

Small supporting data-model note:

- seeded summer-school events should carry explicit `year` so the homepage
  consumer can use a deterministic recent-year window without parsing public
  labels

## Likely Code Surfaces

Primary implementation surfaces:

- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [scripts/sitebuild/source_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/source_validate.py)

Likely tests:

- [tests/test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)
- [tests/test_page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_renderer.py)
- [tests/test_source_validate.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_source_validate.py)

## Validation Contract

After this slice, source validation should enforce:

- the homepage `## Recent Teaching` section contains
  `__HOMEPAGE_RECENT_TEACHING_LIST__`
- the section does not contain a leftover literal repeated recent-teaching
  body
- the trailing teaching-page link still uses canonical `teaching/`

If practical, those checks should be scoped to the homepage section rather
than scanning the whole file blindly.

## Expected Visible Changes

This slice should ideally produce no intentional rendered HTML change.

What should stay the same:

- section heading
- bullet wording
- bullet order
- bullet link targets
- trailing teaching-page sentence

The intended change is source-of-truth cleanup, not presentation change.

## Verification

Verification should include:

- focused homepage projection tests
- focused source-validation tests
- `make verify`
- `git diff --check`

Rendered diff review should confirm:

- no visible change outside [build/index.html](/Users/ztatlock/www/ztatlock.github.io/build/index.html)
- ideally no substantive visible change even within the homepage recent
  teaching block
