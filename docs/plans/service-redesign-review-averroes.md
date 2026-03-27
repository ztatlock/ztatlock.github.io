# Service Redesign Review: Averroes

Status: review draft

Inputs reviewed:

- Proposal A:
  [service-redesign-proposal.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal.md)
- Proposal B:
  `/Users/ztatlock/Downloads/foo/service-model-proposal-claude.md`
- Proposal C:
  `/Users/ztatlock/Downloads/service-model-proposal-claude.md`
- Requirements:
  [service-redesign-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-requirements.md)

This review follows the requested rotation:

1. pass 1 starts from Proposal B
2. pass 2 rotates to Proposal C
3. pass 3 rotates to Proposal A

The goal here is not to reward elegance in the abstract.
The goal is to test each design against the actual long-horizon requirements:

- represent the right granularities honestly
- survive future backfill
- keep editing hand-auditable
- keep validation tractable
- simplify consumers without hiding new seams in derived code

## Pass 1: Proposal B

Proposal B is the uniform identity-plus-instances model.
Every top-level record is a service identity.
Singletons are identities with one instance.
Runs are always derived in code from contiguous years.

### Main Strengths

Proposal B has a real simplicity story.
It is the cleanest of the three proposals if the only question is:

- "How do we stop repeating the same title, role, URL, and details across many
  year-local records?"

Its strongest qualities are:

- explicit recurring identity without a separate foreign-key-only `series_key`
  convention
- nested year-local instances that mirror the already-familiar
  course/offering shape in `teaching.json`
- a clear inheritance story for `role`, `url`, and `details`
- a strong reduction in duplicated metadata
- a hand-editable top-level shape that is still easy to scan in code review

The proposal is also honest about the current pain in the flat model:

- shared metadata is repeated too often
- series identity is currently implied rather than structurally owned
- run partitioning is currently derived from scattered records

For migration, Proposal B is attractive because it is conceptually local:

- group old flat records into identities
- hoist shared fields
- leave only varying facts on instances

That should make first backfill relatively straightforward.

### Requirements It Satisfies Well

Proposal B does well on these requirements:

- recurring identity is explicitly representable
- per-year atomic facts remain preservable
- URLs and details can live at more than one level
- role variation across years is possible
- data shrinks and becomes easier to audit
- future renderers have a clearer identity/instance split than today

It also gives a reasonably disciplined answer to "where should common facts
live?" without inventing a large taxonomy.

### Weaknesses

The deepest weakness is that Proposal B solves the duplication problem more
completely than it solves the visible-unit problem.

The requirements document repeatedly says that the visible unit for `/service/`
and homepage linking is high-risk:

- homepage wants a principled internal link target
- `/service/` wants grouped summaries and instance expansion
- anchors must survive appended years, backfill, multi-view rendering, and
  later non-contiguous runs

Proposal B keeps `run` entirely derived.
That looks simpler at first, but it pushes the hardest service problem into
derived code:

- what is the stable visible unit?
- what anchor owns it?
- what happens when a backfill extends a run backward?
- what happens when a later gap creates a second run?

Proposal B's own anchor section effectively concedes this.
It says anchor change under run-boundary backfill is acceptable because the
rendered content changed too.
That is in direct tension with the requirements, which explicitly say anchor
identity must not depend on fragile assumptions like start/end years never
changing after backfill.

That is not a cosmetic problem.
It means the proposal's cleanest simplification comes from relaxing one of the
strictest requirements.

### Hidden Seams

There are several seams Proposal B understates.

#### 1. Uniform shape quietly weakens the singleton requirement

The requirements say one-offs must remain first-class and should not be forced
into a fake series layer.

Proposal B says a singleton is "simply an identity with one instance."
That is elegant, but it is still a kind of conceptual wrapper around a one-off.
I do not think this is fatal, but it is a real semantic choice, not a free
win.

#### 2. Multi-view semantics are not actually simple once runs are derived

Proposal B allows instance-level `view_groups` override on top of series-level
defaults.
That is flexible, but it creates a hidden consumer question:

- is a run a run across all instances regardless of view group?
- or do different view-group projections effectively create different visible
  runs from the same identity?

This matters for:

- anchors
- primary link targets
- section ordering
- "which copy on `/service/` does the homepage link to?"

Proposal B does not really settle that.
It says the same anchor can be section-prefixed for multi-view identities, but
that still means visible-entry identity is partly section-derived rather than
intrinsic.

#### 3. Same-year multiplicity is only weakly addressed

