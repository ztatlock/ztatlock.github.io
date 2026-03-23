# Structured Content Roadmap

This note captures the medium-term campaign sequence for making the site easier
to extend and maintain by introducing a small number of disciplined structured
single sources of truth.

It builds on the current post-cutover architecture documented in
[site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md).

## Goal

Reduce repeated, highly structured facts across pages while keeping the site
simple to edit and understand.

The point is not to convert everything into JSON.
The point is to move repeated structured facts into small canonical records,
then project those records back into prose-first pages where that pays off.

## Principles

- keep prose near prose
- keep publication-local facts near publication bundles
- introduce shared data only when facts are reused across pages
- prefer a few small canonical records over one giant site-wide schema
- use explicit invariants and focused tests as each data domain grows
- advance in small slices that can be reviewed confidently

## Existing Single Sources Of Truth

The current architecture already has two strong canonical domains:

- `site/data/people.json`
  Canonical people names, aliases, and URLs.
- `site/pubs/<slug>/publication.json`
  Canonical publication-local records and assets.

Future campaigns should build on those instead of inventing parallel
registries.

## Campaign Sequence

### 1. Talks

This should be the first structured-content campaign.

Why first:

- the page is list-shaped and relatively small
- the data model should stay simple
- it is a good place to refine the projection pattern before tackling larger
  domains

Likely target:

- `site/talks/<slug>/talk.json`

Likely outcomes:

- a canonical set of talk-local bundles
- projection into `site/talks/index.dj`
- later reuse in selected CV or news sections if that proves valuable

Important design choice:

- keep talk-local facts with each talk bundle
- derive any global talk table from those bundles at build time
- do not start with one giant cross-site `talks.json` file

The detailed planning note for this campaign is:

- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)

### 2. Students

This should be the next major campaign.

Why next:

- student records are structured and cross-cutting
- they overlap naturally with `people.json`
- they are likely to feed both `students.dj` and later CV sections

Likely target:

- `site/data/students.json`

Likely outcomes:

- canonical student/advising records
- projection into `site/pages/students.dj`
- later projection into selected CV subsections

### 3. Publications

This should be the third major campaign.

Why after talks and students:

- the payoff is high, but the page is much larger and more varied
- by then we should have more practical experience with the projection style

Important constraint:

- this is not a new publication database campaign
- publication bundles are already canonical
- the current publications index is only partially backed by canonical local
  bundles today

The real job is to project publication-list structure from existing
`site/pubs/<slug>/publication.json` records instead of hand-maintaining the
repeated listing shape in `site/pages/publications.dj`

An important first decision for that campaign is whether publications should
mirror the talks collection shape:

- collection root under `site/pubs/`
- authored index wrapper at `site/pubs/index.dj`
- canonical collection URL at `/pubs/`

The current repo still uses `site/pages/publications.dj` and
`/publications.html`, so the publications campaign should decide that route
shape explicitly instead of drifting into it piecemeal.

Another important scoping note:

- the current `site/pages/publications.dj` lists 69 entries
- only 21 of those entries currently have canonical local bundles under
  `site/pubs/`

So the publications campaign is likely not a one-slice "flip the page over"
project.
It will probably need a staged approach that separates:

- deciding the collection index route shape
- deciding whether to extend canonical local bundles more broadly
- projecting the page incrementally without pretending all entries are already
  fully canonicalized in the same way

## Adjacent / Emerging Domains

These are real candidates, but they are not the main initial sequence.

### Collaborators

This may be one of the easiest domains because it is closely tied to people and
publication history.

It may become a small side campaign or fall out naturally from people plus
publication-derived projections.

It should not derail the main sequence of:

- talks
- students
- publications

### Funding / Grants

This is a likely future domain once the structured-content pattern is more
mature.

It is a good example of a cross-page factual domain that may eventually deserve
its own canonical records.

### CV And News

These should come later.

Both pages mix structured facts with a lot of narrative/editorial framing, so
they should benefit from earlier campaigns before we try to project major parts
of them.

The likely long-term model is:

- keep prose-heavy sections hand-authored
- project selected structured subsections from canonical records

## Slice Style

Each campaign should be executed as a series of small slices rather than one
big conversion.

The usual shape should be:

1. audit the current page/content shape
2. define the smallest useful canonical schema
3. add focused validation and tests
4. project one page or one page section from that schema
5. stop and reassess before broadening the scope

## Non-Goals

- turning every page into generated output
- moving prose-heavy editorial sections into JSON
- creating one giant global content schema
- introducing data layers that do not clearly earn their keep

## Current Recommendation

The next campaign should be:

- talks

The next major campaigns after that should be:

- students
- publications

And collaborators/funding should be revisited when they naturally fit the
evolving structured-content model.
