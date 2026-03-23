# Talks Slice 2: Collection Index Page

Status: Implemented

This note defines the next implementation slice after
[talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)
slice 1.

Slice 1 established talk bundles as the canonical source of truth and made the
talks list on the site a projection instead of a hand-maintained duplicate.
That was the right first step.

Before this slice, the wrapper still lived at:

- `site/pages/talks.dj`

and therefore still behaved like an ordinary singleton page routed at:

- `/talks.html`

That was the main mismatch between the talks campaign and the cleaner
long-term model we want for collection-backed content.

## Why This Slice Mattered

The architecture we are converging on is:

- `site/pages/` for singleton pages
- `site/<collection>/index.dj` for collection index pages
- `site/<collection>/<slug>/...` for item bundles

For talks, that means:

- `site/talks/index.dj`
- `site/talks/<slug>/talk.json`

For publications later, that likely means:

- `site/pubs/index.dj`
- `site/pubs/<slug>/publication.json`

So this slice is not just a talks cleanup.
It was the first small step toward a cleaner talks-index pattern while keeping
the implementation honestly talks-specific for now.

## Slice Goal

This slice added explicit support for collection index pages, moved the talks
index wrapper from `site/pages/talks.dj` to `site/talks/index.dj`, and made
its canonical public URL `/talks/`.

## Scope

This slice should do exactly these things:

1. add support for collection index page routes
2. move the talks index wrapper to `site/talks/index.dj`
3. make the talks index route canonical at `/talks/`
4. rewrite authored internal links from `talks.html` to `talks/`
5. keep the UIUC talk detail page separate
6. stop and reassess

## Non-Goals

This slice should not:

- add talk detail routes from `extra.dj`
- fold `site/pages/talk-2023-05-egg-uiuc.dj` into the talk bundle model
- change publications routing yet
- move `site/pages/publications.dj` into `site/pubs/index.dj` yet
- reuse talks in CV
- merge invited talks with publication-local `"talks"` arrays

## Final Invariants For This Slice

At the end of this slice, these things should be true:

1. The canonical authored wrapper for the talks index is:
   - `site/talks/index.dj`
2. The canonical built output for the talks index is:
   - `build/talks/index.html`
3. The canonical public URL for the talks index is:
   - `/talks/`
4. The talks collection index route is explicit in the route table and is not
   disguised as an ordinary singleton page.
5. The talks collection index depends on:
   - `site/talks/index.dj`
   - all discovered `site/talks/<slug>/talk.json` records
6. If talk bundles exist, source validation requires `site/talks/index.dj`
   with `__TALKS_LIST__`.
7. `site/pages/talks.dj` is no longer accepted as the canonical talks index
   wrapper.
8. Authored source should not contain local links to `talks.html`.
9. The UIUC talk page remains reachable via its existing ordinary-page route.

These are the invariants that make the talks collection read like a real
collection instead of a singleton page with special dependencies.

## Design Choices

### 1. Use An Explicit Talks Index Route Kind

The cleanest route model for this slice is:

- `ordinary_page`
- `talks_index_page`
- `publication_page`
- `static_file`

I do not recommend trying to pretend `site/talks/index.dj` is just another
ordinary page.

Why:

- collection indexes have different source roots
- collection indexes naturally want directory URLs like `/talks/`
- collection indexes may depend on bundle discovery in a way ordinary pages do
  not
- publications will likely want the same pattern later

That was enough conceptual difference to justify a small explicit route kind.

### 2. Keep The Projection Logic Slightly More General

The current talks projection had been keyed to the ordinary page stem `talks`.

This slice should move that one step closer to a reusable pattern by making the
projection decision depend on route kind plus collection key, not on a
singleton page-stem convention.

That does not mean building a large projection framework yet.
It only means avoiding another talks-specific assumption that publications
would have to undo later.

### 3. Keep The UIUC Talk Page Separate

`site/pages/talk-2023-05-egg-uiuc.dj` should remain an ordinary page in this
slice.

Its talk bundle should continue to point at that page with `url`.
That keeps the slice tightly scoped and preserves a clean future test case for
talk-local `extra.dj` and detail-route work.

## Implementation Order

### Step 1: Add Collection Index Route Support

Introduce a new route kind for collection index pages.

