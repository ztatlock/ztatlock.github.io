# Talks Campaign

This note captures the next structured-content campaign in detail before the
implementation is split into slices.

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Create one small canonical source of truth for the invited/public talks listed
on the site, then project that data back into the talks page and any later
cross-page views that clearly benefit from it.

The goal is not to invent a giant talks system.
The goal is to remove repeated, list-shaped talk facts from hand-authored pages
while keeping prose and special-case pages simple.

## Why Talks First

Talks are the right first structured-content campaign because:

- `site/pages/talks.dj` is list-shaped and relatively small
- the repeated fields are obvious
- the page has low structural complexity compared with students or
  publications
- the domain is rich enough to teach the projection pattern without forcing a
  huge schema

This is the best place to gain practical experience before tackling larger
campaigns.

## Current Audit

Current relevant sources:

- `site/pages/talks.dj`
  Main talks page with 25 list entries.
- `site/pages/talk-2023-05-egg-uiuc.dj`
  One dedicated talk detail page.
- `site/pages/cv.dj`
  Reuses invited-talk information in hand-authored form.
- `site/pubs/*/publication.json`
  Some publication bundles already include publication-local `"talks"` arrays.

Important current observations:

- the main talks page is a chronological list of invited/public talks
- each entry usually has:
  - title
  - host or venue
  - date
  - optional external link or local talk-page link
- one talk currently has its own dedicated local page
- publication bundles also track talk links, but those are publication-local
  talks or videos and are not the same domain as the invited/public talks page

## Boundary Of The Domain

This campaign should start with a deliberately narrow definition of "talk":

- invited/public talks that belong on `site/pages/talks.dj`

This campaign should not initially absorb:

- publication-local `"talks"` arrays in `site/pubs/<slug>/publication.json`
- service entries like `FPTalks` co-organization
- calendar/course/lab talk references in unrelated prose pages
- one-off prose references in `news.dj`

Why this boundary matters:

- publication-local talk videos already belong with publication bundles
- the invited/public talks page is a simpler and more coherent first target
- crossing those domains too early risks building a messy schema before we have
  experience with the simpler case

If a later slice shows a clean way to connect invited talks and
publication-local talks, that should be a later decision rather than a starting
assumption.

## Likely Canonical Record

The likely first target is:

- `site/data/talks.json`

That file should stay intentionally small.

The initial schema should probably support only the fields the current talks
page actually needs, such as:

- stable key
- title
- date
- event / host text
- optional secondary host / series text
- optional local page path
- optional external URL

Possible extensions, only if they clearly earn their keep:

- speakers
- location
- category / talk kind
- short description or abstract reference

The first schema should not try to model every conceivable talk attribute.

## Relationship To Existing Pages

### `site/pages/talks.dj`

This should be the first projection target.

The likely steady state is:

- hand-authored page header / framing remains in Djot
- repeated talk entries are generated from `site/data/talks.json`

### Dedicated Talk Pages

Dedicated talk pages should remain ordinary pages under `site/pages/`.

The talks data model should probably support an optional link to a local talk
page, but it should not try to absorb those pages into the data file.

That keeps the domain clean:

- shared list facts in `site/data/talks.json`
- talk-specific prose/media on ordinary talk pages

### `site/pages/cv.dj`

The talks campaign should not try to rewrite the CV immediately.

But it should leave a clean path for later reuse of selected talk records in
CV sections once the talks projection pattern is proven.

## Invariants

The first talks data model should validate a small number of clear invariants:

- each talk key is unique
- talk records have a canonical title
- each talk has a usable date representation for sorting
- at most one outward-facing primary link is used for the main list entry
  unless we explicitly decide otherwise
- local talk-page paths, when present, must resolve to real authored pages
- no generated talk entry should require hidden page-specific exceptions

These should be enforced with small focused tests.

## Proposed Campaign Shape

This campaign should proceed in slices.

The likely sequence is:

1. audit the current talks page in detail
   Inventory entry patterns, date formats, links, and special cases.

2. define the smallest useful talks schema
   Keep it honest to the current page instead of overgeneralizing.

3. add a talks loader/validator plus tests
   Fail clearly on duplicate keys, invalid dates, and broken local page links.

4. add a tiny talks renderer/projection helper
   Generate the repeated talks list body from canonical records.

5. switch `site/pages/talks.dj` to use the projection
   Keep header/prose local to the page.

6. stop and reassess
   Only after the talks page is clean should we decide whether to reuse the
   records in CV or elsewhere.

## Expected Benefits

- one canonical source for the talks page
- easier incremental updates when a new talk is added
- less repeated structured editing
- a low-risk proving ground for later students/publications campaigns

## Non-Goals

- building a universal event system
- folding publication-local talk videos into the same schema immediately
- auto-generating all talk detail pages
- rewriting CV or news in the same campaign
- designing around hypothetical future fields before the current page demands
  them

## Current Recommendation

The next planning step after this note should be:

- do a detailed talks-page pattern audit and draft the first talks schema

Only after that should we break the talks campaign into implementation slices.
