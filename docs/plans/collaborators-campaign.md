# Collaborators Campaign

Status: slices 1 and 2 implemented; slice 3 planned

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
It is about giving collaborators a clean public home, then carefully growing
that page from a coauthor list into a broader, sectioned collaborator view
without losing clarity about where each collaborator fact actually comes from.

## Why Collaborators Next

Collaborators is now a strong adjacent campaign because:

- there is now a dedicated public page at
  `site/collaborators/index.dj`
- the current page is mostly list-shaped and lightly framed
- much of its current substance is already derivable from canonical
  publication bundles plus `site/data/people.json`
- the about page has a small collaborator-derived alphabet joke that can drift
- richer collaborator relationships are plausible later, but now need a more
  deliberate audit before the page can safely broaden beyond coauthors

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
- canonical teaching staffing now exposes `84` distinct teaching collaborators
  keyed through `site/data/people.json`
- only `18` of those teaching collaborators overlap with current coauthors,
  which means broadening `/collaborators/` is a real ontology change rather
  than a tiny rendering tweak
- canonical students/advising data currently includes `58` people, `42` of
  whom already overlap with publication coauthors and `16` of whom do not

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

- `name` is the default site-facing canonical label
- aliases are alternate spellings for resolution only
- aliases may include fuller publication-style variants, familiar variants, or
  other spellings that should resolve to the same person
- alias order should not carry hidden display semantics for the whole repo

That keeps the registry small and leaves display policy where it belongs:
with each consumer.

For collaborators specifically, the default display label should now simply be
`person.name`, while publication spellings such as `James R. Wilcox` still
resolve through aliases.

## Design Recommendation

Treat collaborators as a staged hybrid campaign with three different fact
sources:

- publication bundles for research coauthorship
- teaching staffing for teaching collaboration
- a later collaborator-specific shared-data layer only for residual facts that
  are canonical nowhere else

That later residual layer should be intentionally small.
It is not meant to become the permanent home of all research-collaboration
truth.
Some facts that are residual today may later become derivable from a future
structured-data `projects` domain, and the collaborators campaign should be
designed so those facts can move out again cleanly.

Current checkpoint:

- slice 1 is landed
- the public route is now `/collaborators/`
- the current page is still effectively a coauthor page projected from
  publication bundles plus `people.json`
- slice 2 keeps the about-page alphabet joke derived from that same coauthor
  display set
- teaching staffing now provides a second real canonical collaborator source,
  but the public collaborators page does not use it yet

The next campaign phase should not jump straight into rendering. It should
first audit what `Research Collaborators` is intended to mean beyond paper
coauthorship.

That means:

- publication bundles remain canonical for coauthorship
- `people.json` remains canonical for person identity, aliases, and URLs
- `site/data/students.json` remains canonical for student/advising facts
- `site/data/teaching.json` remains canonical for teaching collaboration facts
- collaborator-specific relationship facts only get their own data file once
  the audit proves they are real residual facts that cannot be derived cleanly
  from those existing domains

## Important Boundary

The collaborators campaign should not begin by pretending every collaborator
fact already exists in one tidy registry.

In particular, slice 1 should avoid:

- creating `site/data/collaborators.json` before collaborator-specific facts
  exist
- treating all `people.json` entries as collaborators
- bundling linkability-policy changes into the first collaborators cutover
- mixing coauthor derivation with advising, teaching, community, or grant
  relationships in one first cut

That boundary is now preserved in repo history:

- collaborators slice 1 stayed narrow
- the later people-linkability work landed separately as part of the
  teaching-staffing campaign instead of being smuggled into collaborators

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

### Slice 3. Research Collaborator Audit

Goal:

- decide, person by person, what belongs in a broader `Research
  Collaborators` section beyond publication coauthors

This slice should review at least:

- current collaborators-page inclusions that are not justified by publication
  coauthorship alone
- student/advisee names that are not coauthors but may still belong in
  `Research Collaborators`
- any other research collaborators who are neither publication coauthors nor
  advisees

Required outputs:

- a reviewed candidate `Research Collaborators` population
- explicit reason categories for non-coauthor inclusion
- an explicit classification of whether each non-coauthor inclusion is:
  - already derivable now
  - likely future-project-derived
  - likely always residual/curated
- a recommendation about what residual facts need a collaborator-specific data
  layer

Invariant after slice 3:

- the repo has an explicit reviewed understanding of what `Research
  Collaborators` means
- non-coauthor research collaborators are no longer an implicit grab bag
- no collaborator-specific data file or rendering change is required yet

### Slice 4. Collaborator Relationship Model

Goal:

- add a collaborator-specific shared-data layer only for residual collaborator
  facts that are not already canonical elsewhere

Likely target:

- `site/data/collaborators.json`

Likely first residual fact types:

- explicit inclusion/justification for non-coauthor research collaborators
- future curated relationship notes that are canonical nowhere else

Important design note:

- this layer should be minimal and expected to shrink if a later
  structured-data `projects` domain absorbs some currently residual research
  collaboration facts

Important non-goals:

- do not duplicate publication coauthors into the collaborator registry just
  for symmetry
- do not duplicate teaching staffing into the collaborator registry just for
  symmetry

Invariant after slice 4:

- residual collaborator-specific facts have one canonical home keyed by
  `people.json`
- publication and teaching remain canonical in their own domains

### Slice 5. Sectioned Collaborator Views

Goal:

- broaden the public collaborators page into explicit sections over canonical
  and reviewed relationship sources

Likely sections:

- `Research Collaborators`
- `Teaching Collaborators`

Recommended policy:

- `Research Collaborators` includes publication coauthors plus reviewed
  non-coauthor research collaborators
- `Teaching Collaborators` is a flat section derived from canonical teaching
  staffing
- overlap across sections is allowed when it represents distinct real
  relationship types
- the about-page alphabet joke should likely remain tied to the
  research/coauthor side rather than silently broadening to all collaborators

Invariant after slice 5:

- the public collaborators page can present research and teaching
  collaboration distinctly without hand-maintained drift
- section semantics are explicit and reviewable

### Slice 6. Richer Collaborator Enrichment

Goal:

- support deeper collaborator context only if it clearly earns its complexity

Possible later features:

- per-collaborator overlays or popups
- related publication lists
- related teaching history
- advising years or student relationship summaries
- related project lists
- related grant lists
- possibly later prose-page mention indexing if that ever clearly earns it

Invariant after slice 6:

- richer collaborator context is driven by explicit canonical relationships or
  deliberate derived views
- the repo still avoids building a collaborator mega-framework without a real
  need

## Deferred Work

The following should remain explicitly out of the first collaborators
checkpoint:

- broadening the page to include teaching collaborators without a reviewed
  ontology first
- collaborator detail pages or popups
- collaborator/project/grant cross-linking
- a future structured-data `projects` domain for research work that does not
  yet or may never map cleanly to publications
- changing the about-page alphabet joke without an explicit decision about
  whether it should stay coauthor/research-focused

Those all look plausible later, but they should not complicate the first
post-slice-2 audit checkpoint.

## Recommendation

Continue collaborators with the smallest next real architecture:

1. research-collaborator audit
2. stop and reassess
3. only then decide the minimum collaborator-specific data layer
4. only then broaden the page into explicit research/teaching sections

That keeps the next slice honest to the now-larger ontology while still
leaving room for the richer collaborator directions that may matter later.
