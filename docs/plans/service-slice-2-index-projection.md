# Service Slice 2: Public Wrapper And Projection

This note records the slice that turned the public service page into a
projection-backed wrapper after the canonical service-term model landed in
`site/data/service.json`.

Status: implemented

It builds on:

- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [service-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-slice-1-canonical-model.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Purpose

Remove the biggest remaining duplication seam in the service campaign:

- `site/data/service.json` is canonical
- but the public service page was still a hand-maintained second copy of much
  of the same structured content

This slice made the public service page a thin wrapper around canonical
service-term records while deliberately leaving homepage and CV reuse for
later cross-cutting work.

## Recommendation

The cleaner step was:

- keep the canonical truth in `site/data/service.json`
- move the public wrapper to `site/service/index.dj`
- add a `service_index_page` route kind
- make the canonical public URL `/service/`
- project the repeated public service blocks from `site/data/service.json`
- keep the page heading, section headings, and Aggregators section
  hand-authored in the wrapper

## Why This Should Move Out Of `site/pages/`

Service is not a bundle-root domain like talks or publications.
Its truth should stay in shared data, not in `site/service/<slug>/...`.

But the public service page is also no longer a typical singleton prose page:

- most of its body is repeated structured service data
- the page is likely to gain more projection over time
- the canonical service route should read like a stable landing page

So the clean separation is:

- `site/data/service.json`
  canonical shared truth
- `site/service/index.dj`
  public service wrapper

## Why Combine Route Cutover And Projection

For service, the wrapper move and the first projection pass belong together.

If we projected first into `site/pages/service.dj`, we would spend effort on a
wrapper location and public URL that we already expected to replace.

Combining them kept the slice coherent:

- one wrapper move
- one canonical route decision
- one public projection pass
- one reviewable output change

## Canonical Public URL

The old ordinary-page route kept the public URL at `/service.html`.

After talks, publications, students, and teaching, the repo now has a clearer
pattern for category-like landing pages:

- `/talks/`
- `/pubs/`
- `/students/`
- `/teaching/`

`/service/` fits that same public shape better than `/service.html`.

## What Stays Hand-Authored

The wrapper remains substantially authored.

What stays authored in `site/service/index.dj`:

- page front matter
- page heading
- section headings
- the `Aggregators` section and its links

What is generated:

- the repeated reviewing entries
- the repeated organizing entries
- the repeated mentoring entries
- the repeated department entries
- the faculty-skit note derived from canonical service terms

## Recommended Placeholders

Use one placeholder per repeated public block:

- `__SERVICE_REVIEWING_LIST__`
- `__SERVICE_ORGANIZING_LIST__`
- `__SERVICE_MENTORING_LIST__`
- `__SERVICE_DEPARTMENT_LIST__`

This is better than one giant generated block because:

- the public section headings are page-local framing
- the Aggregators section should remain authored
- the faculty-skit note is canonicalized but still rendered as part of the
  department-section block rather than as a separate wrapper concern

## Public Render Policy

This slice renders the richer public-service view, not the later CV or
homepage views.

For the public service page:

- reviewing/organizing/mentoring entries render as year-first bullet items
- department entries render with the existing `YEAR : TITLE` style
- contiguous yearly records collapse back into ranges when they share the same
  canonical series/title/role/url/details
- if the latest record in a collapsed series is marked `ongoing`, the public
  label renders `Present`
- the annual faculty-skit note is rendered from canonical service records
  rather than hand-maintained prose

## Expected Visible Changes

This slice should not be treated as a no-op refactor.

The implemented public-facing changes include:

- the canonical public route becomes `/service/`
- authored internal links now use `service/` instead of `service.html`
- the service page now derives the previously drifting `EGRAPHS Community
  Advisory Board` and `Dagstuhl Seminar 26022: EGRAPHS` entries from
  canonical data

## Validation Contract

The source-validation contract after this slice enforces:

- wrapper at `site/service/index.dj`
- no legacy `site/pages/service.dj`
- no lingering `service.html` authored links
- all four expected placeholders present in the wrapper
- no leftover literal service entry blocks in the wrapper
- no hand-authored faculty-skit note in the wrapper

## Implemented Slice Scope

1. Add an explicit `service_index_page` route kind.
2. Add support for reading/rendering a wrapper at `site/service/index.dj`.
3. Move `site/pages/service.dj` to `site/service/index.dj`.
4. Make the canonical public URL `/service/`.
5. Rewrite authored internal links from `service.html` to `service/`.
6. Add service-page projection rendering from `site/data/service.json`.
7. Replace the literal repeated service blocks with the four placeholders.
8. Update source validation to enforce the new wrapper location and placeholder
   contract.
9. Stop before touching the homepage recent-service slice.
10. Stop before touching the CV service section.

## Invariant After This Slice

After this slice:

- `site/data/service.json` is still the canonical service truth
- `/service/` is the canonical public service page
- `site/service/index.dj` owns only public framing and section structure
- repeated public service entries are no longer hand-maintained
- the homepage and CV are still hand-authored
