# Teaching Campaign

Status: public-page core implemented; not the active major campaign; later homepage/CV cleanup deferred

## Goal

Establish a small canonical teaching data source that removes repeated
course/offering facts across the public teaching page, the homepage, and the
CV while keeping framing and page-local prose hand-authored.

## Why Teaching Was The Right Next Campaign

Teaching was the strongest next major shared-data domain because:

- the facts are already duplicated across three consumers:
  - `site/pages/teaching.dj`
  - `site/cv/index.dj`
  - `site/pages/index.dj`
- the data shape is regular enough to model cleanly
- the domain is more cross-page than collaborators or funding today
- it fits the same shared-data-first pattern that worked well for students

## Historical Pre-Slice-2 Surface Audit

### Public Teaching Page

The pre-projection public teaching page at `site/pages/teaching.dj`
contained:

- 4 recurring UW instructor course families
- 25 linked UW instructor offerings across those courses
- 3 special-topics instructor course records
- 1 summer-school course record
- 1 hand-authored teaching-award note
- 1 hand-authored Related section

Important pre-slice-2 characteristics:

- the page is mostly structured repeated content
- each recurring course has a stable code, title, audience label, description,
  and ordered offerings
- the special-topics entries add a small amount of per-record note text
- the summer-school entry has one event plus supplemental materials/video links
- the page is not a complete teaching ledger today; for example, the
  Marktoberdorf Summer School appearance in August 2024 is referenced elsewhere
  on the site but is not yet captured on the public teaching page

### CV Teaching Section

`site/cv/index.dj` currently duplicates:

- the 4 recurring UW instructor course families
- the 3 special-topics instructor course records
- the 1 summer-school course record
- 3 teaching-assistant course families not shown on the public teaching page

Important current characteristics:

- this view is intentionally more compressed than the public teaching page
- it omits most offering links
- it keeps the same course ordering and nearly the same wording
- it introduces the additional Teaching Assistant subsection

### Homepage Recent Teaching

`site/pages/index.dj` currently contains:

- 7 recent teaching bullets
- each bullet is one flattened instructor offering with a direct link

Important current characteristics:

- this is a projection-style consumer, not a prose-first page
- it currently draws only from recent instructor offerings
- it should eventually derive from the same canonical teaching records

### Important Audit Constraint

The current teaching page is not the only place with teaching-related facts.

At least one teaching item appeared elsewhere but not on
the old `site/pages/teaching.dj` page:

- Marktoberdorf Summer School, August 2024

That means slice 1 should treat the canonical model as a chance to capture the
current intended teaching record more faithfully, not just mechanically mirror
the current public teaching page.

## Design Recommendation

Teaching should follow the students pattern more than the talks/publications
pattern:

- canonical truth in shared data under `site/data/`
- a thin public wrapper for the teaching page
- separate renderers for the public page, homepage, and CV

Recommended target shape:

- canonical data: `site/data/teaching.json`
- public wrapper: `site/teaching/index.dj`
- canonical public route: `/teaching/`

This is intentionally not a bundle-root campaign.
Teaching records do not currently need per-record local prose, assets, or
detail routes.

## Smallest Useful Canonical Model

The smallest model that appears to cover the current surfaces is:

- top-level ordered `groups`
- each group owns ordered `records`
- each record is one teaching family or one summer-school teaching item

Recommended initial groups:

- `uw_courses`
- `special_topics`
- `summer_school`
- `teaching_assistant`

Important naming note:

- the current `teaching_assistant` group records courses where Zach served as
  the teaching assistant earlier in his own career
- it does **not** mean "people who served as TAs in courses Zach later taught"
- future course-staffing data for instructor-led offerings should be modeled
  separately rather than overloading this group

Recommended initial record kinds:

- `course`
- `summer_school`

Recommended `course` fields:

- `key`
- `kind`
- `code`
- `title`
- optional `institution`
- optional `audience_label`
- optional `description_djot`
- ordered `offerings`
- optional ordered `details`

Recommended `offering` fields:

- `year`
- `term`
- optional `url`

Likely later offering-level extensions, if and when they earn their keep:

- ordered `co_instructors`
- ordered `teaching_assistants`

Those future staffing fields should likely live on individual offerings, not
on whole course records, because co-teaching and TA staffing can vary by term.

Recommended `summer_school` fields:

- `key`
- `kind`
- `title`
- ordered `events`

Recommended `event` fields:

- `label`
- `url`
- optional ordered `links`

Recommended `details` and `links` items:

- small Djot strings or `{label, url}` pairs
- enough to preserve current notes like "Co-taught with [Xi Wang][] and
  [Bryan Parno][]" without inventing a larger ontology yet

The implemented slice-1 model is slightly more permissive than this initial
draft:

- `course` records still require `code`, `title`, and ordered `offerings`
- `institution`, `audience_label`, and `description_djot` are optional
- every `course` record must include at least one of `description_djot` or
  ordered `details`

That keeps the model honest for special-topics and teaching-assistant records
without forcing empty filler fields.

## Ordering Recommendation

Keep canonical order explicit in the file:

- group order is canonical
- record order within a group is canonical
- offering order within a record is canonical

Later consumers may derive additional orderings where clearly justified.
For example, the homepage recent-teaching slice should likely sort flattened
offerings by:

1. `year` descending
2. academic term order within a year

But that should be a renderer concern, not a reason to complicate slice 1.

## What Should Stay Hand-Authored

The campaign should not try to move everything into JSON.

The following should stay in wrappers unless a later slice clearly proves
otherwise:

- the teaching-page heading and framing
- the teaching-award note
- the Related section on the public teaching page
- any future editorial commentary about pedagogy or course design

## Recommended Slice Order

### Slice 1. Canonical Teaching Record Model

- add `site/data/teaching.json`
- add loader/validator tests
- backfill canonical records for the current teaching/CV/homepage content
- stop before any page projection

Implemented in:

- `site/data/teaching.json`
- `scripts/teaching_record.py`
- `tests/test_teaching_record.py`
- `scripts/sitebuild/source_validate.py`

Implemented outcomes so far:

- canonical teaching records now live in `site/data/teaching.json`
- source validation now requires the teaching registry when the teaching page
  exists
- focused teaching-model tests cover duplicate keys, required groups, course
  invariants, and summer-school invariants
- the canonical record now includes Marktoberdorf Summer School 2024 even
  though the old pre-projection public teaching page did not

### Slice 2. Public Teaching Wrapper / Route Cutover

- move the public wrapper to `site/teaching/index.dj`
- canonicalize `/teaching/`
- project the repeated teaching blocks from `site/data/teaching.json`
- keep the award note and Related section hand-authored

Implemented in:

- [teaching-slice-2-index-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-slice-2-index-projection.md)

Implemented outcomes so far:

- the public teaching wrapper now lives at `site/teaching/index.dj`
- the canonical public teaching URL is now `/teaching/`
- the repeated UW course, special-topics, and summer-school blocks now project
  from `site/data/teaching.json`
- authored internal links now use `teaching/` instead of `teaching.html`
- the public teaching page now includes the canonical Marktoberdorf Summer
  School 2024 entry

### Slice 3. Homepage Recent Teaching Projection

- derive the recent-teaching bullets on `site/pages/index.dj`
- update authored links to use canonical `/teaching/`

### Slice 4. CV Teaching Projection

- project the duplicated Teaching section in `site/cv/index.dj`
- preserve the intentionally more compressed CV view
- treat the public page and CV as separate renderers over the same records

## Deferred Questions

These are real possibilities, but they should not shape the first slice:

- richer teaching metadata such as offering-level `co_instructors`
- later teaching-staffing data for instructor-led offerings, including
  offering-level `teaching_assistants` tied into `site/data/people.json`
- additional date/detail normalization beyond `year` plus academic `term`
- course-local extra pages or assets
- broader teaching-adjacent domains such as course recipes or mentoring notes