Proposal B permits same-year multiplicity by array position.
That is technically enough to represent it, but it is not a strong long-term
identity story.

For hand-editing and validation, "same key + same year + array position"
becomes a brittle pseudo-identifier.
That is exactly the sort of hidden identity rule this repo usually tries to
avoid.

#### 4. No explicit home for run-level facts

Proposal B intentionally derives runs rather than modeling them.
That works while run-level metadata is thin.
But the requirements already hint that some facts may want to live at run
granularity:

- section membership may not be uniform forever
- details may be uniform across a run but not across the full series
- homepage internal linking really wants stable visible units

Proposal B does not fail outright here, but it clearly punts the run-level
question rather than resolving it.

### Migration Cost

Migration cost is moderate.

Compared to Proposal A, this is much cheaper:

- no separate run objects to author
- no second key layer for runs
- likely mechanical grouping from the current corpus

But it is not zero-cost:

- old singletons become identity blocks with nested instances
- shared metadata must be hoisted correctly
- instance overrides must be audited carefully
- same-year multiplicity and per-instance view-group overrides need validation
  conventions from the start

So this is a reasonable migration, but not as trivial as the proposal's tone
sometimes suggests.

### Likely Future Backfill Pain

Backfill pain is lower for data entry than Proposal A, but higher for consumer
stability.

Adding a year to a series is easy.
That is Proposal B's best operational property.

But later backfill of older years changes derived runs and therefore derived
anchors.
That means the proposal trades authoring ease for visible-target instability.

If the site later grows richer internal links, overlays, homepage anchors, or
cross-page references into `/service/`, this trade may age poorly.

### Validation Complexity

Validation is medium-to-high, not low.

Why:

- inheritance must be resolved consistently
- two different levels can own `role`, `url`, `details`, and `view_groups`
- same-year multiplicity needs stable interpretation
- anchor uniqueness and anchor stability both live in derived logic
- run partitioning becomes a semantic part of validation even though runs are
  not canonical data

So the JSON shape is simple, but the validator still has to understand derived
run semantics deeply.

### Consumer Implications

Consumers would improve compared to the current flat model, but not equally.

The public service page gets:

- cleaner grouping
- better summary labels
- easier instance expansion

The homepage gets:

- better than today, but still dependent on derived run anchors

The CV gets:

- straightforward range compression

So Proposal B improves all consumers, but it leaves the hardest homepage and
anchor semantics in code rather than making them first-class.

### Does It Truly Simplify The Long-Horizon Design?

Only partially.

Proposal B absolutely simplifies:

- duplication
- shared metadata ownership
- basic grouping
- editing for long uniform series

But it does not fully simplify:

- stable visible-unit identity
- anchor durability
- multi-view run semantics
- future richer internal linking

So I would describe Proposal B as:

- excellent at fixing the current flat-record duplication pain
- weaker at satisfying the strongest long-horizon `/service/` and homepage
  identity requirements

## Pass 2: Proposal C

Proposal C keeps the same general identity-plus-instance direction as Proposal
B, but changes one key design choice:

- one-offs stay true singleton records
- only recurring identities become nested series-with-instances records

Runs are still derived rather than canonical.

### Main Strengths

Proposal C is the most conservative design that still makes recurring identity
explicit.

Its core strengths are:

- one-offs remain genuinely first-class
- recurring series still get an explicit structural home
- the top-level `records` shape stays familiar
- the migration from the current flat model is comparatively understandable
- renderers still get co-located instances instead of scattered records

Relative to Proposal B, Proposal C reads more faithfully against the
requirements document's warning not to force one-offs into fake series.

This is its biggest advantage.

It also stays closer to the repo's bias for narrow models:

- no explicit run layer
- no separate series registry
- no top-level split between series and runs

That keeps the JSON more compact than Proposal A while still addressing much of
the current `series_key` design pressure.

### Requirements It Satisfies Well

Proposal C satisfies these requirements better than Proposal B:

- one-off entries remain first-class in a clear, literal way
- recurring identity becomes explicit
- atomic facts remain intact
- role/URL/detail inheritance has a natural place for recurring series
- migration can remain fairly mechanical

It is also a better fit than Proposal B if one thinks the requirements are
serious about:

- not pretending every service fact is a series
- preserving honest semantics for singletons

### Weaknesses

Proposal C still shares Proposal B's deepest long-horizon weakness:

- `run` remains derived
- stable anchor identity remains mostly derived
- backfill can still change visible run boundaries and therefore anchors

