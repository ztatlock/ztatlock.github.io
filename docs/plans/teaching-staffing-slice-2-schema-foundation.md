# Teaching Staffing Slice 2: Schema Foundation

Status: planned

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-1-people-linkability.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-1-people-linkability.md)
- [teaching-staffing-slice-1a-social-link-normalization.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-1a-social-link-normalization.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Extend the canonical teaching schema so individual instructor-led offerings in
`site/data/teaching.json` can later carry staffing facts cleanly.

This slice should only make staffing representable.
It should not import staffing data yet and should not change any public page.

## Why This Slice Now

The people-registry preconditions have now landed:

- `people.json` can represent linkable and linkless people honestly
- seeded social-profile fallback links now use typed `linkedin` / `github`
  fields consistently
- generated Djot refs and authored-source validation are already safe

That means the next clean move is to extend the teaching schema itself before
any co-instructor or teaching-assistant facts are backfilled.

This keeps the sequence reviewable:

1. make people identity/linkability honest
2. make teaching offerings capable of carrying staffing
3. import co-instructor facts
4. import teaching-assistant facts

## Scope

In scope:

- extend course `offering` objects to allow optional ordered
  `co_instructors`
- extend course `offering` objects to allow optional ordered
  `teaching_assistants`
- key both fields through `site/data/people.json`
- add focused schema-validation tests
- update docs/backlog to reflect the new checkpoint
- do an explicit before/after rendered HTML diff review

Out of scope:

- adding any staffing facts to `site/data/teaching.json`
- changing public teaching rendering
- changing CV teaching rendering
- changing homepage teaching rendering
- adding tutor handling
- collaborator-model work
- people-registry enrichment beyond what has already landed

## Canonical Shape

Recommended new optional `offering` fields for `course` records:

- `co_instructors`
- `teaching_assistants`

Each field should be:

- an ordered array
- of `people.json` keys

Example target shape:

```json
{
  "year": 2025,
  "term": "Autumn",
  "url": "https://courses.cs.washington.edu/courses/cse507/25au/",
  "co_instructors": ["example-person"],
  "teaching_assistants": ["ta-one", "ta-two"]
}
```

This slice should only make that shape valid.
The seeded data should remain unchanged.

## Validation Rules

Use explicit narrow validation:

1. `co_instructors` and `teaching_assistants` are optional.
2. If present, each must be a non-empty array.
3. Each entry must be a non-empty string.
4. Each entry must resolve as an existing `people.json` key.
5. Duplicate keys within the same staffing field are rejected.
6. These staffing fields are allowed only on course offerings, not on
   summer-school events.
7. The existing `teaching_assistant` history group stays separate.
   This slice should not reinterpret or merge it with offering staffing.

Deliberate non-rules for this slice:

- no cross-field dedup rule yet between `co_instructors` and
  `teaching_assistants`
- no role taxonomy beyond those two fields
- no tutor field

Those decisions should stay deferred until real staffing data is imported.

## Why The Slice Should Stay This Narrow

This slice is purely about schema capability.

It should not mix together:

- schema extension
- data backfill
- people-registry growth
- tutor policy
- public rendering decisions

That separation keeps review straightforward and gives later slices a stable
foundation to build on.

## Likely Code Surfaces

Primary implementation surfaces:

- `scripts/teaching_record.py`
- `tests/test_teaching_record.py`

Possible secondary surfaces:

- source/build validation only if the new schema touches any existing teaching
  validation seam outside the loader

This slice should not need rendering changes in:

- `scripts/sitebuild/page_projection.py`
- `site/teaching/index.dj`
- `site/cv/index.dj`

## Test Targets

Focused tests should cover:

- seed teaching registry still loads unchanged
- course offerings accept valid `co_instructors`
- course offerings accept valid `teaching_assistants`
- unknown staffing keys are rejected
- duplicate staffing keys within one field are rejected
- empty staffing arrays are rejected
- staffing fields on summer-school records remain invalid
- existing course/summer-school invariants still hold

Verification should include:

- focused teaching-schema tests
- `make build`
- `make test`
- `make check`

## Rendered Diff Review

This slice should include an explicit before/after rendered HTML diff review.

Expected outcome:

- no rendered HTML changes anywhere

That is the correct result because this slice changes only schema capability,
not any seeded teaching facts or consumer render policy.

If any rendered page changes, the diff must be explained explicitly before the
slice is accepted.

## Docs / Backlog

When this slice lands, update:

- `docs/plans/teaching-staffing-campaign.md`
- `docs/plans/teaching-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

The repo should then show that:

- people linkability is settled
- seeded social-link normalization is done
- teaching offerings can now represent staffing facts canonically
- co-instructor and TA backfill are the next deliberate slices

## Stop Point

Stop after the schema foundation lands and reassess.

The next slice should then be the intentionally smaller co-instructor
canonicalization slice, not the larger TA import and not any public rendering
work.
