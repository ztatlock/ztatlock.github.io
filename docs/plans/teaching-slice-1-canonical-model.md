# Teaching Slice 1: Canonical Model

Status: planned

## Goal

Establish a canonical teaching data source in `site/data/teaching.json`
without changing any public page rendering yet.

This slice should make it possible to represent the current teaching, CV, and
homepage teaching facts in one place before any wrapper/route/projection
changes happen.

## Scope

In scope:

- `site/data/teaching.json`
- loader and validator code
- focused unit tests
- backfilled canonical records for current teaching data

Out of scope:

- moving `site/pages/teaching.dj`
- canonicalizing `/teaching/`
- homepage projection
- CV projection

## Current Audit Facts

The current teaching content breaks down into:

- 4 recurring UW instructor course families
- 25 linked UW instructor offerings across those course families
- 3 special-topics instructor course records
- 1 summer-school course record
- 3 teaching-assistant course families
- 11 teaching-assistant offerings
- 7 recent-teaching bullets on the homepage

The important current view differences are:

- the public teaching page is the richest public-facing view
- the CV is a compressed but overlapping view
- the homepage is a flattened recent-offering view

One important incompleteness is already known:

- Marktoberdorf Summer School, August 2024 appears elsewhere on the site but
  is not yet captured on the public teaching page

So the slice-1 backfill should capture the intended current teaching record,
not merely mirror the current public page line-for-line.

## Recommended Schema

Use a shared-data shape intentionally similar to `site/data/students.json`:

- top-level ordered `groups`
- each group has:
  - `key`
  - ordered `records`

Recommended slice-1 groups:

- `uw_courses`
- `special_topics`
- `summer_school`
- `teaching_assistant`

Each `record` should have:

- `key`
- `kind`
- `title`

Additional required fields by `kind`:

### `course`

- `code`
- `institution`
- `audience_label`
- `description_djot`
- ordered `offerings`

Optional fields:

- ordered `details`

Each `offering` should have:

- `year`
- `term`
- optional `url`

### `summer_school`

- ordered `events`

Each `event` should have:

- `label`
- `url`

Optional fields:

- ordered `links`

Each `links` item should have:

- `label`
- `url`

## Invariants

After slice 1:

- every repeated teaching fact should be representable in
  `site/data/teaching.json`
- group order should be canonical
- record order within a group should be canonical
- offering/event order within a record should be canonical
- current public/cv/homepage pages should remain unchanged
- no projection or route decisions should be forced yet

## Design Notes

Important design choices for slice 1:

- preserve descriptive course text as `description_djot` instead of breaking it
  into micro-fields
- preserve small per-record notes as ordered Djot strings in `details`
- do not add broader pedagogy or staffing taxonomy yet
- do not add exact calendar dates; `year` plus academic `term` is enough for
  the current surfaces

This slice should remain intentionally small.
Its job is to make the later wrapper and projection slices simple and
reviewable.
