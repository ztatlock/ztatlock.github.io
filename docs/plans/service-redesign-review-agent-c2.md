# Service Redesign Review: Agent C2

Status: parent-authored fallback review

This review was written as a fallback after a delegated reviewer process failed
in this environment. It is intentionally kept separate from the genuine
delegated review in
[service-redesign-review-agent-a.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-review-agent-a.md).

Inputs reviewed:

- [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)
- [service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md)
- `/Users/ztatlock/Downloads/foo/service-model-proposal-claude.md`
- `/Users/ztatlock/Downloads/service-model-proposal-claude.md`

Proposal mapping for this review:

- Proposal A:
  [service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md)
- Proposal B:
  `/Users/ztatlock/Downloads/foo/service-model-proposal-claude.md`
- Proposal C:
  `/Users/ztatlock/Downloads/service-model-proposal-claude.md`

This review follows the requested rotation order:

1. pass 1: Proposal C
2. pass 2: Proposal A
3. pass 3: Proposal B

The perspective in this review is intentionally robustness-biased:

- upweight future backfill uncertainty
- upweight anchor and multi-view stability
- accept extra schema if it eliminates recurring design churn
- be skeptical of leaving too much service meaning as implicit derived code

## Executive View

My current ranking is:

1. **Proposal A**
2. **Proposal C**
3. **Proposal B**

My current recommendation is:

- the repo should likely migrate
- the real decision is between A and C
- if the repo wants the strongest chance of not revisiting service structure
  again in a year, **Proposal A** is the safer destination
- if the repo decides that canonical run identity is still too consumer-shaped,
  then Proposal C is the acceptable second-best

The key question from this review is:

- does the repo believe `run` is merely a renderer convenience, or is it
  actually the stable public-facing unit that homepage and `/service/` need?

I come out leaning that it is stable enough, and important enough, to deserve
explicit representation.

## Pass 1: Proposal C

### Summary Judgment

Proposal C is strong. It is materially stronger than Proposal B, and it
understands the repo’s established “identity plus nested instances” pattern
well.

If Proposal A did not exist, Proposal C would probably be my recommendation.

Its weakness is not that it is sloppy.
Its weakness is that it still treats several genuinely important service ideas
as derived conveniences rather than canonical structure.

### What Proposal C Gets Right

#### 1. It chooses the right minimum structural fix

Proposal C correctly identifies that the current model’s biggest flaw is:

- explicit instances
- but only implicit recurring identity

By making recurring series structural, it removes the worst current seam:

- no more `series_key` pointing nowhere
- no more field-equality grouping pretending to be ontology
- much less duplication

That is already a major improvement.

#### 2. It handles one-offs honestly

The singleton-versus-series split is not a weakness here.
It is a strength.

The requirements explicitly warn against forcing false structure on one-offs,
and Proposal C respects that.

Dagstuhl-style entries remain:

- simple
- local
- not wrapped in fake recurring identity machinery

That is good design.

#### 3. It inherits the best part of the teaching pattern

Proposal C adapts the teaching model in a disciplined way:

- outer identity when there is one
- nested year-local instances
- derived consumer views on top

That is familiar and likely maintainable in this repo.

#### 4. It avoids prematurely canonizing runs

This is Proposal C’s best argument against Proposal A.

Runs are real, but they are also:

- derived from year continuity
- subject to reinterpretation under backfill
- closely tied to rendering and anchor policy

Proposal C says:

- keep them derived
- keep canonical data closer to fact ownership

That is an intellectually clean position.

### Where Proposal C Still Falls Short

#### 1. It still treats too many critical semantics as derived

This is my main objection.

The strengthened requirements surfaced that the hard problems are not just:

- recurring identity

but also:

- non-contiguous runs
- stable visible anchors
- section-safe multi-view rendering
- details at the right visible grouping level

Proposal C does not ignore these.
It just keeps them in code.

I think that leaves too much pressure where the repo is already hurting:

- projection helpers
- grouping helpers
- anchor conventions

