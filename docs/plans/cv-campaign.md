# CV Campaign

Status: route/wrapper cutover implemented; students CV projection next

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

But those interfaces have mostly only been exercised by their own primary
public wrappers:

- `site/talks/index.dj`
- `site/pubs/index.dj`
- `site/students/index.dj`
- `site/teaching/index.dj`
- `site/service/index.dj`

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

- the current CV source is `1014` lines
- it contains `29` major section/subsection headings
- it is not one homogeneous repeated-data page
- but it does contain several large duplicated factual domains

Most important duplicated factual domains:

- `Students`
  duplicates the public students page in a more compressed form
- `Teaching`
  duplicates the public teaching page in a more compressed form
- `Service`
  duplicates the public service page in a more compressed form

Other important cross-domain consumers already present near the top of the CV:

- `Selected Recent Highlights`
  especially the `Leadership` subsection, which overlaps service
- `Invited Talks`
  overlaps talks
- `Selected Publications`
  overlaps publications

Current wrapper state:

- the CV wrapper now lives in `site/cv/index.dj`
- the canonical public URL is now `/cv/`
- lingering authored `cv.html` links have been rewritten to `cv/`
- no section projection has happened yet

That means the wrapper shape is now settled and the next real CV work is
consumer-side section projection.

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

That is healthy.
It means the canonical data model is serving multiple real consumers rather
than baking one view into the data.

## What Should Stay Hand-Authored

The CV should still keep substantial authored structure even after consumer
projection begins.

Likely hand-authored for now:

- the page heading and contact block
- `Selected Recent Highlights`
- `Experience`
- `Education`
- `Awards`
- `Funding`

Likely later projection candidates:

- `Students`
- `Teaching`
- `Service`
- maybe selected `Invited Talks`
- maybe selected recent publications or highlights

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

Next.

- replace only the duplicated students sections in the CV
- define the explicit compressed CV renderer policy for student records
- make the visiting-section heading and Ian Briggs policy explicit together
- keep the CV section headings and surrounding framing hand-authored
- resolve whether Ian Briggs should remain omitted or be restored

Invariant after slice 2:

- the first major duplicated factual domain in the CV derives from canonical
  shared data
- the repo has a real downstream consumer renderer over an existing canonical
  domain
- the CV consumer pattern is proven on one domain before broader rollout
- any remaining CV/public divergence in the students section is explicit and
  reviewable

### Checkpoint After Slice 2

Stop and reassess.

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
