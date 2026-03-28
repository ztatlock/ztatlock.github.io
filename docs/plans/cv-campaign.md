# CV Campaign

Status: route/wrapper cutover plus students, teaching, service, indexed
publications, full invited-talks, and funding CV projection implemented;
the top-of-CV executive-summary plan is now latched with slices 1-3
implemented; stop and reassess before broader curated CV consumers

## Goal

Turn the CV into a first-class cross-domain consumer wrapper that gradually
reuses canonical structured data from the existing domain campaigns without
pretending the entire document should become generated in one step.

The goal is not to create `site/data/cv.json`.
The goal is to let the CV consume already-canonical truth from talks,
publications, students, teaching, service, and later other domains, while
keeping the CV's document-level framing and conventions explicit.

## Why CV Now

The repo has now landed a series of domain-level canonical sources of truth:

- `site/talks/<slug>/talk.json`
- `site/pubs/<slug>/publication.json`
- `site/data/students.json`
- `site/data/teaching.json`
- `site/data/service.json`
- `site/data/funding.json`

Before the CV consumer slices, those interfaces had mostly only been
exercised by their own primary public wrappers:

- `site/talks/index.dj`
- `site/pubs/index.dj`
- `site/students/index.dj`
- `site/teaching/index.dj`
- `site/service/index.dj`
- `site/funding/index.dj`

The next important architectural pressure test is to use those interfaces from
the other side:

- a downstream consumer
- with different formatting conventions
- that intentionally compresses or curates the same facts differently

The CV is the clearest place to do that.

## Current Audit

Current relevant source:

- `site/cv/index.dj`

Important current facts:

- the current CV source is `213` lines
- it contains `30` major section/subsection headings
- it is not one homogeneous repeated-data page
- but it still contains curated repeated sections and authored cross-domain
  highlights

Most important remaining duplicated factual domains:

- no comparably large duplicated factual block remains in the CV over the
  current canonical shared-data domains

Other important cross-domain consumers already present near the top of the CV:

- `Selected Recent Highlights`
  especially the `Leadership` subsection, which overlaps service
  while non-service research/community-participation items such as Dagstuhl
  attendance should remain authored there rather than being forced back into
  the service domain
- `Invited Talks`
  overlaps talks
- `Selected Publications`
  overlaps publications

Current wrapper/consumer state:

- the CV wrapper now lives in `site/cv/index.dj`
- the canonical public URL is now `/cv/`
- lingering authored `cv.html` links have been rewritten to `cv/`
- the duplicated students sections now project from `site/data/students.json`
- the duplicated teaching section now projects from `site/data/teaching.json`
- the duplicated service subsection bodies now project from
  `site/data/service.json`
- the duplicated indexed-publication subsection bodies now project from
  canonical publication bundles under `site/pubs/`
- the duplicated full `Invited Talks` section now projects from canonical talk
  bundles under `site/talks/`
- the duplicated funding list now projects from `site/data/funding.json`
- the visiting-section wording is now `Visiting Students and Interns`
- the CV now includes Ian Briggs consistently with the canonical students data
- the next step should be chosen deliberately rather than broadened
  automatically, and the authored top-of-CV highlights review is now ready
  for deliberate reconsideration because the publication slice-4 cleanup has
  settled the current publication boundary and compact-publication semantics
- that top block is now better understood as a likely authored executive
  summary layer rather than merely a leftover projection seam

That means the wrapper shape is now settled and the remaining CV work is more
curated consumer-side cleanup rather than another obviously large repeated
domain cutover.

## Design Recommendation

Treat the CV as a first-class projected consumer wrapper.

Recommended target shape:

- wrapper source: `site/cv/index.dj`
- canonical public route: `/cv/`

Important architectural boundary:

- the CV should **not** become its own canonical data domain
- the CV should **not** get a new `site/data/cv.json`
- the CV should remain a consumer over existing canonical domains

That means:

- domain-local truth stays where it already belongs
- CV rendering policy stays in explicit CV-specific renderers
- document-level framing remains hand-authored in the CV wrapper

## Why Move The Wrapper Early