#### 2. Anchor stability is still not fully convincing

Proposal C’s anchor rules are thoughtful, but they are still a derived
convention layered on top of:

- series key
- run partitioning
- run boundary interpretation

That means the thing we actually link to publicly is not itself canonical.

Given how much of the service discussion has centered on anchor identity, I
think that remains a meaningful weakness.

#### 3. Multi-view section semantics still feel bolted on

Proposal C supports instance-level `view_groups` overrides, which is good.
But it still does not name one stable visible grouped unit that can cleanly say:

- “this is the thing shown here”
- “this is the thing the homepage should link to”
- “this is the thing that owns this anchor”

Proposal A’s `run` plus `primary_view_group` is heavier, but it answers this
more directly.

#### 4. Same-year multiplicity still needs a follow-on design decision

Proposal C acknowledges same-year multiplicity, but the model still feels
slightly provisional there:

- year plus array position
- maybe later an instance key

This is not fatal.
It is just a sign that the design is not quite closed under all of its own
requirements.

### Bottom Line On Proposal C

Proposal C is:

- clean
- plausible
- much better than the current model

But it still leaves enough heavy lifting in derived code that I do not think it
fully closes the service-design chapter.

## Pass 2: Proposal A

### Summary Judgment

Proposal A is the strongest answer to the actual requirements as written.

Its most important strength is not elegance.
It is closure.

Proposal A is the first design that makes me think:

- yes, this likely stops the recurring conversation about what the real visible
  unit is
- yes, this gives anchors a real canonical home
- yes, this makes multi-view service entries legible without more hidden glue

That matters.

### What Proposal A Gets Right

#### 1. It names the three real layers explicitly

The service redesign work kept circling three concepts:

- exact year-local facts
- visible grouped entries
- broader recurring identity

Proposal A simply accepts that all three are real.

That acceptance removes a large amount of downstream ambiguity.

#### 2. `run` is the right canonical visible unit

This is the core of Proposal A.

I think the audit supports it more than the simpler proposals want to admit.

Why?

Because the hard service questions are mostly about:

- what the homepage shows
- what the service page anchors
- what the service page groups
- what multi-view entries point to

Those are all run-level questions.

If the repo is going to care deeply about those questions, canonically
representing `run` is not over-modeling.
It is accuracy.

#### 3. It gives anchors a real identity independent of re-derivation

The stronger requirements are unusually anchor-heavy.
That is not accidental.

Service is becoming a more linked, more projected, more multi-consumer domain.

Proposal A’s run keys solve that directly:

- stable visible identity
- stable public target
- explicit internal link destination

This is a serious advantage over both B and C.

#### 4. It handles multi-view facts best

The requirements explicitly care about:

- multi-view membership
- no duplicate truth
- no anchor ambiguity
- section-safe behavior

Proposal A’s `primary_view_group` is the first mechanism that gives these
requirements a crisp canonical answer.

It is slightly inelegant, but usefully so.

#### 5. It has the best story for run-level details

The audit found that details can meaningfully belong at:

- instance level
- run level
- possibly series level

Proposal A is the only proposal that directly names all three without forcing
renderers to improvise.

That is exactly the kind of seam a redesign should eliminate.

### What Proposal A Complicates

#### 1. It is unquestionably the heaviest schema

This is real.

Authors would need to understand:

- series
- runs
- instances
- field ownership across levels
- primary view groups
- run keys
- time-basis hints

That is more to hold in one’s head than in Proposal C.

#### 2. Migration requires more judgment

Proposal A is not a purely mechanical transform.

It requires explicit choices about:

- run boundaries
- run keys
- metadata placement
- primary view groups

That is cost.

I still think the cost may be worth it, but it is real.

#### 3. It risks over-specifying the current rendering worldview

This is Proposal A’s biggest philosophical risk.

If future service consumers change the meaning of the “best visible unit,” then
Proposal A may feel too concretized around today’s projection concerns.

