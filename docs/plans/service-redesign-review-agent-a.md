# Service Redesign Review: Agent A

Status: draft independent review

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

1. pass 1: Proposal A
2. pass 2: Proposal B
3. pass 3: Proposal C

The standard used here is the latched requirements brief, especially the
long-horizon requirements around:

- stable anchors under backfill and multi-view rendering
- non-contiguous runs
- same-year multiplicity
- title drift
- partial/uncertain historical knowledge
- rich details and URL ownership
- minimizing hidden derivation pressure in renderers

## Executive View

My current ranking is:

1. **Proposal A**: strongest requirements fit, but heaviest canonical model
2. **Proposal C**: best simplification-oriented alternative, but still leaves
   too much run/anchor pressure in code
3. **Proposal B**: elegant at first glance, but now clearly underpowered
   against the strengthened requirements

My current recommendation is:

- if the repo is serious about a redesign, the migration is probably justified
- but only **Proposal A** currently looks robust enough to deserve that cost
- **Proposal C** is attractive and much cleaner than the current flat model,
  but I do not think it fully survives the newer requirements without
  immediately growing follow-on seams
- **Proposal B** feels overtaken by the longer-horizon requirements and should
  mostly be treated as a useful stepping stone in the design conversation, not
  the final answer

## Pass 1: Proposal A

### Summary Judgment

Proposal A is the only one of the three that fully takes the requirements
document seriously as a specification rather than as a list of examples.

It is the least superficially elegant, but it is the most honest about what the
repo actually needs:

- atomic facts
- visible grouped units
- broader recurring identity

Those three things are not the same, and the service domain is already paying a
price for pretending they are.

My main reaction is:

- it is more model than the repo has today
- but it is also the first proposal that looks capable of *stopping* the churn
  of subtle service-specific edge cases

### What Proposal A Gets Right

#### 1. It makes the visible unit explicit

This is its biggest advantage.

The requirements are very clear that `/service/` and the homepage both need a
stable visible unit with:

- stable anchors
- grouped summaries
- predictable links
- multi-view behavior

Proposal A chooses `run` as the canonical visible unit. That is a real design
decision, not a hopeful renderer convention.

I think this is exactly the place where the other proposals remain too
optimistic. They still assume runs can remain derived forever without that
causing friction.

#### 2. It gives anchors a real home

The requirements treat stable anchors as one of the highest-risk issues.

Proposal A addresses that directly:

- anchors live on canonical runs via stable `run.key`
- they do not depend on inferred `start-end` ranges
- they do not depend on the series always having one run
- they do not depend on a single section rendering

That is a very strong point in Proposal A’s favor.

The current service problem is not just “grouping.” It is “what is the thing we
intend to link to?” Proposal A answers that in a clean way.

#### 3. It handles multi-view facts honestly

The explicit `primary_view_group` on runs is slightly inelegant, but it solves a
real problem:

- one fact can appear in multiple sections
- HTML anchors need one canonical home
- homepage internal links need one target

The requirements explicitly call out `2025 PLDI Program Committee Chair` as a
stress case. Proposal A is the only proposal that offers a fully explicit and
stable answer.

#### 4. It gives details, URL, and time semantics explicit levels

The requirements repeatedly stress that details and URLs can belong at more
than one level:

- identity/series
- run
- instance

Proposal A models exactly that.

This matters more than it first appears. The current data already has pressure
from:

- `UW Faculty Skit`
- `FPTalks`
- `Dagstuhl Seminar 26022: EGRAPHS`
- `2025 PLDI Program Committee Chair`

Proposal A can express all of these without pretending one field ownership rule
fits everything.

Likewise, `time_basis` at run level is a realistic acknowledgment of the
academic-year wrinkle without forcing month-level modeling.

#### 5. It supports title drift and same-year multiplicity better than the
others

Proposal A explicitly leaves room for:

- `run.title`
- `instance.title`
- `instance.key`

That means:

- title drift can be represented
- multiple instances in the same year can still be individually identified
- future backfill with messy history is much less likely to force schema pain

The other proposals are materially weaker here.

### What Proposal A Complicates

#### 1. It introduces a lot of canonical structure

Proposal A is the heaviest model:

- top-level `series`
- top-level `runs`
- nested `instances`

That is more than the current repo has in any similar domain.

The immediate risks are:

- more objects to maintain
- more cross-reference invariants
- higher migration complexity
- more chances for partial inconsistency

It is not automatically bad, but it definitely means the redesign cost is
substantial.

#### 2. It risks over-canonicalizing presentation

