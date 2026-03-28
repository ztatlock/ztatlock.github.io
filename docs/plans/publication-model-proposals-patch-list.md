# Publication Model Proposal Patch List

Status: proposal-refinement note

It builds on:

- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-proposal-b-semantic-objects.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-b-semantic-objects.md)
- [publication-model-proposals-claude-review-1.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-1.md)
- [publication-model-proposals-claude-review-2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-2.md)
- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)

## Purpose

Capture the concrete proposal refinements suggested by the two Claude review
passes before choosing a direction.

This note is not a schema choice by itself.
It is a patch/refinement checklist against the current Proposal A / Proposal B
drafts.

## Overall Read

The two Claude reviews converged on a useful shape:

- `A` is still the more believable near-term direction
- `B` is still the cleaner long-term semantic shape
- but both proposals are under-specifying a few migration-critical seams

The most important refinement pressure is shared:

- venue cleanup needs to be reality-tested across the whole corpus
- canonical year semantics must replace or clearly coexist with slug-year
  rendering
- `primary_link` needs explicit treatment
- `person_key` is probably premature
- the `pub_type` requirement/optionality question needs a real answer

So the next refinement pass should focus less on abstract shape and more on
those migration-critical semantics.

## Shared Refinements To Apply To Both A And B

### 1. Add An Explicit Slug-Year Retirement / Coexistence Section

Both proposals currently say:

- canonical year becomes explicit

But neither says clearly what happens to the current code path that renders
year from:

- `publication_year(record.slug)`

Concrete patch:

- add a section explicitly stating whether:
  - slug-year parsing is retired for display consumers
  - or slug-year remains a checked path invariant while canonical year comes
    from record data
- name the migration consequence for:
  - `/pubs/`
  - CV indexed publications
  - homepage recent publications

Current recommendation:

- proposals should assume display consumers switch to canonical year metadata
- slug year may remain a path convention and validation check, but not the
  primary display source

### 2. Add Explicit `primary_link` Treatment

Both proposals still implicitly depend on `primary_link`, but neither explains
it clearly enough.

Concrete patch:

- add an explicit subsection under local-page readiness explaining:
  - whether `primary_link` remains a first-class field
  - where it lives
  - how it interacts with local/external title destinations

Current recommendation:

- keep `primary_link` explicit in this pass
- do not try to derive every title destination solely from identifier fields
  yet

### 3. Add A Corpus-Scale Venue Cleanup Note

Both proposals currently demonstrate venue cleanup only with easy examples.

Concrete patch:

- add a migration note that venue cleanup must be tested against the actual
  current corpus, not only example records
- explicitly call out cases where:
  - full and compact venue labels are identical
  - compact labels may be obscure workshop acronyms
  - venue shortness is real but not especially reader-friendly

Current recommendation:

- make clear that `venue_short` or `venue.short` may legitimately equal the
  full venue label when no better compact form exists
- do not treat equality as a schema problem by itself

### 4. Remove `person_key` From The First-Pass Leading Proposal Draft

Both reviews correctly flagged that `person_key` currently lacks a concrete
consumer.

Concrete patch:

- demote `person_key` from the main proposal shape
- keep it as an explicitly deferred future refinement

Current recommendation:

- first-pass proposals should keep author entries to:
  - `name`
  - optional `ref`
- note that stronger identity keys may come later if real consumers need them

### 5. Add DOI / Publisher-Link Derivation Discussion

The Xavier-inspired review pressure here was good.

Concrete patch:

- both proposals should explicitly discuss whether:
  - DOI and publisher link stay independently authored
  - or publisher links may be derived in some cases from DOI

Current recommendation:

- do not force derivation as a hard requirement in v1
- but add a note that DOI-based landing-link derivation is a serious future
  cleanup option worth keeping open

## Proposal A Refinements

### A1. Clarify What `venue_short` Means When It Equals `venue`

Review pressure:

- Proposal A currently does not explain identical full/compact venue labels
  well enough

Concrete patch:

- add explicit semantics:
  - `venue_short` is the best honest compact consumer label
  - it may equal `venue` when the venue already has a naturally compact label
    or no better short form exists

This lets `<Programming>` and similar future cases remain honest without
pretending every compact label adds new semantic information.

