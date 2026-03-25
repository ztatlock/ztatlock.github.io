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

### 2. Publications

This should be the next major campaign.

Why next:

- publication bundles are already canonical for part of the site
- the publications index still has the clearest remaining collection-shape
  asymmetry in the repo
- the talks campaign already proved the bundle-plus-index-wrapper pattern on a
  smaller domain
- resolving the publications collection shape will strengthen the architecture
  before we take on additional shared-data domains

Important constraint:

- this is not a new publication database campaign
- publication bundles are already canonical
- the current publications index is only partially backed by canonical local
  bundles today

The real job is now to project publication-list structure from
`site/pubs/<slug>/publication.json` records instead of hand-maintaining the
repeated listing shape in `site/pubs/index.dj`

The core publications collection shape is now in place:

- canonical bundles for all indexed publications under `site/pubs/`
- hand-authored collection wrapper at `site/pubs/index.dj`
- canonical collection URL at `/pubs/`
- derived index ordering from bundle `pub_date`
- projected repeated publication-entry sections from bundle data while keeping
  framing and `Aggregators` hand-authored

That collection-shape decision is now implemented:

- collection root under `site/pubs/`
- authored index wrapper at `site/pubs/index.dj`
- canonical collection URL at `/pubs/`

Another important scoping note:

- the current `site/pubs/index.dj` lists 69 entries
- all 69 indexed publications now have canonical local bundles under
  `site/pubs/`
- 48 of those bundles are currently minimal `detail_page: false` records

So the publications campaign has been an explicitly staged project.
It separated:

- deciding the collection index route shape
- establishing the last missing ordering fact in bundle data
- projecting the page incrementally without pretending all entries are already
  equally rich local publication pages

The likely follow-on work is now either:

- local publication artifact enrichment over time
- or downstream reuse in later consumers like CV/news once that earns its keep

### 3. Students

This should be the third major campaign.

Why after publications:

- student records are structured and cross-cutting
- they overlap naturally with `people.json`
- they are likely to feed both `students.dj` and later CV sections
- but they do not currently unlock an architectural seam as directly as the
  publications collection shape does

Current target:

- keep `site/data/students.json` canonical and use it to drive the public
  students wrapper plus later CV projection

Implemented outcomes so far:

- canonical student/advising records
- projection into `site/students/index.dj` at canonical `/students/`

Likely next outcomes:

- later projection into selected CV subsections

### 4. Teaching

Teaching is now at a good public-page checkpoint.

Why next:

- teaching facts are already duplicated across the public teaching page, the
  CV, and the homepage
- the domain is more regular than service and has clearer cross-page payoff
  than collaborators or funding right now
- it naturally fits the same shared-data-first pattern that worked for
  students

Current target:

- keep canonical teaching records in `site/data/teaching.json`
- keep the public teaching wrapper at `site/teaching/index.dj` with canonical
  `/teaching/`
- later project compressed views into the CV and homepage

Implemented outcomes so far:

- canonical teaching records now live in `site/data/teaching.json`
- source validation and focused tests now enforce the teaching data model
- the public teaching wrapper now lives at `site/teaching/index.dj`
- the canonical public teaching URL is now `/teaching/`
- the repeated public teaching blocks now project from canonical teaching data
- the canonical teaching record now includes the previously missing
  Marktoberdorf Summer School 2024 entry, which now also appears on the public
  teaching page

Important design choice:

- do not over-normalize pedagogy or course nuance into rigid enums too early
- keep repeated factual fields structured
- keep descriptive course prose as small Djot strings where that stays clearer

Likely slice order:

1. canonical teaching record model in `site/data/teaching.json`
2. public teaching wrapper/index projection
3. homepage recent-teaching projection
4. CV teaching projection

### 5. Service

Service followed teaching as the next major shared-data campaign and is now at
a good public-page checkpoint.

Why it was next:

- it is duplicated across the public service page, the homepage, and the CV
- the domain is list-shaped and fairly regular even though entries vary more
  than teaching
- it fits the same shared-data-first pattern as students and teaching
- it already showed cross-page drift, so canonicalization improved correctness
  as well as maintenance

Implemented outcomes so far:

- canonical service terms now live in `site/data/service.json`
- the public service wrapper now lives at `site/service/index.dj`
- the canonical public service URL is now `/service/`
- repeated public service blocks now project from canonical service data
- homepage and CV cleanup remain deferred as later cross-cutting consumer work

### 6. CV Consumer Wrapper

The next major structured-content campaign should be the CV as a cross-domain
consumer wrapper.

Why next:

- the repo now has several canonical domain models whose interfaces have mostly
  only been exercised by their own primary public wrappers
- the CV is the clearest downstream consumer with intentionally different
  presentation conventions
- the largest remaining duplicated factual maintenance now sits in the CV over
  already-canonical domains such as students, teaching, and service

Current recommendation:

- keep the CV wrapper at `site/cv/index.dj` with canonical `/cv/`
- keep the full CV body hand-authored while the first consumer slices land
- project students into the CV as the first true downstream-consumer slice
- stop and reassess before touching teaching, service, talks, publications,
  or highlights

## Adjacent / Emerging Domains

These are real candidates, but they are not the main implemented sequence
above.

### Collaborators

This may be one of the easiest domains because it is closely tied to people and
publication history.

It may become a small side campaign or fall out naturally from people plus
publication-derived projections.

It should not derail the main sequence above.

### Funding / Grants

This is a likely future domain once the structured-content pattern is more
mature.

It is a good example of a cross-page factual domain that may eventually deserve
its own canonical records.

### News

News should still come later.

It mixes structured facts with a lot of narrative/editorial framing, so it
should benefit from the earlier domain campaigns and from the later CV
consumer work before we try to project major parts of it.

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

The repo is now at a good checkpoint after the public-page cores for:

- talks
- publications
- students
- teaching
- service

The next major structured-content campaign should be:

- CV as a cross-domain consumer wrapper, with route cutover implemented and
  students CV projection next

Publication follow-on work should continue separately as:

- local artifact enrichment for thinner `detail_page: false` bundles
- later downstream reuse where publication bundle truth clearly earns it

Students follow-on work should continue separately as:

- projection of the duplicated advising sections in the CV consumer wrapper
  from `site/data/students.json`

Teaching and service follow-on work should continue separately as:

- later homepage/CV consumer cleanup once that cross-cutting work clearly
  earns its keep

Later domain campaigns should still likely include:

- collaborators
- funding / grants

but only after the repo has exercised the existing canonical domains through
the CV consumer pattern.
