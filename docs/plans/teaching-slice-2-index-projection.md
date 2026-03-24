# Teaching Slice 2: Public Wrapper And Projection

This note plans the slice that should turn the public teaching page into a
projection-backed wrapper after the canonical teaching-record model landed in
`site/data/teaching.json`.

Status: planned

It builds on:

- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-slice-1-canonical-model.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Purpose

Remove the biggest remaining duplication seam in the teaching campaign:

- `site/data/teaching.json` is now canonical
- but the public teaching page is still a fully hand-maintained second copy of
  much of the same structured content

This slice should make the public teaching page a thin wrapper around
canonical teaching records while deliberately leaving homepage and CV reuse for
later slices.

## Recommendation

The cleaner next step is:

- keep the canonical truth in `site/data/teaching.json`
- move the public wrapper to `site/teaching/index.dj`
- add a `teaching_index_page` route kind
- make the canonical public URL `/teaching/`
- project the repeated teaching blocks from `site/data/teaching.json`
- keep the heading, award note, and Related section hand-authored in the
  wrapper

## Why This Should Move Out Of `site/pages/`

Teaching is not a bundle-root domain like talks or publications.
Its truth should stay in shared data, not in `site/teaching/<slug>/...`.

But the public teaching page is also no longer a typical singleton prose page:

- most of its body is repeated structured course data
- the page is likely to gain more projection over time
- the canonical teaching route should read like a stable landing page

So the clean separation is:

- `site/data/teaching.json`
  canonical shared truth
- `site/teaching/index.dj`
  public teaching wrapper

## Why Combine Route Cutover And Projection

For teaching, the wrapper move and the first projection pass belong together.

If we projected first into `site/pages/teaching.dj`, we would spend effort on a
wrapper location and public URL that we already expect to replace.

Combining them keeps the slice coherent:

- one wrapper move
- one canonical route decision
- one public projection pass
- one reviewable output change

## Canonical Public URL

The current ordinary-page route keeps the public URL at `/teaching.html`.

After talks, publications, and students, the repo now has a clearer pattern
for category-like landing pages:

- `/talks/`
- `/pubs/`
- `/students/`

`/teaching/` fits that same public shape better than `/teaching.html`.

## What Should Stay Hand-Authored

The wrapper should remain substantially authored.

What should stay authored in `site/teaching/index.dj`:

- page front matter
- page heading
- the `Courses at the University of Washington` section heading
- the `Special Topics Graduate Courses` heading
- the Distinguished Teaching Award note
- the `Summer School Courses` heading
- the `Related` section and its links

What should be generated:

- the repeated UW course blocks
- the repeated special-topics entries
- the repeated summer-school entries

## Recommended Placeholders

Use one placeholder per repeated public block:

- `__TEACHING_UW_COURSES_LIST__`
- `__TEACHING_SPECIAL_TOPICS_LIST__`
- `__TEACHING_SUMMER_SCHOOL_LIST__`

This is better than one giant generated block because:

- the award note lives between the UW/special-topics material and the summer
  school section
- the Related section should remain authored
- the section headings are page-local framing, not canonical data

## Public Render Policy

This slice should render the richer public-teaching view, not the compressed CV
view.

For the public teaching page:

- UW courses should render as title/description blocks with linked offerings
- special-topics entries should render as linked course lines plus ordered
  note bullets
- summer-school entries should render as title-first public entries with event
  links and optional supplemental links
- canonical group and record order should come directly from
  `site/data/teaching.json`

Important scope boundary:

- the public teaching page should continue to omit the `teaching_assistant`
  group
- that group records Zach's own earlier TA history and belongs on the CV, not
  on the public teaching page

## Expected Visible Changes

This slice should not be treated as a no-op refactor.

Expected public-facing changes include:

- the canonical public route becomes `/teaching/`
- authored internal links should change from `teaching.html` to `teaching/`
- the public teaching page should now include the canonical
  `Marktoberdorf Summer School 2024` entry that is already present in
  `site/data/teaching.json`

Those are intended output changes, not regressions.

## Validation Contract

The source-validation contract after this slice should enforce:

- wrapper at `site/teaching/index.dj`
- no legacy `site/pages/teaching.dj`
- no lingering `teaching.html` authored links
- all three expected placeholders present in the wrapper

If practical, the validator should also reject obvious leftover literal
teaching-entry blocks in the wrapper so the page cannot silently become a
second source of truth again.

## Projection-Layer Note

This will be the fourth projection-backed domain:

- talks
- students
- publications
- teaching

The current route-kind dispatch in `page_projection.py` is still small enough
to tolerate one more explicit branch.
That said, if the next projection-backed domain lands after teaching, the
projection layer will probably earn a tiny registry cleanup instead of more
`if/elif` growth.

## Implemented Slice Scope

1. Add an explicit `teaching_index_page` route kind.
2. Add support for reading/rendering a wrapper at `site/teaching/index.dj`.
3. Move `site/pages/teaching.dj` to `site/teaching/index.dj`.
4. Make the canonical public URL `/teaching/`.
5. Rewrite authored internal links from `teaching.html` to `teaching/`.
6. Add teaching-page projection rendering from `site/data/teaching.json`.
7. Replace the literal repeated teaching blocks with the three placeholders.
8. Update source validation to enforce the new wrapper location and placeholder
   contract.
9. Stop before touching the homepage recent-teaching slice.
10. Stop before touching the CV teaching section.

## Invariant After This Slice

After this slice:

- `site/data/teaching.json` is still the canonical teaching truth
- `/teaching/` is the canonical public teaching page
- `site/teaching/index.dj` owns only public framing and section structure
- repeated public teaching entries are no longer hand-maintained
- the homepage and CV are still hand-authored
