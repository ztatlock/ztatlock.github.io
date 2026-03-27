# Service Redesign Proposal A2 Patch List Review 2

Status: draft

This note captures the current response to the second external review of
[service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md).

It complements, rather than replaces:

- [service-redesign-proposal-a2-patch-list.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2-patch-list.md)

The main purpose of this note is to record:

- which points from the second review are genuinely new
- which points strongly confirm the first review
- which changes should probably be patched into A2
- and which suggested framings should be adjusted before adoption

## Overall Judgment

This review is strongly positive for A2.

It reinforces several conclusions already reached after the first review:

- A2 is materially better than A1
- the remaining issues are refinement-level, not structural
- the biggest remaining risks are semantic clarity and validator precision,
  not the underlying model choice

It also adds several useful new refinements, especially around:

- preferred-form guidance
- the public statement of the rehydration contract
- example quality
- the risk of under-specifying contiguity in shorthand and other implicit runs

So the right response is again:

- keep A2 as the leading direction
- tighten the proposal
- do not reopen the larger structural choice

## Strong Confirmations From Review 2

These points do not create new design pressure so much as confirm that earlier
concerns were real and correctly targeted.

### 1. A2 Is Strictly Better Than A1 Physically

The review is right that A2 improves all the practical weak spots of A1:

- flat singletons
- self-contained common recurring records
- optional instance keys
- no separate top-level `series` and `runs` arrays
- cleaner common editing flow

This confirms that the A2 pass was the right move, not a cosmetic distraction.

### 2. Canonical Run Is Still The Winning Semantic Bet

The review again confirms the central design point:

- A2 preserves the real semantic win from A1:
  - canonical `series`
  - canonical `run`
  - atomic `instance`

The shorthand forms are physical sugar, not semantic retreat.

This is important because it confirms that the main seam now lives in the
proposal text and validation contract, not in the model choice.

### 3. Rehydration Is A Real Seam But A Manageable One

The review is right to call rehydration out as a seam:

- the authored JSON and the loaded model are not identical
- debugging therefore requires understanding both

But this is not a structural objection.
It is a prompt to document the contract more clearly.

This point should be patched into A2 as a documentation improvement, not taken
as a reason to retreat from A2.

## Accept

These suggestions should be adopted with little or no change.

### 1. Fix The PLDI Program Committee Chair Example

The review is right that the current singleton example teaches the wrong habit
by baking role into title:

- `title: "PLDI Program Committee Chair"`

That fights the label-composition direction we want.

The example should instead separate:

- `title: "PLDI"`
- `role: "Program Committee Chair"`

Why accept:

- it better matches the rendering goals already discussed
- it demonstrates the schema more honestly
- it avoids training the wrong authoring instinct

### 2. Add A Preferred-Form Guideline

The proposal should explicitly say:

- use the lightest authored form whose constraints are not violated

Why accept:

- it reduces inconsistent authoring
- it makes the physical ergonomics story legible
- it turns an already implicit design preference into an explicit one

Concrete patch:

- add a short `Preferred Form` subsection after the three authored forms or in
  the validation section

### 3. Add A Rehydration Contract Note

The proposal should explicitly say:

- the JSON is the authored source
- the loaded Python model is the canonical semantic representation
- consumers must operate on the loaded model, not raw JSON
- the loader's normalization rules are the authoritative mapping

Why accept:

- this is already how A2 works conceptually
- the review is right that the contract should be stated plainly
- it makes debugging and implementation expectations cleaner

Concrete patch:

- add a short `Rehydration Contract` section near canonical semantics or
  consumer semantics

## Adjust

These review points are valuable, but the exact proposed fix should be
modified before adoption.

### 1. Contiguity Needs To Be Stronger Than The Proposal Currently Says

This is the most important new pressure from the second review.

The reviewer is right that the current proposal leaves too much room for a
dangerous implementation mistake:

- a shorthand record could incorrectly encode non-contiguous years
- the loader could then silently invent one fake run

Current judgment:

- yes, A2 should explicitly state that a canonical run is intended to contain
  one contiguous year sequence
- yes, shorthand form should not be allowed to encode non-contiguous years
- yes, the validator should probably enforce this for shorthand records

But I would refine the proposal more broadly than the review's wording:

- the contiguity principle belongs to **canonical runs**, not only to the
  shorthand form