The biggest long-horizon danger in Proposal A is that `run` may be the right
visible unit *today* but become too presentation-shaped in canonical data.

A run is partly ontological and partly consumer-facing:

- it matters for anchors and grouping
- but it is also shaped by how you want `/service/` and homepage recent-service
  to summarize things

That means Proposal A is baking more rendering policy into the data model than
the other two proposals.

This is sometimes the right trade.
But it is real complexity, and it should not be understated.

#### 3. `primary_view_group` is useful but uneasy

I understand why Proposal A adds it.
I also think it is one of the least elegant fields in the proposal.

Why:

- it exists because one run may appear in multiple sections
- but then we need one canonical “home” for anchoring
- which means a presentation concern becomes canonical metadata

This is probably acceptable, but it is a smell. It suggests the section system
and the visible-unit system are not perfectly aligned.

That does not kill the proposal, but it is a seam to watch.

#### 4. It assumes runs deserve stable keys before we have long real-world
experience editing them

Proposal A’s success depends on authoring discipline around run keys.

That creates a new class of editorial work:

- naming runs
- preserving run keys under backfill
- deciding when a set of instances is one run or should be split

The proposal is right that derived `start-end` suffixes are fragile.
But the replacement is not free. It requires confident human modeling.

### Hidden Seams And Likely Future Pain

#### A. It still does not really solve partial/uncertain history

The requirements ask for tolerance of partial or uncertain historical
knowledge.

Proposal A is better positioned than the others because it has multiple levels,
but it still does not really say how uncertainty is expressed.

Examples:

- “I think these two things are one series, but not fully sure yet”
- “I know roughly that this was a 2020-2021 academic-year service lane, but
  not exactly which yearly instances should be split out”
- “I know the recurring identity, but not whether a URL belongs at run or
  instance level”

Proposal A is structurally capable of supporting those, but it does not
actually define an uncertainty strategy.

#### B. Run membership may still be contentious in messy cases

Even with explicit runs, deciding what belongs in one run could still be hard
for messy future backfill:

- same identity, gap year, then return
- same year, two sub-events
- title change plus role change
- academic-year semantics versus event-year semantics

Proposal A gives you the place to put the answer.
It does not remove the judgment call itself.

#### C. There is some duplication pressure between `series` and `run`

Proposal A can end up with:

- `series.title`
- `run.title`
- sometimes maybe the same thing repeated

Likewise:

- `series.url`
- `run.url`
- `instance.url`

That is semantically justified, but it does create some duplication pressure.
The validation story would need to be strong to keep this from getting sloppy.

### Migration Implications

Migration to Proposal A is the hardest of the three:

- current flat records need to be grouped into series
- runs need to be materialized explicitly
- instance keys need to be minted
- primary view groups need to be chosen
- run keys need to be chosen

This is not a trivial mechanical normalization.
It is a real domain-model migration.

That said, it is also the most likely migration to be “worth it” if the repo
really wants to stop revisiting service-model seams repeatedly.

### Validation Complexity

Proposal A would require the richest validator by far:

- duplicate series keys
- duplicate run keys
- duplicate instance keys
- series/run cross-reference integrity
- primary view group validity
- ordering rules across three levels
- field ownership and shadowing checks
- anchor uniqueness

This is a lot, but the complexity is at least honest and explicit.
I would rather validate explicit complexity than hide it in renderer logic.

### Consumer Implications

Proposal A is strongest here:

- `/service/` becomes straightforward
- homepage recent-service can operate over runs cleanly
- CV can consume runs without special-case grouping
- future richer service-page rendering has a natural substrate

The proposal most clearly reduces “consumer cleverness.”
That is one of its strongest arguments.

### Does It Actually Simplify The Long Horizon?

My answer is: **yes, but by moving complexity into canonical data rather than
pretending it does not exist**.

This is not the simplest schema.
It may still be the cleanest long-horizon design.

I think the repo would only regret Proposal A if:

- the service domain turns out to be much simpler than the current requirements
  suggest
- or the repo is unwilling to maintain a more explicit canonical structure

Given the current discussion, neither seems likely.

## Pass 2: Proposal B

### Summary Judgment

Proposal B is elegant, readable, and genuinely attractive.
It is also clearly weaker than Proposal A once judged against the strengthened
requirements.

Its main thesis is:

- make identity explicit
- keep one uniform identity-with-instances shape
- derive runs, anchors, and summaries in code

That is a meaningful improvement over the current flat model.
But I do not think it goes far enough.

