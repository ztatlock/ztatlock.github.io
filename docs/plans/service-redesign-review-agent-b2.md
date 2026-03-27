# Service Redesign Review: Agent B2

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

1. pass 1: Proposal B
2. pass 2: Proposal C
3. pass 3: Proposal A

The perspective in this review is intentionally simplicity-biased:

- downweight cleverness
- downweight inertia
- upweight hand-editability
- upweight future backfill ergonomics
- be skeptical of canonically storing any layer that still feels substantially
  consumer-facing

## Executive View

My current ranking is:

1. **Proposal C**
2. **Proposal A**
3. **Proposal B**

My current recommendation is:

- if the repo redesigns service, **Proposal C** is the best balance of
  simplicity, explicitness, and future tolerance
- **Proposal A** solves more edge cases directly, but I think it pays too much
  canonical complexity too early by freezing `run` into data
- **Proposal B** was a strong improvement over the current flat model, but the
  stronger requirements now expose several places where its “single uniform
  shape” story is too blunt

The sharpest conclusion from this review is:

- the real choice is now **A versus C**
- I do not think B survives the strengthened requirements as the best design
- I do think the repo should migrate away from the current flat per-year model
- but I would only pay the migration cost for a shape that still feels simple
  after the backfill gets much bigger

## Pass 1: Proposal B

### Summary Judgment

Proposal B is attractive for the same reason the current service model was
attractive when it was first introduced:

- one obvious canonical unit
- one obvious nesting pattern
- one obvious inheritance story

That is still a real virtue.

But against the strengthened requirements, Proposal B now reads as too
optimistic about how much structure can remain derived without turning into
another pocket of hidden complexity.

I would describe it as:

- the cleanest first serious redesign draft
- but not the cleanest design after the requirements were strengthened

### What Proposal B Gets Right

#### 1. It makes recurring identity explicit

This is its biggest win over the current flat model.

The current flat model has:

- per-year instances as truth
- `series_key` as a hint
- grouping logic as the real owner of service identity

Proposal B fixes that.

Every top-level record is a service identity. That is a major improvement
because:

- shared metadata finally has a home
- validation can attach to something real
- the JSON reads the way a human thinks about the domain

This is especially compelling for:

- `fptalks`
- `pacmpl-advisory-board`
- `uw-faculty-skit`
- `uw-cse-undergraduate-admissions-committee`

#### 2. The inheritance story is very clear

Proposal B’s inheritance rules are simple and familiar:

- identity-level defaults
- per-instance overrides

That is much easier to reason about than the current “group by equality, then
infer what is uniform” pattern.

For long-running series like `uw-faculty-skit`, this is a real reduction in
noise and maintenance burden.

#### 3. Editing ergonomics are genuinely better than the current model

This matters more than it first appears.

The service redesign is not being done for elegance alone. It is being done
because future backfill will add a lot more material, and the current model
will make that expensive and error-prone.

Proposal B improves authoring in several ways:

- adding a year to a series is small
- repeated roles/details stop being duplicated
- records become more scanable in review
- series-local judgments can be made in one place

That is all real value.

#### 4. It stays close to the repo’s existing `teaching.json` intuition

This is important culturally, not just technically.

The repo already understands:

- identity
- nested instances
- renderers derive consumer-specific projections from that structure

Proposal B fits that existing pattern. That makes it easier to trust.

### Where Proposal B Now Feels Weak

#### 1. Its “one shape for everything” story is weaker than it sounds

The “singleton is just an identity with one instance” line is elegant, but it
does some work that the stronger requirements now make suspicious.

In particular:

- one-offs do not always feel like recurring identities
- singletons do not always benefit from the extra wrapper
- the wrapper becomes obligatory even when there is no series-level meaning

This is not fatal, but it is a cost.

The requirement that one-offs remain first-class does not forbid this shape,
but it does make me ask:

- is the extra identity shell actually buying anything for Dagstuhl-style
  singletons?
- or is it simply enforcing a pleasing uniformity?

