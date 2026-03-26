# Collaborators Slice 3: Research Collaborator Audit

Status: planned

It builds on:

- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)

## Goal

Review and define what should count as `Research Collaborators` before the
public collaborators page broadens beyond publication coauthors.

This is an ontology and audit slice, not an implementation or rendering slice.

## Why This Slice Next

The collaborators page has reached a clean but narrow checkpoint:

- it is now a projected coauthor page
- the about-page alphabet joke derives from that same projected coauthor set
- teaching staffing is now canonical and therefore can support a later
  `Teaching Collaborators` section

But the next broadening step is no longer straightforward.

`Research Collaborators` is not just:

- all publication coauthors, or
- all advisees, or
- all people in `people.json`

It likely includes:

- publication coauthors
- some advisees/students who worked on real research but do not yet or may
  never have a paper
- some other research collaborators who are neither publication coauthors nor
  advisees

That means the next slice must be an explicit review first.

## Current State

Current public collaborators page:

- [site/collaborators/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/collaborators/index.dj)
- thin wrapper
- one projected flat alphabetical coauthor list

Current about-page collaborator consumer:

- [site/pages/about.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/about.dj)
- prose about collaborators
- computed alphabet gaps
- punchline still clearly tied to writing papers

Current relevant canonical sources:

- publication coauthorship in `site/pubs/<slug>/publication.json`
- student/advising facts in `site/data/students.json`
- teaching collaboration facts in `site/data/teaching.json`
- person identity/aliases/URLs in `site/data/people.json`

Key current facts:

- current projected coauthor set: `131`
- current distinct teaching-collaborator set: `84`
- overlap between those sets: `18`
- current distinct student/advising set: `58`
- student names not currently in coauthors: `16`

So broadening `/collaborators/` is a real ontology change, not a small append.

## Questions To Answer

This slice should answer:

1. What should `Research Collaborators` mean?
2. Which current or likely people belong there even without publication
   coauthorship?
3. For each non-coauthor research collaborator, what is the reason they
   belong?
4. Which of those reasons are already canonical somewhere else?
5. Which residual reasons/facts would need a collaborator-specific data layer?
6. Which non-coauthor research-collaborator facts are:
   - already derivable now
   - likely future-project-derived
   - likely always residual/curated
7. Should the about-page alphabet joke remain tied to the research/coauthor
   side rather than silently broadening to all collaborators?

## Audit Inputs

The audit should review at least:

- current collaborators-page inclusions that are not justified by publication
  coauthorship alone
- student/advisee names that are not coauthors but may still be research
  collaborators
- other known research collaborators who are neither students nor coauthors

The audit should not assume that every student belongs in `Research
Collaborators`.

## Expected Output

The output of this slice should be a reviewed memo or plan update that
includes:

- a candidate `Research Collaborators` population
- reviewed buckets such as:
  - `coauthor`
  - `student-research-collaborator`
  - `other-research-collaborator`
- a short reason for every non-coauthor inclusion
- an explicit classification of whether each non-coauthor inclusion is:
  - already derivable now
  - likely future-project-derived
  - likely always residual/curated
- a recommendation about what residual facts need stable storage in a later
  `site/data/collaborators.json`

## Invariant

After this slice:

- the repo has an explicit reviewed understanding of what `Research
  Collaborators` means
- the later collaborators page expansion can be planned against reviewed
  semantics instead of intuition
- the repo has an explicit view of which current collaborator facts are likely
  to move into a future structured-data `projects` domain
- no public rendering change is required yet
- no collaborator-specific data file is required yet

## Scope

In scope:

- analyze current collaborator, student, and teaching sets
- review likely non-coauthor research collaborators one by one
- record the reason categories for inclusion
- decide whether the about-page alphabet joke should stay research/coauthor
  focused for now
- identify whether a future collaborator-specific shared-data layer is needed
- identify which current residual collaborator facts may later be absorbed by
  a future projects domain

Out of scope:

- changing the public collaborators page
- adding a `Teaching Collaborators` section yet
- introducing `site/data/collaborators.json` yet
- changing the about-page prose or alphabet values yet
- implementing per-collaborator overlays or popups
- introducing a new structured-data `projects` domain

## Future Direction

This slice should keep one longer-term direction in mind:

- a later collaborators campaign may want a per-collaborator view that can
  show publications, teaching relationships, advising, projects, and maybe
  grants in one place

That likely points toward:

- person-keyed collaborator aggregation logic
- later residual collaborator-specific data only where existing canonical
  domains are insufficient
- a future `projects` structured-data campaign for research work that is not
  adequately captured by publications alone

That future projects campaign may later absorb some research-collaborator
facts that are residual today.
So this audit should help discover projects requirements, not harden all
research-collaborator facts permanently into collaborator-specific data.

But none of that should be implemented in this audit slice.

## Stop Point

Stop after the audit and reassess.

The next decision should be between:

- introducing a minimal collaborator-specific data layer for residual research
  collaborator facts
- planning the sectioned public collaborators page
- revisiting the about-page collaborator alphabet wording/policy

not jumping straight into page rendering while the research-collaborator
ontology is still implicit.
