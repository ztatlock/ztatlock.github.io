# CV Slice 1: Route Cutover

Implemented.

## Goal

Move the CV from an ordinary page at `site/pages/cv.dj` to a first-class
consumer wrapper at `site/cv/index.dj`, with canonical public URL `/cv/`,
before any section projection begins.

## Why This Slice Should Come First

The eventual CV direction is already clear enough:

- the CV will become a cross-domain consumer over existing canonical data
- it will remain one authored document with selectively projected sections

So it is cleaner to move the wrapper early than to keep building future CV
consumer slices against the legacy ordinary-page route and then move it later.

This slice separates:

- where the CV lives
- from how the CV consumes structured data

That keeps the next slices smaller and easier to review.

## Scope

1. Add an explicit `cv_index_page` route kind.
2. Add support for reading/rendering metadata from `site/cv/index.dj`.
3. Move `site/pages/cv.dj` to `site/cv/index.dj`.
4. Canonicalize the public route as `/cv/`.
5. Rewrite lingering authored internal links from `cv.html` to `cv/`.
6. Add source validation for the moved wrapper and legacy-link rejection.
7. Keep the full CV body hand-authored for this slice.

## Out Of Scope

- no students projection yet
- no teaching projection yet
- no service projection yet
- no talks/publications/highlights projection yet
- no attempt to redesign the internal structure of the CV body

## Expected Invariants After This Slice

- the canonical CV source is `site/cv/index.dj`
- the canonical public URL is `/cv/`
- no `build/cv.html` is produced
- authored internal links should use `cv/`, not `cv.html`
- the CV remains a prose-first authored document at this checkpoint

## Verification Targets

- route model accepts `cv_index_page`
- route discovery finds the CV wrapper route
- rendering uses the correct canonical URL for `/cv/`
- old-vs-new rendered CV HTML should match in document body aside from the
  expected route/canonical/link changes:
  - `/cv.html` -> `/cv/`
  - canonical URL changes
  - internal authored `cv.html` links rewritten to `cv/`
- source validation rejects:
  - legacy `site/pages/cv.dj`
  - lingering `cv.html` authored links
- `make test`
- `make check`

## Stop Point

Stop after the route cutover and reassess before any section projection.

The point of this slice is to settle the wrapper shape first, not to smuggle
in the students projection at the same time.
