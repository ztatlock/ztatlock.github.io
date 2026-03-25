# CV Slice 5: Publications Projection

Implemented.

## Goal

Replace only the duplicated indexed-publication bodies in the CV with
projection from canonical publication bundles under `site/pubs/`, while
keeping the `## Publications` section, its subsection headings, and the
`Book Chapters` subsection hand-authored in `site/cv/index.dj`.

## Why Publications Next

Publications is now the strongest remaining high-payoff CV consumer slice
because:

- canonical publication truth already exists in bundle-local records under
  `site/pubs/<slug>/publication.json`
- the build already has a derived bundle-discovery and ordering pass in
  `scripts/publication_index.py`
- the CV still duplicates the largest remaining repeated factual block in one
  place:
  `58` conference/journal entries and `10` workshop entries
- canonical publication bundle truth already aligns closely with that CV
  shape:
  `58` `main` records and `11` `workshop` records
- the known current drift is concrete and reviewable:
  the CV workshop list is missing `Exploring Self-Embedded Knitting Programs
  with Twine`, which already exists canonically in
  `site/pubs/2023-farm-twine/publication.json`

That means this slice should **not** start by inventing a new authored global
publication table.

The canonical truth is already the bundle root.
This slice should consume that truth.

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Publications` heading and the current subsection headings:
   - `### _Conference and Journal Papers_`
   - `### _Workshop Papers_`
   - `### _Book Chapters_`
3. Replace only the repeated `Conference and Journal Papers` and `Workshop
   Papers` bodies with placeholders.
4. Add an explicit CV-specific publication renderer over canonical publication
   bundles discovered from `site/pubs/`.
5. Keep the `Book Chapters` subsection hand-authored.
6. Add source validation for the placeholder-based indexed-publication
   subsections in the CV.

Likely placeholders:

- `__CV_PUBLICATIONS_MAIN_LIST__`
- `__CV_PUBLICATIONS_WORKSHOP_LIST__`

## Important Rendering Principle

This slice should **not** blindly reuse the public publications index
renderer.

The public publications page at `/pubs/` is intentionally more link-heavy:

- linked titles
- linked author references where available
- direct reuse of public/publication-page destinations

The current CV is intentionally lower-link and more bibliography-like.

The CV publication renderer should therefore optimize for a compressed CV view.

Recommended first-slice policy:

- preserve the current three-line CV entry shape:
  title, authors, venue/badges
- keep titles italicized
- keep titles plain text rather than linked in the first slice
- keep author names plain text rather than person-reference links
- preserve canonical badge lines such as `★ Distinguished Paper`
- derive ordering from canonical `pub_date` descending
- derive grouping from canonical `listing_group`
- accept canonical corrections where bundle truth differs from the old CV

## Important Boundary Decision

This slice should consume existing indexed publication bundles only.

It should **not** reopen the publication-domain boundary just to eliminate the
single authored `Book Chapters` entry.

Why keep `Book Chapters` authored for now:

- the current publication schema only needs `listing_group: main|workshop`
- the current publication bundle root represents the indexed publications
  collection cleanly
- there is no canonical publication bundle for the current CV book chapter
- broadening the publication model for one entry would mix a real consumer win
  with a larger domain-boundary decision

## Important Global-Table Constraint

This slice should not add:

- `site/data/publications.json`
- `site/data/cv.json`
- any second authored publication registry

If a build-time consolidated list is needed, it should remain a derived helper
over bundle truth, not a new source of truth.

The existing publication discovery pass in `scripts/publication_index.py`
already points in the right direction.

## Out Of Scope

- no `Book Chapters` canonicalization yet
- no publication-schema expansion such as a new `chapter` listing group
- no public `/pubs/` wrapper changes
- no publication-artifact enrichment work
- no collaborator generation from publication authors
- no homepage/news/selected-publication projection here

## Expected Invariants After This Slice

- the CV `Conference and Journal Papers` subsection derives from canonical
  publication bundles
- the CV `Workshop Papers` subsection derives from canonical publication
  bundles
- the public publications page and the CV now share one canonical publication
  source while keeping separate consumer presentation policy
- the CV explicitly proves that bundle-root publication truth can power a
  lower-link downstream consumer without becoming a new global data domain
- no duplicated literal indexed-publication entry blocks remain in those two
  CV subsections
- the `Book Chapters` subsection remains authored by explicit policy rather
  than by accident

## Observed Rendered Changes

The rendered diff for this slice was limited to the `## Publications`
section.

Explicit visible changes included:

- the canonical workshop paper `Exploring Self-Embedded Knitting Programs with
  Twine` is now present in the CV
- ordering now follows canonical publication-bundle `pub_date` descending with
  title tie-break, matching the public publications collection rather than the
  old hand-authored CV order
- venue text now matches canonical bundle truth where that differs from the
  old CV wording, for example `Magic Markup` now renders as `<Programming>`
- the old stray trailing line-break artifact on the PLATEAU 2020 workshop
  entry is gone
- `Book Chapters` remains authored and unchanged

## Verification Targets

- focused renderer/projection tests for the CV publication view:
  - `main` and `workshop` grouping
  - `pub_date` ordering
  - plain-text title policy
  - plain-text author policy
  - badge rendering
- validation that required CV publication placeholders are present
- validation that literal duplicated publication entry blocks are rejected in
  the two projected subsections
- compare old and new rendered CV HTML with attention to the `## Publications`
  section specifically:
  - only the intended `Conference and Journal Papers` and `Workshop Papers`
    bodies should change
  - `Book Chapters` should remain stable
  - surrounding CV sections should remain stable
  - differences should be explainable by explicit renderer policy or canonical
    correction
  - the addition of `Exploring Self-Embedded Knitting Programs with Twine`
    should be called out explicitly if it lands
- `make test`
- `make build`
- `make check`

## Stop Point

Stop after the indexed-publications CV projection and reassess.

The next decision should then be deliberate:

- keep `Book Chapters` authored longer
- or plan a separate book-chapter/domain-boundary slice if that complexity
  clearly earns its keep

Do not automatically broaden from this slice into publication-domain
expansion, homepage projection, or collaborator derivation.