I now think Proposal C answers that question better.

#### 2. Anchors remain too derived

Proposal B derives anchors from:

- identity key
- and run boundaries

That is serviceable, but it does not fully solve the anchor problem.

The strengthened requirements were explicit about:

- stable anchors under backfill
- no ambiguity under multi-view rendering
- non-contiguous runs
- future repeated runs

Proposal B’s anchor story is still partly “derive the right anchor from the
rendered run shape.” That is cleaner than the current model, but it still
leaves anchors downstream of run detection and run-boundary interpretation.

This is much better than today, but I do not think it is the final answer if
the repo becomes extremely anchor-sensitive.

#### 3. It assumes more yearly uniqueness than the requirements now warrant

Proposal B says:

- each `year` is unique within an identity
- instance is globally addressable as `{identity_key}/{year}`

That immediately conflicts with the strengthened requirement that same-year
multiplicity may appear in future backfill.

It tries to solve that partly in prose, but the canonical shape itself is still
conceptually “one year, one instance” inside an identity.

That means Proposal B is subtly overfit to the current corpus.

#### 4. Multi-view facts are still awkward

Proposal B puts `view_groups` at identity level.

That works for many current cases, but the requirements now explicitly say:

- higher-level groupings must not assume a single stable `view_groups` set
- group membership may matter at multiple granularities

Proposal B can survive that by pushing `view_groups` to instances or keeping it
per identity and accepting some over-broadness, but neither feels especially
clean.

This is a sign that the single uniform shape is starting to strain.

#### 5. Rich details are still under-modeled

Proposal B has `details` at identity level or instance level.

That is better than today, but it still does not name the intermediate case
very well:

- facts true for a visible grouped run
- but not for the whole recurring identity

This is exactly the gap the stronger requirements surfaced around:

- run-level supporting details
- summary versus instance semantics
- preserving authored Djot without flattening it into display hacks

Proposal B does not fully solve that. It mostly hopes renderers can handle it.

### Migration View

Proposal B’s migration is easy to imagine.

That is a real advantage:

- group by `series_key`
- hoist shared fields
- reduce instances to what varies

This is probably the easiest migration of the three.

But I would not let migration ease dominate the design choice. If the redesign
is supposed to prevent future pain, the best migration is not automatically the
best model.

### Bottom Line On Proposal B

Proposal B is strong as:

- a first clean break from flat scattered service records

It is weak as:

- a long-horizon design after the requirements were expanded

I do not think it is bad.
I do think it is now too optimistic.

## Pass 2: Proposal C

### Summary Judgment

Proposal C is the one I find most convincing on balance.

Its key move is subtle but important:

- keep explicit series where they are real
- keep true singletons simple
- derive runs in code
- do not store a canonical run layer unless that has clearly earned its keep

That feels much closer to the repo’s stated design philosophy:

- simple
- narrow
- explicit where necessary
- not more abstract than needed

### What Proposal C Gets Right

#### 1. It identifies the real win correctly: explicit series identity

Proposal C understands that the current model’s biggest problem is not “we do
not have runs in JSON.” It is:

- series identity is only implicit
- inheritance is only emergent
- grouping is presentation-driven

By making series structural, Proposal C resolves most of that pressure while
still resisting the temptation to canonically store every derived layer.

That feels wise.

#### 2. Two shapes fit the service domain better than one

Proposal C’s split between:

- singleton records
- series records with nested instances

is not messy. It is honest.

The service domain really does contain both:

- one-off facts
- recurring identities

Trying to force both into exactly one shape mostly helps elegance, not
understanding.

Proposal C’s two-shape model lets:

- Dagstuhl remain small
- FPTalks become structured
- PLDI PC Chair remain straightforward
- UW Faculty Skit collapse repetition cleanly

That feels like a practical improvement over both the current model and
Proposal B’s uniform wrapper story.

#### 3. It preserves the right layers as derived

This is the heart of why I prefer it to Proposal A.

Proposal C stores:

- identity
- instance

and derives:

- runs
- summary labels
- anchors for multi-run cases
- uniform role/url/details facts

That is the right tradeoff in my view because:

- runs are highly consumer-facing
- run semantics can shift as render policy shifts
- backfill may change run boundaries
- canonical data should not overfit current renderer needs

The requirements call out run semantics as real, but they do not require that
runs themselves be stored canonically.

Proposal C respects that distinction.

#### 4. It has the best fit with “future simplicity”

This proposal feels most likely to age well under broad backfill because it
does not lock too much consumer logic into the schema.

It gives the repo enough explicit structure to stop re-inferring series
identity, while still leaving room for the service page and homepage to evolve.

That seems especially valuable because the service surface is still mid-audit.

### Where Proposal C Still Has Seams

#### 1. Run identity remains derived

This is the biggest argument for Proposal A.

Proposal C still derives:

- contiguous runs
- run anchors
- run-level summary semantics

That means some nontrivial logic remains in code. If the repo strongly values
stable anchor identity as a first-class canonical concern, Proposal C may still
feel too soft.

I think this is a real seam, but not a fatal one.

The requirements ask for stable anchors.
They do not necessarily require anchor stability to be independent of all
future reinterpretation.

I think that is an important distinction.

#### 2. It still needs a good answer on run-level details

Proposal C’s default/override model is strong, but like Proposal B, it does not
name run-level detail ownership directly in canonical data.

That may be okay if:

- run-level details are rare
- renderers can derive them from resolved instance content

But it is still a place to watch.

#### 3. Instance identity for same-year multiplicity is slightly underspecified

Proposal C openly allows same-year multiplicity and suggests:

- series key
- year
- array position when necessary

This is honest, but still a little uneasy.

I would want the eventual implementation plan to decide whether same-year
instances should gain:

- an optional per-instance `key`
- or an explicit small discriminator field

before we call the model truly finished.

Still, this is fixable without upsetting the overall design.

#### 4. `view_groups` inheritance needs careful validation

Proposal C allows instance-level `view_groups` overrides.

That is good because the requirements explicitly need that flexibility.
But it also means validation must be thoughtful:

- inherited defaults
- per-instance overrides
- section-level anchor generation
- no silent accidental widening

That is manageable, but not free.

### Migration View

Proposal C’s migration is still quite manageable.

It is only somewhat harder than Proposal B because:

- you need to distinguish series from singletons
- you need to preserve singleton simplicity
- some groups need judgment on what belongs at series level

But that is all understandable work.

I think the migration burden is justified if the repo wants:

- a cleaner canonical model
- less duplication
- fewer grouping hacks

### Bottom Line On Proposal C

Proposal C is the best balance of:

- explicitness
- simplicity
- editability
- future flexibility

It does leave more logic in code than Proposal A.
I think that is good, not bad, for this domain.

## Pass 3: Proposal A

### Summary Judgment

Proposal A is impressive and serious. It is also the first proposal that made
me think, “yes, this would definitely stop many of the current service seams.”

But after the initial admiration, my main reaction is:

- it is too eager to make `run` canonical

That is not obviously wrong.
It may even be correct if the repo decides anchors and run-level rendering are
important enough to deserve canonical status.

I just do not think the current evidence quite reaches that bar.

### What Proposal A Gets Right

#### 1. It resolves the anchor problem most directly

This is Proposal A’s strongest advantage.

By putting:

- `key`
- `primary_view_group`
- and stable visible identity

on the canonical `run`,

Proposal A makes:

- homepage internal links
- service page anchors
- multi-view rendering

much easier to reason about.

If anchor stability is the overriding priority, Proposal A wins.

#### 2. It models the three real layers explicitly

Proposal A is the most faithful to the requirements’ granularity language:

- series
- run
- instance

That means many difficult cases become explicit:

- non-contiguous service
- run-level details
- run-level view-group membership
- academic-year hints
- anchor targets

There is real power here.