### What Proposal B Gets Right

#### 1. It fixes the most obvious current problem: implicit identity

This is the core win:

- `series_key` goes away
- recurring identity becomes structural
- shared metadata lives once
- editing gets much cleaner

This is real value.
Proposal B is not cosmetic.

#### 2. It follows a proven repo pattern

The analogy to `teaching.json` is persuasive:

- stable identity
- nested instances
- defaults at identity level
- per-instance overrides

This gives Proposal B a strong “repo-native” feel.
It sounds like something the repo already knows how to live with.

#### 3. It materially improves editing and reduces duplication

For cases like:

- `FPTalks`
- `UW Faculty Skit`
- `PACMPL Advisory Board`

Proposal B is obviously better than today:

- fewer repeated fields
- easier year additions
- easier metadata edits
- easier auditing by eye

That is a serious operational advantage.

#### 4. It keeps the canonical model lighter than Proposal A

Compared to Proposal A, Proposal B has a strong simplicity story:

- one top-level shape
- no explicit run objects
- no explicit series registry plus separate runs
- no run keys to manage

If the requirements were slightly weaker, this would be a very compelling
argument.

### What Proposal B Gets Wrong Or Leaves Weak

#### 1. It under-specifies same-year multiplicity

This is a major failure against the strengthened requirements.

Proposal B explicitly says:

- each `year` is unique within an identity’s `instances` array
- an instance is globally addressable as `{identity_key}/{year}`

That is incompatible with the requirement that same-year multiplicity remain
possible.

This is not a minor edge case anymore.
The requirements explicitly elevated it.

Proposal B was written before that strengthening, and it shows.

#### 2. It does not adequately support title drift

Proposal B’s instances can override:

- `role`
- `url`
- `details`

But not `title`.

That means a recurring identity with meaningful title evolution does not fit
cleanly.

The requirements explicitly require tolerance for title drift.
Proposal B does not really meet that.

#### 3. It does not have a clean story for varying view-group membership

Proposal B’s identity owns `view_groups`.
That means it is quietly assuming a largely uniform section-membership story at
identity level.

That is exactly one of the longer-horizon concerns the requirements warn
against.

It is especially weak for:

- multi-view behavior
- future years where one instance of a series participates in a different set
  of sections than the rest

Once again, the strengthened requirements hurt Proposal B badly here.

#### 4. Anchor stability is weaker than it first appears

Proposal B derives anchors from identity key and run boundaries:

- single run: `key`
- multi-run: `key--start-end`
- section-prefixed anchors for multi-view rendering

This is clever.
I do not think it is robust enough.

Problems:

- if a run boundary changes under backfill, the derived anchor changes
- section-prefixed anchors imply duplicated entry points for the “same” thing
- multi-view behavior is solved in rendering rather than in the canonical model
- there is no stable visible-unit identity apart from derived boundaries

This is exactly the kind of derivation pressure the requirements were trying to
flush out.

#### 5. One uniform shape is not actually as clean as it sounds

The “singletons and series are structurally identical” idea is elegant, but it
also creates friction:

- a true singleton still has to be an identity-with-instances wrapper
- the model has only two real levels despite the requirements stressing three
  useful granularities
- run-level facts still have nowhere explicit to live

I think Proposal B’s uniformity is partly aesthetic.
It is not obvious that it maps best to the real service domain.

### Hidden Seams And Likely Future Pain

#### A. It still makes code do too much

Proposal B says the canonical data defines identity and instances, and runs are
derived.

That means code still has to derive:

- runs
- uniform role
- uniform URL
- uniform details
- anchors
- multi-view section-safe rendering behavior

That is much better than today, but it still leaves the repo with significant
non-trivial service-specific view logic.

#### B. Identity-level `ongoing` is somewhat muddy

Proposal B places `ongoing` on the identity.

That is convenient.
It is also a little semantically fuzzy for:

- non-contiguous identities
- identities with multiple runs
- same-year multiplicity

Proposal A’s run-level time semantics are stronger here.

#### C. The “instance globally addressable as key/year” rule is too brittle

It seems elegant, but it relies on assumptions that the requirements no longer
permit:

- one instance per year per identity
- no need for separate instance keys

I would not build the redesign on that.

### Migration Implications

Migration to Proposal B is conceptually simpler than Proposal A:

- group records into identities
- hoist shared fields
- keep per-year variation in `instances`

That is appealing.

But the migration would likely be followed by additional follow-on redesign
pressure once the repo hits:

- same-year multiplicity
- title drift
- non-uniform section membership
- anchor instability under backfill

