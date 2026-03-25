# People Registry Semantics

Status: planned

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Make the semantics of `site/data/people.json` explicit and coherent before
more consumers depend on it as central shared data.

This note is about the meaning of:

- `name`
- `aliases`
- `url`

It is not yet about collaborator relationship modeling, optional-URL support,
or a broader people/profile system.

## Why This Matters Now

The people registry is already central:

- Djot people references are generated from it
- collaborators derives identity and labels from it
- students uses it for key resolution and some visible labels
- future teaching staffing and richer collaborator work will depend on it even
  more

That means ambiguous semantics here will spread architecture debt outward.

## Current Repo State

Current documented intent is already close to a clean design:

- `people.json` is a small shared registry
- aliases are intended primarily for resolution
- consumer-specific display policy is supposed to stay with the consumer

Current implementation facts:

- schema today is just `name`, `url`, and optional `aliases`
- names and aliases share one unique resolution namespace
- generated Djot refs include both `name` and all aliases
- some consumers use `registry.person(...).name` directly as a visible label
- collaborators currently uses a heuristic over `name` plus `aliases` to find
  a familiar-looking label

Current data audit:

- the registry currently has `155` people records
- only `14` records currently use aliases
- only `1` record currently has more than one alias
- alias-bearing records are semantically mixed:
  - some use `name` as the familiar/default label and aliases for more formal
    publication variants
  - others use `name` as the fuller/formal label and aliases for shorter
    familiar variants

Representative examples:

- `James Wilcox` + alias `James R. Wilcox`
- `Tom Anderson` + alias `Thomas E. Anderson`
- `Gilbert Louis Bernstein` + alias `Gilbert Bernstein`
- `Steven L. Tanimoto` + alias `Steve Tanimoto`
- `Yisu Remy Wang` + alias `Remy Wang`

So the registry is still small, but the norms are not yet coherent.

## Main Seam

There is a real unresolved difference between:

- default site-facing display label
- formal / publication-style spelling
- alternate spellings used only for resolution

Today those concepts are partially collapsed into `name` plus `aliases`.

That is why collaborators needed the current "shortest human-facing label"
heuristic: the data is not yet strong enough to support a simple default-label
rule.

## Important Consumer Facts

### Publication Bundles

Publication-author spellings are canonical in publication-local records under
`site/pubs/<slug>/publication.json`.

That is important because it means the people registry does not need to own
publication-style names as the default display source for publication pages.
Publications already carry their own local author strings.

### Djot People Refs

The generated Djot refs currently render both `name` and every alias as valid
reference labels pointing to the same URL.

That is compatible with aliases being resolution labels.
It does not require aliases to carry global display semantics.

### Collaborators

Collaborators is the clearest current consumer pressure.

It wants a familiar human-facing label, but that should be explicit consumer
policy rather than a hidden meaning baked into alias order.

### Students And Future Teaching Staffing

Students already uses `registry.person(...).name` in a few visible places.
Future teaching staffing and later collaborator relationships will likely do
the same unless we settle a clearer default-name policy first.

## Design Options

### Option A. Keep The Current Small Schema And Clarify Semantics

Use:

- `name` as the default site-facing canonical label
- `aliases` as alternate spellings for resolution only

Then normalize current records so they actually follow that rule.

Implications:

- collaborators can stop needing the "shortest label" heuristic and can
  usually just use `name`
- students and future teaching staffing get a cleaner default display label
- publication pages remain unaffected because publication bundles already own
  publication-author spellings
- generated Djot refs can continue to emit both `name` and aliases

Cost:

- a small cleanup pass over the current alias-bearing records
- some records will need `name` / `aliases` swapped or adjusted

### Option B. Add One Extra Display Field

For example:

- `name`
- optional `display_name`
- `aliases`

This would let the registry separate formal identity from default display
without renaming current data.

Cost:

- broader schema change
- more consumer updates
- more semantics to explain and test

This may be warranted later, but it is likely too much for the current
surface area.

### Option C. Add Typed Alias Categories

For example:

- publication aliases
- familiar aliases
- historical aliases

This is almost certainly overkill right now.

The registry is too small, and the actual current need is much simpler.

## Recommendation

Prefer **Option A** first:

- keep the schema small
- explicitly define `name` as the default site-facing canonical label
- treat `aliases` as resolution-only alternate spellings
- clean up the current alias-bearing records so they follow that rule

This fits the repo's simplicity bias best.

It also matches the architecture more honestly:

- publication-local spellings stay with publications
- consumer-specific formatting still stays with consumers
- the people registry becomes a clean identity/default-label layer rather than
  a vague blend of formal and familiar names

Only consider an extra field later if the cleanup pass reveals cases that
still cannot be expressed cleanly.

## What This Note Does Not Recommend Yet

- no collaborator relationship model yet
- no optional-URL support yet
- no full people-profile campaign
- no attempt to encode every possible naming nuance in the schema

Those should remain separate decisions.

## Suggested Slice Order

### Slice 1. Semantics Decision And Docs

Invariant:

- the repo explicitly defines what `name` and `aliases` mean
- the decision is documented in architecture and campaign notes

No data or consumer behavior changes yet.

### Slice 2. Registry Normalization

Invariant:

- current alias-bearing records in `site/data/people.json` follow the chosen
  `name` / `aliases` semantics

This should stay a narrow data-cleanup slice with focused registry tests.

### Slice 3. Consumer Cleanup

Invariant:

- collaborators and other default-display consumers can rely on the cleaned-up
  `name` semantics instead of ad hoc label heuristics

This likely means simplifying the collaborators consumer.

### Later Optional Slice. Schema Extension

Only if the normalization pass reveals truly irreducible cases.

Invariant:

- any extra field earns its keep by solving a real demonstrated problem

## Dependency Note

This work should happen before:

- the later teaching staffing slice becomes more people-registry dependent
- the collaborator relationship-model slice builds on top of unresolved naming
  semantics

That makes this a likely near-term planning checkpoint even if the actual data
cleanup remains a separate implementation slice.