The first implementation only needs one collection:

- `talks`

Suggested initial rule:

- source: `site/talks/index.dj`
- output: `build/talks/index.html`
- public URL: `/talks/`
- canonical URL: `https://ztatlock.net/talks/`
- draft status: same `# DRAFT` rule used for ordinary Djot pages

Keep the route model explicit and small.
Do not add speculative support for every future collection in the same step.

Tests to add or update:

- route-model validation accepts the new route kind
- route discovery finds `talks_index_page:talks`
- route discovery gives it the expected output path and public URL
- the route source paths include `site/talks/index.dj` plus talk records

Stop and reflect:

- Is the route kind naming clear?
- Is the route table becoming simpler, not more magical?

### Step 2: Move Talks Projection Selection To The New Route Shape

Update the projection/render path so the talks list is applied for:

- `talks_index_page`
- key `talks`

instead of:

- ordinary page stem `talks`

This should be the smallest generalization that makes the code read honestly.

Good end state for this step:

- the page renderer does not need to know about `site/pages/talks.dj`
- the projection helper no longer pretends the talks index is a singleton page

Tests to add or update:

- collection index page rendering fills `__TALKS_LIST__`
- non-talk collection pages or ordinary pages are unaffected

Stop and reflect:

- Did this step reduce hardcoded page-name assumptions?
- Did we keep the abstraction small?

### Step 3: Update Source Validation And Authoring Rules

Move the source expectation from:

- `site/pages/talks.dj`

to:

- `site/talks/index.dj`

Source validation should now enforce:

- if talk bundles exist, `site/talks/index.dj` must exist
- it must contain `__TALKS_LIST__`
- `site/pages/talks.dj` should not coexist as a second canonical wrapper

This step should also explicitly reject legacy authored internal links to:

- `talks.html`

because after this slice that will no longer be the canonical talks URL.

Tests to add or update:

- missing `site/talks/index.dj` is reported
- missing placeholder is reported
- legacy `talks.html` source links are reported
- the old `site/pages/talks.dj` expectation is gone

Stop and reflect:

- Are we making the source rules clearer for a newcomer?
- Did we avoid temporary dual-wrapper support?

### Step 4: Move The Wrapper And Rewrite Source Links

Move the current wrapper content from:

- `site/pages/talks.dj`

to:

- `site/talks/index.dj`

Keep its authored front matter and header intact.

Also update any authored local links that currently point at:

- `talks.html`

to instead point at:

- `talks/`

At the moment this appears to be a small, reviewable edit set.

Tests to update:

- end-to-end build writes `build/talks/index.html`
- no `build/talks.html` is produced

### Step 5: Verify And Stop

Run the normal checks:

- `make test`
- `make build`
- `make check`

Then stop.

Do not continue automatically into:

- talk detail routes
- publications collection index work
- CV reuse

This slice should end with a deliberate reassessment.

## Tests We Want

The slice should leave behind focused tests for these invariants:

- collection index route discovery
- collection index route rendering
- talk bundle dependency tracking for the talks index route
- source validation for `site/talks/index.dj`
- rejection of legacy `talks.html` links in authored source
- end-to-end build output at `build/talks/index.html`

The tests should read like executable documentation for the new collection
index pattern.

## Key Risks To Watch

### Hidden URL Drift

If authored pages still point at `talks.html`, the route move will quietly
break navigation.

This is why link rewriting is part of the slice, not an optional cleanup.

### Too Many Talks-Specific Hacks

If we implement collection index pages with a pile of `if key == "talks"`
branches, publications will later inherit another awkward special case.

This slice should keep the abstraction as small as possible while still being
honest.

### Premature Generalization

This slice is not the place to invent a generic CMS layer.

We only need enough structure to represent one real collection index cleanly.

## Explicit Reassessment Questions

After the slice lands, stop and ask:

1. Does the collection-index-page route feel like a clean general pattern?
2. Does `site/talks/index.dj` feel more natural than `site/pages/talks.dj`?
3. Does this make the future `site/pubs/index.dj` direction clearer?
4. Is the UIUC talk page still the right next detail-page test case?
5. Is the next talks slice about detail pages, or should we first reuse the
   new collection-index pattern for publications?

We should answer those questions before planning the following slice.
