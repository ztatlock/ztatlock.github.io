# Students Slice 2: Index Wrapper And Projection

This note defines the recommended next students slice after the canonical
advising-record model landed in `site/data/students.json`.

It is a planning note only.
No code changes should happen until this route/wrapper shape feels right.

It builds on:

- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [students-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-slice-1-canonical-model.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Purpose

Use the canonical advising records to drive the public students page while
making one explicit route/wrapper decision first:

- should the students page remain an ordinary singleton page under
  `site/pages/students.dj`, or
- should it become a projection-backed wrapper at `site/students/index.dj`
  with canonical `/students/`?

## Recommendation

The cleaner next step is:

- keep the canonical truth in `site/data/students.json`
- move the public wrapper to `site/students/index.dj`
- add a `students_index_page` route kind
- make the canonical public URL `/students/`
- project the repeated section bodies from `site/data/students.json`
- keep the quote, explanatory framing, FACET note, and section headings
  hand-authored in the wrapper

## Why This Is Better Than Keeping `site/pages/students.dj`

### Students Is Shared-Data-First, But The Public Page Is Still Collection-Like

Students is not a bundle-root domain like talks or publications.
The truth should stay in shared data, not in `site/students/<slug>/...`.

But the public page itself is not a typical singleton prose page either:

- most of its body is repeated structured listings
- it is likely to become even more projection-backed soon
- it reads more like a category landing page than like a one-off page

So the clean separation is:

- `site/data/students.json`
  canonical shared truth
- `site/students/index.dj`
  public wrapper for the students landing page

### `/students/` Is A Better Canonical URL

The current ordinary-page route would keep the public URL at
`/students.html`.

That is workable, but after talks and publications the repo now has a clearer
pattern for category-like pages:

- `/talks/`
- `/pubs/`

`/students/` fits that same public shape better than `/students.html`.

### It Keeps `site/pages/` More Honest

The long-term direction of `site/pages/` is:

- singleton pages
- primarily prose-first pages
- pages whose body is mostly local to that page

The students page is already less like that than a normal singleton page.
Moving its wrapper out of `site/pages/` makes that distinction clearer.

## Why This Still Differs From Talks And Publications

Students should **not** become a bundle root.

This slice should not create:

- `site/students/<slug>/...`
- per-student detail pages
- collection-local student assets

The only thing moving under `site/students/` should be the collection wrapper:

- `site/students/index.dj`

The truth stays in `site/data/students.json` because:

- the same advising data feeds both the students page and the CV
- there are no record-local assets today
- there are no per-student routes today

## Wrapper Shape

The wrapper should stay substantially hand-authored.

What should remain authored in `site/students/index.dj`:

- page front matter
- page heading
- the Habermann quote block
- the explanatory prose
- the FACET note
- the six section headings

What should be generated:

- the repeated advising-entry list body for each section

One section-title refinement is likely worth making in this slice:

- the current heading `Visiting Summer Students, Internships Mentored in
  Industry` is accurate but clunky
- a cleaner public heading is likely `Visiting Students and Interns`
- this still gives Ian Briggs's Amazon internship a clear home without forcing
  a narrower term like only `interns`
- the canonical section key can remain `visiting_students`; this is a wrapper
  wording decision, not a schema redesign

That means the wrapper should use section-local placeholders rather than one
giant generated block.

## Recommended Placeholders

Use one placeholder per advising section:

- `__STUDENTS_CURRENT_LIST__`
- `__STUDENTS_POSTDOC_LIST__`
- `__STUDENTS_PHD_LIST__`
- `__STUDENTS_MASTERS_LIST__`
- `__STUDENTS_BACHELORS_LIST__`
- `__STUDENTS_VISITING_LIST__`

This is slightly more verbose than one big placeholder, but it is the right
tradeoff because:

- the FACET note lives between sections
- the section headings are still authored framing
- later page-local notes can move without changing canonical data

## Recommended Render Policy For The Students Page

Slice 2 should render the richer students-page view, not the compressed CV
view.

For the students page:

- student names should render as links via `person_key` / `people.json`
- thesis details should render as linked thesis lines
- co-advisor details should render as linked people lines
- `outcome` and `note` details should render as authored Djot bullet lines
- canonical section/record/detail order should come directly from
  `site/data/students.json`

The CV projection should remain a later slice with its own condensed renderer.

## Recommended Slice Scope

1. Add an explicit `students_index_page` route kind.
2. Add support for reading/rendering a wrapper at `site/students/index.dj`.
3. Move `site/pages/students.dj` to `site/students/index.dj`.
4. Make the canonical public route `/students/`.
5. Rewrite authored internal links from `students.html` to `students/`.
6. Add students-page projection rendering from `site/data/students.json`.
7. Replace the literal repeated list bodies with the section placeholders.
8. Update source validation to enforce:
   - wrapper at `site/students/index.dj`
   - no legacy `site/pages/students.dj`
   - no lingering `students.html` links
   - all six expected placeholders present
9. Stop before touching the CV.

## Invariant After This Slice

After this slice:

- `site/data/students.json` is still the canonical advising truth
- `/students/` is the canonical students landing page
- `site/students/index.dj` owns only framing and section structure
- repeated advising entries are no longer hand-maintained in the page wrapper
- the CV is still hand-authored

## Why Not Split Route Cutover And Projection

For students, the wrapper move and the first projection pass belong together.

If we projected into `site/pages/students.dj` first, we would likely rebuild
projection logic against a wrapper location and public URL that we already
suspect are not the clean end state.

Combining them keeps the change coherent:

- one route decision
- one wrapper move
- one projection-backed public page

## Follow-On Work After Slice 2

The next likely slice after this one should be:

- CV projection from the same canonical advising records

That later slice should answer:

- whether the Ian Briggs mismatch is intentional
- exactly which detail kinds the CV suppresses
- whether the CV should use separate section placeholders or one larger block

## Questions To Reassess After Slice 2

1. Does `site/students/index.dj` feel like the right public-wrapper location?
2. Does `/students/` feel clearly better than `/students.html` in practice?
3. Are the section-local placeholders the right granularity?
4. Does the richer students-page renderer still feel simple, or does it expose
   one small schema refinement before CV projection?
5. Does the students page now feel cleanly separated into canonical data,
   authored framing, and projection logic?
