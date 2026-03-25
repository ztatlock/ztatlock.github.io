# Teaching Staffing Campaign

Status: drafted for review

It builds on:

- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)
- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Canonicalize staffing facts for instructor-led teaching offerings without
mixing that work into public rendering or a larger people-profile system.

This campaign should:

- let `site/data/teaching.json` represent offering-level staffing facts
- let `site/data/people.json` represent real people who may or may not have a
  public link
- keep public teaching, CV, homepage, and collaborators rendering unchanged
  until later consumer slices deliberately opt in

This campaign is not the later teaching/course enrichment campaign.
It is the data-foundation campaign that should come first.

## Why This Campaign Now

Teaching staffing is now a strong next campaign because:

- the teaching campaign already anticipated later offering-level
  `co_instructors` and `teaching_assistants`
- the collaborators campaign explicitly identified teaching staffing as the
  clearest likely prerequisite for richer non-coauthor collaborator modeling
- the current `people.json` URL contract is too strict for the real-world
  teaching staffing surface we now want to represent
- this is a clean way to extend the canonical teaching record without forcing
  immediate public design decisions

## Core Design Decisions

### 1. People Registry Stays Small, But Becomes Honest About Linkability

`site/data/people.json` should remain a small identity/default-label registry,
not grow into a large profile framework.

But it should become honest about the fact that some real people are:

- linkable through a personal site
- linkable only through LinkedIn
- linkable only through GitHub
- not linkable publicly at all

Recommended rule:

- `name` remains the default site-facing canonical label
- `aliases` remain resolution-only alternate spellings
- `url`, `linkedin`, and `github` are optional public-link fields
- a small derived helper such as `primary_url(person)` chooses the best link in
  this order:
  1. `url`
  2. `linkedin`
  3. `github`

### 2. Person Existence And Djot Linkability Must Be Decoupled

The repo should stop assuming that every person record can automatically become
a generated Djot reference.

Recommended rule:

- all people may exist canonically in `people.json`
- only people with a derived `primary_url` should generate Djot refs
- structured consumers may render a person as linked text when linkable, or
  plain text when not

### 3. Authored Djot Prose Must Stay Safe

Once linkless people are allowed in `people.json`, authored source should not
silently assume that every `[Name][]` reference still has a generated people
ref behind it.

So this campaign should include an explicit guardrail:

- authored Djot should continue to use generated people refs only for linkable
  people
- linkless people should remain available to structured renderers, but should
  not silently appear as missing-link authoring failures

### 4. Teaching Staffing Belongs On Offerings

Teaching staffing should extend the existing teaching campaign shape rather
than invent a parallel registry.

Recommended first staffing fields on individual offerings:

- ordered `co_instructors`
- ordered `teaching_assistants`

These should key into `site/data/people.json`.

This remains intentionally separate from the existing `teaching_assistant`
history group, which records courses where Zach served as a TA earlier in his
own career.

### 5. Tutor Is A Real Role Decision, Not Incidental Noise

If the data exposes tutors as a distinct role, the repo should treat that as a
real later policy decision.

So this campaign should not initially:

- collapse tutors into `teaching_assistants` by convenience
- quietly drop them without recording the boundary

Instead, tutor handling should be its own later slice.

### 6. Provenance Should Not Enter Repo Truth

This campaign should only land canonical public facts and public links.

It should not encode:

- how staffing facts were gathered
- private breadcrumbs or non-public notes
- operational research workflow details

The repo should record only the landed canonical model and the facts
themselves.

## What Stays Out Of Scope

This campaign should not yet do any of the following:

- render teaching staffing on `/teaching/`
- render teaching staffing on the homepage
- render teaching staffing in the CV
- implement the later collaborator relationship-model slice
- broaden `people.json` into a generic person-profile framework
- add unrelated people metadata fields "for later"
- resolve tutor policy in the same slice as core staffing

## Recommended Slice Order

### Slice 1. People Linkability And Ref Guardrail

Goal:

- let `people.json` represent linkable and linkless people honestly without
  breaking generated Djot refs or authored prose assumptions

Invariant after slice 1:

- a person may exist canonically in `people.json` with or without a public
  link
- generated Djot people refs are emitted only for linkable people
- authored Djot prose is protected against silently depending on linkless
  people refs
- the current `name` / `aliases` semantics remain unchanged

### Slice 2. Teaching Staffing Schema Foundation

Goal:

- extend teaching offering records so staffing facts can exist canonically in
  `site/data/teaching.json`

Invariant after slice 2:

- teaching offerings may include ordered `co_instructors` and ordered
  `teaching_assistants`
- staffing values are keyed through `site/data/people.json`
- no public rendering changes yet

### Slice 3. Co-Instructor Canonicalization

Goal:

- backfill confirmed co-instructor facts into `site/data/teaching.json` and
  any needed `people.json` entries

Invariant after slice 3:

- confirmed co-instructors are canonical on the relevant offerings
- every referenced co-instructor resolves through `people.json`
- no public rendering changes yet

This slice should stay intentionally small and high-confidence.

### Slice 4. Teaching Assistant Canonicalization

Goal:

- backfill confirmed teaching-assistant facts into `site/data/teaching.json`
  and any needed `people.json` entries

Invariant after slice 4:

- confirmed TA facts are canonical on the relevant offerings
- every referenced TA resolves through `people.json`
- linkless people are allowed canonically where needed
- no public rendering changes yet

This is the larger data-import slice and should therefore stand alone.

### Slice 5. Tutor Decision

Goal:

- make tutor handling explicit once the core staffing model is landed

Possible outcomes:

- add ordered `tutors`
- explicitly keep tutors out of canonical staffing for now
- represent tutors in another narrow teaching-specific way

Invariant after slice 5:

- the repo has an explicit tutor policy rather than silently collapsing or
  dropping the role

## Verification Themes

Across the campaign, verification should focus on:

- focused loader and validator tests
- people-ref generation tests
- authored-source validation tests where linkability matters
- explicit data diffs for canonical backfills
- `make build`
- `make test`
- `make check`

No rendered HTML diff should be required until a later consumer slice actually
changes a public page.

## Campaign Stop Point

Stop after the tutor decision slice and reassess.

At that checkpoint, the repo should have:

- honest people-linkability semantics
- canonical teaching staffing facts
- a clean prerequisite for the later collaborator relationship-model slice

Only then should the next decision be whether to:

- enrich the teaching page with staffing views
- enrich collaborators with non-coauthor relationships
- or pursue another separate campaign first