Moving the CV wrapper before any section projection is worthwhile because:

- the eventual shape is already clear enough
- later consumer slices should target the final wrapper location from the
  start
- it avoids late route churn and link churn once more CV sections begin
  depending on the projection layer
- it makes the architecture more honest: the CV is no longer just an ordinary
  prose page in `site/pages/`

This should be framed as a wrapper/route cutover, not as a claim that the CV
is already mostly generated.

## Important CV-Specific Principle

The CV should not blindly reuse the same renderers as the public domain pages.

Instead:

- each canonical domain may later supply a separate CV-specific renderer
- those renderers may intentionally compress, omit, or restyle details
- those differences should remain explicit and reviewable

Examples:

- public students page:
  richer, more linked, more advisory detail
- CV students section:
  more compressed and more selective
- CV teaching section:
  may reasonably differ from the public teaching wrapper if the rendered CV
  becomes clearer while preserving the same substance

That is healthy.
It means the canonical data model is serving multiple real consumers rather
than baking one view into the data.

## Format Flexibility

The current hand-authored CV layout is useful, but it is not sacred.

Future CV consumer slices may improve section formatting where that helps the
canonical model or the rendered document, provided that:

- the same underlying information is preserved or improved
- any visible format changes are explicit policy, not accidental fallout
- the old/new rendered HTML diff is reviewed carefully

This keeps the CV honest as a real downstream consumer instead of forcing new
renderers to imitate old hand-authored Djot line-for-line.

## What Should Stay Hand-Authored

The CV should still keep substantial authored structure even after consumer
projection begins.

Likely hand-authored for now:

- the page heading and contact block
- `Selected Recent Highlights`
- small non-service research/community-participation highlights such as
  Dagstuhl attendance
- `Experience`
- `Education`
- `Awards`

Current planning note for the top-of-CV block:

- [cv-top-summary-executive-block-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-executive-block-plan.md)
- [../policy/cv-top-summary.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/cv-top-summary.md)
- [cv-top-summary-slice-2-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-slice-2-audit.md)
- [cv-top-summary-slice-3-shape-proposals.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-slice-3-shape-proposals.md)

Likely later projection candidates:

- maybe a separate `Book Chapters` / bibliography-boundary decision later
- maybe selected recent talks/highlights

## Recommended Slice Order

### Slice 1. CV Wrapper / Route Cutover

Implemented.

- add explicit `cv_index_page` route support
- move `site/pages/cv.dj` to `site/cv/index.dj`
- canonicalize the public URL as `/cv/`
- rewrite lingering authored `cv.html` links to `cv/`
- keep the body fully hand-authored for this slice

Invariant after slice 1:

- the CV is a first-class consumer wrapper at `site/cv/index.dj`
- the canonical route is `/cv/`
- no section projection has happened yet
- all later CV consumer slices target the final wrapper location

### Slice 2. Students CV Projection

Implemented.

- replace only the duplicated students sections in the CV
- define the explicit compressed CV renderer policy for student records
- make the visiting-section heading and Ian Briggs policy explicit together
- keep the CV section headings and surrounding framing hand-authored
- verify the old/new rendered CV HTML diff is isolated to the students section

Invariant after slice 2:

- the first major duplicated factual domain in the CV derives from canonical
  shared data
- the repo has a real downstream consumer renderer over an existing canonical
  domain
- the CV consumer pattern is proven on one domain before broader rollout
- any remaining CV/public divergence in the students section is explicit and
  reviewable

### Checkpoint After Slice 2

This checkpoint led to the next-slice choice.

At that point:

- the CV wrapper shape is settled
- the first cross-domain consumer slice is real
- the repo will have concrete evidence about how much CV renderer policy
  should diverge from the public-domain renderers

Only after that checkpoint should we decide whether the next CV slice should
be:

- teaching
- service
- selected talks/publications/highlights
- or something else entirely

### Slice 3. Teaching CV Projection

Implemented.

- replace only the duplicated teaching section bodies in the CV
- preserve the `## Teaching` heading, the existing subsection headings, and
  the teaching-award note