So the lower migration cost may be a false economy.

### Validation Complexity

Proposal B is lighter than Proposal A but still non-trivial:

- identity key uniqueness
- instance year uniqueness
- inheritance checks
- role normalization checks
- derived anchor uniqueness

The problem is that some of its validation rules actually encode assumptions
that the strengthened requirements reject.

So its simpler validator is not purely a virtue. It partly comes from a weaker
model.

### Consumer Implications

Proposal B would definitely help:

- `/service/` grouping
- homepage identity selection
- CV compression

But it would still leave consumers leaning heavily on derived logic for runs
and anchors. I think that means the repo would still feel the model’s seams in
future work.

### Does It Actually Simplify The Long Horizon?

My answer is: **partially, but not enough**.

Proposal B is a meaningful improvement over the current flat model.
I would not call it robust enough for the long-horizon requirements as they now
stand.

## Pass 3: Proposal C

### Summary Judgment

Proposal C is the strongest “minimal redesign” candidate.

Compared to Proposal B, it is:

- more realistic about singletons
- more flexible about instance-level `view_groups`
- more honest that two shapes are acceptable if they reduce fake structure

Compared to Proposal A, it is:

- much lighter
- more teaching-like
- probably easier to migrate
- but still structurally weaker around runs and anchors

If I were trying very hard to avoid over-modeling, Proposal C is where I would
look first.
I still think it falls short of the full requirements.

### What Proposal C Gets Right

#### 1. It hits a better simplicity/fit balance than Proposal B

I prefer Proposal C to Proposal B because it avoids one of B’s main aesthetic
mistakes:

- not every singleton needs a fake identity-with-instances wrapper

That matters.
The requirements explicitly say one-offs must remain first-class.
Proposal C respects that more honestly.

#### 2. It still fixes explicit recurring identity

For recurring service, Proposal C offers:

- series record
- nested instances
- explicit defaults and overrides

So it retains the main benefit of B:

- no more implicit `series_key`
- no more duplicated metadata across every yearly record

This is good and important.

#### 3. It handles instance-level view-group override

This is a genuine improvement over Proposal B.

By allowing instance-level `view_groups` override, Proposal C is more aligned
with the strengthened requirement that higher-level groupings must not assume
uniform view membership forever.

I still do not think it completely solves the problem, but it is a serious step
in the right direction.

#### 4. It keeps inheritance simple and understandable

Proposal C’s inheritance story is strong:

- top-down defaults
- per-instance overrides
- thin derived view layer in code

This is a very understandable editing and validation model.
That is one of its best qualities.

### What Proposal C Still Leaves Weak

#### 1. It still does not give runs a canonical home

This is the central problem.

Proposal C keeps:

- series canonical
- instances canonical
- runs derived in code

That means the repo still has no canonical visible grouped unit.

Given how heavily the requirements emphasize:

- stable visible anchors
- run-level summaries
- homepage links to visible service entries
- non-contiguous repeated runs

I think this is still too optimistic.

#### 2. Its anchor story is still only “acceptable,” not strong

Proposal C explicitly says:

- single-run series anchor to key
- multi-run series anchor to `key--start-end`
- if start/end changes due to backfill, anchor changes too, and that is
  acceptable

I disagree with the confidence of that last step.

The requirements do not want anchors to be casually boundary-derived if better
alternatives exist.

Proposal C’s fallback argument is basically:

- yes, anchor churn can happen
- but visible content changed too

I do not think that is wrong.
I also do not think it is good enough for a redesign whose main purpose is to
remove long-horizon service friction.

#### 3. Same-year multiplicity is only partially handled

Proposal C is better than B because it at least contemplates same-year
multiple instances.

But its answer is weak:

- identity by series key + year + array position

That is not a strong identifier model.

It may be enough for rendering.
It is not enough for stable long-horizon semantics.

Proposal A’s explicit instance keys are much better.

#### 4. Title drift remains under-modeled

Like Proposal B, Proposal C still centers the series title heavily and does not
give a really satisfying place for title evolution beyond the current
lightweight override story.

It is better than B structurally, but it still does not feel fully ready for a
future where recurring identities change public naming.

#### 5. Run-level details and time semantics are still only inferred

Proposal C is good on series-level defaults and instance-level overrides.
It is not good on facts that are true of a run but not the whole series.

The requirements explicitly call out that these may matter.
Proposal C still has nowhere canonical to put them.

### Hidden Seams And Likely Future Pain

#### A. The derived view layer becomes the real model

