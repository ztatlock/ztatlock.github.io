# Publication Model Corpus-Backed Refinement Pass

Status: proposal-grounding note

It builds on:

- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-proposal-b-semantic-objects.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-b-semantic-objects.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)
- current implementation in:
  - [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
  - [publication_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_index.py)
  - [page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
  - [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)

## Purpose

Move from abstract proposal comparison to concrete corpus-backed refinement.

This note asks:

- what do the current indexed publication records actually imply?
- where do Proposal A and Proposal B survive that contact well?
- where do they need sharpening before a direction is latched?

## Corpus Facts That Now Feel Concrete

Current non-draft indexed corpus:

- `69` bundles total
- `58` currently in `listing_group: main`
- `11` currently in `listing_group: workshop`
- `21` currently have rich local pages
- `48` are currently thin bundles
- among thin bundles:
  - `43` use `primary_link: "publisher"`
  - `5` use `primary_link: "event"`

This strongly supports:

- `primary_link` remaining first-class
- a still-binary local-page readiness seam
- not over-modeling readiness yet

## 1. Concrete Venue Cleanup Pass

The venue cleanup is real, but the concrete corpus confirms it is tractable.

### Mechanical Core

For `68/69` indexed bundles, the current venue string already has a final
parenthetical short label.

That means both proposals are justified in separating:

- full venue display
- compact venue display

The only current equality case is:

- `2024-programming-magicmarkup`
  - full: `<Programming>`
  - compact: `<Programming>`

So both proposals should keep saying:

- compact label may legitimately equal full label

### Awkward But Honest Compact Labels

The compact labels that deserve explicit honesty rather than heuristic
pretending are:

- `SECURITY`
- `CoqPL`
- `NetPL`
- `CoNGA`
- `CORRECTNESS`
- `FTPL`
- `SIGA`
- `SPLASH-E`
- `PLATEAU`
- `LATTE`
- `MAPS`
- `MLSys`
- `SFF`
- `FARM`
- `PLARCH`
- `<Programming>`

Interpretation:

- these are not arguments against compact venue support
- they are arguments for explicitly authored compact labels
- compact venue support should not claim to be purely acronym logic

### Venue / Container Seams Already Visible

One current indexed venue already carries more than one provenance layer in a
single string:

- `2019-siga-carpentry`
  - `SIGGRAPH Asia, ACM Transactions on Graphics (SIGA)`

This is not enough to force a fuller venue/container model immediately.
But it is enough that both proposals should stay honest:

- first-pass venue cleanup fixes full-vs-compact display
- it does not fully solve venue/container semantics

## 2. Concrete `pub_type` Draft

The corpus now supports a concrete small-vocabulary first pass.

Draft assignment counts:

- `conference`: `49`
- `journal`: `7`
- `workshop`: `13`

The clear journal-like indexed records are:

- `2011-lmcs-eqsat`
- `2019-ftpl-proofengineering`
- `2019-siga-carpentry`
- `2022-tog-carpentry`
- `2024-programming-magicmarkup`
- `2024-todaes-3la`
- `2024-tog-illusionknitting`

The most important concrete refinement is that `pub_type` is **not** just a
copy of current `listing_group`.

More strongly:

- current `listing_group` should be treated as a legacy/current projection
  field
- it is useful migration evidence
- but it is not authoritative publication semantics

Current likely divergences include:

- `2016-netpl-bagpipe`
  - `listing_group: main`
  - likely `pub_type: workshop`
- `2018-mapl-relay`
  - `listing_group: main`
  - likely `pub_type: workshop`

That matters a lot.
It means the `pub_type` field should be classified directly from the
publication itself, then compared against current `listing_group` rather than
derived from it.

## 3. Concrete Temporal Semantics Pass

The current code still mixes three notions of year:

- slug year
- exact `pub_date`
- rendered display year

The current indexed mismatch cases are:

- `2016-nsv-fpbench`
  - slug year `2016`
  - `pub_date` year `2017`
- `2017-icalepcs-neutrons`
  - slug year `2017`
  - `pub_date` year `2018`
- `2018-popl-disel`
  - slug year `2018`
  - `pub_date` year `2017`

Current code still renders venue lines from slug year:

- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
  - `_render_venue_line()`
- [page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
  - `_render_cv_publication_entry()`
  - `_render_homepage_recent_publication_entry()`

Current homepage recent-publication selection still uses `pub_date.year`.

So the concrete consequence for both proposals is now non-negotiable:

- canonical year metadata has to become the displayed year
- homepage/CV/publication index display should stop using `publication_year(slug)`
- homepage selection policy must choose whether it anchors on canonical year,
  exact date year, or some mixed rule

This is not decorative migration.
It is the core temporal-semantics rewrite.

## 4. Concrete Migration Surface

Proposal comparison is clearer once stated as current-field rewrites.

### Current Flat Consumer Assumptions

Current live readers assume direct access to:

- `record.detail_page`
- `record.primary_link`
- `record.pub_date`
- `record.venue`
- `record.listing_group`
- slug-year parsing via `publication_year(record.slug)`

### Proposal A Rewrite Shape

Proposal A still requires real migration because consumers must switch to:

- `record.pub_year` for display year
- cleaned `record.venue`
- `record.venue_short` for compact consumers
- renamed `record.local_page`
- required `record.pub_type`

But the access pattern stays top-level.

### Proposal B Rewrite Shape

Proposal B still requires heavier migration because consumers must switch to:

- `record.time.year`
- `record.time.date`
- `record.venue.full`
- `record.venue.short`
- `record.classification.listing_group`
- `record.classification.pub_type`

The local-page seam is no longer a major B differentiator because the
corpus-backed review supports keeping:

- `local_page`
- `primary_link`

flat in B as well.

## 5. What This Teaches Us About Proposal A

Concrete refinements now supported by the corpus:

1. `pub_type` should stay required in A.
   The field now has demonstrated real value because it diverges from
   current projection grouping in the current corpus.

2. A should explicitly name the likely first-pass counts.
   This makes the backfill burden feel concrete and believable rather than
   speculative.

3. A should stay honest that venue/container semantics remain later work.
   The `SIGA` case shows the seam is real, but not yet large enough to force
   a bigger first-pass structure.

4. A should keep `primary_link` prominent.
   `48` thin bundles make this too central to leave implicit.

## 6. What This Teaches Us About Proposal B

Concrete refinements now supported by the corpus:

1. B was right to drop `local_page.mode`.
   The corpus still looks binary enough on readiness that a nested mode field
   was paying cost without earning new truth.

2. B’s strongest grouped objects are now clearly:
   - `time`
   - `venue`
   - `classification`
   - `identifiers`

3. B should treat `classification.listing_group` as retained consumer-facing
   grouping, not as canonical semantic type.

4. B should justify itself mainly on:
   - cleaner grouped time semantics
   - cleaner grouped venue semantics
   - clearer distinction between page grouping and publication type

5. B should not pretend to solve venue/container semantics yet either.

## Current Read After The Concrete Pass

The concrete pass strengthens Proposal A more than Proposal B.

Why:

- the required `pub_type` field now feels more justified than before
- treating `listing_group` as non-authoritative semantics further strengthens
  the need for a real canonical classification field
- the local-page seam looks even more binary than before, which weakens one of
  B’s earlier differentiators
- the strongest current semantic wins still fit inside A’s flatter shape

Proposal B still has real appeal as a cleaner long-term grouping of semantic
clusters.
But after the concrete pass, the remaining choice is even narrower:

- do grouped `time` / `venue` / `classification` objects justify their extra
  migration and authoring cost now?

My current answer remains:

- probably not yet

That is not because B is wrong.
It is because the concrete corpus evidence now makes A’s first-pass semantic
payload feel more credible and sufficient than it did before.
