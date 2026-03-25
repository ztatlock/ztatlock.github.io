# Collaborators Slice 2: About-Page Alphabet Stats Projection

Status: implemented

It builds on:

- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [collaborators-slice-1-wrapper-and-coauthor-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-slice-1-wrapper-and-coauthor-projection.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Replace only the hand-authored collaborator alphabet-gap facts in
`site/pages/about.dj` with projection from the same collaborator display set
used by `/collaborators/`.

The heading, prose, joke, and link to `/collaborators/` should remain
hand-authored.

## Why This Slice Now

This is the clean immediate follow-on to collaborators slice 1 because:

- it removes one more small but obvious drift seam
- it reuses the collaborator consumer policy we just established
- it does not force any new collaborator relationship modeling
- the about-page text is already structured enough that only two tiny factual
  values need to be projected

This is a better next move than jumping straight into richer collaborator
categories or detail views.

## Current State

The current about-page section at `site/pages/about.dj` says:

- first-name gaps: `F, Q, U`
- last-name gaps: `I, U, V, X, Y`

Using the current collaborator display set from `/collaborators/`, those
values are already correct.

That means the intended visible result of this slice is ideally no rendered
HTML change at all.

## Scope

In scope:

1. Replace only the two hand-authored letter-list facts in `site/pages/about.dj`
   with placeholders.
2. Extend the collaborators consumer code so it can derive missing first-name
   initials and missing last-name initials from the same collaborator display
   set used by `/collaborators/`.
3. Add a tiny about-page projection path that applies only to the `about`
   ordinary page.
4. Add focused source validation so the about-page collaborator section must
   contain the placeholders and must not keep hand-authored literal gap lists.
5. Add focused tests and a rendered old/new review of `about.html`.

Likely placeholders:

- `__COLLABORATORS_FIRST_INITIAL_GAPS__`
- `__COLLABORATORS_LAST_INITIAL_GAPS__`

Recommended authored shape in `site/pages/about.dj`:

- keep the existing prose and blockquote/code formatting
- replace only the code-span contents inside the two blockquotes

That keeps the projection seam tiny and obvious.

## Important Source-Of-Truth Rule

Slice 2 should derive alphabet coverage from the same collaborator display set
as slice 1.

That means:

- use the collaborator entries produced by publication bundles plus
  `people.json`
- use the same familiar-label policy already established for the collaborators
  page
- do not re-derive from raw publication author strings separately
- do not introduce `site/data/collaborators.json`

This keeps the about-page joke as a downstream consumer over the collaborator
consumer policy, rather than creating a second collaborator interpretation.

## Alphabet Render Policy

The alphabet-gap computation should stay explicit and small.

### Input Set

- use the projected collaborator display names from slice 1

### Initial Extraction Policy

- first-name initial:
  - split the display name on whitespace
  - use the first token
- last-name initial:
  - split the display name on whitespace
  - use the last token
- normalize the chosen token to an uppercase A-Z initial with a tiny explicit
  helper
- do not attempt broader name parsing or ontology beyond that

This is intentionally simple and matches the existing joke well enough.

### Output Policy

- render missing initials as comma-separated uppercase letters
- keep the surrounding code-span formatting authored in `site/pages/about.dj`

## Out Of Scope

- no new collaborator relationship model
- no changes to `/collaborators/` list policy
- no changes to `site/data/people.json` schema
- no changes to the about-page prose outside the two factual gap values
- no homepage/CV curated-block cleanup

## Landed Invariant

- the about-page collaborator alphabet joke can no longer drift from the
  current `/collaborators/` display set
- the prose around the joke remains hand-authored
- only the first-name and last-name gap values become projected
- no new collaborator-specific data file is introduced

## Rendered Review

- `about.html` is byte-identical before and after this slice
- no visible presentation changes landed
- the slice removes a drift seam without changing the authored joke

## Verification Targets

- focused collaborator alphabet tests for:
  - missing first-name initials
  - missing last-name initials
  - reuse of collaborator display labels rather than raw publication spellings
- projection test that applies only to `ordinary_page` with key `about`
- source-validation tests requiring the two placeholders in the about-page
  collaborator section
- source-validation tests rejecting literal hand-authored gap lists in that
  section
- rendered review of:
  - old/new `about.html`
- `make build`
- `make test`
- `make check`

## Stop Point

Stop after the about-page alphabet-stats projection slice and reassess.

The next collaborators-related question should then remain deliberate:

- introduce a collaborator relationship model for non-coauthor facts
- or continue broader collaborator design exploration before coding more

Do not automatically broaden from this slice into collaborator categories,
detail pages, or grant/project/publication cross-links.
