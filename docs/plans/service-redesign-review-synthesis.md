# Service Redesign Review Synthesis

Status: draft

This note synthesizes the three real independent review files:

- [service-redesign-review-agent-a.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-a.md)
- [service-redesign-review-agent-b.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-b.md)
- [service-redesign-review-agent-c.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-c.md)

Additional fallback review tracks also exist:

- [service-redesign-review-agent-b2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-b2.md)
- [service-redesign-review-agent-c2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-c2.md)

## Important Note

The A/B/C reviews are the primary delegated-review corpus.

The B2/C2 reviews were written later as explicit fallback tracks while two
reviewer jobs appeared stalled. They are still useful as extra reading, but
they are not needed to establish the main independent-review result.

## High-Level Convergence

The three reviews converge strongly on several points.

### 1. The current flat service-term model is no longer the best long-horizon foundation

All three reviews agree that the redesign threshold has likely been crossed.

That convergence matters more than the proposal ranking.
It means the repo probably should not:

- finish the service audit
- shrug
- and then harden homepage recent-service on top of the current flat model

without a more serious redesign decision.

### 2. Proposal B is no longer the leading option

All three reviews put Proposal B last.

Why:

- it was designed against the earlier, weaker requirement set
- its uniform-shape elegance now looks somewhat overfit
- it underperforms on:
  - stronger run semantics
  - same-year multiplicity
  - multi-granularity `view_groups`
  - richer detail ownership

So the practical decision is no longer A vs B vs C.
It is A vs C.

### 3. The core design fork is whether `run` belongs in canonical data

This is the real question now.

Proposal A says:

- yes, `run` is the canonical visible unit

Proposal C says:

- no, `run` is still a derived layer over explicit series + instances

That is the most useful simplification of the whole debate.

## Where The Reviews Disagree

### Review A

Ranking:

1. Proposal A
2. Proposal C
3. Proposal B

Main thesis:

- Proposal A is the strongest full fit to the strengthened requirements
- Proposal C is attractive but still leaves too much run/anchor pressure in
  code

### Review B

Ranking:

1. Proposal C
2. Proposal A
3. Proposal B

Main thesis:

- Proposal C is the best balance of explicitness and restraint
- Proposal A is robust but canonically stores too much run-level structure too
  early

### Review C

Ranking:

1. Proposal A
2. Proposal C
3. Proposal B

Main thesis:

- Proposal A is heavy, but in ways that track the hardest actual requirements
- Proposal C is strong, but still leaves too much structural meaning in derived
  code

## What Seems Most Decision-Relevant

The disagreement is not random. It clusters exactly where it should:

- simplicity versus explicitness
- canonical run identity versus derived run identity

That suggests the next useful step is not another broad corpus audit.

It is a direct design decision on this question:

> Do we believe the stable public-facing service unit is a canonical `run`, or
> do we believe the stable canonical facts stop at `series` plus `instance`,
> with runs remaining a derived consumer layer?

## Current Synthesis Recommendation

My current synthesis recommendation is:

1. Treat Proposal B as no longer leading.
2. Carry forward both Proposal A and Proposal C.
3. Frame the next review explicitly around the `run in canonical data?` fork.
4. Do not proceed to homepage recent-service projection until that fork is
   resolved.

The real independent-review scoreboard is:

- **Proposal A** wins two of three reviews
- **Proposal C** wins one of three reviews
- **Proposal B** wins none

If forced to choose today, the synthesis lean is:

- **Proposal A** as the current leading candidate
- **Proposal C** as the clearest simplification-oriented fallback

That is a real fork, not a fake one.

## Suggested Next Move

The next best design conversation is narrower than the full redesign review.

Review just these two questions:

1. Should stable `/service/` anchor targets be canonical objects or derived
   objects?
2. Should run-level details and primary section membership be canonical or
   derived?

If the answer to both is “canonical,” Proposal A likely wins.
If the answer to both is “derived,” Proposal C likely wins.
If the answers split, the repo needs one more targeted design pass before
choosing.
