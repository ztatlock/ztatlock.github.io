# Collaborators Slice 4: Sectioned Public Page

Status: implemented

It builds on:

- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [collaborators-slice-3-research-collaborator-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-slice-3-research-collaborator-audit.md)
- [collaborators-slice-3-research-collaborator-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-slice-3-research-collaborator-audit-notes.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)

## Goal

Broaden `/collaborators/` from a flat projected coauthor list into a sectioned
public page with:

- `Research Collaborators`
- `Teaching Collaborators`

using only existing canonical sources.

This slice should not introduce a collaborator-specific shared-data layer.

## Why This Slice Next

The collaborator audit is now complete enough for the next public step:

- no hidden historical non-coauthor collaborator set was lost during
  projection
- the near-term research-collaborator expansion can proceed from existing
  canonical domains
- teaching collaboration is now canonical in `site/data/teaching.json`

So the next collaborators move should be the public sectioned page, not a
temporary `site/data/collaborators.json`.

## Current Behavior

Today [site/collaborators/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/collaborators/index.dj)
is a thin wrapper with:

- hand-authored title
- hand-authored intro
- one flat placeholder, `__COLLABORATORS_LIST__`
- a surrounding `{.columns .columns-12rem}` block

That flat list is rendered by
[scripts/collaborators_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/collaborators_index.py)
from publication coauthors plus `people.json`.

So the page is still really a coauthor page.

## Proposed Behavior

After this slice, the collaborators page should render two projected sections:

- `## Research Collaborators`
- `## Teaching Collaborators`

The wrapper should keep:

- the page title
- the intro text
- the section headings:
  - `## Research Collaborators`
  - `## Teaching Collaborators`

The projected body should only own:

- the research-collaborator list
- the teaching-collaborator list

That means the current single columns wrapper around `__COLLABORATORS_LIST__`
should be replaced by two authored section blocks, each with its own list
placeholder.

## Canonical Sources

### Research Collaborators

Near-term policy:

- publication coauthors
- plus the current canonical student/advising set from
  `site/data/students.json`

No collaborator-specific data file is needed for this slice.

This is intentionally a near-term policy, not a claim that future research
collaborators will always be derivable only from publications plus students.
A later `projects` domain may eventually supply richer research-collaboration
truth.

### Teaching Collaborators

Derive from canonical offering-level staffing in `site/data/teaching.json`:

- `co_instructors`
- `teaching_assistants`
- `tutors`

Publicly, this section stays flat.
It should not subdivide into role-specific subsections in this slice.

## Section Policies

### Research Section

- unique people only
- dedupe by `person_key` when available
- display with default `people.json` `name`
- link when `primary_url` exists
- plain text when no public link exists
- sort alphabetically by displayed label
- exclude `Zachary Tatlock`

### Teaching Section

- unique people only
- dedupe by `person_key`
- display with default `people.json` `name`
- link when `primary_url` exists
- plain text when no public link exists
- sort alphabetically by displayed label
- exclude `Zachary Tatlock` if ever present indirectly

### Overlap Policy

Overlap across sections is allowed.

If someone is both:

- a research collaborator, and
- a teaching collaborator

they should appear in both sections.

This page is surfacing relationship types, not forcing one global partition.

## About-Page Policy

This slice should not broaden the about-page alphabet joke.

The current about-page prose in
[site/pages/about.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/about.dj)
still clearly points at the coauthor/research-publication side:

- it links to `/collaborators/`
- it says `let's write a paper together!`

So this slice should keep the current alphabet computation unchanged.
Any wording or scope adjustment to the about-page joke should be a separate
later decision.

## Wrapper / Placeholder Shape

I recommend changing the collaborators wrapper from:

- one flat list placeholder inside one columns block

to:

- two authored section headings
- two authored columns blocks
- two explicit list placeholders

Suggested new placeholders:

- `__RESEARCH_COLLABORATORS_LIST__`
- `__TEACHING_COLLABORATORS_LIST__`

Why:

- the section names are editorial framing and should stay authored
- the old `__COLLABORATORS_LIST__` name suggests one flat list and fights the
  new structure
- two explicit placeholders keep the wrapper readable and make future small
  authored notes under each section easy to add
- route validation can stay simple and explicit

Expected wrapper shape:

- page title
- authored intro
- `## Research Collaborators`
- authored columns block
- `__RESEARCH_COLLABORATORS_LIST__`
- `## Teaching Collaborators`
- authored columns block
- `__TEACHING_COLLABORATORS_LIST__`

## Implementation Shape

Likely code changes:

- [site/collaborators/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/collaborators/index.dj)
  Replace the old single columns block and list placeholder with authored
  research/teaching section headings and the two new list placeholders.
  Update front-matter `description` and `share_description` so they no longer
  describe the page as coauthors-only.
- [scripts/collaborators_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/collaborators_index.py)
  Split the current flat coauthor helper into explicit loaders/renderers for:
  - research collaborators
  - teaching collaborators
  - each public collaborators list
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
  Swap route projection from the old single list placeholder to the two new
  section-list placeholders.
- [scripts/sitebuild/source_validate.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/source_validate.py)
  Update wrapper validation to require the two new placeholders and reject
  copied literal collaborator entry blocks under either section.

Likely test updates:

- [tests/test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)
- [tests/test_source_validate.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_source_validate.py)
- [tests/test_page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_renderer.py)
- likely new focused collaborator-render tests if the current
  `scripts/collaborators_index.py` tests are too flat for sectioned behavior

## Expected Visible Change

This slice should visibly change only `/collaborators/`.

Expected change:

- the page stops being one flat coauthor list
- the page becomes two sections:
  - `Research Collaborators`
  - `Teaching Collaborators`

Expected non-change:

- no about-page visible change
- no collaborator overlay/pop-up work
- no homepage/CV change

## Verification

- focused tests for research-section derivation from publications plus
  students
- focused tests for teaching-section derivation from teaching staffing
- focused tests for overlap behavior across sections
- focused tests for linkless people rendering as plain text
- wrapper-validation tests for the two new placeholders
- `make verify`
- explicit rendered diff review focused on `/collaborators/`
- confirm:
  - the page title and intro remain authored
  - the section headings remain authored
  - only `/collaborators/` changes
  - the about-page alphabet section remains unchanged

## Out Of Scope

- no `site/data/collaborators.json`
- no per-collaborator overlays or popups
- no role-specific teaching subsections
- no projects domain
- no about-page wording changes
- no collaborator/project/grant cross-linking

## Stop Point

Stop after the sectioned public page lands.

The next decision should be between:

- later about-page collaborator wording/policy cleanup
- later collaborator-specific residual data only if a real case appears
- later richer collaborator enrichment, likely after a future projects domain

not broadening into a larger collaborator framework by inertia.
