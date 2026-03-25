# Students Campaign

This note captures the students structured-content campaign that followed talks
and publications and is now at a good public-page checkpoint.

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

Students was the strongest next major campaign at the time because:

- it is the clearest remaining cross-page duplication domain in the repo
- it naturally builds on `site/data/people.json`
- it should reduce repeated factual maintenance in both the public students
  page and the CV
- unlike publications, it is fundamentally a shared-data domain rather than a
  collection-root route problem

Collaborators remains attractive as a later or smaller side campaign, but
students has the bigger payoff because it directly reduces duplication across
multiple important pages.

## Current Audit

Current relevant sources:

- `site/students/index.dj`
  The current public students/advising wrapper at `/students/`.
- `site/cv/index.dj`
  A second hand-maintained representation of much of the same student data.
- `site/data/people.json`
  The current shared people registry that student records will likely need to
  integrate with.

Current observed facts from the pre-projection audit:

- the former `site/pages/students.dj` wrapper was `339` lines and had `69` top-level advising
  entries across 6 sections
- `site/cv/index.dj` is `1014` lines and repeats most of the same student
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
  - one current entry present on the students page but omitted from the CV
    (`Ian Briggs`)

### Important Structural Observation

This domain is not "one person, one row."

Several people appear multiple times across sections as their relationship to
the lab evolved, for example:

- current PhD student after earlier BS or MS entry
- BS then MS entry
- MS then PhD entry

So the canonical model should likely represent advising records or milestones,
not unique people records.

People identity still matters, but it should be carried by a required
`person_key` into the people registry rather than by forcing a one-record-per-
person model.

### Important Registry Observation

People-registry coverage is stronger than it first appears.

The current students-page names are already almost completely resolvable
through `site/data/people.json` by canonical name or alias, and the remaining
display mismatch is a display-name variant rather than a missing identity.

That means this campaign can likely afford a stronger first-slice invariant:

- every canonical student/advising record should carry a required `person_key`
  pointing at `site/data/people.json`
- record-local `name` should stay as the rendered display name so page-specific
  variants like `Zhiyuan (Kevin) Yan` remain possible

This is cleaner than treating people-registry integration as optional forever.

## Current Status

Slices 1 and 2 are now implemented:

- canonical advising records live in `site/data/students.json`
- `person_key` is required and resolves through `site/data/people.json`
- thesis links, co-advisors, alumni outcomes, and free-form notes are
  preserved in ordered typed detail lists
- source validation now treats the canonical students data file as required
  when the public students wrapper exists
- the public wrapper now lives at `site/students/index.dj`
- the canonical students landing page is now `/students/`
- repeated students-page section bodies are projected from
  `site/data/students.json` while the quote, intro, FACET note, and section
  headings remain hand-authored
- the CV wrapper now already lives at `site/cv/index.dj` with canonical
  `/cv/`, but its students sections are still hand-maintained

The next students work should build on that canonical record model rather than
reopening the schema without a strong reason.

The next important design work is no longer the public-wrapper decision.
One likely follow-on is CV reuse:

- keep the CV wrapper at `site/cv/index.dj` with canonical `/cv/`
- define the condensed CV projection policy explicitly
- decide whether the Ian Briggs omission is intentional or drift
- decide whether the CV visiting-section heading should stay
  `Visiting Summer Students` or align more closely with the broader public
  `Visiting Students and Interns`
- project the duplicated advising sections in the CV wrapper from
  `site/data/students.json`

## Desired End State

The intended long-term shape is:

- one canonical shared-data file for advising records, likely
  `site/data/students.json`
- `site/students/index.dj` becomes the public wrapper around projected section
  blocks
- canonical students route becomes `/students/`
- the duplicated students sections in the CV wrapper project from the same
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

The first schema should also preserve the current section ordering directly
rather than trying to infer it from many individual fields.

At a high level, the likely top-level shape is:

- ordered `sections`
- each section has:
  - stable `key`
  - canonical students-page `title`
  - ordered `records`

Each record will likely need:

- stable `key`
- required `person_key`
- rendered display `name`
- display `label`
  for values like `PhD Student`, `PhD 2025`, or `BS, Summer 2022 @ Amazon`
- ordered typed `details`

The first schema should avoid over-modeling.
For example, it is probably better to keep a small display-oriented `label`
than to invent a complicated ontology for every status/program variation
immediately.

The first schema should also avoid premature date normalization.

Why:

