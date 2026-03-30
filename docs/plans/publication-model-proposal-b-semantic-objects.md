# Publication Model Proposal B: Semantic Objects

Status: historical alternative kept for comparison

It builds on:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-requirements-review-synthesis.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements-review-synthesis.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)
- [publication-model-corpus-refinement-pass.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-refinement-pass.md)
- [publication-model-proposals-patch-list.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-patch-list.md)
- [publication-model-xavier-leroy-lessons.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-xavier-leroy-lessons.md)

## Executive Summary

Keep the current bundle-local publication architecture, but make the authored
record more semantic by grouping related facts into a few explicit objects.

Proposal B is still not a service-style redesign.
It still keeps:

- one bundle per publication
- one `publication.json` per bundle
- the current local-assets model

But instead of solving the seams with more flat top-level fields, it groups
the semantic clusters that most clearly earn it:

- time
- venue
- publication classification
- identifiers

This proposal aims for a cleaner long-term model than Proposal A, at the cost
of somewhat heavier authoring and migration.

## Why This Proposal Exists

The main risk in a conservative publication refinement is not that it fails
the current consumers.
It is that it turns the publication record into a growing flat checklist:

- `pub_year`
- `pub_date`
- `venue`
- `venue_short`
- `listing_group`
- `pub_type`
- `detail_page` / `local_page`
- `doi`
- `arxiv`
- and so on

Proposal B asks whether the repo should instead take this opportunity to make
the main semantic clusters explicit now, before larger backfill lands.

## Core Design

### 1. Keep Bundle-Local Architecture

This proposal does **not** introduce:

- a separate publication registry
- a venue registry
- series/run/instance-like hierarchy
- consumer-local publication shadow data

The architecture remains bundle-local.

### 2. Group Related Facts Explicitly

Instead of a large flat record, Proposal B introduces semantic groupings.

The main grouped areas are:

- `time`
- `venue`
- `classification`
- `identifiers`

This proposal now makes one important refinement explicit:

- not every seam deserves an object
- local-page readiness stays flat in this pass because the current semantics
  are still effectively binary
- B should win only if its grouped objects earn their cost, not because nested
  JSON feels cleaner in the abstract

### 3. Time Becomes An Explicit Object

Use:

```json
"time": {
  "year": 2025,
  "date": "2025-03-30"
}
```

Semantics:

- `time.year`
  - canonical publication year for display and year-based selection
- `time.date`
  - optional more precise date

This makes the distinction between canonical year and exact date explicit
without requiring consumers to infer which field is the “real year.”

First-pass stance:

- `time.year` becomes the canonical display year for:
  - `/pubs/`
  - the CV indexed publication sections
  - homepage recent publications
- `time.date` remains useful for ordering and richer metadata
- slug-year remains a path convention and validation check, not the primary
  display-year source

### 4. Venue Becomes An Explicit Object

Use:

```json
"venue": {
  "full": "Architectural Support for Programming Languages and Operating Systems",
  "short": "ASPLOS"
}
```

Semantics:

- `full`
  - bibliography-facing display
- `short`
  - compact display
- `short` may legitimately equal `full` when the venue already has a naturally
  compact label or no better short form exists

Proposal B does **not** require a full venue ontology.

Optional later extension:

- a separate venue-identity field such as `series` may still be considered
  later where venue-family identity is genuinely clear
- but this proposal no longer treats that as part of the first-pass leading
  shape because workshop and one-off venues make it too ambiguous today

Concrete corpus backing:

- `68/69` current indexed venues already support a clean full/compact split
- `<Programming>` is the current equality case where `short == full`
- awkward but honest compact labels such as `SECURITY`, `CoqPL`, `NetPL`,
  `SPLASH-E`, `PLATEAU`, `LATTE`, and `MLSys` reinforce that the compact
  label should remain authored rather than heuristic
- `2019-siga-carpentry` shows a real mixed event/journal provenance seam, but
  still not enough current pressure to force a fuller venue/container model in
  the first pass

### 5. Classification Becomes Explicitly Separate

Use:

```json
"classification": {
  "listing_group": "main",
  "pub_type": "conference"
}
```

This makes the split explicit:

- page-facing grouping retained for current public consumers
- semantic publication type treated as canonical publication classification

It also gives the model a cleaner long-term home for additional semantic axes
if they later become real, such as:

