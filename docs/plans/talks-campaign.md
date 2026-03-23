# Talks Campaign

This note captures the talks structured-content campaign, the implemented
opening slices, and the current next-checkpoint questions.

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Create one small canonical source of truth for the invited/public talks listed
on the site, then project that data back into the talks page and any later
cross-page views that clearly benefit from it.

The goal is not to invent a giant talks system.
The goal is to remove repeated, list-shaped talk facts from hand-authored pages
while keeping talk-local prose/assets with the talk that they belong to.

## Why Talks First

Talks are the right first structured-content campaign because:

- the talks index is list-shaped and relatively small
- the repeated fields are obvious
- the page has low structural complexity compared with students or
  publications
- the domain is rich enough to teach the projection pattern without forcing a
  huge schema

This is the best place to gain practical experience before tackling larger
campaigns.

## Current Audit

Current relevant sources:

- `site/talks/index.dj`
  Main talks collection index wrapper, projected from 25 talk bundles.
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

### Pattern Summary

The current talks page has 25 entries.

Observed date patterns:

- 23 entries use a month-plus-year date such as `February 2026`
- 2 entries use a season-plus-year date such as `Fall 2023`

Observed title-link patterns:

- 22 entries use a plain unlinked title
- 2 entries use an external title link
- 1 entry uses a local title link to a dedicated talk page

Observed host/venue patterns:

- most entries have one display line after the title
- 2 entries split the host and date onto separate continuation lines
- 1 entry uses a two-part host/series display where the second segment is
  linked (`Compilers Seminar`)

Observed content-shape patterns:

- duplicate titles are common, so title alone is not a stable identifier
- the list is reverse-chronological
- all current entries are talks by Zach, so the first schema does not need a
  speaker field
- dedicated talk prose/media is currently exceptional rather than the norm
- exactly one current entry points at a local talk page, so that case should be
  treated as an explicit first-slice decision rather than hidden in the schema

### Consequences For The First Schema

These patterns imply:

- the model needs a stable identity independent of title
- the schema needs a structured date model that supports both month/year and
  season/year
- the schema needs one primary title link slot
- the schema needs a small amount of structured host/series support, but not a
  general event model
- the schema does not need to model speakers, abstracts, or detail-page prose
  in the first slice
- the one existing local talk-page link must be handled deliberately, not by
  quietly distorting the common-case schema

## Boundary Of The Domain

This campaign should start with a deliberately narrow definition of "talk":

- invited/public talks that belong on `site/talks/index.dj`

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

## Likely Canonical Source Model

The likely first target is a new bundle root:

- `site/talks/<slug>/talk.json`

Each talk bundle should be allowed to stay extremely small.
A simple talk may only need:

- `talk.json`

But the model should also allow optional talk-local files such as:

- `extra.dj`
- local images
- talk-local attachments if they ever clearly earn their keep

This mirrors the successful `site/pubs/<slug>/publication.json` pattern:

- keep local facts with the record
- allow optional per-record assets or prose
- derive global lists from the bundles when needed

### Why Bundles Instead Of One Global `talks.json`

The bundle model is a better fit here because talks may naturally grow:

- a dedicated talk page
- talk-specific prose
- embeds or media
- local assets

The current dedicated talk page at
`site/pages/talk-2023-05-egg-uiuc.dj` is already a signal that talk-local
context is real, even if it is still rare.

So the intended model is:

- keep talk-local facts in `site/talks/<slug>/`
- derive a global in-memory talk table during the build
- render the talks index from those bundles

That is a little more file structure than one flat JSON list, but it is a
cleaner long-term shape.

### Draft Minimal `talk.json` Schema

The first `talk.json` schema should probably support only the fields the
current talks page actually needs, such as:

- title
- structured date
- one or more host / series display segments
- optional external URL

Possible extensions, only if they clearly earn their keep:

- `extra.dj` for local detail-page prose
- local media/assets
- speakers
- location
- category / talk kind

The first schema should not try to model every conceivable talk attribute.

The first schema should be intentionally small and should map directly to the
current page shape.

At a high level:

```text
site/talks/
  2026-02-brown-eqsat/
    talk.json
  2023-05-uiuc-egg/
    talk.json
    extra.dj
```

Example `talk.json`:

```json
{
  "title": "Everything is a compiler, try Equality Saturation!",
  "when": { "year": 2026, "month": 2 },
  "at": [
    { "text": "Brown University" },
    { "text": "PL and Graphics groups" }
  ],
  "url": "https://events.brown.edu/computer-science/event/326439-bvc-seminar-zachary-tatlock-university-of"
}
```

Suggested field meanings:

- bundle slug
  The directory name is the stable identifier, for example
  `2026-02-brown-eqsat`. The schema does not need a second synthetic `key`
  field unless experience later shows that it earns its keep.
- `title`
  Canonical rendered title text for the list entry.
- `when`
  Structured date object with required `year` and exactly one of:
  - `month`
  - `season`
- `at`
  Ordered display segments for the host / venue / series portion of the entry.
  Each segment has:
  - required `text`
  - optional `url`
- `url`
  Optional primary link target for the title.
  In the first slice this may be either:
  - an external URL
  - the existing ordinary-page URL `talk-2023-05-egg-uiuc.html`