- current students do not expose start dates on the page
- graduated sections already have a stable manually curated order
- ties within the same year are common
- file order gives explicit control without forcing date backfill or tie-break
  policy before it has earned its keep

So the first slice should treat file order as canonical ordering.
If a later slice clearly benefits from derived ordering by start date or
graduation date, we can add those facts deliberately then.

The ordered `details` list is likely cleaner than many special-case fields
because order matters and different records mix:

- thesis entries
- co-advisor lines
- placement/outcome lines
- free-form notes

So the first detail kinds should likely be:

- `thesis`
- `coadvisor`
- `outcome`
- `note`

with a small kind-specific payload for each.

### Likely Page-Specific Projection Policy

The two main consumers are not identical.

The likely clean policy is:

- `students.dj`
  richer projection with links, co-advisors, thesis URLs, and full outcome
  notes
- `cv`
  condensed projection with fewer details and explicit omission rules where the
  current CV intentionally differs

That means the campaign should not pretend one renderer fits every consumer.
It should aim for one canonical data source with small, explicit per-view
renderers.

The current evidence suggests those differences are mostly about rendering
richness, not about fundamentally different record sets.
So the default assumption should be:

- the same canonical advising records feed both pages
- the CV renderer is more compressed
- true inclusion mismatches should be treated as exceptional and justified
  explicitly, not assumed as a normal part of the model

The current CV suggests a few concrete compression rules to start from:

- render plain `Name, Label` lines by default rather than the richer public
  linked-name style
- render thesis details as plain text rather than thesis-title links
- render alumni outcomes as plain bullets
- omit co-advisor detail lines unless the current CV clearly demonstrates that
  they belong in the compressed view

One current wrinkle needs to stay explicit in the slice plan:

- the CV subsection heading is still `Visiting Summer Students`
- the canonical students section is now `Visiting Students and Interns`
- `Ian Briggs` exists canonically in `site/data/students.json` but is omitted
  from the current CV

So the CV slice should treat the visiting-section heading and the Ian Briggs
decision as one coupled policy question rather than pretending they are
independent.

## Boundary Of The Campaign

This campaign should include:

- canonical advising records for the current students page sections
- explicit integration policy with `site/data/people.json`
- projection into the public students wrapper, likely `site/students/index.dj`
- later projection into the duplicated students sections in `site/cv/index.dj`

This campaign should not initially include:

- a full CV rewrite outside the students section
- collaborator derivation
- publication-derived advising facts
- faculty/service/funding modeling
- per-student detail pages

Important future follow-ons that should stay explicit but out of the current
slice sequence:

- optional advising-date fields if later ordering/timeline views clearly earn
  them
- optional student-to-publication linkage for papers coauthored with a given
  student
- continued enrichment of thesis URLs and alumni outcomes as canonical records
  evolve

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

Implemented in:

- `site/data/students.json`
- `scripts/student_record.py`
- `tests/test_student_record.py`
- `scripts/sitebuild/source_validate.py`

Key invariant after this slice:

- every advising entry currently maintained on the students page can be
  represented canonically in `site/data/students.json`

### Slice 2: Students Index Wrapper And Projection

Implemented.

What landed:

- public wrapper moved to `site/students/index.dj`
- canonical public URL became `/students/`
- repeated students-page section bodies now project from
  `site/data/students.json`
- the quote, intro, FACET note, and section headings remain hand-authored

Key invariant after this slice:

- the richer public students page is no longer a second source of truth for
  advising facts and has a clean canonical route/wrapper shape

### Slice 3: CV Students Projection

Goal:

- replace the duplicated students sections in `site/cv/index.dj` with a
  condensed projection from the same canonical records

This slice should make omission and condensation rules explicit rather than
smuggling them through manual edits.

Key invariant after this slice:

- the main duplicated advising facts in `/students/` and `site/cv/index.dj`
  now come from one canonical source
- any remaining intentional divergence in the CV students section is explicit
  renderer policy, not silent drift

### Later Follow-On Work

Possible later work:

- improve people-registry coverage for student names
- add richer temporal facts such as start dates or graduation dates if later
  ordering, timeline, or alumni-history views clearly earn them
- enrich alumni outcomes over time with more structured placement/history data
- decide whether collaborators can partly derive from publications plus people
- decide whether selected publication relationships by student should become a
  later derived view
- reuse canonical student records in selected highlights or other pages if that
  clearly earns its keep

## Current Recommendation

The next students slice should be:

- CV projection from `site/data/students.json`
- explicit condensed-renderer policy for CV sections
- deliberate resolution of the Ian Briggs mismatch
