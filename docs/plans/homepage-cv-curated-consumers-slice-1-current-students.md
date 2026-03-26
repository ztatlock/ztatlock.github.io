# Homepage / CV Curated Consumers Slice 1: Homepage Current Students

Status: implemented

It builds on:

- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Turn the homepage `## Current Students` block into a tiny derived consumer of
[site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json),
while keeping the section heading and trailing "students page" sentence
authored in the homepage wrapper.

This slice should:

- stop hand-maintaining the repeated current-students body on the homepage
- reuse canonical student names and labels
- preserve the current compact columns-style homepage presentation

It should not:

- change the public `/students/` page
- change the CV students sections
- broaden into alumni, postdocs, or visiting students
- redesign homepage layout generally

## Why This Slice Is Safe

The current homepage block is almost the ideal tiny-consumer case.

Current authored block in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj):

- contains 8 entries
- all 8 correspond directly to the canonical `current_students` section in
  [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)
- uses exactly the same person names and labels as the canonical data
- already behaves like a structured list rather than editorial prose

So the main job is not policy invention.
It is simply to stop keeping a second copy of a canonical list.

## Current Behavior

Today:

- the homepage keeps a literal `{.columns .columns-16rem}` list of current
  students
- each entry is one `[Name][]`, `Label` pair
- the trailing sentence remains authored:
  `Please see my [students page](students/) for more.`

This is already a consumer shape.
It is just hand-maintained instead of projected.

## Proposed Behavior

After this slice:

- `## Current Students` stays authored in
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- the trailing "students page" sentence stays authored
- only the repeated list body is projected from canonical students data

Recommended placeholder:

- `__HOMEPAGE_CURRENT_STUDENTS_LIST__`

Recommended render policy:

- use only the canonical `current_students` section
- preserve canonical record order
- render each record as:
  - linked `name` when a `people.json` primary URL exists
  - plain-text `name` otherwise
  - `, label`
- preserve the current homepage columns wrapper rather than inventing a new
  layout

## Invariant

After this slice:

- the homepage current-students body can no longer drift from the canonical
  current-students section
- remaining variation is only homepage wrapper framing, not duplicated facts
- no new homepage-only student-selection metadata is introduced

## Likely Code Surfaces

Primary implementation surfaces:

- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- likely a tiny helper alongside existing students/homepage projection code
- [scripts/sitebuild/source_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/source_validate.py)

Likely tests:

- [tests/test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)
- [tests/test_page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_renderer.py)
- [tests/test_source_validate.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_source_validate.py)

## Validation Contract

After this slice, source validation should enforce:

- the homepage `## Current Students` section contains
  `__HOMEPAGE_CURRENT_STUDENTS_LIST__`
- the section does not contain a leftover literal repeated current-students
  body
- the trailing students-page link still uses canonical `students/`

If practical, those checks should be scoped to the homepage section rather
than scanning the whole file blindly.

## Expected Visible Changes

This slice should ideally produce no intentional rendered HTML change.

What should stay the same:

- section heading
- entry order
- entry names
- entry labels
- columns layout
- trailing students-page sentence

The intended change is source-of-truth cleanup, not presentation change.

## Verification

Verification should include:

- focused homepage projection tests
- focused source-validation tests
- `make verify`
- `git diff --check`

Rendered diff review should confirm:

- no visible change outside [build/index.html](/Users/ztatlock/www/ztatlock.github.io/build/index.html)
- ideally no substantive visible change even within the homepage current
  students block

Implemented result:

- the rendered diff was empty once `sitemap.xml` noise was excluded
