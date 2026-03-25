# Collaborators Campaign

Status: slice 2 implemented

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)

## Goal

Give collaborators a clean public home and a clear growth path without
inventing a bigger collaborator data model than the current page actually
needs.

This campaign is not about building collaborator profiles, popups, or a full
relationship graph on day one.
It is about replacing the current hand-maintained collaborators list with a
thin wrapper over existing canonical truth where possible, while leaving room
for later collaborator-specific enrichment when it clearly earns its keep.

## Why Collaborators Next

Collaborators is now a strong adjacent campaign because:

- there is now a dedicated public page at
  `site/collaborators/index.dj`
- the current page is mostly list-shaped and lightly framed
- much of its current substance is already derivable from canonical
  publication bundles plus `site/data/people.json`
- the about page has a small collaborator-derived alphabet joke that can drift
- richer collaborator relationships are plausible later, but do not need to be
  solved in the first slice

This is a better next move than forcing an immediate decision about trimming
the authored homepage/CV highlights blocks.

## Current Audit

Current explicit collaborator-related surfaces:

- `site/collaborators/index.dj`
  a thin wrapper over a projected alphabetical coauthor list
- `site/pages/about.dj`
  a hand-authored collaborator alphabet-coverage note with projected gap values
- `site/pubs/<slug>/publication.json`
  canonical publication-author lists
- `site/data/people.json`
  canonical people names, aliases, and URLs

Important current facts:

- the collaborators page is really a coauthor page today, even though
  the title says `Collaborators`
- before slice 1, the hand-authored page listed `118` names
- canonical publication bundles currently expose `133` unique author strings
- only a small number of publication-author strings are still unresolved
  through `people.json`, and most of those appear to be alias cleanup rather
  than deeper modeling gaps
- the current projected page renders `131` collaborator names after excluding
  `Zachary Tatlock` and adding missing canonical coauthors

Important current constraints:

- not every `people.json` entry is a collaborator
- not every intended collaborator is a publication coauthor
- some publication-author strings should display using a more familiar short
  form than the publication spelling
- the page should not list `Zachary Tatlock` as his own collaborator in the
  first projected cutover
- at least one important name, `Robert Rabe`, should still appear even though
  there is no URL to attach today

That means collaborators is not identical to either:

- all people in `site/data/people.json`, or
- all raw publication-author strings

It is a derived public view with its own explicit display policy.

## People Registry Alias Norm

For this campaign, `people.json` aliases should remain simple:

- aliases are alternate human-facing spellings for resolution
- aliases may include familiar short forms or publication-style variants
- alias order should not carry hidden display semantics for the whole repo

That keeps the registry small and leaves display policy where it belongs:
with each consumer.

For collaborators specifically, slice 1 can still render familiar labels by
choosing the shortest human-facing label among `name` and `aliases`, while
still resolving publication spellings such as `James R. Wilcox`.

## Design Recommendation

Treat collaborators as a staged hybrid campaign.

For slice 1:

- derive the public collaborators page from publication coauthors plus
  `people.json` normalization
- move the wrapper to `site/collaborators/index.dj`
- canonicalize `/collaborators/`
- do not create `site/data/collaborators.json` yet

Current checkpoint:

- slice 1 is landed
- the public route is now `/collaborators/`
- the list is projected from publication coauthors plus `people.json`
- display uses the shortest human-facing label among `name` and `aliases`
- unresolved names such as `Robert Rabe` remain as plain text

Later, if non-coauthor collaborator facts clearly matter, add a small
collaborator-specific shared-data layer keyed by `people.json` person keys.

That means:

- publication bundles remain canonical for coauthorship
- `people.json` remains canonical for person identity, aliases, and URLs
- collaborator-specific relationship facts only get their own data file once
  they are real facts, not just anticipated future possibilities
- familiar-name display remains an explicit collaborator-consumer policy rather
  than a hidden people-registry rule

## Important Boundary

The collaborators campaign should not begin by pretending every collaborator
fact already exists in one tidy registry.

In particular, slice 1 should avoid:

- creating `site/data/collaborators.json` before collaborator-specific facts
  exist
- treating all `people.json` entries as collaborators
- forcing optional-URL support into `people.json` just to handle one current
  unresolved case
- mixing coauthor derivation with advising, teaching, community, or grant
  relationships in one first cut

## What Should Stay Hand-Authored

The collaborators campaign should not move everything into structured data.

The following should stay authored unless a later slice clearly proves
otherwise:

- the collaborators-page heading
- the collaborators-page intro text
- the about-page prose around the collaborator alphabet joke
- any future editorial framing around collaborator categories or impact

## Recommended Slice Order

### Slice 1. Collaborators Wrapper / Coauthor Projection

Goal:

- replace the current literal collaborator list with projection from canonical
  publication authors plus `people.json` normalization

Invariant after slice 1:

- the public collaborators page is a thin wrapper at
  `site/collaborators/index.dj`
- the canonical public route is `/collaborators/`
- the repeated coauthor list derives from publication bundles plus
  `people.json`
- the projected collaborator list excludes `Zachary Tatlock`
- no literal collaborator list remains in the wrapper
- broader collaborator relationships remain explicitly deferred

### Slice 2. About-Page Alphabet Stats Projection

Goal:

- derive the collaborator alphabet-coverage note on `site/pages/about.dj` from
  the same collaborator display set as `/collaborators/`

Invariant after slice 2:

- the about-page alphabet joke can no longer drift from the collaborators page
- the about-page prose remains authored while only the letter-set facts become
  projected

### Slice 3. Collaborator Relationship Model

Goal:

- add a collaborator-specific shared-data layer only for relationships that are
  not already canonical in publications plus `people.json`

Likely target:

- `site/data/collaborators.json`

Likely first relationship categories:

- non-coauthor research collaborators
- advising/collaboration relationships that do not imply coauthorship
- teaching collaborators such as co-instructors or TAs
- community collaborators such as running-club organizers

Invariant after slice 3:

- collaborator-specific relationship facts have one canonical home keyed by
  `people.json`
- publication coauthorship still remains canonical in publication bundles
- the repo does not duplicate coauthor facts into a collaborator registry just
  for symmetry

### Slice 4. Sectioned Collaborator Views

Goal:

- let the collaborators page show explicit sections when relationship
  categories become real and stable

Potential sections:

- coauthors
- advising collaborators
- teaching collaborators
- community collaborators

Invariant after slice 4:

- the public collaborators page can present multiple relationship categories
  without hand-maintained drift
- category policy remains explicit rather than hidden in one flat list

### Slice 5. Richer Collaborator Enrichment

Goal:

- support deeper collaborator context only if it clearly earns its complexity

Possible later features:

- related publication lists
- related project lists
- related grant lists
- popups or detail pages

Invariant after slice 5:

- richer collaborator context is driven by explicit canonical relationships or
  deliberate derived views
- the repo still avoids building a collaborator mega-framework without a real
  need

## Deferred Work

The following should remain explicitly out of the first collaborators
checkpoint:

- non-coauthor collaborator categories
- optional-URL support in `people.json`
- collaborator detail pages or popups
- collaborator/project/grant cross-linking
- turning the about-page alphabet note into a same-day requirement

Those all look plausible later, but they should not complicate the first
wrapper/projection slice.

## Recommendation

Start collaborators with the smallest real architecture:

1. wrapper plus coauthor projection
2. stop and reassess
3. only then decide whether the about-page alphabet note or a
   collaborator-specific relationship model should come next

That keeps the first slice honest to the current public page while still
leaving room for the richer collaborator directions that may matter later.
