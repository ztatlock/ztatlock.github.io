# Teaching Staffing Slice 4: Teaching Assistant Canonicalization

Status: drafted for review

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-2-schema-foundation.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-2-schema-foundation.md)
- [teaching-staffing-slice-3-co-instructor-canonicalization.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-3-co-instructor-canonicalization.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)

## Goal

Backfill confirmed teaching-assistant facts into canonical teaching data for
the UW instructor-led offerings, along with the needed `people.json` growth
to key those staffing facts cleanly.

This slice should keep public rendering unchanged.

## Why This Slice Next

The teaching-staffing foundation is now in place:

- `people.json` can represent linkable and linkless people honestly
- seeded social-link normalization is landed
- teaching offerings can carry ordered `teaching_assistants`
- the smaller co-instructor slice already proved the data-import pattern

That leaves the larger TA import as the next clean canonical-data step.

## Invariant

After this slice:

- confirmed TA facts for the researched UW instructor-led offerings are
  canonical in `site/data/teaching.json`
- every referenced TA resolves through `site/data/people.json`
- linkless TAs are allowed canonically where needed
- no tutor facts are silently collapsed into `teaching_assistants`
- no public teaching, CV, homepage, or collaborators rendering changes are
  introduced yet

## Scope

In scope:

- add ordered `teaching_assistants` arrays to the relevant UW course
  offerings in `site/data/teaching.json`
- add the needed TA person entries and aliases to `site/data/people.json`
- normalize obvious person-key/name/url cases needed by that import
- keep the import limited to confirmed TA facts for the UW instructor-led
  offerings already represented in canonical teaching data
- add focused seeded-registry and teaching-record tests
- update docs/backlog to reflect the new checkpoint
- do an explicit before/after rendered HTML diff review

Out of scope:

- any tutor import
- any public rendering of staffing fields
- any collaborator-model implementation
- any non-UW staffing import
- any new people-profile fields beyond the already landed
  `url` / `linkedin` / `github` model

## Data Boundary

This slice should only backfill teaching assistants for the current UW
instructor-led offerings already modeled in `site/data/teaching.json`:

- `uw-cse-507`
- `uw-cse-505`
- `uw-cse-341`
- `uw-cse-331`
- `uw-cse-599z-accurate-computing`
- `uw-cse-599w-systems-verification`
- `uw-cse-506-advanced-topics-in-programming-languages`

Do not expand this slice to:

- UCSD or Purdue teaching records
- the historical `teaching_assistant` group where Zach served as a TA
- summer-school records

## People Registry Policy

This slice should use the already landed people-registry semantics:

- `name` is the default site-facing canonical label
- `aliases` are resolution-only alternate spellings
- `url`, `linkedin`, and `github` are optional public-link fields
- some TAs may be linkless

Recommended normalization policy for the TA import:

- use existing person keys when the identity is already in `people.json`
- add new person keys only when needed by confirmed TA facts
- prefer stable, human-readable slug keys derived from the canonical `name`
- add aliases when they are needed to preserve resolution of known alternate
  spellings
- do not invent or infer public links that are not already confirmed

## Tutor Boundary

Tutor handling must stay explicit in this slice.

Policy:

- do not put tutors in `teaching_assistants`
- do not add `tutors` in the same slice
- if any current researched offering has only tutor evidence for a person,
  leave that fact out of this slice and record the omission explicitly in the
  review and backlog

## Redundant Prose Review

Current public consumers do not render offering-level `teaching_assistants`,
so the expected rendered result is still no site change.

However, this slice should still review the seeded teaching records for any
literal TA prose note that would become a second source of truth once the
structured fact is canonical.

Recommended policy:

- remove redundant literal TA notes only if the same fact is now canonical in
  `offerings[*].teaching_assistants`
- call out any such removal explicitly in the rendered diff review

## Likely File Surfaces

Primary data surfaces:

- `site/data/teaching.json`
- `site/data/people.json`

Primary code/test surfaces:

- `tests/test_teaching_record.py`
- `tests/test_people_registry.py`
- likely `tests/test_page_projection.py` if any redundant prose seam affects
  current rendered teaching/CV output

No renderer changes should be required in this slice.

## Tests And Verification

Focused tests should cover:

- the seeded teaching registry loads with representative `teaching_assistants`
  arrays
- representative offerings expose the expected canonical TA keys
- new TA people entries resolve cleanly through `people.json`
- linkless TA people remain valid canonical records
- tutor facts are not silently accepted as `teaching_assistants`
- existing non-staffing details remain intact where still intended

Verification should include:

- focused unit tests
- the repo's safe sequential verification path
- an explicit before/after rendered HTML diff review
- `git diff --check`

## Rendered Diff Review

This slice should save and compare before/after rendered output.

Expected outcome:

- ideally no rendered HTML changes anywhere, because current consumers do not
  render TA staffing fields

Possible exception:

- if a redundant literal TA prose note is removed from seeded teaching data,
  that visible diff must be called out explicitly and justified as removal of
  a now-redundant second source of truth

## Docs And Backlog

When this slice lands, update:

- `docs/plans/teaching-staffing-campaign.md`
- `docs/plans/teaching-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

It should then be explicit that:

- teaching staffing now has canonical co-instructors and teaching assistants
- tutor handling is still a separate later decision
- public staffing rendering is still deferred
- collaborator relationship modeling is better grounded but still deferred

## Stop Point

Stop after the TA import lands and reassess.

The next decision should then be the separate tutor-policy slice, not public
staffing rendering by inertia.