So while it improves the singleton story, it does not truly resolve the
highest-risk visible-unit requirement.

Its second major weakness is that the two-shape model is less cheap than it
first appears.

Proposal C presents itself as "minimal extra structure," but it introduces a
new conceptual branch:

- singleton record
- series record

That means:

- loader branching
- validation branching
- migration branching
- promotion seam when a singleton later becomes a recurring series

None of that is terrible, but it is real complexity.

### Hidden Seams

#### 1. Promotion from singleton to series is a real migration seam

Proposal C explicitly acknowledges the case where a one-off later becomes a
series and recommends possibly renaming the key.

That is a meaningful seam:

- either the old year-prefixed singleton key remains and becomes misleading
- or the key changes, which can affect future internal references

This is much less elegant than Proposal B's "same outer shape from day one."

#### 2. Derived run semantics still own too much

Like Proposal B, Proposal C says:

- run partitioning is mechanical
- summary labels are derived
- anchors depend on single-run vs multi-run status

This still means the most consumer-sensitive unit is not canonical data.

That leaves unresolved:

- what if a backfill changes single-run to multi-run?
- what if a run boundary changes?
- what if multi-view rendering wants a stable visible-unit target independent
  of section?

Proposal C improves modeling honesty for one-offs, but it does not resolve
that consumer seam.

#### 3. Same-year multiplicity remains under-modeled

Proposal C also leans on year plus array position for future same-year
multiplicity.
That is a weak identity rule.

It is enough for a sketch, but not a great long-horizon validation contract.

#### 4. Run-level metadata still has nowhere canonical to live

Because runs are derived, Proposal C still has no true home for facts that are
uniform across one run but not across the entire series.

The requirements explicitly highlight that URLs, details, roles, and even
view-group membership may want to live at more than one level.
Proposal C handles series-level and instance-level ownership, but leaves
run-level ownership as a derived convention rather than a modeled choice.

### Migration Cost

Migration cost is likely the lowest of the three proposals if measured only in
schema disruption.

Why:

- many current one-offs stay very close to their present shape
- recurring groups get nested
- the top-level `records` container survives
- no explicit run authoring is needed

That said, promotion logic and key policy for later-recurring singletons still
need to be settled up front.
Without that, migration may be easy initially but ambiguous later.

### Likely Future Backfill Pain

Backfill pain is mixed.

Good:

- adding years to an existing series is simple
- current one-offs stay easy to author

Bad:

- later promotion from singleton to series is awkward
- later anchor stability still depends on derived run behavior
- later backfill can still change rendered run boundaries

So Proposal C improves near-term authoring but still leaves future visible-unit
stability partly unsettled.

### Validation Complexity

Validation complexity is moderate.

Lower than Proposal A because:

- no explicit run registry
- no separate run keys
- less canonical structure overall

But not trivial because:

- there are now two record shapes
- inheritance must still resolve cleanly
- run partitioning and anchor rules remain semantic and derived
- same-year multiplicity needs a rule more explicit than array position if the
  repo ever actually hits that case

Proposal C has a clean surface, but the validator still needs to know quite a
lot.

### Consumer Implications

Compared with today's flat model, consumers would clearly improve.

The service page gets:

- explicit recurring identity
- better grouped summaries
- instance expansion when URLs vary

The homepage gets:

- better candidate grouping
- better direct-link vs internal-anchor choice

The CV gets:

- straightforward compressed run summaries

But Proposal C still does not make the homepage and `/service/` share an
explicit canonical visible unit.
It only makes that unit easier to derive.

### Does It Truly Simplify The Long-Horizon Design?

Proposal C is closer than Proposal B to the repo's usual design taste.

It is:

- narrower than Proposal A
- more semantically honest about one-offs than Proposal B
- materially better than the current flat model

But I do not think it fully simplifies the long horizon because it still ducks
the hardest requirement:

- stable visible-unit identity under backfill and non-contiguous recurrence

So I would describe Proposal C as:

- the best lightweight redesign
- but still not a complete answer to the anchor and visible-unit problem

## Pass 3: Proposal A

Proposal A is the repo proposal.
It explicitly models three levels:

- optional `series`
- canonical `runs`
- nested `instances`

This is the heaviest of the three proposals, but it is also the only one that
tries to make the visible grouped unit first-class in the canonical data.

### Main Strengths

Proposal A is the strongest proposal if judged against the hardest consumer
requirements rather than the lowest migration cost.

Its core insight is correct:

- the service page does not render raw instances
- the homepage does not want raw instances either
- both really want a visible grouped unit

