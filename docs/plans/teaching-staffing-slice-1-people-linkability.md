# Teaching Staffing Slice 1: People Linkability And Ref Guardrail

Status: implemented

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Make `site/data/people.json` honest about linkability before teaching staffing
or richer collaborator work depends on it any further.

This slice should let a person exist canonically even when no public link is
available, while keeping generated Djot refs and authored Djot prose safe and
predictable.

## Why This Slice First

This is the right first slice because the current registry still assumes every
person is linkable:

- `people_registry.py` only allows `name`, `url`, and `aliases`
- `url` is currently required
- generated Djot refs currently emit `name` and aliases for every person
- the manual-refs audit currently compares against `person.url`
- some structured consumers still assume a people-backed reference is always
  linkable

That assumption was acceptable while `people.json` mostly represented
well-linked senior collaborators and advisors.
It is no longer a clean fit for broader teaching staffing.

If we canonicalize staffing first without fixing this seam, we risk either:

- forcing fake or low-quality URLs into `people.json`, or
- breaking authored and generated link assumptions later

## Scope

In scope:

- extend the people-registry schema to support optional public-link fields
- add one explicit derived "best available public link" rule
- update generated people refs to emit only linkable people
- add an explicit guardrail so authored Djot does not silently rely on
  linkless generated people refs
- add focused tests and docs for the new semantics

Out of scope:

- bulk backfill of new teaching staff into `people.json`
- teaching staffing fields in `site/data/teaching.json`
- teaching staffing rendering on any public page
- collaborator relationship modeling
- any general person-profile expansion beyond public links

## Current Audit Facts

### People Registry

Pre-slice allowed person fields:

- `name`
- `url`
- `aliases`

Pre-slice semantics:

- `name` is the default site-facing canonical label
- `aliases` are resolution-only alternate spellings
- every person currently must have `url`

### Generated Refs

Pre-slice generated Djot-ref behavior:

- emit refs for `name` plus every alias
- point every generated ref at `person.url`

That means the current implementation treats these as the same thing:

- person exists canonically
- person is publicly linkable
- authored Djot may safely use generated people refs for that person

This slice should separate those concepts.

## Recommended Schema Contract

Keep the people registry small, but let public links be more honest.

Landed person fields after this slice:

- required `name`
- optional `aliases`
- optional `url`
- optional `linkedin`
- optional `github`

Recommended semantics:

- `name` remains the default site-facing canonical label
- `aliases` remain resolution-only alternate spellings
- `url` remains the preferred public link when present
- `linkedin` and `github` are fallback public-link fields, not new display
  identities

## Recommended Derived Link Rule

This slice landed a small helper with this exact selection order:

1. `url`
2. `linkedin`
3. `github`

This keeps public-link policy explicit and easy to reason about.

This slice should not add:

- multiple rendered links per person
- link-type-specific authoring semantics
- a richer profile schema

## Generated Ref Contract

Landed generated-ref contract:

- a person with a `primary_url` should generate Djot refs for `name` and all
  aliases
- a person without a `primary_url` should generate no Djot refs

This means generated people refs become a property of linkable people, not a
synonym for person existence.

## Authored-Prose Guardrail

This slice should explicitly protect authored source against silent drift once
linkless people are allowed.

Landed guardrail:

- authored Djot that relies on generated people refs should only be able to
  reference linkable people
- linkless people should remain available to structured renderers, which can
  choose linked or plain-text output explicitly

Implemented scope:

- authored `.dj` sources are validated against linkless generated people refs
- current structured Djot-bearing data sources are also validated:
  - `site/data/service.json`
  - `site/data/teaching.json`
  - `site/data/students.json`

That keeps the guardrail aligned with the repo's actual current people-ref
surfaces rather than only with page wrappers.

## Likely Code Surfaces

Expected primary code surfaces:

- `scripts/sitebuild/people_registry.py`
- `scripts/sitebuild/people_refs.py`
- `scripts/sitebuild/djot_refs.py`
- `scripts/sitebuild/people_refs_audit.py`
- source/build validation where generated ref safety is enforced

This slice may also need small follow-on adjustments in structured render
helpers that currently assume a people-backed reference is always linkable.

## Test Targets

Focused tests should cover:

- loader accepts people with:
  - only `url`
  - only `linkedin`
  - only `github`
  - no public link at all
- unknown person fields are still rejected
- `primary_url` chooses `url` over `linkedin` over `github`
- generated refs include all labels for linkable people
- generated refs exclude linkless people
- manual-refs audit stays coherent when only some people generate refs
- authored-source validation catches linkless people being used where a
  generated people ref is required
- existing `name` / `aliases` semantics remain intact

Verification should include:

- focused unit tests
- focused audit tests for generated-vs-manual ref behavior
- `make build`
- `make test`
- `make check`

## Documentation Updates When This Lands

Update:

- `docs/plans/people-registry-semantics.md`
- `docs/plans/teaching-campaign.md`
- `docs/plans/collaborators-campaign.md`
- `docs/plans/site-architecture-spec.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

The docs should describe the new linkability rule, but should not record
research provenance or private breadcrumbs.

## Landed Invariant

After this slice:

- `site/data/people.json` is an identity/default-label registry, not a
  guarantee that every person has a public link
- `name` and `aliases` semantics stay the same as the recent people-registry
  cleanup
- generated people refs exist only for linkable people
- authored Djot remains protected against silently depending on linkless
  people refs
- no teaching staffing facts are canonical yet
- no public page rendering changes yet

## Implemented Result

This slice landed in:

- `scripts/sitebuild/people_registry.py`
- `scripts/sitebuild/people_refs.py`
- `scripts/sitebuild/people_refs_audit.py`
- `scripts/sitebuild/source_validate.py`
- `scripts/collaborators_index.py`
- `scripts/sitebuild/page_projection.py`
- focused tests under `tests/`

It established:

- optional `url`, `linkedin`, and `github` public-link fields in the people
  registry
- a derived `primary_url` rule with explicit `url` -> `linkedin` -> `github`
  precedence
- generated people refs only for linkable people
- source-validation errors for authored or structured Djot that tries to use a
  linkless generated people ref
- safe plain-text fallback in current structured consumers where a person key
  may later refer to a linkless person

## Stop Point

Stop after this slice and reassess before extending `site/data/teaching.json`.

The next slice should then be the actual teaching-staffing schema foundation,
not a broader public-rendering or collaborator-enrichment change.
