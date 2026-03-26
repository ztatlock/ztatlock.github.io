# News Slice 1: Canonical News Model

Status: planned

It builds on:

- [news-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Capture the current news stream in one canonical ordered data file before any
wrapper cutover, route change, or homepage reuse.

This slice should make the repeated news items reviewable as structured data
without yet changing:

- the public route
- the public wrapper location
- the homepage consumer
- the visible rendered site

## Why This Slice First

The current news surface is already acting like one canonical stream with two
hand-maintained consumers:

- [site/pages/news.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/news.dj)
- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)

But there is no canonical shared-data layer yet.

The right first step is therefore not route churn or homepage policy.
It is to capture the repeated item stream in a small explicit data model so the
repo can review and validate it before any consumer cutover.

## Scope

In scope:

- add canonical ordered news records in `site/data/news.json`
- add a small validated news-record loader
- backfill the current `23` public news items into the canonical data file
- keep explicit `kind` and explicit `emoji` on every canonical item
- define ordering policy for month-grouped public rendering later
- add focused tests and source validation for the new data model

Out of scope:

- moving the public wrapper to `site/news/index.dj`
- canonicalizing `/news/`
- projecting the public news page from the new records
- changing homepage news behavior
- adding typed links back to talks/publications/teaching/service/projects

## Current Audit Facts

Current authored news page facts:

- `15` month buckets
- `23` individual items

Current item kinds are mixed enough that news should remain its own editorial
domain rather than a derived event view:

- `talk`
- `teaching`
- `community`
- `release`
- `recognition`
- `media`

The icon usage is also mixed enough that emoji should stay explicit in slice 1:

- `🗣️`: `14`
- `🧰`: `3`
- `🧑‍🏫`: `2`
- `🎯`: `1`
- `⛰️`: `1`
- `📰`: `2`

## Canonical Shape

Recommended top-level shape:

- ordered `records`

Recommended per-record fields:

- required `key`
- required `year`
- required `month`
- optional `sort_day`
- required `kind`
- required `emoji`
- required `body_djot`

Example shape:

```json
{
  "records": [
    {
      "key": "2026-02-brown-talk",
      "year": 2026,
      "month": 2,
      "kind": "talk",
      "emoji": "🗣️",
      "body_djot": "Visiting the PL and Graphics groups at Brown University to give a talk."
    }
  ]
}
```

## Key Policy

Recommended key format:

- `YYYY-MM-short-slug`

Examples:

- `2026-02-brown-talk`
- `2025-06-pldi-success`
- `2024-09-marktoberdorf`

The key should be:

- unique
- stable
- descriptive enough for diffs and review

It should not encode the emoji or try to capture every semantic dimension of
the item.

## Kind Policy

Slice 1 should use a small controlled vocabulary, but not a tiny taxonomy that
only fits today's page.

Recommended approved `kind` list:

- `talk`
- `publication`
- `teaching`
- `community`
- `release`
- `recognition`
- `student`
- `media`
- `funding`
- `other`

Important policy:

- `kind` captures the primary editorial angle of the item
- it does not need to express every dimension the item touches
- new items should normally fit one of the approved kinds
- if repeated future items do not fit well, the approved list can be revised
  deliberately in a later slice

## Emoji Policy

Emoji should remain explicit in slice 1 rather than being derived from `kind`.

Why:

- some kinds already have stable icon habits
- others still use icon choice as editorial tone rather than strict category
  signaling
- explicit emoji preserves the current page exactly while keeping the schema
  honest

This slice should not try to establish default emoji-by-kind rules.

## Ordering Policy

The canonical source should stay as one ordered flat record list.

Display grouping later should be renderer behavior:

- group consecutive records by `(year, month)`
- render a month heading when the pair changes

Ordering rules for slice 1:

- records are maintained in canonical display order
- `year` and `month` establish the primary reverse-chronological grouping
- `sort_day`, when present, refines order within the same month
- when `sort_day` is absent, file order remains the same-month tie-break

This slice should not introduce free-form internal ordering notes.

## Validation Contract

Focused validation should enforce:

- `site/data/news.json` exists and parses
- top-level shape contains ordered `records`
- every record has a unique `key`
- `year` is an integer
- `month` is an integer in `1..12`
- `sort_day`, when present, is an integer in `1..31`
- `kind` is one of the approved values
- `emoji` is a non-empty string
- `body_djot` is a non-empty string
- records stay grouped in non-increasing `(year, month)` order
- when two adjacent records share `(year, month)` and both have `sort_day`,
  their `sort_day` values stay in non-increasing order

This slice does not need to validate typed cross-links because it does not add
any.

## Likely Code Surfaces

Primary implementation surfaces:

- `site/data/news.json`
- `scripts/news_record.py`
- `scripts/sitebuild/source_validate.py`

Likely tests:

- `tests/test_news_record.py`

This slice should stay out of:

- `scripts/sitebuild/route_model.py`
- `scripts/sitebuild/route_discovery.py`
- `scripts/sitebuild/page_projection.py`
- `site/pages/news.dj`
- `site/pages/index.dj`

## Verification

Focused verification should include:

- `python3 -m unittest tests.test_news_record`
- `make verify`
- `git diff --check`

Because this slice is data-foundation only, the expected rendered diff is:

- none

## Documentation Updates When This Lands

Update:

- `docs/plans/news-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

The docs should describe the new canonical record model without yet claiming
that the public route or homepage consumer has changed.

## Planned Invariant

After this slice:

- the repo has one canonical ordered source of truth for news items at
  `site/data/news.json`
- the canonical unit is an individual news item, not a month bucket
- each canonical item has explicit `kind` and explicit `emoji`
- later public grouping by month/year is a renderer concern rather than a data
  nesting decision
- the public `/news.html` page and homepage news block remain hand-authored
  consumers until later slices cut them over deliberately
