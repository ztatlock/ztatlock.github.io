# CV Slice 2: Students Projection

Implemented.

## Goal

Replace only the duplicated students sections in the CV with projection from
`site/data/students.json`, while keeping the CV wrapper and surrounding
section structure hand-authored.

## Why Students First

Students is the best first CV consumer slice because:

- the data is already canonical
- the duplication is large and obvious
- the CV view is clearly different from the public students page
- it will force the first real downstream-renderer policy decisions without
  dragging multiple CV domains into one slice

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Students` heading and the current subsection headings in
   the wrapper.
3. Replace only the repeated students subsection bodies with placeholders.
4. Add an explicit compressed CV renderer over `site/data/students.json`.
5. Decide the visiting-section heading and Ian Briggs policy together.
6. Add source validation for the placeholder-based CV students section.

Likely placeholders:

- `__CV_STUDENTS_CURRENT_LIST__`
- `__CV_STUDENTS_POSTDOC_LIST__`
- `__CV_STUDENTS_PHD_LIST__`
- `__CV_STUDENTS_MASTERS_LIST__`
- `__CV_STUDENTS_BACHELORS_LIST__`
- `__CV_STUDENTS_VISITING_LIST__`

## Important Rendering Principle

This slice should **not** blindly reuse the public students-page renderer.

The CV renderer should be intentionally different where the current CV style
demands it, for example:

- plain `Name, Label` lines by default
- thesis details rendered as plain text rather than thesis-title links
- outcome lines retained as plain bullets
- fewer person links than the public students page unless a stronger policy is
  justified
- co-advisor details omitted unless the current CV clearly demonstrates they
  belong
- clearer omission rules where the CV intentionally differs

Those differences should live in the CV renderer, not in special-case
canonical data.

## Important Visiting-Section Constraint

This slice has one coupled policy question that should be decided explicitly:

- the public students page now uses `Visiting Students and Interns`
- the CV still says `Visiting Summer Students`
- `Ian Briggs` exists canonically in `site/data/students.json` but is omitted
  from the current CV

So this slice should not treat:

- heading wording
- Ian inclusion/omission

as separate arbitrary choices. The rendered heading and inclusion rule should
be consistent with one another.

## Out Of Scope

- no teaching CV projection yet
- no service CV projection yet
- no talks/publications/highlights projection yet
- no route move in this slice; that belongs to slice 1
- no new student schema churn unless the first consumer truly proves it
  necessary

## Expected Invariants After This Slice

- the CV students sections derive from `site/data/students.json`
- the public students page and CV now share one canonical advising source
- CV-specific rendering differences are explicit in one small consumer
  renderer
- any intentional omission or heading divergence is documented policy rather
  than silent drift
- no duplicated literal students records remain in the CV wrapper

## Verification Targets

- focused renderer/projection tests for the compressed CV students view
- validation that required CV students placeholders are present
- validation that literal duplicated CV students records are rejected
- explicit test coverage for the visiting-section/Ian policy
- compare old and new rendered CV HTML with attention to the `## Students`
  section specifically:
  - only the intended students subsection bodies should change
  - surrounding CV headings and non-students sections should remain stable
  - differences should be explainable by the explicit compressed renderer
    policy, not accidental formatting drift
- `make test`
- `make check`

## Stop Point

Stop after the students CV projection and reassess before touching teaching,
service, or any highlights sections.

This is the first real interface-pressure test for the existing canonical
student model.