I think this risk is real.
I just think the current service audit evidence is strong enough to accept it.

### Bottom Line On Proposal A

Proposal A is heavy, but for reasons that track the hardest actual service
requirements.

I believe that makes it the strongest design.

## Pass 3: Proposal B

### Summary Judgment

Proposal B now reads as the least convincing of the three.

It still makes a huge improvement over the current flat model, but it now feels
like a design that optimizes elegance and editability a little too aggressively
relative to the harder requirements.

### What Proposal B Gets Right

#### 1. It reduces duplication dramatically

This is undeniable.

For things like:

- `uw-faculty-skit`
- `pacmpl-advisory-board`
- `fptalks`

Proposal B makes the data smaller and clearer.

#### 2. It makes recurring identity explicit

Like Proposal C, this is a major structural improvement over the current model.

#### 3. It uses a single uniform pattern

There is real beauty in:

- one identity block
- nested instances
- one validation path

That should not be dismissed.

### Why Proposal B Still Comes Last

#### 1. Uniform shape is not actually the most honest shape

The service domain really does have:

- one-offs
- recurring identities

Proposal B’s insistence that both should use the same wrapper feels more like
schema tidiness than domain clarity.

#### 2. It underestimates run-level requirements

Proposal B derives runs, anchors, labels, and visible grouping from a nested
identity structure, but it still does not give run-level semantics enough
status.

The strengthened requirements made run-level seams much more central:

- non-contiguous runs
- stable anchors
- run-level details
- visible unit identity

Proposal B does not answer those as directly as Proposal A, and not as
flexibly as Proposal C.

#### 3. It has the weakest same-year multiplicity story

Proposal B’s “year unique within identity” assumption now looks brittle.

The requirements explicitly warn against overfitting to current cleanliness,
and Proposal B does that more than the others.

#### 4. Multi-view handling still feels too identity-centric

Proposal B’s identity-level `view_groups` works until it doesn’t.

Once the requirements insist that membership may differ at multiple
granularities, Proposal B starts to feel under-specified.

### Bottom Line On Proposal B

Proposal B is useful as a design stepping stone.
I would not choose it now.

## Comparative Section

### Common Ground Across All Three

All three proposals correctly see that the current flat model is under too much
pressure.

All three improve materially on:

- implicit recurring identity
- repeated metadata
- brittle grouping from scattered per-year records

So the redesign conversation is now productive. The disagreement is no longer
“whether to redesign,” but “how far to go.”

### The Real Decision Boundary

The real decision is:

- **Proposal A** if the repo wants to make visible run identity canonical
- **Proposal C** if the repo wants to keep visible run identity derived

That is the central design fork.

Proposal B is no longer the leading option once the requirements are taken
seriously.

### When Proposal A Is Better

Proposal A is better if the repo prioritizes:

- explicit stable run anchors
- explicit visible-unit identity
- explicit multi-view run home
- explicit run-level metadata ownership
- maximum reduction in downstream projection ambiguity

### When Proposal C Is Better

Proposal C is better if the repo prioritizes:

- simpler canonical JSON
- less authored structural bookkeeping
- keeping more view semantics in code
- staying closer to the teaching-style identity/instances pattern

### Is Migration Worth It?

Yes.

The current service model already required:

- prolonged audit work
- requirements extraction
- anchor redesign discussions
- grouped-view redesign discussions

That is enough evidence that the current flat model is not the right
long-horizon foundation.

### Recommendation

My recommendation from this review is:

1. Retire Proposal B from the lead position.
2. Make the next decision explicitly between Proposal A and Proposal C.
3. Prefer Proposal A if the repo wants the redesign to fully absorb the anchor,
   run, and multi-view seams into canonical structure.
4. Prefer Proposal C only if the repo decides that canonical data should stop
   strictly at identity-plus-instance and keep runs as a derived layer on
   principle.

My own lean is:

- **Proposal A** is the better long-horizon redesign
- **Proposal C** is the better compromise if the repo decides A is too heavy