- topic tags
- selection or prominence signals
- broader publication-kind distinctions like books, proceedings, or reports

First-pass stance:

- `classification.pub_type` should be required for indexed publications
- the first-pass vocabulary can stay deliberately small:
  - `conference`
  - `journal`
  - `workshop`
- later extension remains possible for:
  - `tech-report`
  - `book`
  - `book-chapter`
  - `misc`

Concrete corpus backing:

- a current draft assignment looks plausible at:
  - `49` conference
  - `7` journal
  - `13` workshop
- `classification.pub_type` already pulls real semantic weight because the
  current corpus likely includes current page-grouping records whose semantic
  type is `workshop`, including:
  - `2016-netpl-bagpipe`
  - `2018-mapl-relay`
- B therefore should not be read as trusting current `listing_group` as
  semantic truth; it keeps `classification.listing_group` because current
  `/pubs/` and CV projections still depend on it

This proposal intentionally does **not** treat `classification` as a general
metadata junk drawer.
Its first-pass job is still narrow:

- preserve the current page grouping for current consumers
- carry a real semantic publication type independently of that grouping
- leave room for future axes only if concrete consumers later justify them

### 6. Keep Local Page Readiness Flat For Now

Keep:

- `local_page`
- `primary_link`

Semantics:

- `local_page: false`
  - canonical thin bundle exists, title links externally through
    `primary_link`
- `local_page: true`
  - richer local page exists and local-page requirements apply

Proposal B now treats this as a deliberate simplification.
The important semantic win in B is the grouping of time, venue,
classification, and identifiers.
The current binary readiness seam does not yet justify its own nested object.

Concrete corpus backing:

- current indexed corpus still looks binary enough here:
  - `48` thin bundles
  - `21` rich local pages
  - thin bundles currently use only:
    - `primary_link: "publisher"` (`43`)
    - `primary_link: "event"` (`5`)

The explicit `primary_link` selector still remains first-class in this
proposal.
B does **not** try to replace it with implicit identifier-based routing.

### 7. Identifiers Become A Dedicated Object

Use:

```json
"identifiers": {
  "doi": "10.1145/3669940.3707277",
  "arxiv": "2403.03481"
}
```

Links remain separate landing-page destinations.

This object also gives a cleaner home for later identifiers such as:

- `hal`
- `isbn`

Current stance on DOI and publisher links:

- both may remain authored in the first pass
- but the model should keep open a later cleanup where some publisher landing
  URLs may be derived from DOI when that meaningfully reduces authoring burden

### 8. Keep Author Identity Conservative In The First Pass

Use:

```json
{ "name": "Zachary Tatlock", "ref": "Zachary Tatlock" }
```

Like Proposal A, B now explicitly defers stronger author-identity keys such as
`person_key`.

Rationale:

- current consumers already use `name` and `ref`
- stronger site-local identity keys do not yet have a real publication
  consumer
- the first-pass publication redesign should not over-model this seam

## Proposed Record Shape

Illustrative thin external-destination bundle:

```json
{
  "local_page": false,
  "primary_link": "publisher",
  "classification": {
    "listing_group": "main",
    "pub_type": "conference"
  },
  "time": {
    "year": 2025,
    "date": "2025-03-30"
  },
  "title": "Target-Aware Implementation of Real Expressions",
  "authors": [
    { "name": "Brett Saiki" },
    { "name": "Jackson Brough" },
    { "name": "Jonas Regehr" },
    { "name": "Jesús Ponce" },
    { "name": "Varun Pradeep" },
    { "name": "Aditya Akhileshwaran" },
    { "name": "Zachary Tatlock" },
    { "name": "Pavel Panchekha" }
  ],
  "venue": {
    "full": "Architectural Support for Programming Languages and Operating Systems",
    "short": "ASPLOS"
  },
  "identifiers": {
    "doi": "10.1145/3669940.3707277"
  },
  "links": {
    "publisher": "https://dl.acm.org/doi/10.1145/3669940.3707277"
  }
}
```

Illustrative richer local-page bundle:

```json
{
  "local_page": true,
  "classification": {
    "listing_group": "main",
    "pub_type": "journal"
  },
  "time": {
    "year": 2024,
    "date": "2024-07-09"
  },
  "title": "Magic Markup: Maintaining Document-External Markup with an LLM",
  "authors": [
    { "name": "Edward Misback", "ref": "Edward Misback" },
    { "name": "Zachary Tatlock", "ref": "Zachary Tatlock" },
    { "name": "Steven L. Tanimoto", "ref": "Steven L. Tanimoto" }
  ],
  "venue": {
    "full": "<Programming>",
    "short": "<Programming>"
  },
  "identifiers": {
    "doi": "10.1145/3660829.3660836",
    "arxiv": "2403.03481"
  },
  "description": "Magic Markup keeps document-external annotations aligned as text evolves using an LLM-backed re-tagging system.",
  "links": {
    "publisher": "https://doi.org/10.1145/3660829.3660836",
    "arxiv": "https://arxiv.org/abs/2403.03481",
    "code": "https://github.com/elmisback/magic-markup",
    "demo": "https://observablehq.com/@elmisback/magic-markup-demo"
  }
}
```

## Consumer Story

### `/pubs/` and CV

Use:

- `title`
- `authors`
- `venue.full`
- `time.year`
- `badges`

### Homepage

Use:

- `title`
- `venue.short`
- `time.year`
- title destination derived from `local_page` plus explicit `primary_link`

### Collaborator / Cross-Domain Consumers

Use:

- `authors[].name`
- optional `authors[].ref`
- possibly later `classification.pub_type` or future topic tags if those ever
  become worth modeling

### Tooling

Can use:

- `time`
- `identifiers`
- `local_page`
- `classification`

without scraping display strings.

## Migration Story

Migration is still feasible, but heavier than Proposal A.

Expected work:

1. introduce `time`, `venue`, `classification`, and `identifiers` objects
2. keep `local_page` / `primary_link` flat, but update their naming and
   consumer story alongside the grouped migration
3. switch display consumers from slug-year rendering to `time.year`
4. rewrite current flat consumers and validators to use the grouped shape
5. clean venue strings and add compact forms
6. keep `primary_link` explicit for thin bundles
7. backfill required `classification.pub_type` using a deliberately small
   first-pass vocabulary
8. backfill identifiers gradually

This proposal is still much smaller than the service redesign, but it is a
meaningful schema rewrite.

Important note:

- venue cleanup should be tested against the full current corpus, not only
  easy example records
- `time.year` should become the canonical display year everywhere current
  consumers still parse year from slug text; if that rewrite does not happen,
  the temporal semantics remain half-migrated
- the concrete mismatch cases that justify that rewrite already exist:
  - `2016-nsv-fpbench`
  - `2017-icalepcs-neutrons`
  - `2018-popl-disel`
- B requires coordinated consumer rewrites across:
  - record loading/validation
  - `/pubs/` rendering
  - CV rendering
  - homepage recent publications
  - inventory/tooling readers

## Advantages

1. More semantically organized than Proposal A.
2. Avoids steady drift toward a crowded flat schema.
3. Makes the main seam clusters explicit in the authored data.
4. Gives a cleaner long-term home for classification and later richer semantic
   axes.
5. Better supports future analysis and richer cross-domain consumers.
6. Leaves a cleaner path toward by-kind or later topic-aware projections if
   the repo ever wants them.
7. Prunes one of the weakest earlier B ideas by keeping local-page readiness
   flat until a richer readiness consumer actually appears.

## Costs And Risks

1. Higher migration cost.
2. Heavier authoring for ordinary bundles.
3. More nested JSON means slightly noisier diffs.
4. `classification` still has to prove it buys enough over a flatter
   `listing_group` plus `pub_type` pairing.
5. May still be more structure than the current consumers truly require.
6. Risks solving some near-future needs before they are fully real.
7. Still does not actually solve venue identity or broader
   books/chapters/proceedings semantics in this first pass.

## Current Judgment

Proposal B is the cleaner semantic model on paper.

Its main question is pragmatic:

- does the repo want this much structure now, before the next large
  publication backfill?

If the answer is yes, B may age better than A.
If the answer is no, A is probably the better near-term choice because it
captures most of the value with less migration cost.

Proposal B is strongest if the repo believes:

- grouped semantic clusters will age materially better than a disciplined flat
  schema
- the extra migration is worth paying before larger backfill lands
- selective grouping of the most important clusters is cleaner than carrying
  them as more top-level fields
