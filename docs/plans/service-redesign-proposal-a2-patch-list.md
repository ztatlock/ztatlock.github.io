# Service Redesign Proposal A2 Patch List

Status: draft

This note captures the current patch list against
[service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md)
based on the first external review of A2.

It is intentionally a **response and patch-planning note**, not the proposal
itself.

The goal is to preserve:

- which feedback seems correct
- which feedback should be adopted but adjusted
- which feedback should be rejected
- and what concrete edits we should probably make to the A2 proposal before
  treating it as final

## Overall Judgment

The review increases confidence in A2.

It does **not** reveal a structural flaw in the design.
It mostly reveals places where the proposal should be:

- more explicit about semantics
- clearer about validation boundaries
- sharper about shorthand promotion rules

So the right response is a tightening pass on A2, not a redesign pivot.

## Accept

These suggestions should be applied to
[service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md)
essentially as-is.

### 1. Add An Explicit Inheritance Rule

The proposal should say plainly:

- resolved value order is `instance -> run -> series -> absent`
- the first level that provides a value wins
- omitted fields inherit
- there is no implicit null/clear mechanism in the initial design

Why accept:

- the current intent is already this
- the review is right that the rule is too implicit
- this is exactly the kind of hidden convention the redesign is trying to
  avoid

Concrete patch:

- add one short `Inheritance` section near the canonical-semantics or
  field-ownership discussion

### 2. Add A Promotion Note For Shorthand -> Explicit

The proposal should explicitly say:

- when a shorthand single-run series is promoted to explicit form,
  the original run should keep the old series key as its run key whenever that
  preserves existing anchors cleanly

Why accept:

- this is the right anchor-stability discipline
- the current proposal implies it but does not say it clearly enough

Concrete patch:

- add a `Promotion Rule` note in the shorthand or run-key section

### 3. State Global Canonical Run-Key Uniqueness Explicitly

The proposal should explicitly require:

- all canonical run keys must be globally unique across the entire file
- this includes:
  - singleton keys used as run keys
  - shorthand series keys used as implicit run keys
  - explicit run keys inside multi-run series

Why accept:

- anchor ids live in one global `/service/` document namespace
- the current proposal relies on this but does not state it directly

Concrete patch:

- add one bullet to the run-key rules
- mirror it in the validation section

### 4. Add A Cross-Form Field-Ownership Summary

The proposal should restore a compact conceptual ownership summary similar to
the stronger section in Proposal A1.

It should summarize:

- `title`
- `role`
- `url`
- `details`

across:

- `series`
- `run`
- `instance`

Why accept:

- the current per-form explanations are locally clear
- but the cross-form conceptual picture is harder to see at once
- the review is right that A1 was stronger on this point

Concrete patch:

- add a short `Field Ownership Summary` section after the three authored forms
  or near validation

### 5. Make The Shorthand Tradeoff Explicit

The proposal should explicitly state that shorthand is an intentional
authorial bet:

- in shorthand form, non-title metadata is treated as run-level for now
- if series-level vs run-level distinction later starts to matter,
  the record should be promoted to explicit form

Why accept:

- this is already the practical design
- making it explicit will reduce later confusion during promotion

Concrete patch:

- add a paragraph under `Important Constraint` in the shorthand section

## Adjust

These review points are valuable, but the exact proposed fix should be changed.

### 1. `ongoing` On Singletons

Review suggestion:

- forbid `ongoing` on singletons

Adjusted response:

- do **not** forbid it
- instead clarify what it means on a singleton

Current view:

- a singleton means "no recurring series identity is being modeled here"
- it does **not** necessarily mean "this run cannot be open-ended"
- an ongoing one-off appointment can still make sense as one open-ended run
  without a broader recurring identity

So the better patch is:

- explicitly define singleton `ongoing` as:
  - an open-ended run with no separate recurring series identity currently
    modeled
- note that if a broader recurring identity later matters, the record can be
  promoted

Concrete patch:

