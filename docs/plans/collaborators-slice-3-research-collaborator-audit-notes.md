# Collaborators Slice 3 Audit Notes

Status: in progress

It builds on:

- [collaborators-slice-3-research-collaborator-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-slice-3-research-collaborator-audit.md)
- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)

## Current Derived Baseline

Current canonical sets:

- projected publication-coauthor set: `131`
- canonical teaching-collaborator set: `84`
- teaching/coauthor overlap: `18`
- canonical student/advising set: `58`
- student names not currently in the projected coauthor set: `16`

Important observation:

- the old hand-authored collaborators page at `ce7412e^:site/pages/collaborators.dj`
  did not contain any non-self names outside the union of current coauthors
  and students
- the only old-manual name removed relative to the current coauthor projection
  was `Zachary Tatlock`

So the research-collaborator audit is not cleaning up a hidden old
non-coauthor list.
It is deciding what should be added beyond coauthors.

## Student Review Set

These are the current student/advising names that are not justified by
publication coauthorship alone and therefore need explicit review if
`Research Collaborators` broadens beyond coauthors.

### Current Students

- Haobin Ni
- Kevin Mu
- Noah Huck

### Graduated Bachelors Students

- Alex Fischman
- Kirsten Graham
- Zhiyuan (Kevin) Yan
- Jifan Zhang
- Paul Curry
- Melissa Hovik
- Justin Adsuara
- Miranda Edwards
- Luke Nelson
- Keith Simmons
- Seth Pendergrass

### Visiting Students and Interns

- Ian Briggs
- Juliet Oh

## Current Policy Pressure

This review set is already enough to show why a future structured-data
`projects` domain probably matters.

Some of these people are likely to become publication coauthors soon.
Others may have done real research collaboration that never maps cleanly to a
paper.

That means the audit should classify each non-coauthor research collaborator
as one of:

- already derivable now
- likely future-project-derived
- likely always residual/curated

The collaborator-specific layer, if added later, should only hold the minimal
residual facts that cannot yet be derived from publications, students, or a
future projects domain.

## Other Research Collaborators

This section is intentionally left for explicit reviewed additions that are:

- not publication coauthors, and
- not current student/advising records

Those names will need a short reviewed reason for inclusion and the same
`derivable now` / `future-project-derived` / `residual` classification.

## About-Page Alphabet Note

Current coauthor-only gaps:

- first initials: `F, Q, U`
- last initials: `I, U, V, X, Y`

If the research-collaborator set were broadened today by simply unioning in
all current students/advising names, the gaps would become:

- first initials: `F, Q, U`
- last initials: `I, U, V, X`

That reinforces the current policy recommendation:

- keep the about-page joke tied to the coauthor/research-publication side
  until the broadened collaborators ontology is reviewed explicitly

## Stop Point

The next step in this slice is person-by-person review of:

- the `16` student-only names above
- any additional non-student, non-coauthor research collaborators that should
  belong in `Research Collaborators`

Do not plan page rendering or a collaborator registry until that review is
explicit.