### A2. Decide Whether `pub_type` Is Required Or Optional

This is the biggest unresolved A-specific question.

Review pressure:

- optional `pub_type` may become dead weight
- required `pub_type` adds authoring burden

Concrete patch:

- add an explicit decision section
- state one of:
  - `pub_type` is required with a deliberately small vocabulary
  - `pub_type` is deferred entirely from this pass

Current recommendation:

- lean toward making `pub_type` required **if** the current corpus can be
  backfilled cheaply with a small vocabulary such as:
  - `conference`
  - `journal`
  - `workshop`
  - `tech-report`
  - `book`
  - `book-chapter`
  - `misc`

If that turns out not to be cheap, then A should probably defer `pub_type`
rather than carry it as optional decorative metadata.

### A3. Strengthen The Migration-Cost Honesty Around Renames And Loader Changes

Review pressure:

- A currently understates the cost of:
  - `detail_page` -> `local_page`
  - adding identifiers
  - changing person-entry validation

Concrete patch:

- expand migration section to say clearly:
  - loader whitelist changes are all-at-once
  - consumer rewrites still happen for year rendering and renamed fields
  - “small migration” means smaller than B, not “almost no code changes”

### A4. Address Venue Identity More Honestly

Review pressure:

- A largely punts venue identity

Concrete patch:

- add an explicit limitation note:
  - A does not model venue identity directly in the first pass
  - venue identity remains future work if/when that pressure becomes real

This is better than leaving it implicit.

## Proposal B Refinements

### B1. Acknowledge The Workshop / `venue.series` Problem Explicitly

Review pressure:

- `venue.series` is attractive for conferences but ambiguous for many
  workshops

Concrete patch:

- add an explicit discussion of where `venue.series` is easy vs hard
- make clear that one-off or loosely recurring workshop venues are a real
  modeling risk

Current recommendation:

- either:
  - make `venue.series` explicitly optional and narrow in scope
  - or demote it from the proposal’s leading shape and treat it as a possible
    later extension

### B2. Justify Why Nesting Helps Enough To Pay For It

Review pressure:

- B currently adds structure more convincingly than it proves the structure is
  worth the migration

Concrete patch:

- strengthen the “why B” section with a sharper argument for why grouping:
  - time
  - venue
  - classification
  - local-page readiness
  actually reduces long-term complexity rather than just moving it around

Without that, B reads as elegant but somewhat speculative.

### B3. Be More Honest About The All-At-Once Consumer Rewrite Cost

Review pressure:

- B’s migration burden is currently understated

Concrete patch:

- explicitly state that B requires coordinated rewrites of:
  - record loader
  - index rendering
  - CV rendering
  - homepage rendering
  - inventory tooling
  - any collaborator/publication readers

That cost should be stated plainly rather than implied.

### B4. Reconsider `local_page.mode` As The Main Differentiator

Review pressure:

- this may be more complexity than value today

Concrete patch:

- either:
  - keep it, but justify it more strongly against the current boolean
  - or simplify it back toward A’s binary approach and let B’s main difference
    rest on venue/time/classification grouping instead

Current recommendation:

- this is a real weak spot in B and should be tightened if B is going to stay
  alive as a serious contender

## Questions To Resolve Before Choosing A Direction

These now look like the real decision questions:

1. Will display consumers switch from slug-year parsing to canonical year
   metadata in this redesign pass?
2. Does first-pass publication redesign keep `primary_link` explicit?
3. What should happen when compact venue label equals full venue label?
4. Is `pub_type` required, deferred, or optional?
5. Should DOI/publisher-link duplication remain fully authored, or should the
   model keep open a later derivation path?
6. Does B’s extra structure buy enough real value now to justify a larger
   migration before backfill?

## Current Recommendation

The next refinement step should probably be:

1. patch A and B with the shared fixes above
2. remove or defer `person_key`
3. settle the `pub_type` decision
4. prototype venue cleanup and year semantics against the actual corpus
5. then compare the tightened proposals again

Current leaning remains:

- `A` is the stronger near-term favorite
- but only if it becomes more explicit about its limitations and migration
  mechanics
- `B` remains the cleaner long-term alternative, but it still needs a sharper
  defense of why its added structure is worth paying for now