Proposal C says renderers should consume:

- `ServiceSeriesView`
- `ServiceRunView`
- `ServiceInstanceView`

That is a sensible implementation pattern.
It also means the real service model still partly lives in Python dataclasses
rather than in the canonical JSON.

That is fine if the derived layer is thin.
I suspect it would not stay thin.

#### B. Run-level decisions will keep showing up in code review

Any time the repo asks:

- is this one run or two?
- what should this anchor be?
- should this link point externally or to `/service/`?
- do these details belong to the series or the instance?

Proposal C still answers many of those in code rather than in canonical data.
That is exactly the kind of seam the service domain has been exposing.

#### C. Two shapes are acceptable, but they do increase branching

I do not think two shapes are a serious problem.
But they do mean:

- singleton path
- series path

Validation and loading stay manageable, but they are no longer truly uniform.
That is a fair trade, not a fatal flaw.

### Migration Implications

Proposal C is probably the best migration story of the three:

- singletons mostly stay close to current records
- recurring series get nested instances
- a derived view layer handles the rest

This is a strong practical advantage.

If the repo were extremely migration-averse, Proposal C would be tempting.

### Validation Complexity

Proposal C’s validator would be manageable:

- singleton schema
- series schema
- instance inheritance
- ordering
- derived anchor uniqueness

This is easier than Proposal A.
But again, some of that simplicity comes from leaving harder semantics in code.

### Consumer Implications

Proposal C would make all three main consumers better.
I do not dispute that.

The question is whether it would make them better *enough* to prevent the next
round of service-model discomfort.

I am not convinced.

### Does It Actually Simplify The Long Horizon?

My answer is: **it simplifies a lot, but not quite enough to deserve being the
final redesign if the repo is already willing to migrate**.

If migration is on the table, I would rather pay that cost once for the model
that resolves more of the real seams.

## Comparative Evaluation

### Proposal A vs Proposal B

Proposal A is much stronger on:

- stable anchors
- non-contiguous runs
- run-level metadata
- title drift
- same-year multiplicity
- multi-view section semantics

Proposal B is stronger only on:

- apparent simplicity
- editing ease
- lower migration cost

For the strengthened requirements, that trade overwhelmingly favors A.

### Proposal A vs Proposal C

This is the real comparison.

Proposal C is the better argument if the priority is:

- keep canonical data lean
- stay close to teaching-style identity/instances
- avoid explicit run objects

Proposal A is better if the priority is:

- stop future anchor churn
- make visible grouped units canonical
- reduce hidden consumer derivation
- give run-level facts an explicit home

The requirements, as written, lean toward Proposal A.

### Proposal B vs Proposal C

Proposal C is better almost everywhere:

- better singleton story
- better multi-view flexibility
- clearer acknowledgment of derived runs
- stronger implementation realism

Proposal B’s main surviving advantage is the seductive elegance of one uniform
shape. I do not think that is enough.

## Strongest And Weakest Aspects

### Proposal A

Strongest aspects:

- canonical visible run unit
- stable-anchor story
- multi-level field ownership
- best requirements coverage

Weakest aspects:

- heaviest canonical model
- `primary_view_group` is slightly awkward
- larger migration and validation surface

### Proposal B

Strongest aspects:

- explicit identity
- one uniform shape
- strong deduplication and editing simplicity

Weakest aspects:

- fails same-year multiplicity
- weak on title drift
- weak on varying view membership
- derived anchor/run story is too fragile

### Proposal C

Strongest aspects:

- best minimal redesign
- good singleton/series balance
- explicit identity without over-wrapping singletons
- practical migration path

Weakest aspects:

- run is still not canonical
- anchor churn still accepted
- same-year multiplicity still weakly identified
- run-level facts still lack a clear canonical home

## Overall Recommendation

I think the repo has probably already crossed the line where **some** redesign
is justified.

The service domain is too important and too structurally specific to keep
leaning on the current flat model plus ever-richer grouping heuristics forever.

My concrete recommendation is:

1. Treat Proposal A as the current leading redesign candidate.
2. Treat Proposal C as the best fallback if Proposal A is judged too heavy.
3. Treat Proposal B as superseded by the stronger requirements.

If the deciding question is:

“Which proposal is actually simpler enough to justify migrating?”

my answer is:

- **Proposal A** is justified if the repo wants real long-horizon stability
- **Proposal C** is attractive but probably not final-form enough
- **Proposal B** is not strong enough against the current requirements

So I would currently choose:

**Proposal A over Proposal C over Proposal B.**