#### 3. It makes consumer logic much thinner

Proposal A’s renderers would mostly consume:

- explicit runs
- explicit instances
- explicit section home

instead of reconstructing them.

That is a substantial simplification of code.

### Where Proposal A Feels Too Heavy

#### 1. It canonically stores a layer that is still partly presentational

This is my central objection.

Runs are real, but they are also highly entangled with:

- contiguous-year interpretation
- current render grouping
- anchor policy
- summary-label semantics
- homepage selection behavior

I believe those are important, but I am not yet convinced they should all
crystallize into canonical JSON.

Proposal A turns a large amount of previously derived structure into authored
data. That makes some things clearer, but it also hardens choices that still
feel somewhat consumer-facing.

#### 2. It asks authors to maintain more structural bookkeeping

Proposal A says the extra model pays for itself in simpler consumers.
That is plausible.

But it also means authors now manage:

- series array
- runs array
- nested instances
- primary view-group semantics
- time-basis hints
- possibly both series-level and run-level metadata

This is a lot more schema surface.

Even if each individual field is reasonable, the total shape starts to feel
less hand-obvious than Proposal C.

#### 3. It may overfit to current service-page/homepage needs

Proposal A is strongest exactly where current service consumers are painful:

- visible runs
- anchors
- homepage links

That is good.

But it also raises the concern that the data model is being bent around current
projection problems rather than around the most stable long-horizon facts.

The most stable facts are:

- recurring identity
- exact year-local participation

Run feels more derived than that.

#### 4. `primary_view_group` is useful but slightly uneasy

I understand why it exists, and I think it is a smart local fix.
But the fact that Proposal A needs it so early is also revealing:

- section duplication
- anchor disambiguation
- canonical “home” choice

are being pushed into the data layer.

That may be justified, but it is exactly the kind of extra representational
burden I would prefer to avoid unless absolutely necessary.

### Migration View

Proposal A would be the hardest migration of the three.

Not impossibly hard, but meaningfully harder:

- promote current groups into explicit runs
- choose stable run keys
- choose primary view groups
- decide where URL/details belong
- decide where time-basis hints belong

That is a more opinionated migration than Proposal B or C.

If I were convinced the resulting model was clearly better, I would accept that
cost. I am not fully convinced.

### Bottom Line On Proposal A

Proposal A is the most robust if:

- you think run identity is itself canonical truth

It is less attractive if:

- you think run identity is an important but still derived lens over service

I currently believe the second framing is the better one.

## Comparative Section

### Strongest Aspect Of Each Proposal

Proposal A:

- best anchor and multi-view story

Proposal B:

- most elegant first clean break from flat records

Proposal C:

- best balance between explicitness and restraint

### Weakest Aspect Of Each Proposal

Proposal A:

- canonically stores too much run-level structure too early

Proposal B:

- over-uniform shape and underpowered treatment of stronger requirements

Proposal C:

- still leaves some real run/anchor complexity in code

### Which Proposal Best Fits The Requirements?

If “best fits” means “answers the largest number of requirements directly in
the schema,” then Proposal A wins.

If “best fits” means “satisfies the requirements while still honoring the
repo’s simplicity bias,” then Proposal C wins.

That second criterion matters more to me.

### Is Migration Worth It?

Yes, probably.

The service audit has exposed enough structural friction that I no longer think
the current flat model should be treated as the long-term foundation.

But I would migrate only once.

That means the target should be:

- explicit enough to stop the current churn
- simple enough not to become the next long-term regret

I think Proposal C best satisfies that.

## Recommendation

My recommendation from this review is:

1. Treat Proposal B as informative but no longer leading.
2. Focus the real decision on Proposal A versus Proposal C.
3. Prefer Proposal C unless the repo decides that:
   - stable run identity
   - stable run-level anchors
   - and canonical multi-view run homes
   are important enough to belong in canonical data.

If the repo reaches that stronger conclusion, Proposal A becomes the right
choice.

If not, Proposal C is the cleaner design.