- shorthand is just the most obvious place where violating the rule would be a
  silent foot-gun

Open caution:

- the requirements still mention partial or uncertain historical knowledge
- so if we add a hard validator rule, the proposal should also acknowledge that
  future uncertainty modeling may eventually need a more nuanced mechanism

Concrete patch:

- add a semantic statement in the run section:
  - a canonical run represents one contiguous span of service years
- add a validation statement:
  - shorthand records with non-contiguous years are invalid
- likely also say:
  - explicit multi-instance runs are expected to be contiguous unless/until a
    future uncertainty design says otherwise

### 2. Shorthand Field Ownership Needs Better Framing

The review is right that shorthand form creates a subtle ambiguity:

- physically, some top-level fields are treated as implicit run-level facts
- conceptually, those same facts may also feel true of the one-run recurring
  identity as a whole

The review proposes saying such fields are semantically both series-level and
run-level.

I would adjust that slightly.

Current judgment:

- the proposal should **not** say that every shorthand field literally belongs
  to both levels in the normalized model
- but it **should** say that shorthand intentionally collapses the distinction
  where it does not matter yet

So the better patch is:

- state that shorthand form deliberately merges series and sole-run authoring
  concerns into one compact record
- state that the loader normalizes these facts into the canonical series/run
  model
- state that if the distinction between series-level and run-level ownership
  starts to matter, the record should be promoted to explicit form

This keeps the highest-true-level discipline while acknowledging why shorthand
can still feel a little dual-purpose to human readers.

### 3. "These Three Forms Are Final" Should Be Softened Slightly

The review suggests saying:

- these three forms are the complete set
- no further shorthand forms should be introduced

The underlying instinct is good.
Form proliferation would be a real risk.

But I would soften the exact wording.

Current judgment:

- yes, the proposal should strongly prefer these three forms as the intended
  complete authored surface
- but it should avoid pretending no future redesign could ever revisit that

Better phrasing:

- these three forms are the intended authored forms for this redesign
- adding further shorthand forms should be treated as a redesign-level change,
  not as an ordinary incremental extension

That gives the right stability signal without pretending to know the future too
absolutely.

### 4. Singleton -> Recurring Promotion Wants A Short Note

This review usefully surfaces one subtle promotion case:

- a singleton may later become a recurring identity
- the existing singleton key may be a good stable run key
- but a broader recurring `series.key` might want a cleaner, non-year-prefixed
  identity

Current judgment:

- this is real and should be noted
- the safest future-proof promotion path is likely:
  - keep the old singleton key as the first run key
  - introduce a cleaner new series key if needed
  - promote directly to explicit form when preserving old anchors matters

This is not a structural problem.
It is just a promotion rule worth stating once.

Concrete patch:

- add a brief note in the promotion guidance section once that section exists

## Reject

These suggestions should not be adopted exactly as written.

### 1. Say Shorthand Fields Are Simply "Both Series-Level And Run-Level"

Rejected as the final wording.

Reason:

- it blurs the normalized ownership model too much
- it risks weakening the "highest level where the fact remains true" principle

The better framing is the adjusted version above:

- shorthand intentionally collapses the distinction at authoring time
- normalization still maps to one canonical series/run structure

### 2. Treat Contiguity As Merely A Shorthand Concern

Rejected as too narrow.

Reason:

- the real invariant belongs to canonical `run`
- shorthand is just the easiest place to violate it by accident
- the proposal should not imply that explicit runs are free to become
  non-contiguous blobs

## Concrete Patch Sequence

If we patch
[service-redesign-proposal-a2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a2.md)
using this second review as input, the best sequence is:

1. Fix the PLDI singleton example.
2. Add a preferred-form guideline.
3. Add a rehydration contract section.
4. Strengthen the run-contiguity statement and shorthand validation rule.
5. Clarify shorthand as an intentional collapse of series/run distinction where
   it is not yet worth separating.
6. Add a singleton-to-recurring promotion note.
7. Add a strong-but-not-absolute statement that these three forms are the
   intended authored surface for the redesign.

## Current Bottom Line

After this second review, the conclusion is even clearer:

- A2 still looks like the best design direction
- the remaining work is specification tightening, not model replacement

The most important new pressure from this review is:

- contiguity should probably be specified more strongly than the current A2
  draft does

Everything else is an improvement pass, not a reason to back away from A2.
