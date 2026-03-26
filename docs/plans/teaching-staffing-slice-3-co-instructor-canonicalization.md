# Teaching Staffing Slice 3: Co-Instructor Canonicalization

Status: planned

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-2-schema-foundation.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-2-schema-foundation.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Backfill confirmed co-instructor facts into canonical teaching data in
`site/data/teaching.json`, along with the one clearly needed new
`people.json` entry.

This slice should keep public rendering unchanged.
It should only canonicalize co-instructor facts that are already high
confidence.

## Why This Slice Next

The schema foundation is now landed:

- offerings can carry ordered `co_instructors`
- offerings can carry ordered `teaching_assistants`
- those fields are keyed through `people.json`

That means the next clean move is the smaller staffing-data import first:

1. co-instructors
2. then teaching assistants
3. then the separate tutor decision

This keeps review manageable because the co-instructor surface is small and the
facts are relatively high-confidence.

## Scope

In scope:

- add confirmed `co_instructors` arrays to the relevant offerings in
  `site/data/teaching.json`
- add the needed new co-instructor person entry to `site/data/people.json`
- keep existing teaching descriptions/details intact unless one now becomes a
  redundant second source of the same co-instructor fact
- add focused tests for the seeded co-instructor backfill
- update docs/backlog to reflect the new checkpoint
- do an explicit before/after rendered HTML diff review

Out of scope:

- any `teaching_assistants` data import
- any tutor handling
- any public teaching/CV/homepage staffing rendering
- broader people-registry enrichment beyond what this one co-instructor needs
- collaborator-model work

## Intended Canonical Facts

Current high-confidence target set:

- `uw-cse-341`, Autumn 2024: `anjali-pal`
- `uw-cse-331`, Winter 2024: `anjali-pal`
- `uw-cse-505`, Spring 2025: `james-wilcox`
- `uw-cse-505`, Winter 2023: `james-wilcox`
- `uw-cse-505`, Spring 2021: `james-wilcox`
- `uw-cse-505`, Autumn 2017: `leonardo-de-moura`
- `uw-cse-505`, Winter 2015: `valentin-robert`
- `uw-cse-599w-systems-verification`, Spring 2016:
  - `bryan-parno`
  - `xi-wang`

This is intentionally just the co-instructor set.

## People Registry Scope

Current `people.json` coverage for those co-instructors:

- `anjali-pal`: already present
- `james-wilcox`: already present
- `valentin-robert`: already present
- `bryan-parno`: already present
- `xi-wang`: already present
- `leonardo-de-moura`: missing, needs a new entry

This slice should add only the clearly needed new person entry:

- `leonardo-de-moura`

No other staffing people should be added yet.

## Policy On Existing Prose Notes

One current record already contains literal co-teaching prose:

- `uw-cse-599w-systems-verification` has the detail
  `Co-taught with [Xi Wang][] and [Bryan Parno][]`

This slice should make an explicit choice about that note.

Recommended policy:

- canonical co-instructor truth should move to the `offerings[*].co_instructors`
  field
- the existing detail note should be removed once the structured fact is
  canonical, because otherwise the same fact would live in two places in the
  same record

That is still consistent with the repo's principle that repeated facts become
canonical while prose stays authored where prose is actually needed.

This slice should not do broader editorial cleanup beyond that one seam.

## Validation / Data Rules

Use the schema from slice 2 without expanding it further:

- only `co_instructors`, not `teaching_assistants`
- only `people.json` keys
- preserve offering order
- preserve course/group order
- preserve any existing non-staffing details

No new policy should be added for:

- tutor roles
- co-instructor ordering beyond using the observed canonical order where there
  are two names on one offering
- rendering of co-instructor names on public pages

## Likely Code Surfaces

Primary data surfaces:

- `site/data/teaching.json`
- `site/data/people.json`

Primary test surfaces:

- `tests/test_teaching_record.py`
- likely one focused people-registry regression check for the new person entry

No renderer changes should be required in this slice.

## Test Targets

Focused tests should cover:

- the seeded teaching registry loads with the new co-instructor arrays
- representative offerings expose the expected `co_instructors`
- the new `leonardo-de-moura` entry resolves cleanly through `people.json`
- existing non-staffing details remain intact where they are still intended

Verification should include:

- focused unit tests
- `make build`
- `make test`
- `make check`

## Rendered Diff Review

This slice should include an explicit before/after rendered HTML diff review.

Expected outcome:

- likely no rendered HTML changes anywhere, because current consumers do not
  render offering staffing fields

Possible exception:

- if removing the `Co-taught with [Xi Wang][] and [Bryan Parno][]` detail from
  the `uw-cse-599w-systems-verification` record affects a currently rendered
  page, that visible diff must be called out explicitly and justified as the
  removal of a now-redundant second source of truth

## Docs / Backlog

When this slice lands, update:

- `docs/plans/teaching-staffing-campaign.md`
- `docs/plans/teaching-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

The repo should then show that:

- teaching staffing schema exists
- confirmed co-instructor facts are now canonical
- the larger TA import is still the next separate slice

## Stop Point

Stop after the co-instructor backfill lands and reassess.

The next slice should then be the larger teaching-assistant canonicalization
slice, not tutor policy and not staffing rendering.
