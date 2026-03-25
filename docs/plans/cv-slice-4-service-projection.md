# CV Slice 4: Service Projection

Implemented.

## Goal

Replace only the duplicated service subsection bodies in the CV with
projection from `site/data/service.json`, while keeping the `## Service`
section, its subsection headings, and the faculty-skit prose note
hand-authored in `site/cv/index.dj`.

## Why Service Next

Service was the right next CV consumer slice after teaching because:

- it was the largest remaining duplicated structured block in the CV
- it exercises a third shared-data-first canonical domain from the consumer
  side
- it proves the CV can reuse canonical range-collapsing and ongoing-term
  semantics without becoming its own data domain
- it leaves later homepage consumer cleanup explicitly deferred

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Service` heading and the current subsection headings:
   - `### _Reviewing_`
   - `### _Organizing_`
   - `### _Mentoring_`
   - `### _Department_`
3. Replace only the repeated service subsection bodies with placeholders.
4. Add an explicit CV-specific service renderer over `site/data/service.json`.
5. Reuse canonical service range-collapsing and `Present` semantics.
6. Keep the faculty-skit prose note hand-authored in the CV.
7. Add source validation for the placeholder-based CV service section.

Placeholders:

- `__CV_SERVICE_REVIEWING_LIST__`
- `__CV_SERVICE_ORGANIZING_LIST__`
- `__CV_SERVICE_MENTORING_LIST__`
- `__CV_SERVICE_DEPARTMENT_LIST__`

## Important Rendering Principle

This slice should not blindly reuse the public service renderer.

The public service page is already compressed, but the CV still needs explicit
consumer policy.

For this slice, that policy is:

- reuse canonical grouping, range collapse, and ongoing rendering semantics
- keep primary links when canonical service records provide them
- keep canonical detail lines for richer entries such as PLDI chair and
  Dagstuhl
- keep the faculty-skit prose note out of the generated department list for
  now

## Format Flexibility

The CV service slice does not need to preserve the previous hand-authored Djot
line-for-line.

Visible changes are acceptable when they are explained by explicit policy, for
example:

- linked canonical service entries that were previously plain text
- canonical range collapse like `2016 - 2018`
- canonical corrections such as the previously missing `2024 FPTalks
  Co-Organizer`

## Important Consumer Boundary

This slice proves that one canonical service source can support:

- the public service wrapper at `/service/`
- a compressed CV service view
- shared range/ongoing semantics across both consumers

without adding `site/data/cv.json` and without expanding the service schema.

## Out Of Scope

- no homepage recent-service projection yet
- no homepage recent-teaching projection here
- no talks/publications/highlights projection here
- no service-schema expansion
- no attempt to generate the faculty-skit prose note

## Expected Invariants After This Slice

- the CV service subsection bodies derive from `site/data/service.json`
- the public service page and CV share one canonical service source
- the CV service renderer makes its link/detail policy explicit and reviewable
- the faculty-skit prose note remains an authored CV concern for this slice
- no duplicated literal service list blocks remain in the CV wrapper

## Verification Targets

- focused renderer/projection tests for the CV service view
- validation that required CV service placeholders are present
- validation that literal duplicated CV service records are rejected
- compare old and new rendered CV HTML with attention to the `## Service`
  section specifically:
  - only the intended service subsection bodies should change
  - the faculty-skit prose note should remain
  - surrounding CV sections should remain stable
  - differences should be explainable by explicit renderer policy or canonical
    correction
- `make test`
- `make check`

## Stop Point

Stop after the CV service projection and reassess before moving on to homepage
consumer cleanup or more curated CV domains.
