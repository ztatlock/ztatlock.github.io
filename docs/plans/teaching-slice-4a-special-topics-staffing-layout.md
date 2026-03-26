# Teaching Slice 4A: Special Topics Staffing-Aware Layout

Status: implemented

It builds on:

- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-slice-4-public-page-staffing-layout.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-slice-4-public-page-staffing-layout.md)
- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Make the public `Special Topics Graduate Courses` section staffing-aware so
special-topics offerings can visibly reflect canonical offering-level staffing
facts just like the main UW course section.

This is a public-page consumer slice, not a data-model slice.

## Why This Slice Next

The current public teaching page is better than it was before the recent
teaching staffing work:

- staffing facts are canonical
- the main UW course section now shows them
- the page is more consistent with the structured data model than before

But one seam is now more visible:

- `special_topics` records are still UW courses
- some special-topics offerings now carry canonical staffing facts
- the current special-topics renderer still ignores those facts

So the page is now richer but still slightly inconsistent in ontology and
presentation.

This slice should fix that inconsistency while keeping a future styling/polish
campaign explicitly separate. The short-term goal is cleaner data fidelity and
uniform projection behavior, not final visual polish.

## Current Rendering

Today the public teaching page has two different UW-course rendering styles in
`scripts/sitebuild/page_projection.py`:

- `uw_courses` uses the staffing-aware vertical offering-list renderer
- `special_topics` still uses an older compact renderer

Current `special_topics` policy:

1. render one compact bullet like:
   - `UW CSE 599W: Systems Verification, 2016 Spring`
2. render `details` lines beneath it when present
3. do not render `co_instructors`, `teaching_assistants`, or `tutors`

That means the public page currently hides canonical staffing facts on
special-topics offerings such as:

- `UW CSE 599W` Spring 2016
  - `Co-Instructors: Bryan Parno, Xi Wang`

## Proposed Rendering

Keep:

- the `## Special Topics Graduate Courses` heading
- the `special_topics` grouping in `site/data/teaching.json`
- the rest of the public teaching page unchanged

Change:

- render each special-topics record with the same general offering-list pattern
  as the main UW course section
- allow special-topics offerings to show nested staffing bullets when present
- keep special-topics `details` visible

Conceptually, instead of:

- `UW CSE 599W: Systems Verification, 2016 Spring`
  - `Formally verifying systems implementations`

render more like:

- `UW CSE 599W: Systems Verification`
  - `Formally verifying systems implementations`
  - `2016 Spring`
    - `Co-Instructors: Bryan Parno and Xi Wang`

This makes special topics behave like a presentation subgroup of UW courses,
not like a staffing-blind exception.

## Rendering Policy

Recommended public teaching policy:

- keep the `Special Topics Graduate Courses` heading unchanged
- keep special-topics record order canonical from `site/data/teaching.json`
- keep offering order canonical within a record
- keep the teaching-award note unchanged
- keep summer-school and Related unchanged

Recommended special-topics record policy:

- render a title line without inlining the year/term into that title line
- render `details` beneath the title when present
- render offerings as top-level vertical bullets, even when there is only one
  offering
- render nested staffing bullets beneath an offering when present

Recommended staffing display policy:

- show `Co-Instructors` only when non-empty
- show `Teaching Assistants` only when non-empty
- show `Tutors` only when non-empty
- use `people.json` default `name`
- link a person name when `primary_url` exists
- render plain text when a person is linkless

Recommended implementation policy:

- reuse as much of the existing offering-plus-staffing rendering logic as is
  reasonable
- do not broaden into a public-teaching-page redesign beyond this consistency
  fix
- do not try to solve the broader “teaching page is now richer but uglier”
  styling question in this slice

## Invariant

After this slice:

- the public teaching page treats special-topics offerings as staffing-capable
  UW course offerings
- canonical staffing facts on special-topics offerings are visible when present
- the `Special Topics Graduate Courses` section remains a distinct subsection
- the teaching data model remains unchanged

## Scope

In scope:

- adjust the special-topics renderer in
  `scripts/sitebuild/page_projection.py`
- share/reuse offering-plus-staffing rendering helpers where it keeps the code
  cleaner
- add focused projection and rendered-output tests
- update docs/backlog after landing
- do an explicit rendered HTML diff review focused on `/teaching/`

Out of scope:

- homepage recent-teaching projection
- CV teaching renderer changes
- collaborator relationship-model work
- any teaching data-model changes
- any broad CSS/styling cleanup campaign

## Likely File Surfaces

Primary implementation surfaces:

- `scripts/sitebuild/page_projection.py`

Primary tests:

- `tests/test_page_projection.py`
- `tests/test_page_renderer.py`

Likely docs/backlog:

- `docs/plans/teaching-campaign.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

## Verification

Verification should include:

- focused unit tests for special-topics rendering
- `make verify`
- explicit before/after rendered HTML diff review
- `git diff --check`

Rendered diff review should answer:

- did anything outside `/teaching/` change?
- within `/teaching/`, did the change stay limited to the special-topics
  section?
- do Bryan Parno and Xi Wang now appear for `UW CSE 599W`?
- did the main UW course section remain unchanged from slice 4?
- did summer school, the award note, and Related remain unchanged?

## Stop Point

Stop after the special-topics staffing-aware layout slice lands and reassess.

The next decision should then be between:

- collaborator relationship-model work
- homepage curated-block exploration
- later teaching-page styling/projection polish

not automatic broadening of the teaching page by inertia.

Implemented outcome:

- the public `Special Topics Graduate Courses` section now uses the same
  general offering-plus-staffing rendering pattern as the main UW course
  section
- canonical special-topics staffing facts now appear when present, including
  Bryan Parno and Xi Wang for `UW CSE 599W`
- the broader teaching-page styling/polish question remains explicitly
  deferred to a later campaign
