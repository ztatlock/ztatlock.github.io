# Teaching Staffing Slice 5: Tutor Canonicalization

Status: drafted for review

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-2-schema-foundation.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-2-schema-foundation.md)
- [teaching-staffing-slice-3-co-instructor-canonicalization.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-3-co-instructor-canonicalization.md)
- [teaching-staffing-slice-4-teaching-assistant-canonicalization.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-4-teaching-assistant-canonicalization.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Make the tutor role explicit in canonical teaching data by adding ordered
offering-level `tutors` and backfilling the small known set of tutor facts.

This slice should keep public rendering unchanged.

## Why This Slice Next

The core staffing model is now in place:

- `people.json` can represent linkable and linkless people honestly
- teaching offerings can carry ordered `co_instructors` and ordered
  `teaching_assistants`
- confirmed co-instructor and TA facts are now canonical on the relevant UW
  offerings
- tutor handling is the one remaining explicit staffing-policy seam in the
  current campaign

At this point, leaving tutors unmodeled would preserve an avoidable gap in the
canonical staffing record.

## Decision

This slice adopts the explicit-tutors policy.

Policy:

- tutors are a real role and should not be folded into
  `teaching_assistants`
- tutors should be modeled as ordered offering-level `tutors`
- tutor facts should be keyed through `site/data/people.json`
- public teaching/CV/homepage/collaborators rendering should remain deferred

## Invariant

After this slice:

- teaching offerings may canonically carry ordered `tutors`
- the known tutor facts are canonical on the affected offerings in
  `site/data/teaching.json`
- every referenced tutor resolves through `site/data/people.json`
- tutor facts are no longer silently omitted or flattened into
  `teaching_assistants`
- no public rendering changes are introduced yet

## Scope

In scope:

- extend teaching-offering schema to allow ordered `tutors`
- add the small canonical tutor backfill to the affected offerings in
  `site/data/teaching.json`
- add the one needed new person entry to `site/data/people.json`
- add focused loader and seeded-data tests
- update docs/backlog to reflect the new checkpoint
- do an explicit before/after rendered HTML diff review

Out of scope:

- any new public rendering of staffing roles
- any collaborator-model changes
- any broader teaching enrichment beyond these tutor facts
- any new tutor notes or annotations beyond the ordered person-key arrays

## Data Boundary

This slice should stay tightly limited to the known tutor-bearing UW offering
records already present in canonical teaching data:

- `uw-cse-505` Autumn 2016:
  - `teaching_assistants`: `konstantin-weitz`
  - `tutors`: `james-wilcox`, `eric-mullen`, `joe-redmon`
- `uw-cse-505` Autumn 2015:
  - `teaching_assistants`: `doug-woos`
  - `tutors`: `eric-mullen`, `joe-redmon`

This slice should not broaden into:

- any additional staffing imports
- any retrospective reinterpretation of flat staff lists on other offerings
- any non-UW records
- the historical `teaching_assistant` group where Zach served as a TA
- summer-school records

## People Registry Policy

This slice should use the already landed people-registry semantics:

- `name` is the default site-facing canonical label
- `aliases` are resolution-only alternate spellings
- `url`, `linkedin`, and `github` are optional public-link fields
- a tutor may be linkable or linkless

Expected people work in this slice:

- reuse existing entries for `james-wilcox` and `eric-mullen`
- add `joe-redmon` as the one new tutor-linked person record
- do not broaden into unrelated people cleanups while touching `people.json`

## Schema And Validation Policy

Recommended `tutors` rules should mirror the existing staffing fields:

- `tutors` is optional on course offerings
- if present, it must be a non-empty ordered array of person keys
- entries must be non-empty strings
- entries must resolve through `site/data/people.json`
- duplicates within `tutors` are rejected
- `tutors` remains invalid on the historical `teaching_assistant` group

This slice does not need additional cross-role validation such as forbidding a
person from appearing in both `teaching_assistants` and `tutors` on the same
offering. The known data already uses distinct roles cleanly, and the slice
should stay narrow.

## Redundant Prose Review

Current consumers do not render offering-level staffing fields, so the
expected rendered result is no site change.

This slice should still review the seeded teaching records for any literal
tutor prose note that would become a second source of truth once the
structured tutor fact is canonical.

Recommended policy:

- if no such prose exists, do nothing
- if any redundant tutor prose is found, remove it only when the same fact is
  now canonical and call that out explicitly in the rendered diff review

## Likely File Surfaces

Primary data/code surfaces:

- `site/data/teaching.json`
- `site/data/people.json`
- `scripts/teaching_record.py`

Primary test surfaces:

- `tests/test_teaching_record.py`
- `tests/test_people_registry.py`
- likely `tests/test_page_projection.py` only if a redundant prose seam affects
  current rendered teaching/CV output

No renderer changes should be required in this slice.

## Tests And Verification

Focused tests should cover:

- teaching-offering schema accepts ordered `tutors`
- representative seeded offerings expose the expected canonical tutor arrays
- `joe-redmon` resolves cleanly through `people.json`
- duplicates in `tutors` are rejected
- unknown tutor person keys are rejected
- empty `tutors` arrays are rejected
- `tutors` remains invalid on the historical `teaching_assistant` group

Verification should include:

- focused unit tests
- the repo's safe sequential verification path: `make verify`
- an explicit before/after rendered HTML diff review
- `git diff --check`

## Rendered Diff Review

This slice should save and compare before/after rendered output.

Expected outcome:

- ideally no rendered HTML changes anywhere, because current consumers do not
  render tutor staffing fields

Possible exception:

- if a redundant literal tutor prose note is removed from seeded teaching
  data, that visible diff must be called out explicitly and justified as
  removal of a now-redundant second source of truth

## Docs And Backlog

When this slice lands, update:

- `docs/plans/teaching-staffing-campaign.md`
- `docs/plans/teaching-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

It should then be explicit that:

- teaching staffing now has canonical co-instructors, teaching assistants, and
  tutors
- public staffing rendering remains deferred
- later collaborator work has a fuller teaching-staffing foundation

## Stop Point

Stop after tutor canonicalization lands and reassess.

The next decision should then be whether to:

- start a later teaching/course enrichment campaign
- return to richer collaborator modeling now that teaching roles are more
  complete
- or pursue another separate campaign first
