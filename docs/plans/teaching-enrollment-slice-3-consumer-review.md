# Teaching Enrollment Slice 3 Consumer Review

Status: implemented

## Purpose

Capture the explicit consumer review after the slice-2 canonical teaching-data
extension and historical enrollment backfill.

This slice is about visible behavior, not additional schema or data work.

## Reviewed Consumers

- [site/teaching/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/teaching/index.dj)
- [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- [page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)

## Main Visible Effects Reviewed

### Public Teaching Page

The `uw-cse-507` family now renders:

- `2026 Spring`
- `2025 Autumn`
- `2023 Autumn`

Important current behavior:

- Spring 2026 is visible as a plain unlinked offering
- this is intentional for now because the course-site URL has not been added
- the family-level heading remains `UW CSE 507: Computer-Aided Reasoning for
  Software`

Judgment:

- acceptable for now
- honest enough under the agreed current umbrella-family stance

### CV Teaching Section

The compressed CV instructor view now shows `2026 Spring` at the front of the
`UW CSE 507` family.

Important current behavior:

- there is no link
- there is no per-offering catalog-label nuance
- the family still reads coherently in the compressed CV format

Judgment:

- acceptable
- no CV renderer change needed

### Homepage Recent Teaching

The homepage recent-teaching block now reflects the latest-year shift caused by
Spring 2026.

Current reviewed result:

- `2026 Spring, UW CSE 507: Computer-Aided Reasoning for Software`
- `2025 Autumn, UW CSE 507: Computer-Aided Reasoning for Software`
- `2025 Spring, UW CSE 505: Concepts of Programming Languages`
- `2024 Autumn, UW CSE 341: Programming Languages`
- `2024 Summer, Marktoberdorf Summer School: Analysis and Optimizations with Equality Saturation`
- `2024 Winter, UW CSE 331: Software Design and Implementation`

Important current behavior:

- Spring 2026 appears without a link
- Autumn 2023 `UW CSE 507` drops out of the homepage block because the trailing
  window now runs `2024-2026`

Judgment:

- acceptable
- this is the intended consequence of the existing recent-teaching policy
- no homepage policy change is needed just because the latest year advanced

## Outcome

Slice 3 did not require renderer changes.

The useful work here was:

- explicit review of the consumer diffs
- explicit confirmation that the no-link Spring 2026 presentation is honest
  for now
- explicit confirmation that the homepage recent-teaching window shift is
  acceptable
- tests hardened to make these conclusions durable

## Remaining Deferred Question

The remaining enrollment-related question is now later and editorial:

- after Spring 2026 enrollment stabilizes, does any public teaching summary or
  CV executive-summary teaching stat clearly earn its keep?

That is a later slice-4 question, not a reason to reopen the current teaching
consumers now.