- clarify singleton `ongoing` semantics in the singleton form section
- possibly add a validation note that `ongoing` on a singleton is allowed, but
  only as a run-level property

### 2. Contiguity Within A Run

Review suggestion:

- single runs should contain only contiguous years
- validator should reject year gaps

Adjusted response:

- adopt the **semantic rule** strongly
- be more cautious about the **validator rule**

Current view:

- yes, a run is supposed to represent one contiguous visible appointment/run
- non-contiguous service should normally be modeled as multiple runs
- but the requirements also want tolerance for partial or uncertain historical
  knowledge

So the right patch is probably:

- say clearly that a canonical run is intended to contain contiguous years
- say non-contiguous service should be promoted to explicit multiple runs
- defer the final validation strictness until we decide how uncertainty should
  be represented

Concrete patch:

- add a normative contiguity statement to the run semantics or validation
  section
- avoid committing yet to a harsh unconditional rejection rule in the proposal
  text

### 3. Synthesized Instance Keys

Review suggestion:

- define a public synthesis format like `{run_key}--{year}`
- validate collisions against authored keys

Adjusted response:

- specify the semantics more clearly
- but avoid turning synthesized ids into part of the authored public surface

Current view:

- the proposal is too vague today
- but a human-visible synthesis format is not ideal
- better is:
  - synthesized instance ids are deterministic
  - synthesized instance ids are internal loader artifacts
  - they live in a reserved namespace that cannot collide with authored keys

So the right patch is:

- specify that synthesized ids are internal-only
- define collision-avoidance behavior
- require explicit `instance.key` when same-year multiplicity makes synthesis
  insufficient

Concrete patch:

- rewrite the synthesis paragraph to use reserved internal ids rather than a
  public authored-looking string template
- add validator language forbidding authored keys from colliding with the
  reserved synthesis namespace

### 4. Validation Around Ordering

Review suggestion:

- add stricter validation for year ordering inside instances

Adjusted response:

- keep newest-first as a strong convention
- do not make descending order a foundational validity rule

Current view:

- canonical array order is already semantically meaningful
- there may be legitimate future reasons for authored order to carry intent
  that is not reducible to descending years
- this feels more like style guidance than core schema validity

Concrete patch:

- mention newest-first as the default norm
- keep canonical array order as the final truth
- do not require strict descending order in the core proposal

## Reject

These suggestions should not be adopted in their exact proposed form.

### 1. Forbid `ongoing` On Singletons

Rejected as proposed.

Reason:

- it overconstrains the model
- it collapses "no recurring series identity" into "cannot be an open-ended
  run"
- those are different concepts

The better fix is the adjusted clarification above.

### 2. Make Synthesized Instance-Key Format Part Of The Public Authored Contract

Rejected as proposed.

Reason:

- synthesized ids exist to support normalized internal identity
- they should not become a second authored naming surface unless a real
  consumer requires that
- otherwise we leak loader internals into the human-facing schema

The better fix is the adjusted internal-only synthesis rule above.

### 3. Turn Every Suspected Style Preference Into Hard Validation

Rejected as a general direction.

Reason:

- the review usefully identifies several semantic seams
- but not every style/default rule belongs in strict schema validation
- the redesign should stay strict where correctness depends on it and lighter
  where editorial judgment still matters

## Concrete Patch Sequence

If we patch
[service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md)
based on this review alone, the best order is:

1. Add explicit inheritance semantics.
2. Add global run-key uniqueness and shorthand-promotion anchor guidance.
3. Add a cross-form field-ownership summary.
4. Clarify shorthand as an intentional run-level defaulting form.
5. Clarify singleton `ongoing` semantics.
6. Tighten the run-contiguity language.
7. Tighten the synthesized-instance-id language without exposing it as public
   authored syntax.

## Current Bottom Line

This review should make the proposal better, not different.

It reinforces:

- A2 is probably the right structural direction
- the remaining work is mainly semantic clarification and validator-boundary
  clarity

So after this review, the leading stance is still:

- keep A2
- tighten it
- do not retreat from canonical runs
