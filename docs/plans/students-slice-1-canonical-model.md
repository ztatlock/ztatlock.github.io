# Students Slice 1: Canonical Advising Record Model

This note defines and records the exact scope of the first students slice.

This slice is now implemented.
It remains useful as the durable statement of the canonical advising-record
model that later students slices should build on.

It builds on:

- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Purpose

Establish one canonical data model for advising records under
`site/data/students.json` without changing any rendered pages yet.

This slice should answer three questions cleanly:

1. What is the unit of truth?
2. How does it integrate with `site/data/people.json`?
3. What is the smallest schema that can later drive both `students.dj` and the
   students section of `cv.dj`?

## Implemented Data Shape

The canonical file now looks like this in shape:

```json
{
  "sections": [
    {
      "key": "current_students",
      "title": "Current Students",
      "records": [
        {
          "key": "amy-zhu-phd-current",
          "person_key": "amy-zhu",
          "name": "Amy Zhu",
          "label": "PhD Student",
          "details": [
            {
              "kind": "coadvisor",
              "person_keys": ["adriana-schulz"]
            }
          ]
        }
      ]
    },
    {
      "key": "visiting_students",
      "title": "Visiting Summer Students, Internships Mentored in Industry",
      "cv_title": "Visiting Summer Students",
      "records": [
        {
          "key": "ian-briggs-summer-2022",
          "person_key": "ian-briggs",
          "name": "Ian Briggs",
          "label": "PhD, Summer 2022 @ Amazon",
          "details": [
            {
              "kind": "note",
              "djot": "Developed [Haploid](https://github.com/IanBriggs/haploid) for EqSat-driven SMT query simplification."
            }
          ]
        }
      ]
    }
  ]
}
```

## Why This Shape

This shape is intentionally simple.

Why sections are top-level and ordered:

- the current students page is already organized around six stable sections
- the CV mirrors almost the same grouping
- order is canonical and should not be inferred indirectly
- the one known section-title divergence (`Visiting Summer Students...` vs
  `Visiting Summer Students`) belongs naturally in section metadata

Why records are nested inside sections:

- each advising record belongs to exactly one current section
- future projection should preserve section-local order directly
- this avoids adding a separate ranking field before it is needed

Why records model milestones rather than unique people:

- the same person can appear in multiple sections over time
- a one-record-per-person model would distort the actual content and force
  awkward historical substructures immediately

Why `person_key` should be required:

- the current students page already aligns closely with the people registry
- person identity is important for links and future reuse
- keeping the rendered `name` separate still allows display variants

Why file order should be canonical in slice 1:

- current graduated-section ordering is already curated and mostly
  reverse-chronological
- current-students ordering is not obviously derivable from a real date field
- date-based ordering would require additional fields and tie-break policy that
  the first slice does not otherwise need
- preserving current order is the lowest-risk way to establish one source of
  truth before any renderer cutover

Why details should be an ordered typed list:

- current entries mix thesis lines, co-advisor lines, placement lines, and
  free-form notes
- order matters within an entry
- later renderers can include or omit detail kinds per consumer without losing
  canonical fact order

## Exact Slice-1 Schema

### Top Level

- `sections`
  Required ordered array of section objects.

### Section Object

Required fields:

- `key`
  Stable machine-readable identifier.
- `title`
  Canonical students-page section title.
- `records`
  Ordered array of advising record objects.

Optional fields:

- `cv_title`
  Only needed when the CV heading intentionally differs.

### Advising Record Object

Required fields:

- `key`
  Stable unique identifier for this specific advising record.
- `person_key`
  Key into `site/data/people.json`.
- `name`
  Rendered display name for this record.
- `label`
  Rendered status/date label, for example:
  - `PhD Student`
  - `Postdoc 2023`
  - `BS 2024`
  - `BS, Summer 2022 @ Amazon`

Optional fields:

- `details`
  Ordered array of detail objects.

### Detail Object

Every detail object must have a required `kind`.

Allowed kinds for slice 1:

- `thesis`
  Required fields:
  - `title`
  - `url`
- `coadvisor`
  Required fields:
  - `person_keys`
    ordered non-empty array of people-registry keys
- `outcome`
  Required fields:
  - `djot`
- `note`
  Required fields:
  - `djot`

The `djot` field should hold the exact inline/renderable text fragment for
that detail line.
That keeps the model simple while preserving the current authored wording.

## Implemented First-Slice Invariants

The first slice should enforce:

1. `site/data/students.json` exists and is valid JSON.
2. `sections` are in canonical display order.
3. section `key` values are unique.
4. every advising record belongs to exactly one section.
5. record `key` values are globally unique.
6. every record has a required `person_key` that resolves in
   `site/data/people.json`.
7. detail objects use only the allowed kinds.
8. kind-specific required fields are present.
9. canonical order is the order in the file:
    - section order at the top level
    - record order within each section
    - detail order within each record
10. the current model assumes the same canonical record set will later drive
    both `students.dj` and the CV students section unless a later review
    establishes a justified exception

## What This Slice Did Not Do

This slice should not:

- project `students.dj`
- project `cv.dj`
- change rendered site output
- redesign the people registry
- invent per-student detail pages
- over-normalize placements, companies, or degree programs

## Tests Added

The implemented slice includes focused tests for:

- loading a valid `students.json`
- duplicate section keys
- duplicate record keys across sections
- missing `person_key`
- unresolved `person_key`
- unsupported detail kinds
- missing required thesis/coadvisor/outcome/note fields
- preserving canonical order from the file
- accepting display names that differ from the people-registry canonical name
  when `person_key` is correct
- preserving the full current students-page record set without introducing a
  CV-only filtering field in slice 1

## Stop Point

Stop after this slice and reassess before any projection work.

Questions to answer at that checkpoint:

1. Does the advising-record model feel natural in actual data entry?
2. Is the required `person_key` invariant helping more than it hurts?
3. Does the ordered detail-list model feel clean, or does it want one small
   refinement before projection?
4. Are the current students-page and CV differences still small enough that one
   canonical source with two renderers feels clearly right?
5. Is there any justified reason to introduce record-level CV filtering later,
   or should the canonical record set remain identical across both pages?