Proposal A names that unit explicitly as `run`.

That has several real benefits:

- stable internal targets have an actual canonical object
- homepage linking can target a real visible unit
- multi-view membership can live on the run instead of being rediscovered from
  instances
- the CV can compress run summaries directly
- non-contiguous recurrence is represented honestly rather than rediscovered
  mechanically

It is also the only proposal that treats anchor identity as first-class rather
than as a side effect of a derivation algorithm.

Given how strong the requirements are on anchor stability, that matters.

Proposal A also has a better answer than the others for ownership at multiple
levels:

- series-level recurring identity metadata
- run-level visible grouping metadata
- instance-level atomic facts

That is more structure, but it also aligns better with the requirements
document's insistence that meaning may live at more than one granularity.

### Requirements It Satisfies Well

Proposal A best satisfies these requirements:

- explicit visible grouped unit for `/service/`
- stable internal anchor potential
- run-aware homepage linking
- non-contiguous runs without fake continuity
- multi-group membership at the visible-unit level
- room for different fact ownership across instance, run, and series
- honest anticipation of future richer consumers

It is also compatible with one-off first-class treatment because not every run
needs a series.

### Weaknesses

The proposal's main weakness is that it risks over-modeling the domain.

It introduces:

- more object types
- more keys
- more authoring decisions
- more migration work
- more validation burden

That is not automatically wrong, but it absolutely raises the bar for:

- hand-editability
- backfill discipline
- avoiding accidental structural churn

The question is whether the service domain has truly earned that much explicit
structure.
Proposal A makes the best case for "yes," but the burden is still real.

### Hidden Seams

#### 1. The run-key story is not fully coherent yet

This is the biggest hidden seam in Proposal A.

The prose says run keys should not be fragile derived `START-END` suffixes.
But several concrete examples use keys like:

- `fptalks-2020-2025`
- `uw-cse-undergraduate-admissions-2020-2021`

Those are exactly range-derived keys.

So as written, the proposal is internally conflicted on its most important
selling point.

If run boundaries later change under backfill, one of two bad things happens:

- the key changes, breaking the promised stability
- or the key stays frozen and becomes semantically misleading

Proposal A can still be the best design, but only if it fixes this.
Run keys need a non-derived identity policy.

#### 2. Explicit runs create authoring burden during backfill

Proposal B and C derive runs mechanically from contiguous years.
Proposal A instead makes runs canonical.

That means backfill is no longer just "add an instance."
It may also mean:

- move an instance into an existing run
- extend a run
- split or merge a run
- decide whether a new gap deserves a new run object

This is not necessarily wrong, but it is meaningful authoring and review work.

#### 3. Field ownership still needs sharper rules around multi-view and mixed
granularity facts

Proposal A is better than the other proposals here, but not fully finished.

It says:

- series do not own `view_groups`
- runs do

That is a good simplification.
But the requirements also warn that group membership may be meaningful at more
than one granularity and may not stay uniform forever.

Proposal A needs a slightly sharper answer to:

- what happens if one instance in a run needs extra view-group membership?
- does that force a new run?
- or are instance-level `view_groups` also allowed?

Without a firm answer, the design still has a seam at one of the requirements'
most sensitive points.

#### 4. Explicit instance keys may be more than the current corpus needs

Proposal A gives every instance a key.
That is the most robust answer to same-year multiplicity, but it may also be
more machinery than the current corpus warrants.

This is a softer critique than the run-key issue.
I would not reject the design for this alone.
But it does contribute to the overall sense that Proposal A is structurally
heavy.

### Migration Cost

Migration cost is the highest of the three.

Not because migration is impossible, but because it is no longer mostly
mechanical.

The migration has to decide:

- what counts as a series
- what counts as a run
- which facts belong at series vs run vs instance level
- what the stable run keys should be
- what the stable instance keys should be

That is a lot of judgment.
It may be the right judgment to encode, but it is undeniably more expensive
than the other two proposals.

### Likely Future Backfill Pain

Proposal A has the highest short-term backfill burden and the lowest long-term
consumer ambiguity if implemented carefully.

That is the central tradeoff.

If the repo expects:

- more service backfill
- more internal links into `/service/`
- richer homepage linking
- later collaborator or overlay reuse

then explicit runs may save pain later.

But only if run identity is truly stable and not range-derived.
If run keys remain implicit or derived from boundaries, Proposal A pays the
highest authoring cost without fully earning the benefit.

### Validation Complexity

Validation complexity is highest here.

