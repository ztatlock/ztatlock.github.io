# Students Campaign

This note captures the next major structured-content campaign after talks and
publications.

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)

## Goal

Create one canonical source of truth for advising-related student records, then
project that truth into both the richer students page and the duplicated
student sections in the CV.

The goal is not to create personal mini-websites for individual students.
The goal is to remove repeated advising facts from multiple pages while keeping
page-specific framing and emphasis hand-authored.

## Why Students Next

Students is now the strongest next major campaign because:

- it is the clearest remaining cross-page duplication domain in the repo
- it naturally builds on `site/data/people.json`
- it should reduce repeated factual maintenance in both `students.dj` and
  `cv.dj`
- unlike publications, it is fundamentally a shared-data domain rather than a
  collection-root route problem

Collaborators remains attractive as a later or smaller side campaign, but
students has the bigger payoff because it directly reduces duplication across
multiple important pages.

## Current Audit

Current relevant sources:

- `site/pages/students.dj`
  The richer canonical-looking students/advising page.
- `site/pages/cv.dj`
  A second hand-maintained representation of much of the same student data.
- `site/data/people.json`
  The current shared people registry that student records will likely need to
  integrate with.

Current observed facts:

- `site/pages/students.dj` is `339` lines and has `69` top-level advising
  entries across 6 sections
- `site/pages/cv.dj` is `1014` lines and repeats most of the same student
  sections in compressed form
- the sections align closely:
  - current students
  - completed postdoctoral mentoring
  - graduated doctoral students
  - graduated masters students
  - graduated bachelors students
  - visiting summer students / internships
- the students page is richer than the CV:
  - thesis links
  - co-advisor lines
  - multiple outcome lines
  - a broader visiting/internship section
- the CV is intentionally more compressed:
  - plain thesis text instead of linked titles
  - fewer co-advisor details
  - at least one entry present on the students page but omitted from the CV

### Important Structural Observation

This domain is not "one person, one row."

Several people appear multiple times across sections as their relationship to
the lab evolved, for example:

- current PhD student after earlier BS or MS entry
- BS then MS entry
- MS then PhD entry

So the canonical model should likely represent advising records or milestones,
not unique people records.

People identity still matters, but it should probably be represented through an
optional link to the people registry rather than by forcing a one-record-per-
person model.

### Important Registry Observation

Many names on the current students page are not yet in `site/data/people.json`.

That means this campaign must make an explicit decision about people-registry
integration:

- require every student record to have a people-registry entry, or
- allow student records to start with plain names and optional `person_ref`,
  tightening registry coverage over time

My current recommendation is the second option for the first slices.
That keeps the students campaign moving without turning the first slice into a
large people-registry cleanup pass.

## Desired End State

The intended long-term shape is:

- one canonical shared-data file for advising records, likely
  `site/data/students.json`
- `site/pages/students.dj` becomes a wrapper around projected section blocks
- the duplicated students sections in `site/pages/cv.dj` project from the same
  canonical records with a more condensed renderer
- page-specific framing remains hand-authored
- projection differences between the students page and the CV remain explicit
  and small rather than hidden in duplicated text

## Why `site/data/students.json` Is Likely Right

Unlike talks and publications, this domain does not currently want:

- per-record local assets
- per-record prose pages
- collection-local routes

What it wants is a shared cross-page registry of advising facts.

So the likely right shape is a shared data file under `site/data/`, not a new
bundle root like `site/students/<slug>/`.

That keeps the design simple and matches the actual reuse pattern.

## Likely Canonical Schema Direction

The first schema should be deliberately small and oriented around current page
needs rather than an imagined advising CRM.

The likely unit of truth is one advising record, not one person.

At a high level, each record will likely need:

- stable `key`
- display `name`
- optional `person_ref`
- section/group, matching the current top-level page sections
- display `label`
  for values like `PhD Student`, `PhD 2025`, or `BS, Summer 2022`
- optional co-advisors
- optional thesis metadata
- optional ordered detail notes for placement or follow-on outcomes
- optional view controls where the richer students page and condensed CV need
  to differ

The first schema should avoid over-modeling.
For example, it may be better to keep a small display-oriented `label` than to
invent a complicated ontology for every status/program variation immediately.

### Likely Page-Specific Projection Policy

The two main consumers are not identical.

The likely clean policy is:

- `students.dj`
  richer projection with links, co-advisors, thesis URLs, and full outcome
  notes
- `cv.dj`
  condensed projection with fewer details and explicit omission rules where the
  current CV intentionally differs

That means the campaign should not pretend one renderer fits every consumer.
It should aim for one canonical data source with small, explicit per-view
renderers.

## Boundary Of The Campaign

This campaign should include:

- canonical advising records for the current students page sections
- explicit integration policy with `site/data/people.json`
- projection into `site/pages/students.dj`
- later projection into the duplicated students sections in `site/pages/cv.dj`

This campaign should not initially include:

- a full CV rewrite outside the students section
- collaborator derivation
- publication-derived advising facts
- faculty/service/funding modeling
- per-student detail pages

## Recommended Slice Order

### Slice 1: Canonical Advising Record Model

Goal:

- define the smallest useful `site/data/students.json` schema
- decide the people-registry integration policy
- backfill the current students-page records into canonical data
- keep both `students.dj` and `cv.dj` hand-authored for this slice

Why first:

- it establishes one canonical truth before we start projecting multiple pages
- it forces the milestone-vs-person model question to be answered explicitly
- it keeps the first slice reviewable and testable

Key invariant after this slice:

- every advising entry currently maintained on the students page can be
  represented canonically in `site/data/students.json`

### Slice 2: Students Page Projection

Goal:

- make `site/pages/students.dj` a wrapper around projected section blocks from
  `site/data/students.json`

Keep hand-authored:

- the page intro
- the Habermann quote
- the FACET note
- section framing text, if any

Key invariant after this slice:

- the richer students page is no longer a second source of truth for advising
  facts

### Slice 3: CV Students Projection

Goal:

- replace the duplicated students sections in `site/pages/cv.dj` with a
  condensed projection from the same canonical records

This slice should make omission and condensation rules explicit rather than
smuggling them through manual edits.

Key invariant after this slice:

- the main duplicated advising facts in `students.dj` and `cv.dj` now come from
  one canonical source

### Later Follow-On Work

Possible later work:

- improve people-registry coverage for student names
- decide whether collaborators can partly derive from publications plus people
- reuse canonical student records in selected highlights or other pages if that
  clearly earns its keep

## Current Recommendation

The next major structured-content campaign should be:

- students

The first students slice should be:

- schema and canonical data first
- no page projection yet
- strong tests and explicit invariants before consumer cutover
