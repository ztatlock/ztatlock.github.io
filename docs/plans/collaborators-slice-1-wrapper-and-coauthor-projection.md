# Collaborators Slice 1: Wrapper / Coauthor Projection

Status: implemented

It builds on:

- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Move the collaborators page to `site/collaborators/index.dj`, canonicalize
`/collaborators/`, and replace only the repeated collaborator list body with a
projection derived from canonical publication authors plus `people.json`
normalization.

The heading and intro should remain hand-authored.

## Why This Slice First

This is the right first slice because:

- the current collaborators page is mostly a flat coauthor list already
- publication bundles already contain canonical coauthor facts
- `people.json` already provides a useful identity/alias layer for display and
  links
- the page is stale enough that projection should improve correctness, not
  just maintenance
- it avoids prematurely inventing a collaborator-specific registry before
  broader collaborator relationships are actually modeled

## Scope

In scope:

1. Move the public wrapper from `site/pages/collaborators.dj` to
   `site/collaborators/index.dj`.
2. Canonicalize the public route at `/collaborators/`.
3. Rewrite authored internal links from `collaborators.html` to
   `collaborators/`.
4. Replace only the repeated collaborator list body with a placeholder.
5. Add an explicit collaborators renderer over publication bundles plus
   `people.json`.
6. Add focused validation for the placeholder-backed collaborators wrapper.
7. Add small `people.json` alias backfills where current publication-author
   strings are obviously the same collaborator already represented there.

Likely placeholder:

- `__COLLABORATORS_LIST__`

## Important Source-Of-Truth Rule

Slice 1 should use:

- publication bundles as canonical truth for coauthorship
- `people.json` as canonical truth for person identity, aliases, and URLs

Slice 1 should not use:

- all `people.json` entries as collaborators
- a new `site/data/collaborators.json`

This means the collaborators page is a derived consumer over existing
canonical domains, not a new domain registry yet.

## Collaborator Render Policy

The slice-1 collaborators renderer should be explicit and simple.

### Resolution Policy

- collect all non-draft publication authors from canonical publication bundles
- resolve each author string through the `people.json` alias namespace when
  possible
- deduplicate by resolved `people.json` key when resolution succeeds
- otherwise deduplicate by raw author name

### Display Policy

- when a collaborator resolves through `people.json`:
  - use the default site-facing `people.json` `name`
- when a collaborator does not resolve through `people.json`:
  - use the raw publication-author string as plain text

This makes the default-label policy explicit for this page, rather than
silently inheriting publication-author spellings or imposing a global
alias-order meaning on `people.json`.

That lets one record resolve both `James Wilcox` and `James R. Wilcox`, or
both `Remy Wang` and `Yisu Remy Wang`, while keeping one obvious default
label for downstream consumers.

### Link Policy

- when a collaborator resolves through `people.json`, render the collaborator
  as a linked Djot people reference
- when a collaborator does not resolve through `people.json`, render plain
  text with no link

That keeps `Robert Rabe`-style cases possible in slice 1 without forcing an
immediate optional-URL change in `people.json`.

### Ordering Policy

- sort collaborators alphabetically by the displayed collaborator label

### Inclusion Policy

- exclude `Zachary Tatlock` from the derived collaborator list

That makes the page read more naturally as a list of collaborators rather than
including the page owner as his own collaborator.

## Out Of Scope

- no `site/data/collaborators.json`
- no non-coauthor collaborator categories yet
- no about-page alphabet-stats projection yet
- no collaborator detail pages or popups
- no related publications/projects/grants shown on the collaborators page
- no optional-URL schema change for `people.json`
- no attempt to solve every future collaborator relationship in this slice

## Landed Invariant

- the public collaborators page is a thin wrapper at
  `site/collaborators/index.dj`
- the canonical public route is `/collaborators/`
- the repeated coauthor list derives from canonical publication bundles plus
  `people.json` normalization
- `Zachary Tatlock` is no longer listed as his own collaborator
- no literal collaborator list remains in the wrapper
- the repo is now ready for either:
  - about-page collaborator-stat projection, or
  - a later collaborator-specific relationship model

## Observed Visible Changes

Visible changes on the collaborators page are acceptable if they are explainable as:

- canonical correction from current publication bundles
- explicit familiar-name display policy from `people.json` aliases
- plain-text fallback for unresolved names

Observed examples:

- newer coauthors missing from the current page now appear
- collaborator labels now follow the normalized default `people.json` `name`
  rather than ad hoc shortest-label selection
- `Zachary Tatlock` no longer appears in the list
- unresolved names like `Robert Rabe` may remain as plain text

Nothing outside the collaborators route and the rewritten about/notes links
should change.

## Verification Targets

- focused collaborator-derivation tests for:
  - dedup by resolved person key
  - default display labels taken from `people.json` `name`
  - plain-text fallback for unresolved names
  - alphabetical ordering by displayed label
- route discovery and page-rendering tests for the new collaborators wrapper
- source-validation tests requiring the collaborators wrapper and placeholder
- source-validation tests rejecting literal collaborator bullet lists in the
  projected wrapper
- rendered review of:
  - old/new collaborators page body
  - the about-page link rewrite from `collaborators.html` to
    `collaborators/`
  - the notes-page link rewrite from `collaborators.html` to
    `collaborators/`
- `make build`
- `make test`
- `make check`

## Stop Point

Stop after the collaborators wrapper/coauthor projection slice and reassess.

The next collaborators-related question should then remain deliberate:

- project the about-page alphabet note next
- or introduce a collaborator-specific relationship model next

Do not automatically broaden from this slice into non-coauthor collaborator
categories, relationship graphs, or collaborator detail pages.