- define an explicit compressed CV renderer policy for teaching records
- keep the rendered diff focused on the teaching section and explain any
  visible policy changes

Invariant after slice 3:

- the second major duplicated factual domain in the CV now derives from
  canonical shared data
- the CV now proves that a downstream consumer may expose more of a canonical
  domain than the public wrapper does, via the `Teaching Assistant`
  subsection
- the CV teaching renderer now makes its low-link, compressed policy explicit
  and reviewable

### Slice 4. Service CV Projection

Implemented.

- replace only the duplicated service subsection bodies in the CV
- preserve the `## Service` heading, the existing subsection headings, and the
  faculty-skit prose note
- define an explicit compressed CV renderer policy for service records
- reuse canonical range-collapsing and `Present` semantics
- keep the rendered diff focused on the service section and explain visible
  policy changes and canonical corrections

Invariant after slice 4:

- the third major duplicated factual domain in the CV now derives from
  canonical shared data
- the CV and public service page now share canonical range/ongoing service
  semantics while still allowing different presentation policy
- the CV service renderer now makes its link/detail policy explicit and
  reviewable
- the faculty-skit prose note remains authored in the wrapper for now

### Slice 5. Publications CV Projection

Implemented.

- replace only the duplicated `Conference and Journal Papers` and `Workshop
  Papers` bodies in the CV
- preserve the `## Publications` heading, the existing subsection headings,
  and the authored `Book Chapters` subsection
- define an explicit compressed CV renderer policy for indexed publication
  bundles
- reuse canonical publication-bundle discovery and `pub_date` ordering
- keep the rendered diff focused on the publications section and explain
  canonical corrections and ordering changes

Invariant after slice 5:

- the fourth major duplicated factual domain in the CV now derives from
  canonical domain truth
- the CV and public publications page now share one canonical indexed
  publication source while still allowing different presentation policy
- the CV publication renderer now makes its low-link bibliography policy
  explicit and reviewable
- the `Book Chapters` subsection remains authored by explicit policy for now

### Slice 6. Talks CV Projection

Implemented.

- replace only the duplicated full `## Invited Talks` body in the CV
- preserve the `## Invited Talks` heading hand-authored
- define an explicit CV talks renderer over canonical talk bundles
- keep the rendered diff focused on the invited-talks section and explain
  canonical corrections and ordering/link changes

Invariant after slice 6:

- the fifth major duplicated factual domain in the CV now derives from
  canonical domain truth
- the CV and public talks page now share one canonical invited/public talks
  source while still allowing separate consumer renderers
- the CV talks section now uses canonical talk title/link/host truth and
  canonical reverse-chronological ordering rather than a hand-maintained copy
- the top-of-CV `Selected Recent Highlights -> Invited Talks` block remains
  authored by explicit policy for now

### Slice 7. Funding CV Projection

Implemented.

- replace only the duplicated funding list body in the CV
- preserve the `## Funding` heading hand-authored
- define an explicit CV funding renderer over canonical funding data
- keep the rendered diff focused on the funding section and explain any
  visible policy changes

Invariant after slice 7:

- the sixth major duplicated factual domain in the CV now derives from
  canonical shared data
- the CV and public funding page now share one canonical funding source while
  still allowing separate consumer renderers
- no literal duplicated funding-entry block remains in the CV
- the rendered Funding section stayed byte-identical in HTML after the
  projection cutover

## Current Recommendation

Stop and reassess before choosing another CV consumer slice.

Why stop here:

- the largest duplicated shared-data domains in the CV are now canonicalized
  from the consumer side, including talks and funding
- the remaining likely work is now more curated and less obviously list-shaped
- homepage cleanup now competes with narrower curated CV consumers like the
  top-of-CV highlights, and with the separate publication-boundary question
  around `Book Chapters`
- the next step should be selected from current repo needs rather than from
  campaign inertia

Likely candidates from here:

1. homepage recent-service or recent-teaching cleanup
2. curated CV consumers such as selected highlights
3. no immediate CV broadening if the current checkpoint already earns its keep
4. a separate `Book Chapters` / bibliography-boundary slice only if that
   complexity clearly earns its keep