- `extra.dj`
  Optional talk-local prose file. If present, it is a signal that the bundle
  may deserve a dedicated detail page.

First-slice rendering rule:

- if `url` is present, link the title to that target
- else render the title as plain text

First-slice bundle rule:

- all talk bundles participate in the global talks index
- no dedicated talk-page route is required in the first slice
- if a bundle has `extra.dj`, treat that as future-facing talk-local content,
  not an immediate requirement to add a new route class

First-slice date rendering rule:

- `month` renders as `Month YYYY`
- `season` renders as `Season YYYY`

This should reproduce the common entry shape cleanly.
The one current local talk-page link remains the main explicit first-slice
decision to resolve.

## Relationship To Existing Pages

### Talks Index Wrapper

Slice 2 moved the talks wrapper to:

- `site/talks/index.dj`

The current talks index model is now:

- hand-authored page header / framing remains in Djot
- repeated talk entries are generated from discovered talk bundles
- the public route is `/talks/`

That matches the intended collection model:

- singleton pages under `site/pages/`
- collection indexes under the collection root
- collection items under the same collection root

### Dedicated Talk Pages

Dedicated talk pages should move toward living with the talk bundle rather than
remaining separate ordinary pages forever.

That does not mean the first slice has to add talk detail-page routes.
It means the campaign should leave a clean path for a later slice to say:

- if `site/talks/<slug>/extra.dj` exists, build `build/talks/<slug>/index.html`

That keeps the domain clean:

- shared list facts in talk bundles
- talk-specific prose/media in the same bundle when needed

### `site/pages/cv.dj`

The talks campaign should not try to rewrite the CV immediately.

But it should leave a clean path for later reuse of selected talk records in
CV sections once the talks projection pattern is proven.

## Invariants

The first talks data model should validate a small number of clear invariants:

- each talk bundle slug is unique
- talk records have a canonical title
- each talk has `when.year` plus exactly one of `when.month` or
  `when.season`
- `when.month`, when present, is a valid month number
- `when.season`, when present, is one of a very small allowed set such as
  `spring`, `summer`, `fall`, `winter`
- each talk has a usable date representation for reverse-chronological sorting
- each talk has at least one `at` segment
- `talk.json` must exist for every talk bundle
- `extra.dj`, when present, must live in the same bundle
- no generated talk entry should require hidden page-specific exceptions
- entries should remain stable under deterministic sort order

These should be enforced with small focused tests.

## Proposed Campaign Shape

This campaign should proceed in slices.

The likely sequence is:

1. audit the current talks page in detail
   Inventory entry patterns, date formats, links, and special cases.

2. define the smallest useful talks schema
   Keep it honest to the current page instead of overgeneralizing.

3. add a talks bundle loader/validator plus tests
   Fail clearly on invalid bundle contents, invalid dates, and broken optional
   local files.

4. add a tiny talks renderer/projection helper
   Generate the repeated talks list body from discovered talk bundles.

5. switch `site/pages/talks.dj` to use the projection
   Keep header/prose local to the page.

6. stop and reassess
   Only after the talks page is clean should we decide whether to reuse the
   bundles in CV or elsewhere, or whether to introduce dedicated talk-page
   routes from `extra.dj`.

## First Slice

The first implementation slice should stay deliberately narrow:

1. add `site/talks/<slug>/talk.json` bundles for the current talks page
2. add a talks bundle loader/validator plus tests
3. add a projection helper that can render the repeated talks list body
4. switch `site/pages/talks.dj` to use that projection
5. keep `site/pages/talk-2023-05-egg-uiuc.dj` unchanged for now and point the
   corresponding talk bundle at it via `url`

That is the right size because it:

- establishes the canonical bundle model
- proves the projection pattern on one real page
- avoids taking on talk detail routes in the same slice
- leaves the one exceptional local talk page in place as a clean future test
  case

### Explicit Stop Point

After that first slice lands, stop and reassess before doing more.

Questions for that checkpoint:

- does the bundle model feel clean in day-to-day editing?
- does the generated talks page remain easy to review?
- does the UIUC talk page still look like a good candidate for folding into a
  later `extra.dj` + talk-detail-route slice?
- do we want CV reuse next, or should talks remain isolated until later?

The campaign should not move past that checkpoint automatically.
This is where we should reflect and choose the next slice deliberately.

## Expected Benefits

- one canonical source model for the talks page
- easier incremental updates when a new talk is added
- less repeated structured editing
- a low-risk proving ground for later students/publications campaigns

## Non-Goals

- building a universal event system
- folding publication-local talk videos into the same schema immediately
- auto-generating all talk detail pages in the first slice
- rewriting CV or news in the same campaign
- designing around hypothetical future fields before the current page demands
  them

## Current Recommendation

Slices 1 and 2 were the right opening steps for this campaign:

- slice 1 established talk bundles and projection from canonical talk records
- slice 2 introduced the collection index pattern via `site/talks/index.dj`
  and `/talks/`

The right move now is to stop and reassess before planning slice 3.

Questions for the next checkpoint:

- does `site/talks/index.dj` feel like the right long-term pattern for
  collection indexes?
- does the new route kind feel small and honest enough to reuse later for
  `site/pubs/index.dj`?
- should the next talks slice be a talk detail-page slice from `extra.dj`, or
  should we first reuse the collection-index pattern elsewhere?
