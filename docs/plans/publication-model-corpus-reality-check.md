# Publication Model Corpus Reality Check

Status: proposal-grounding note

It builds on:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-proposal-b-semantic-objects.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-b-semantic-objects.md)
- [publication-model-proposals-patch-list.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-patch-list.md)

## Purpose

Ground the current proposal discussion in the actual indexed publication
corpus.

This note focuses on the three pressure points that currently matter most:

1. venue cleanup and compact venue labels
2. `pub_type` feasibility
3. canonical year vs exact date semantics

## Corpus Size

Current non-draft indexed publication corpus:

- `69` bundles
- `58` `listing_group: main`
- `11` `listing_group: workshop`

## 1. Venue Cleanup Reality Check

### High-Level Result

The venue cleanup problem is real but mostly tractable.

Observed facts:

- `68/69` current indexed publication venue strings end in a parenthetical
  suffix of the form `(...SHORT...)`
- the only current non-parenthetical exception is:
  - `<Programming>`

That means a full/compact split is not speculative.
It matches the current corpus very closely.

### Mechanically Clean Cases

For the large majority of bundles, a split such as:

- full venue = text before the final parenthetical
- compact venue = text inside the final parenthetical

would work mechanically and honestly.

Examples:

- `Programming Language Design and Implementation (PLDI)`
  - full: `Programming Language Design and Implementation`
  - compact: `PLDI`
- `Architectural Support for Programming Languages and Operating Systems (ASPLOS)`
  - full: `Architectural Support for Programming Languages and Operating Systems`
  - compact: `ASPLOS`
- `ACM Transactions on Graphics (TOG)`
  - full: `ACM Transactions on Graphics`
  - compact: `TOG`

### Current Awkward Cases

The compact-label cases that deserve explicit thought are:

- `USENIX Security Symposium (SECURITY)`
  - compact candidate `SECURITY`
- `Software Correctness for HPC Applications (CORRECTNESS)`
  - compact candidate `CORRECTNESS`
- `ACM SIGPLAN International Symposium on SPLASH-E (SPLASH-E)`
  - compact candidate `SPLASH-E`
- `<Programming>`
  - no parenthetical compact suffix at all

Interpretation:

- these are not arguments against a compact-venue field
- they are arguments for making the compact label an honest authored value,
  not a rigid acronym heuristic

### Equality Cases

The corpus already gives at least one case where:

- full venue
- compact venue

may legitimately be identical:

- `<Programming>`

That means any future `venue_short` or `venue.short` semantics should allow:

- compact label equals full label

without treating that as a schema smell by itself.

### Repeated Compact Labels

The most repeated compact venue labels in the current corpus are:

- `PLDI` (`10`)
- `OOPSLA` (`5`)
- `POPL` (`5`)
- `SNAPL` (`3`)
- `CoqPL` (`2`)
- `CAV` (`2`)
- `CPP` (`2`)
- `NSV` (`2`)
- `ICFP` (`2`)
- `CORRECTNESS` (`2`)
- `TOG` (`2`)
- `ASPLOS` (`2`)

This is good evidence that compact venue labels are not one-off homepage
formatting sugar.
They capture repeated venue identity visible in the current corpus.

## 2. `pub_type` Feasibility Check

### High-Level Result

A small required `pub_type` vocabulary looks feasible.

The current indexed corpus appears to be classifiable with a small set such
as:

- `conference`
- `journal`
- `workshop`

with optional room later for:

- `tech-report`
- `book`
- `book-chapter`
- `misc`

### Current Corpus Shape

With a lightweight first-pass classification:

- all `listing_group: workshop` bundles naturally map to `pub_type: workshop`
- most `listing_group: main` bundles naturally map to `pub_type: conference`
- a small number of main bundles look naturally like `journal`

Current obvious journal-like indexed records include:

- `2011-lmcs-eqsat`
- `2019-siga-carpentry`
- `2022-tog-carpentry`
- `2024-programming-magicmarkup`
- `2024-todaes-3la`
- `2024-tog-illusionknitting`

### Implication

This makes one strong option look plausible:

- require `pub_type`
- keep the first vocabulary deliberately small

That avoids the “optional field that never gets backfilled” trap while still
keeping the first pass manageable.

### Caveat

The current quick pass is enough to show feasibility, not enough to settle
every borderline case.

So if `pub_type` is made required, the proposal should still say:

- the first-pass vocabulary is intentionally small
- exact finer-grained distinctions can come later

## 3. Canonical Year vs Exact Date Reality Check

### High-Level Result

The current corpus contains a small but real seam between:

- slug-embedded year
- exact `pub_date` year

Observed facts:

- `66/69` indexed bundles currently have matching slug year and
  `pub_date.year`
- `3/69` indexed bundles currently do not

The current mismatches are:

- `2016-nsv-fpbench`
  - slug year `2016`
  - `pub_date` `2017-02-17`
- `2017-icalepcs-neutrons`
  - slug year `2017`
  - `pub_date` `2018-01-01`
- `2018-popl-disel`
  - slug year `2018`
  - `pub_date` `2017-12-27`

### Interpretation

This is exactly the kind of seam the requirements are trying to surface.

The mismatch cases look like plausible publication-year vs exact-date issues,
not like arbitrary bad data.

That means:

- canonical publication year should not be derived only from exact date
- exact `pub_date` still remains useful

### Implication

A proposal that introduces explicit canonical year metadata is justified by
the real current corpus, not only by hypothetical future backfill.

It also means the proposals should stop treating “slug year retirement” as
optional hand-waving.
The corpus already demonstrates why canonical year and exact date need to be
separate concepts.

## Overall Conclusions

The corpus reality check strengthens a few conclusions:

1. A venue split is justified by the current corpus.
2. Compact venue labels should be authored honestly, not derived by a rigid
   rule.
3. A small required `pub_type` vocabulary now looks feasible.
4. Explicit canonical year metadata is justified by the current corpus.
5. The hardest real questions are no longer whether these seams exist.
   They do.
   The question is how cleanly A or B chooses to represent them.

## Current Recommendation

The next proposal refinement pass should assume:

- compact venue support is real and should be explicit
- full and compact venue labels may legitimately be identical in some cases
- canonical year metadata should become the display-year source
- `pub_type` is a serious candidate for a required small-vocabulary field

That should tighten the next A/B comparison substantially.
