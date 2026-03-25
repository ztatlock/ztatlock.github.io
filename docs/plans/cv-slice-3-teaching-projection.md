# CV Slice 3: Teaching Projection

Planned.

## Goal

Replace only the duplicated teaching section bodies in the CV with projection
from `site/data/teaching.json`, while keeping the `## Teaching` section and
its subsection headings hand-authored in `site/cv/index.dj`.

## Why Teaching Next

Teaching is the best next CV consumer slice after students because:

- it is still one of the largest duplicated factual domains in the CV
- it exercises a second shared-data-first canonical domain after students
- it tests an important downstream-consumer property:
  the CV legitimately includes a `Teaching Assistant` subsection even though
  the public teaching wrapper at `site/teaching/index.dj` does not
- it is less policy-heavy than service, which would immediately force more
  choices about collapsing yearly service terms into ranges and rendering
  ongoing appointments

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Teaching` heading and the current subsection headings:
   - `### _Instructor_`
   - `### _Summer School Courses_`
   - `### _Teaching Assistant_`
3. Replace only the repeated teaching subsection bodies with placeholders.
4. Add an explicit CV-specific teaching renderer over `site/data/teaching.json`.
5. Keep the teaching-award note hand-authored.
6. Add source validation for the placeholder-based CV teaching section.

Likely placeholders:

- `__CV_TEACHING_INSTRUCTOR_LIST__`
- `__CV_TEACHING_SUMMER_SCHOOL_LIST__`
- `__CV_TEACHING_TA_LIST__`

## Important Rendering Principle

This slice should not blindly reuse the public teaching renderer.

The public teaching page is optimized for a dedicated teaching page with:

- richer course descriptions
- public-facing course ordering and spacing
- linked offerings
- no `Teaching Assistant` subsection

The CV renderer should instead optimize for a compressed consumer view.

That likely means:

- preserving the current `Instructor` / `Summer School Courses` /
  `Teaching Assistant` subsection structure
- retaining ordered offering/year history
- using fewer public links than the teaching page unless they clearly help
- keeping details like special-topics notes and co-teaching only where they
  materially improve the CV

## Format Flexibility

The CV teaching slice does not need to preserve the current hand-authored Djot
line-for-line.

It may improve the visible format if that makes the projected CV cleaner and
more coherent, provided that:

- the same teaching facts are preserved or improved
- visible changes are explicit policy, not accidental renderer fallout
- the old/new rendered HTML diff is reviewed carefully and explained

## Important Consumer Boundary

This slice should prove that one canonical teaching source can support:

- the public teaching wrapper at `/teaching/`
- a more compressed CV teaching view
- the CV-only `Teaching Assistant` subsection

without adding a new canonical `cv` data model and without re-opening the
teaching schema unless a real consumer need clearly requires it.

## Out Of Scope

- no service CV projection yet
- no talks/publications/highlights projection yet
- no homepage teaching cleanup in this slice
- no teaching-staffing enrichment yet
  (`co_instructors` / `teaching_assistants` remain later offering-level work)

## Expected Invariants After This Slice

- the CV teaching section derives from `site/data/teaching.json`
- the public teaching page and CV share one canonical teaching source
- the CV explicitly proves that a downstream consumer may expose more of a
  canonical domain than the public wrapper does
- any intentional CV/public divergence in teaching presentation is explicit
  renderer policy rather than silent drift
- no duplicated literal teaching blocks remain in the CV wrapper

## Verification Targets

- focused renderer/projection tests for the compressed CV teaching view
- validation that required CV teaching placeholders are present
- validation that literal duplicated CV teaching records are rejected
- compare old and new rendered CV HTML with attention to the `## Teaching`
  section specifically:
  - only the intended teaching subsection bodies should change
  - surrounding CV headings and non-teaching sections should remain stable
  - differences should be explainable by explicit renderer policy
- `make test`
- `make check`

## Stop Point

Stop after the teaching CV projection and reassess before moving on to service
or more curated CV domains like talks, publications, or highlights.
