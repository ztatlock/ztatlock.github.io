# Publication Model Proposal A: Conservative Refinement

Status: proposal draft

It builds on:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-requirements-review-synthesis.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements-review-synthesis.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)
- [publication-model-corpus-refinement-pass.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-refinement-pass.md)
- [publication-model-proposals-patch-list.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-patch-list.md)
- [publication-model-xavier-leroy-lessons.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-xavier-leroy-lessons.md)
- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

## Executive Summary

Keep the current bundle-local publication architecture and keep the authored
record mostly flat.

The main move is not to invent a new publication hierarchy.
It is to make the current record shape more semantically honest by adding the
few explicit fields that current and near-term consumers now clearly need.

Proposal A is therefore:

- one bundle per publication
- one primary `publication.json` record per bundle
- explicit canonical publication year separate from exact publication date
- explicit compact venue label separate from full venue label
- explicit required small-vocabulary `pub_type` beside `listing_group`
- explicit identifiers object
- a lightly cleaned local-page-readiness field with `primary_link` kept
  first-class

Just as importantly, Proposal A is primarily a choice about the **authored
schema on disk**.
It does **not** require the loaded/in-memory publication model used by code to
stay equally flat.
After parsing and validation, the repo may still rehydrate publication data
into richer internal objects if that makes consumers or tooling cleaner.

This is the lowest-risk proposal that still addresses the real seams.

## Why This Proposal Exists

The audit did **not** show a need for a service-style structural reset.

The strongest seams in the current model are:

- overloaded `venue`
- implicit temporal semantics
- awkward `detail_page` naming
- thin identifiers
- page-shaped `listing_group`
- unclear author display-vs-identity semantics

Those are all fixable without abandoning the current bundle-local
architecture.

Proposal A therefore favors:

- schema refinement over structural reinvention
- disciplined flatness over “one more field” sprawl
- smaller migration
- simpler backfill work
- preserving the current mental model for bundle authoring

## Core Design

### 1. Keep One Bundle Per Publication

The current bundle-local architecture remains:

- `site/pubs/<slug>/publication.json`
- bundle-local assets
- optional richer local page content

There is no new multi-record publication graph and no venue registry.

### 2. Keep The Record Mostly Flat

The record stays top-level and mostly field-oriented.

The goal is:

- fix semantics
- avoid nesting unless it adds real clarity
- keep diffs small
- keep hand-auditing easy

This proposal is intentionally not “flat at any cost.”

Its design rule is:

- keep facts top-level when they are simple, independently useful, and common
- allow a small grouped object when it already corresponds to a real repeated
  semantic cluster, as `identifiers` does
- do **not** keep accreting new top-level fields indefinitely just because the
  record is already flat

That means Proposal A is only a good long-term answer if this pass remains
disciplined.
If future publication work needs multiple new coupled axes such as venue
identity, proceedings/container semantics, and broader type systems, that
would be a sign that a later B-like regrouping pass has become justified.

### 2.5. Keep Authored Shape And Loaded Shape Distinct

Proposal A is a proposal about the **physical JSON representation** that
humans and agents author.

It is **not** a claim that every consumer should read raw JSON fields directly
forever.

A compatible internal approach is:

- keep `publication.json` physically simple and reviewable
- parse and validate that shape
- rehydrate it into a richer normalized in-memory representation where useful

That means the repo does **not** have to choose between:

- simple authored source
- richer semantic objects in code

If code benefits from grouped internal concepts such as:

- time
- venue
- classification
- identifiers

that can still happen after load without forcing the authored JSON to carry
that full structure directly.

### 3. Make Temporal Semantics Explicit

Add:

- `pub_year`
- keep `pub_date`, but make it optional precise date metadata rather than the
  only temporal field

Semantics:

- `pub_year` is the canonical publication year for display and year-based
  selection consumers
- `pub_date`, when present, is a more precise date used for ordering or richer
  metadata consumers
- `slug` remains a stable path identity, but year semantics no longer depend
  only on slug parsing

Important consequence:

- `pub_year` may legitimately differ from `pub_date.year`
- this supports cases where proceedings date, journal issue date, or artifact
  publication date does not match the display/publication year humans expect

First-pass stance:

- `pub_year` becomes the canonical display year for:
  - `/pubs/`
  - the CV indexed publication sections
  - homepage recent publications
- `pub_date` remains useful for:
  - ordering
  - richer metadata
  - exact-date consumers
- slug-year remains a path convention and validation check, not the primary
  display-year source

### 4. Split Full And Compact Venue Display

Add:

- `venue`
- `venue_short`

Semantics:

- `venue` is the full bibliography-facing venue label
- `venue_short` is the compact venue label for consumers like the homepage
- `venue` should no longer carry acronym duplication such as
  `(...ACRONYM...)` just to support compact consumers
- `venue_short` may legitimately equal `venue` when the venue already has a
  naturally compact label or no better short form exists

This proposal intentionally treats compact venue labeling as an independent
authored fact rather than a heuristic derivation rule.

Concrete corpus backing:

- `68/69` current indexed venues already have an obvious full/compact split
- `<Programming>` is the current equality case where full and compact are the
  same honest label
- awkward but acceptable compact labels such as `SECURITY`, `CORRECTNESS`,
  `SPLASH-E`, `CoqPL`, `NetPL`, `PLATEAU`, and `MLSys` reinforce that this
  should stay authored rather than heuristic

### 5. Clarify Local Page Readiness And Keep `primary_link` First-Class

Rename:

- `detail_page` -> `local_page`

Keep:

- `primary_link`

Keep the semantics binary for now:

- `local_page: true`
  - rich local publication page exists and local-page requirements apply
- `local_page: false`
  - thin external-destination canonical bundle

`primary_link` remains the explicit title-destination selector for thin
bundles.
This proposal does **not** try to hide title-destination policy inside
identifiers or derived link rules.

This proposal does **not** introduce a richer readiness enum yet.
It only makes the current meaning more honest.

### 6. Preserve `listing_group`, But Stop Pretending It Is Enough

Keep:

- `listing_group`

Add:

- `pub_type` as a required small-vocabulary semantic classification field for
  indexed publications

Intended role split:

- `listing_group`
  - current page-facing grouping for `/pubs/` and CV sections
  - retained because current public consumers already depend on it
  - treated as a current projection field, not authoritative publication
    semantics
- `pub_type`
  - light semantic classification such as:
    - `conference`
    - `journal`
    - `workshop`
  - with room to extend later to other real publication kinds such as:
    - `tech-report`
    - `book`
    - `book-chapter`
    - `misc`

This lets the repo preserve the current projections while acknowledging that
page grouping and publication type are not the same concept.
Proposal A therefore does **not** assume existing `listing_group` values are
semantically correct.

This proposal also treats `pub_type` as:

- deliberately small in first-pass vocabulary
- required for indexed publications
- not a hidden venue-identity field
- not a dumping ground for future selection/prominence metadata

Current corpus reality check:

- a small required vocabulary now looks feasible
- making `pub_type` optional would likely create dead-weight metadata that
  never gets backfilled consistently
- a concrete first-pass draft assignment looks plausible at:
  - `49` conference
  - `7` journal
  - `13` workshop
- the current corpus already contains likely divergences between current
  projection grouping and semantic type, including:
  - `2016-netpl-bagpipe`
  - `2018-mapl-relay`
  which currently live in `listing_group: main` but look semantically like
  `pub_type: workshop`
- this supports classifying `pub_type` directly from publication semantics,
  then checking where current `listing_group` no longer lines up

### 7. Add Explicit Identifiers

Add:

- `identifiers`

Initial likely contents:

- `doi`
- `arxiv`

Possible later contents:

- `hal`
- `isbn`

Links remain useful and are not replaced.
The distinction is:

- `identifiers` hold canonical identifiers
- `links` hold landing pages and related destinations

Current stance on DOI and publisher links:

- both may remain authored in the first pass
- but the model should keep open a later cleanup where some publisher landing
  URLs can be derived from DOI when that meaningfully reduces authoring burden

### 8. Keep Author Identity Conservative In The First Pass

Keep `authors` as an ordered array with:

- `name`
- optional `ref`

This proposal explicitly defers stronger author-identity keys such as
`person_key`.

Rationale:

- current consumers already use `name` and `ref`
- adding a stronger site-local identity key now would be speculative because
  no current publication consumer requires it
- a later smaller pass can revisit stronger cross-domain identity if real
  consumers justify it

## Proposed Record Shape

Illustrative thin external-destination bundle:

```json
{
  "local_page": false,
  "listing_group": "main",
  "pub_type": "conference",
  "pub_year": 2025,
  "pub_date": "2025-03-30",
  "primary_link": "publisher",
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
  "venue": "Architectural Support for Programming Languages and Operating Systems",
  "venue_short": "ASPLOS",
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
  "listing_group": "main",
  "pub_type": "journal",
  "pub_year": 2024,
  "pub_date": "2024-07-09",
  "title": "Magic Markup: Maintaining Document-External Markup with an LLM",
  "authors": [
    { "name": "Edward Misback", "ref": "Edward Misback" },
    { "name": "Zachary Tatlock", "ref": "Zachary Tatlock" },
    { "name": "Steven L. Tanimoto", "ref": "Steven L. Tanimoto" }
  ],
  "venue": "<Programming>",
  "venue_short": "<Programming>",
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
- ordered `authors`
- `venue`
- canonical display year from `pub_year`
- `badges`

They do not need `venue_short`.

### Homepage Recent Publications

Use:

- `title`
- compact venue label from `venue_short`
- canonical display year from `pub_year`
- canonical title destination from the existing local-vs-external rule

This directly fixes the original homepage seam without heuristics.

### Collaborator / Cross-Domain Consumers

Can continue using:

- `authors[].name`
- optional `authors[].ref`

This proposal intentionally leaves stronger cross-domain person identity for a
later pass.

### Future Topic / Kind / Analysis Consumers

This proposal does not add explicit topic metadata now.
But it does make two future projection axes materially more feasible than the
current model:

- publication kind via `pub_type`
- identifier-aware analysis via `identifiers`

It does **not** make venue identity, proceedings/container semantics, or
books/chapters classification fully explicit in this first pass.
Those remain honest later seams rather than pretending to be solved here.

Current concrete seam:

- `2019-siga-carpentry` already carries mixed event/journal provenance in its
  current venue string

That is enough to keep venue/container semantics visible as later work, but
not enough to justify a larger first-pass venue structure on its own.

### Inventory / Tooling

Can use:

- `identifiers`
- `pub_year`
- `pub_date`
- `local_page`

without scraping display strings.

## Migration Story

This proposal is intentionally migration-friendly.

Expected migration work:

1. add `pub_year` to indexed bundles
2. switch display consumers from slug-year rendering to `pub_year`
3. clean `venue` strings to remove embedded acronym suffixes where present
4. add `venue_short`
5. rename `detail_page` to `local_page`
6. keep `primary_link` explicit for thin bundles
7. add `identifiers` gradually, starting with DOI and arXiv where obvious
8. add required `pub_type` using a deliberately small first-pass vocabulary

Important note:

- venue cleanup should be treated as an atomic corpus-wide migration, not as a
  casual one-record-at-a-time tweak, because the homepage and future compact
  consumers depend on it
- `pub_year` should become the canonical display year everywhere current
  consumers still parse year from slug text; if that consumer rewrite does not
  happen, this proposal has not actually landed its temporal semantics
- the concrete mismatch cases that justify this rewrite already exist:
  - `2016-nsv-fpbench`
  - `2017-icalepcs-neutrons`
  - `2018-popl-disel`
- `ref` can remain as-is during transition
- proposal A does not require immediate venue ontology or author-identity
  normalization campaign
- `pub_type` should be backfilled as a real required field for indexed
  publications, not carried as optional future decoration
- that backfill should be done from publication semantics, not by blindly
  translating existing `listing_group` values
- the current thin/rich split still looks binary enough in practice:
  - `48` thin bundles
  - `21` rich local pages
  - among thin bundles, `primary_link` currently distributes as:
    - `43` publisher
    - `5` event
- “small migration” here means smaller than Proposal B, not “almost no code
  changes”

## Advantages

1. Smallest migration among serious options.
2. Keeps the current bundle-local authoring mental model.
3. Solves the strongest current seams directly.
4. Avoids heuristic compact venue derivation.
5. Makes temporal semantics explicit without overengineering dates.
6. Adds identifiers without forcing the whole repo through BibTeX.
7. Keeps future refinement possible.
8. Leaves a clean path toward broader publication kinds without forcing them
   into scope now.

## Costs And Risks

1. The record gets wider and flatter.
2. `listing_group` plus required `pub_type` introduces two parallel
   classification fields.
3. A still does not model venue identity directly in the first pass.
4. `local_page` is clearer than `detail_page`, but still only a binary
   readiness abstraction.
5. `venue` plus `venue_short` still duplicates some human knowledge.
6. The proposal now depends on making `pub_type` work as a real required field
   rather than decorative metadata.
7. If future publication work quickly wants more semantic axes, Proposal A may
   still trigger a later regrouping pass.

## Current Judgment

Proposal A is the likely leading candidate if the repo wants the cleanest path
to:

- fix the visible seams now
- keep migration/backfill cheap
- preserve the current publication bundle architecture almost unchanged

Its biggest weakness is not correctness.
It is that the record risks becoming a somewhat crowded flat schema over time,
and still leaves venue identity and broader container semantics as later work
rather than solving them now.

So Proposal A should only win if the repo believes:

- the currently visible seams are the right ones to solve now
- the next backfill wave benefits more from simpler authoring than from
  deeper regrouping
- a disciplined flat schema is still likely to remain honest for a while
- the repo can keep authored JSON simple while still using richer normalized
  internal objects in code when that is helpful