The validator would need to check:

- series keys
- run keys
- instance keys
- nesting integrity
- ownership rules for role/URL/details
- multi-view membership semantics
- anchor semantics
- ordering at multiple levels

This is a lot.

The upside is that more of the important semantics become directly checkable in
canonical data rather than hidden in consumer derivation code.
So this is "more validation" but also "less invisible logic."

That is a real tradeoff, not purely a drawback.

### Consumer Implications

Proposal A is the best proposal for consumers.

The service page gets:

- explicit visible grouped units
- better stable anchors in principle
- simpler grouped rendering
- easier instance expansion logic

The homepage gets:

- a real canonical link target for grouped service
- less ambiguity around which visible entry should receive an internal link

The CV gets:

- direct run-summary reuse instead of yet another derived grouping convention

If the redesign is evaluated from the renderer side outward, Proposal A is the
strongest design.

### Does It Truly Simplify The Long-Horizon Design?

Potentially yes, but only if the proposal tightens its key and ownership
policy.

As written, I think Proposal A is:

- the best fit to the requirements
- the most honest about the visible-unit problem
- the most likely to produce simpler consumers

But it is not yet the cleanest finished design because its run-key policy is
not actually resolved.

So I would not call Proposal A "done."
I would call it the proposal with the strongest long-horizon shape and the
largest need for a careful second refinement pass.

## Comparative Evaluation

### Proposal B vs Proposal C

Both B and C share the same core philosophy:

- explicit recurring identity
- nested instances
- derived runs

The main difference is singleton handling.

Proposal B advantages over C:

- one uniform shape
- no promotion seam when a singleton later recurs
- slightly simpler loader surface

Proposal C advantages over B:

- one-offs remain more semantically honest
- better fit to the "do not force fake series wrappers" requirement

My judgment:

- Proposal C is the better lightweight design
- Proposal B is the cleaner inheritance story but slightly too eager to unify
  shapes at the cost of ontology clarity

### Proposal A vs B/C

Proposal A is fundamentally different because it stops treating run as a
purely derived convenience and instead treats it as canonical data.

That means:

- higher authoring and migration cost
- stronger consumer fit
- better chance of truly stable visible units
- much better alignment with the homepage-anchor problem

The core question is whether the service domain has earned explicit run
objects.

Given the requirements document, I think the answer is:

- probably yes, because the anchor and visible-unit problem is not secondary
- but only if the run-key policy is fixed so runs are not secretly range-based

### Hidden Pattern Across All Three

All three proposals are wrestling with the same unresolved truth:

- service has at least three useful granularities
- but only some of them may deserve first-class canonical objects

Proposal B and C try to keep run out of canonical data.
Proposal A pulls it in.

The real discriminator is not elegance.
It is whether the repo believes stable visible-unit identity is worth explicit
data ownership.

The requirements strongly suggest that it is.

## Final Ranking

### 1. Proposal A

Best requirements fit.

Why first:

- only proposal that takes the visible-unit and anchor problem seriously
- best consumer story for `/service/`, homepage, and CV
- best support for multi-granularity ownership
- strongest long-horizon potential

Why not a runaway winner:

- over-modeled in places
- highest migration cost
- run-key policy still needs real cleanup

If Proposal A wins, it should not be adopted unchanged.
It needs a refinement pass that makes run keys non-derived and sharpens field
ownership rules.

### 2. Proposal C

Best lightweight alternative.

Why second:

- more semantically honest than B about one-offs
- much cheaper than A
- still gives explicit recurring identity
- likely easiest to socialize and migrate incrementally

Why not first:

- still punts stable visible-unit identity into derived code
- still leaves anchor durability weaker than the requirements seem to want
- still has a promotion seam when singletons become recurring series

### 3. Proposal B

Cleanest on paper, weakest on the hardest requirements.

Why third:

- very attractive edit story
- very good duplication reduction
- strong inheritance model

But:

- it softens the one-off requirement the most
- it still leaves visible-unit identity and anchor durability derived
- it leans too hard on "run changes are acceptable if content changes," which
  the requirements do not really permit

## Bottom Line

If the redesign is supposed to satisfy the requirements document as written,
Proposal A is the strongest foundation, but it needs a second pass before it
is safe to adopt.

If the redesign instead wants the smallest credible near-term improvement,
Proposal C is the best fallback.

Proposal B is thoughtful and elegant, but in my view it gives away too much on
the exact requirement that seems most likely to hurt later: stable visible-unit
identity under backfill and multi-view rendering.
