# News Slice 3: Homepage Consumer

Status: planned

It builds on:

- [news-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-campaign.md)
- [news-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-slice-1-canonical-model.md)
- [news-slice-2-public-wrapper-and-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-slice-2-public-wrapper-and-projection.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Turn the homepage `## News` block into an explicit curated consumer of
canonical news records, without changing the public `/news/` page into a
homepage-driven view.

This slice should:

- stop hand-maintaining the repeated homepage news item body
- keep the homepage `## News` heading and trailing "past news" sentence
  authored
- make homepage inclusion policy explicit in projection logic
- add a small optional homepage-stickiness signal to canonical news records
- keep homepage news order aligned with canonical news order

It should not yet:

- add typed cross-domain links
- invent a separate homepage-only news schema
- redesign the homepage news presentation
- change the canonical `/news/` page away from showing the full news stream

## Why This Slice Matters

The repo has already reached the awkward middle state:

- the canonical editorial records live in
  [site/data/news.json](/Users/ztatlock/www/ztatlock.github.io/site/data/news.json)
- the public news page at
  [site/news/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/news/index.dj)
  now projects from those records
- the homepage
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
  still carries a second literal copy of most of the same item stream

That means the homepage is now the last real drift seam in the news domain.

## Current Behavior

Today:

- the public `/news/` page shows the full canonical record stream
- the homepage `## News` block still contains literal month headings and
  literal news items
- the homepage ends with an authored `Please see [past news](news/) for more.`
  sentence

Current overlap facts:

- the homepage duplicates `13` of the `15` month buckets in the full news page
- the homepage duplicates `21` of the `23` individual items
- the homepage omits exactly:
  - April 2023 Business Insider interview
  - August 2017 Neutrons feature roundup

That omission pattern is important:

- the homepage is not just "latest N"
- the homepage is a curated teaser of the full news stream

## Recommended Curation Model

This slice should make homepage curation explicit as a deterministic derived
policy, not as a second hand-maintained filter.

Recommended rule:

- start from the most recent canonical news month
- consider only items from that month back through the previous `11` months
- show at most `15` homepage news items from that `12`-month window
- always include the `10` most recent items from the window
- if the `12`-month window has more than `10` items, use optional
  `homepage_featured` on older in-window items to keep a few sticky items on
  the homepage before filling remaining slots by pure recency

Why this is the right level of structure:

- it keeps the homepage a derived teaser over the canonical stream
- it uses only one small per-record homepage-only signal rather than a second
  homepage registry
- it keeps the policy simple and reviewable
- it keeps homepage ordering aligned with canonical news order
- it is robust to both sparse periods and heavy-news periods

What this slice should not add:

- homepage-specific reordering fields
- homepage-specific headline rewrites
- separate homepage-only emoji or kind rules

Important determinism note:

- the window should be anchored to the most recent canonical news month in
  `site/data/news.json`, not to the wall clock at build time

That keeps builds deterministic and avoids silent month-rollover drift.

Recommended field addition:

- optional `homepage_featured`
  boolean, default false

Important policy note:

- `homepage_featured` only affects the homepage consumer
- it does not affect ordering or rendering on `/news/`
- it only matters when the `12`-month window contains more than `10` items
- if the `12`-month window contains `15` or fewer items, all in-window items
  still appear and `homepage_featured` has no visible effect

## Wrapper / Projection Policy

What should stay authored in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj):

- the `## News` heading
- any local framing text
- the trailing `Please see [past news](news/) for more.` sentence

What should become projected:

- the repeated month-grouped homepage news body

Recommended placeholder:

- `__HOMEPAGE_NEWS_MONTH_GROUPS__`

That keeps the homepage readable and lets the page continue to own its local
framing without staying a second source of truth for repeated news items.

## Projection Policy

Recommended behavior:

- compute the latest canonical `(year, month)` pair from the news records
- include all records whose `(year, month)` falls within that latest month and
  the previous `11` months
- if the in-window set has `15` or fewer items, show them all in canonical
  order
- if the in-window set has more than `15` items:
  - always keep the `10` most recent in-window items
  - then consider the remaining older in-window items, newest first
  - add `homepage_featured` items from that older pool until reaching `15` or
    exhausting featured candidates
  - if fewer than `15` items have been selected, continue filling from the
    remaining older non-featured pool by recency until reaching `15`
- preserve canonical relative order in the final selected subset
- group consecutive filtered items by `(year, month)`
- render the same broad month-grouped shape the homepage uses today

This keeps the homepage teaser aligned with the canonical news stream through a
simple recency-first rule while still giving you a narrow sticky override in
high-volume periods.

## Validation Contract

After this slice, source validation should enforce:

- `homepage_featured`, when present, is boolean
- the homepage `## News` section contains
  `__HOMEPAGE_NEWS_MONTH_GROUPS__`
- the homepage `## News` section does not contain literal repeated month
  headings or literal repeated news item blocks
- the authored `past news` sentence still points to `news/`

If practical, the validator should scope those checks to the homepage `## News`
section rather than scanning the whole file blindly.

## Likely Code Surfaces

Primary implementation surfaces:

- [site/data/news.json](/Users/ztatlock/www/ztatlock.github.io/site/data/news.json)
- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- [scripts/news_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/news_record.py)
- [scripts/news_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/news_index.py)
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [scripts/sitebuild/source_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/source_validate.py)

Likely tests:

- [tests/test_news_record.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_news_record.py)
- [tests/test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)
- [tests/test_page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_renderer.py)
- [tests/test_source_validate.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_source_validate.py)

## Expected Visible Changes

This slice should intentionally change the homepage source of truth, but not
its editorial content.

What should stay the same:

- the homepage `## News` heading
- the visible item wording
- the visible month grouping
- the visible item order
- the trailing `past news` line

What should change:

- the repeated homepage news body is no longer hand-maintained
- the homepage becomes a deterministic recent-news view over the canonical
  stream
- older items outside the trailing `12`-month window will disappear from the
  homepage even though they remain on `/news/`
- in heavier-news periods, a small number of older in-window featured items
  may remain visible after the `10` most recent items

Current-state consequence:

- with the current canonical data, the trailing `12`-month window from
  February 2026 contains only three items, so the homepage will become much
  shorter until later news backfill expands that window

## Verification

Verification should include:

- focused news-record tests for optional `homepage_featured`
- focused projection tests for trailing-`12`-month filtering
- focused projection tests for `>15` item overflow with featured stickiness
- focused projection tests for homepage news filtering and grouping
- focused source-validation tests for the homepage news placeholder
- `make verify`
- `make routes`
- `git diff --check`

Rendered review should confirm:

- the homepage remains unchanged in visible substance
- the public `/news/` page remains unchanged
- no new routes are introduced

## Invariant After This Slice

After this slice:

- `site/data/news.json` remains the one canonical editorial news source
- the public `/news/` page still shows the full canonical stream
- the homepage `## News` block becomes an explicit curated consumer of that
  same stream
- homepage inclusion is reviewable through one deterministic recent-news rule:
  trailing `12` months, hard cap `15`, always keep the `10` most recent, and
  use optional `homepage_featured` only for older in-window stickiness when
  the window overflows
- homepage and news page can no longer drift silently
