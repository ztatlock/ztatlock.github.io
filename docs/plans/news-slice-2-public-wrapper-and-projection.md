# News Slice 2: Public Wrapper And Projection

Status: implemented

It builds on:

- [news-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-campaign.md)
- [news-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-slice-1-canonical-model.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Turn the public news page into a thin authored wrapper over canonical news
records, while deliberately leaving the homepage `## News` block alone.

This slice should:

- move the public wrapper out of `site/pages/news.dj`
- canonicalize the public route as `/news/`
- project the repeated month-grouped news body from `site/data/news.json`
- keep the page title and front matter authored

It should not yet:

- change homepage news behavior
- add typed cross-domain links
- change the canonical news data model from slice 1

## Why Combine Wrapper Move, Route Cutover, And Projection

For news, these belong together.

If we projected first into `site/pages/news.dj`, we would immediately invest in
an ordinary-page location and `/news.html` route that we already expect to
replace.

Combining the wrapper move, route cutover, and first projection keeps the
slice coherent:

- one public wrapper move
- one canonical route decision
- one projection pass
- one reviewable visible change

## Current Behavior

Today:

- canonical repeated news data lives in `site/data/news.json`
- the public news page is still hand-authored at `site/pages/news.dj`
- the public route is still `/news.html`
- the homepage still links to `news.html`

So the repo has canonical news data, but the public news page is still a
literal second copy of the repeated item stream.

## Proposed Behavior

After this slice:

- the public wrapper lives at `site/news/index.dj`
- the canonical route is `/news/`
- the wrapper keeps front matter and the `# ... / News` heading authored
- the repeated month-grouped news body is projected from `site/data/news.json`

The homepage remains intentionally separate for now.

## Why `site/news/`

Once news has:

- canonical shared data in `site/data/news.json`
- a public wrapper
- a later homepage consumer

it is no longer just an ordinary prose page.

The cleaner separation is:

- `site/data/news.json`
  canonical editorial records
- `site/news/index.dj`
  authored public wrapper

That keeps the route/source shape aligned with the repo's other structured
wrapper domains without pretending news is derived from another domain.

## Canonical Public URL

The current route is `/news.html`.

After talks, students, teaching, service, funding, collaborators, pubs, and
CV, the repo has a clear wrapper-route pattern for category-like landing pages.

`/news/` is the cleaner long-term route for the public news page.

## What Should Stay Hand-Authored

The wrapper should remain intentionally small.

What should stay authored in `site/news/index.dj`:

- page front matter
- page heading
- any later short intro or framing text

What should be generated:

- the repeated month-grouped news body

At the current checkpoint, the wrapper can stay minimal because the current
page has no extra authored prose beyond the heading.

## Recommended Placeholder

Use one explicit placeholder:

- `__NEWS_MONTH_GROUPS__`

Why one placeholder is enough here:

- the current page is a single repeated news stream
- there are no authored interstitial notes between month groups
- the wrapper should stay simple until a later homepage or enrichment slice
  proves that more structure is needed

## Public Render Policy

This slice should reconstruct the existing public page shape as closely as
possible from the flat record stream.

Recommended projection policy:

- walk canonical records in order
- group consecutive records by `(year, month)`
- render a month heading when the pair changes
- under each month heading, render each item as:
  - explicit `emoji`
  - Djot body text from `body_djot`

The projection should preserve the current broad public feel of the page
rather than inventing a new visual structure.

## Route / Config Surfaces

This slice likely needs:

- a new `news_index_page` route kind in
  [route_model.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_model.py)
- route discovery for `site/news/index.dj` in
  [route_discovery.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_discovery.py)
- a new `news_dir` in
  [site_config.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_config.py)
- source-path helpers alongside the existing wrapper domains

## Likely Code Surfaces

Primary implementation surfaces:

- `site/news/index.dj`
- remove `site/pages/news.dj`
- `site/pages/index.dj`
  rewrite `news.html` to `news/`
- `scripts/news_record.py`
  keep using the canonical data model from slice 1
- likely new `scripts/news_index.py`
  for the placeholder constant and public-render helper
- `scripts/sitebuild/site_config.py`
- `scripts/sitebuild/route_model.py`
- `scripts/sitebuild/route_discovery.py`
- `scripts/sitebuild/page_projection.py`
- `scripts/sitebuild/source_validate.py`
- route and renderer tests

## Validation Contract

After this slice, source validation should enforce:

- wrapper at `site/news/index.dj`
- no legacy `site/pages/news.dj`
- no lingering authored `news.html` links
- wrapper contains `__NEWS_MONTH_GROUPS__`

If practical, the validator should also reject obvious leftover literal
month-group or item blocks in the wrapper so the page cannot silently become a
second source of truth again.

## Expected Visible Changes

This slice should not be a no-op refactor.

Expected visible changes:

- canonical public route changes from `/news.html` to `/news/`
- authored internal links use `news/` instead of `news.html`

What should ideally stay the same:

- the visible news item stream itself
- month grouping
- item order
- item wording
- item emoji

So the main rendered diff should be route/layout plumbing, not content churn.

## Verification

Verification should include:

- focused route/model/discovery tests
- focused news projection tests
- focused source-validation tests
- `make verify`
- `git diff --check`

Rendered review should confirm:

- the public news body is unchanged in substance
- route output moves from `build/news.html` to `build/news/index.html`
- homepage only changes where the link target becomes `news/`

Landing note:

- this slice landed with the planned route move and homepage link rewrite
- the direct old/new news-page diff showed only canonical URL metadata changes
  plus projection-owned HTML reflow, not content drift

## Invariant After This Slice

After this slice:

- `site/data/news.json` remains the canonical editorial source of truth
- `site/news/index.dj` is the thin public wrapper for the news page
- `/news/` is the canonical public route
- the repeated public news item body is no longer hand-maintained
- the homepage `## News` block is still separate and authored until slice 3
