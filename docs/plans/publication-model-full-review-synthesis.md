# Publication Model Full Review Synthesis

Status: pre-refinement synthesis note

It synthesizes:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-proposal-b-semantic-objects.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-b-semantic-objects.md)
- [publication-model-proposals-claude-review-1.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-1.md)
- [publication-model-proposals-claude-review-2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-2.md)
- [publication-model-review-agent-1.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-1.md)
- [publication-model-review-agent-2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-2.md)
- [publication-model-review-agent-3.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-3.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)

## Purpose

Capture the state of the publication-model design after:

- requirements iteration
- external review
- internal subagent review
- Xavier Leroy comparison
- one round of proposal tightening

This note is not another proposal.
It is a checkpoint before the next concrete corpus-backed refinement pass.

## Current Read

The requirements now look stable enough.

The strongest remaining disagreements are no longer about hidden consumer
needs.
They are about physical schema shape and how much structure is worth paying
for now.

That is good.
It means the design work has surfaced the real fork.

## What Now Feels Settled

The following points now look settled across the requirements, audits, and
proposal reviews:

1. Canonical publication-year semantics must be explicit.
   Display consumers should stop treating slug-year parsing as the primary
   source of truth.

2. Full and compact venue display are distinct facts.
   Compact venue labels should be authored honestly, not reverse-engineered
   heuristically from bibliography strings.

3. `primary_link` remains first-class.
   Thin bundles still need an explicit title-destination selector.

4. `person_key` should stay out of this pass.
   Current publication consumers do not justify a stronger author-identity key
   yet.

5. A small required `pub_type` vocabulary is now plausible.
   The current indexed corpus looks manageable enough that `pub_type` should
   probably be a real field rather than optional decorative metadata.

6. Venue identity across papers remains future work.
   Both proposals now acknowledge this honestly rather than pretending the
   first pass solves it.

## Updated Decision Surface

After the latest tightening, the real choice is now:

- **Proposal A**
  - disciplined flat schema
  - explicit `pub_year`, `venue_short`, `pub_type`, `local_page`,
    `primary_link`, `identifiers`
  - smaller migration
  - stronger backfill ergonomics

- **Proposal B**
  - grouped semantic objects only where they clearly earn it:
    - `time`
    - `venue`
    - `classification`
    - `identifiers`
  - keeps `local_page` and `primary_link` flat after review pressure showed
    that `local_page.mode` was not earning its keep
  - cleaner long-term semantic clustering
  - heavier migration

That means B is now more disciplined than before, and A is now more honest
than before.

## Current Lean

Proposal A still looks like the leading direction.

Why:

- it now captures most of the clearly needed semantics
- it preserves simpler authoring before larger backfill lands
- much of B's semantic-organizing value could still be recovered in a richer
  normalized in-memory model after parse, even if the authored JSON stays
  simpler
- B’s main remaining advantage is cleaner grouping, not a decisive semantic
  capability that A lacks right now

Proposal B still matters as the strongest counter-pressure against flat-field
sprawl.
It may yet win if the next concrete refinement pass shows that the grouped
shape materially reduces real corpus awkwardness.

## What The Next Refinement Pass Should Prove

The next concrete corpus-backed refinement pass should not revisit abstract
taste questions first.
It should test the now-sharper proposals against the actual indexed corpus.

The most useful proof work is:

1. draft concrete venue cleanup for the real corpus under both proposals
2. draft concrete `pub_type` assignments for the real corpus
3. explicitly map current consumers from slug-year display to canonical-year
   display
4. see whether B’s grouped shape actually makes the cleaned corpus feel more
   truthful or merely more nested

That should teach us more than another round of purely abstract comparison.
