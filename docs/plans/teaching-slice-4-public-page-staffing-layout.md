# Teaching Slice 4: Public Page Staffing Layout

Status: drafted for review

It builds on:

- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-slice-2-index-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-slice-2-index-projection.md)
- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-5-tutor-canonicalization.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-5-tutor-canonicalization.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Improve the public teaching page so the UW course offerings render in a
staffing-aware vertical layout that can actually expose the canonical
`co_instructors`, `teaching_assistants`, and `tutors` facts.

This should be a public-page consumer slice, not a new data-model slice.

## Why This Slice Next

The teaching data foundation is now strong:

- the public teaching page already projects from `site/data/teaching.json`
- teaching staffing is now canonical on the relevant instructor-led offerings
- people-linkability semantics are now explicit and safe for linked/plain-text
  person display

But the current UW course renderer still reflects the pre-staffing layout
assumption: each course ends in a flowing columns block of flat offering
entries.

That layout is compact, but it is a poor fit for nested staffing information.

## Current Rendering

Today the public teaching wrapper at
`site/teaching/index.dj` keeps only the page framing:

- `# Teaching`
- `## Courses at the University of Washington`
- special-topics heading
- teaching-award note
- `## Summer School Courses`
- `## Related`

The actual UW course body comes from
`render_teaching_uw_courses_list_djot(...)` in
`scripts/sitebuild/page_projection.py`.

Current policy for each UW course:

1. render one course heading line:
   - `*UW CSE 505: Concepts of Programming Languages*`
2. render the audience label and description
3. render the offerings as a flat `{.columns .columns-8rem}` bullet list

That means current offerings are effectively rendered like a compact term/year
grid:

- Autumn 2025
- Autumn 2023
- Spring 2021
- ...

This works for chronology, but it has two limitations:

- it visually reads more like a compact table than like a list of distinct
  offerings
- it provides no clean place to show per-offering staffing substructure

## Proposed Rendering

Keep the page framing and section structure the same.

For UW courses only, change the per-course renderer policy to:

1. keep the course header line:
   - `*UW CSE 505: Concepts of Programming Languages*`
2. keep the audience label and description directly under the course title
3. replace the flowing columns block with a vertical offering list
4. render each offering as one top-level bullet
5. when staffing facts exist for that offering, render nested bullets beneath
   the offering

Conceptually:

- `Spring 2025`
  - `Co-Instructors: James Wilcox`
  - `Teaching Assistants: Oliver Flatt, Kevin Mu`
- `Winter 2023`
  - `Co-Instructors: James Wilcox`
  - `Teaching Assistants: Gus Smith, Audrey Seo, Anjali Pal`
- `Autumn 2016`
  - `Teaching Assistants: Konstantin Weitz`
  - `Tutors: James Wilcox, Eric Mullen, Joe Redmon`

## Rendering Policy

Recommended public teaching policy:

- keep course order canonical from `site/data/teaching.json`
- keep offering order canonical within each course
- keep special-topics rendering unchanged in this slice
- keep summer-school rendering unchanged in this slice
- keep the teaching-award note unchanged
- keep the Related section unchanged

Recommended staffing display policy:

- show `Co-Instructors` only when non-empty
- show `Teaching Assistants` only when non-empty
- show `Tutors` only when non-empty
- use `people.json` default `name` for labels
- link a person name when `primary_url` exists
- render plain text when a person is linkless

Recommended layout/CSS policy:

- prefer markup-first change with minimal CSS churn
- start with normal nested lists rather than inventing a more styled card or
  grid layout
- only add tiny teaching-specific CSS if the default list spacing is clearly
  inadequate after rendered review

## Invariant

After this slice:

- the public teaching page visibly reflects canonical offering-level staffing
  facts for UW courses
- UW course offerings render as vertical list items rather than flowing
  column blocks
- the public teaching page remains a thin wrapper over canonical teaching and
  people data
- special-topics and summer-school sections remain unchanged
- no homepage, CV, or collaborators rendering changes are introduced

## Scope

In scope:

- adjust the public UW course teaching renderer in
  `scripts/sitebuild/page_projection.py`
- add any tiny CSS needed for readable nested staffing lists
- add focused renderer/projection tests
- update docs/backlog after the slice lands
- do an explicit rendered HTML diff review focused on `/teaching/`

Out of scope:

- homepage recent-teaching projection
- CV teaching renderer changes
- collaborator relationship-model work
- changes to the canonical teaching data model itself
- special-topics or summer-school redesign

## Likely File Surfaces

Primary implementation surfaces:

- `scripts/sitebuild/page_projection.py`
- possibly `site/static/style.css`

Primary wrapper surface:

- `site/teaching/index.dj`
  - likely unchanged unless a tiny wrapper-side class/helper is clearly useful

Primary tests:

- `tests/test_page_projection.py`
- optionally a small rendered-output assertion in any existing page-render test
  if needed

## Verification

Verification should include:

- focused unit tests for representative UW course rendering
- `make verify`
- explicit before/after rendered HTML diff review
- `git diff --check`

Rendered diff review should answer:

- did anything outside `/teaching/` change?
- within `/teaching/`, did only the UW course offering layout change?
- were special topics, award note, summer school, and Related unchanged?
- is every staffing line sourced from canonical data and intentionally shown?

## Stop Point

Stop after the public teaching page layout/staffing slice lands and reassess.

The next decision should then be between:

- collaborators slice 3
- homepage curated-block work
- curated CV cleanup

not automatic broadening of teaching consumers by inertia.
