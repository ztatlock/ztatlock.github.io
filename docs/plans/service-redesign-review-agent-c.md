# Service Redesign Review: Agent C

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

1. pass 1: Proposal C
2. pass 2: Proposal A
3. pass 3: Proposal B

The standard used here is the latched requirements brief, especially the
stronger long-horizon requirements around:

- future backfill
- stable anchors
- multi-view rendering
- title drift
- partial knowledge
- rich details with validation
- same-year multiplicity
- keeping designs explicit but not over-clever

## Executive View

My current ranking is:

1. **Proposal A**: the only one that fully closes the hard seams
2. **Proposal C**: a strong contender, but still too dependent on derived code
3. **Proposal B**: useful transitional idea, not enough now

My current recommendation is:

- if the repo is willing to redesign the service model at all, it should do it
  in a way that actually resolves the identified long-horizon problems
- that points to **Proposal A**
- **Proposal C** is respectable and substantially cleaner than the current
  model, but I think it would still leave enough unresolved pressure that the
  repo would be back in service-model debates later

This review deliberately gives extra weight to:

- future-proof anchors
- reducing hidden semantics in renderers
- making grouped visible units first-class when the site already depends on
  them

That weighting explains why I rank Proposal A first.

## Pass 1: Proposal C

### Summary Judgment

Proposal C is the most intellectually attractive competitor to Proposal A.

It has several strong instincts:

- recurring identity should be structural
- singletons should remain simple
- derived views are a normal and acceptable part of this repo
- explicit runs in JSON may be more than the schema truly needs

I take those points seriously.
But after evaluating it against the strengthened requirements, I think Proposal
C still leaves too much of the domain’s real semantics in code.

It is a strong redesign.
I do not think it is the final redesign.

### What Proposal C Gets Right

#### 1. It fixes the current identity problem cleanly

Proposal C decisively improves on the current model by making recurring
identity structural instead of inferred from `series_key`.

That alone is valuable:

- no more bottom-up grouping to reconstruct series identity
- explicit inheritance for shared metadata
- dramatically less canonical duplication

This is a major improvement over the current flat term model.

#### 2. Two shapes is a realistic compromise

Proposal C’s distinction between:

- singleton records
- series records with instances

is more convincing than Proposal B’s single-shape universal identity block.

That keeps truly one-off facts from paying needless schema overhead while still
making recurring identities explicit.

#### 3. It gives a plausible migration path

The migration story is very believable:

- group by `series_key`
- create series records where recurring identity is already evident
- preserve singleton facts directly
- hoist shared metadata

This matters because a redesign that is conceptually clean but operationally
painful often stalls.

Proposal C does not have that problem.

#### 4. It stays closer to the repo’s established patterns

Proposal C feels like an extension of:

- teaching outer records plus offerings
- current projection-backed wrapper domains
- thin view-layer normalization in Python

That makes it culturally plausible in this codebase.

### What Proposal C Complicates Or Leaves Weak

#### 1. Runs remain too important to stay merely derived

This is my core objection.

The requirements do not describe runs as a minor display convenience.
They describe them as central to:

- stable anchors
- homepage summary targets
- non-contiguous recurring identity
- grouped summaries
- future service-page formatting

Proposal C still treats runs as:

- derived view objects
- not canonical data

I think that leaves a mismatch between what the domain needs and what the
schema acknowledges.

#### 2. Anchor semantics are still too fragile

Proposal C’s anchor story is honest, but not strong enough.

It says, in effect:

- if run boundaries change under backfill, anchors can change too

That may be acceptable in some systems.
I do not think it matches the tone of this repo’s requirements, which are
trying to eliminate exactly these kinds of hidden instability points.

Proposal C has improved the model.
It has not fully solved anchor identity.

#### 3. It has no canonical run-level metadata home

This is the next big gap.

The strengthened requirements emphasize that some facts may belong at:

- instance level
- run level
- recurring identity level

Proposal C only canonically models:

- singleton
- series
- instance

That means run-specific facts still have nowhere clean to live.

Examples of future pressure:

- one run of a recurring identity having a shared landing page
- one run having a shared note or detail block
- one run needing an academic-year or event-year interpretation
- one run being the canonical visible thing the homepage should link to

Proposal C pushes all of that into derived logic or awkward field ownership.

#### 4. It is underpowered on title drift

Proposal C is too optimistic about title stability.

The requirements explicitly ask for tolerance of:

- renamed programs
- rebranded committees
- evolving public labels within one underlying service lane

Proposal C does not provide a strong enough story for that beyond implicit
series continuity.

That is manageable, but it is still a seam.

### Hidden Seams And Likely Future Pain

#### A. Same-year multiplicity without instance keys is thin ice

Proposal C says:

- same-year multiplicity can be distinguished by array position

That is serviceable.
It is not robust.

If same-year multiplicity becomes something the site wants to link to or reason
about, Proposal C will immediately want instance keys.

#### B. Multi-view facts are still awkward

Proposal C improves on Proposal B by allowing instance-level `view_groups`.
Good.

But it still does not completely answer:

- which rendered copy is the canonical internal-link destination?
- which section “owns” the anchor when one visible thing appears in more than
  one section?

Proposal A answers that.
Proposal C does not.

#### C. Partial historical knowledge remains only partially supported

Proposal C is structurally better than the current model, but it still assumes
the editor often knows enough to confidently form:

- a recurring series
- inherited defaults
- clean instance sets

For messy historical backfill, that may still be optimistic.

### Migration And Validation Implications

Migration is quite tractable.
Validation is better than today.

That is important.
But those are not the only standards.

I think Proposal C would migrate cleanly and still leave enough domain pressure
that the next stage of service work would reopen the model question.

### Bottom Line On Proposal C

Proposal C is a serious design and a strong improvement.

If Proposal A did not exist, I would treat Proposal C as the leading candidate.

But Proposal A does exist, and once it does, Proposal C starts to look like a
half-step:

- much better than today
- but not clearly the end of the redesign conversation

## Pass 2: Proposal A

### Summary Judgment

Proposal A is the only proposal that fully internalizes what the requirements
are really saying:

- the service domain has at least three meaningful levels
- the site already needs the middle level in a stable way
- pretending otherwise just moves semantics into code

It is heavier than the alternatives.
I think it is heavy for good reason.

### What Proposal A Gets Right

#### 1. It matches the actual semantic pressure

Proposal A gives first-class canonical homes to:

- recurring identity (`series`)
- visible grouped unit (`run`)
- atomic fact (`instance`)

That is not arbitrary layering.
It is a direct answer to the current seams.

This matters because the service audit did not discover one nuisance.
It discovered a cluster:

- non-contiguous returns
- anchor instability
- multi-view ambiguity
- run-level detail pressure
- homepage/service-page link divergence

Proposal A is the only model that answers all of those in one coherent way.

#### 2. It gives the homepage and `/service/` the same stable middle unit

This is a major strength.

Under Proposal A:

- `/service/` renders runs
- homepage recent-service selects runs
- anchors attach to runs
- internal links target runs

That means consumers are no longer asking the loader to infer “what the real
visible thing is.”

That is exactly the kind of clarity the redesign is trying to create.

#### 3. It is strongest on anchors

The requirements are paranoid about anchors for good reason.

Proposal A handles that best because:

- run identity is canonical
- run keys do not depend on inferred `START-END`
- multi-view anchor home is explicit

This is the most convincing answer across the three proposals.

#### 4. It gives run-level details and time semantics a real place

This is a point the simpler proposals keep dodging.

Proposal A can cleanly express:

- series-level metadata
- run-level metadata
- instance-level metadata

That is the first time the requirements around detail ownership and
academic-year semantics actually feel satisfied rather than merely tolerated.

#### 5. It reduces hidden derivation pressure the most

Proposal A does not eliminate derived logic.
It does eliminate the need for derived logic to shoulder core ontology.

That is the most important difference.

### What Proposal A Complicates

#### 1. It is the largest schema

This is the obvious tradeoff.

Proposal A adds:

- top-level `series`
- top-level `runs`
- nested `instances`

That is more to edit, more to validate, and more to migrate.

The schema bulk is real.

#### 2. It risks canonicalizing present consumer policy

This is the best criticism of Proposal A.

Runs are semantically real, but they are also currently tied to:

- visible summary lines
- anchor strategy
- homepage grouping

If those consumer needs change later, Proposal A may feel too rigid.

I think this risk is real, but smaller than the risk of continuing to hide
run semantics in code.

#### 3. `primary_view_group` is inelegant

This is the ugliest field in Proposal A.

But I think it is ugly because the underlying problem is ugly:

- one thing appears in more than one section
- one anchor home still has to win

I view this less as a flaw in Proposal A than as evidence that Proposal A is
actually modeling the real problem instead of dodging it.

### Hidden Seams And Likely Future Pain

#### A. Editorial certainty is required earlier

Proposal A expects authors to commit more clearly to:

- series boundaries
- run boundaries
- level ownership

That is a cost.
It may feel heavy during uncertain historical backfill.

#### B. Migration would need careful review

Because Proposal A is richer, its migration cannot just be:

- group by `series_key`
- hoist shared fields

It also needs:

- run decomposition
- run key design
- primary view-group decisions

This is a real cost and should not be minimized.

### Bottom Line On Proposal A

Proposal A is the only design that looks genuinely capable of resolving the
service model question instead of just improving it.

If the repo is redesigning at all, that matters.

## Pass 3: Proposal B

### Summary Judgment

Proposal B is the most elegant in prose and the weakest in long-horizon fit.

It is a strong conceptual step beyond the current flat model, but it was
written against an earlier and less demanding version of the requirements.
That shows.

### What Proposal B Gets Right

#### 1. Identity-with-instances is still the correct basic move

Proposal B deserves credit for seeing the fundamental problem clearly:

- recurring identity should not be implicit

That is still right.

#### 2. One-shape authoring is attractive

There is real beauty in:

- one record type
- nested instances
- consistent inheritance

It would be easy to explain and easy to edit.

#### 3. Boilerplate reduction is excellent

Proposal B is probably best at making the JSON visually compact.

That is meaningful.

### What Proposal B Gets Wrong

#### 1. It leaves too much crucial semantics derived

The fatal problem is that Proposal B still expects code to carry too much
meaning around:

- runs
- anchors
- section-safe link behavior
- visible grouped-unit semantics

That is exactly what the redesign is supposed to improve.

#### 2. It is too relaxed about anchors

Proposal B’s anchor story depends on:

- derived runs
- key plus range logic
- sometimes section prefixes

That is not strong enough for the requirements as written now.

#### 3. It is weak on same-year multiplicity and title drift

Those newer requirements expose Proposal B’s age.

It does not really have:

- strong same-year instance identity
- strong title-drift handling
- strong partial-knowledge handling

#### 4. One shape is not actually enough

The simplicity of one shape comes at the cost of semantic precision.

The service domain already wants:

- true one-offs
- recurring identities
- grouped visible units

Proposal B’s single-shape aesthetic starts to feel like discipline imposed on
the data rather than clarity earned from it.

### Bottom Line On Proposal B

Proposal B is an important design step, but not the final answer.

It helped reveal what matters.
It no longer satisfies enough of the requirements to deserve first place.

## Overall Comparative Evaluation

### Strongest Aspect Of Each Proposal

#### Proposal A

- It canonically represents the actual semantic layers the site already needs.

#### Proposal B

- It expresses recurring identity and inheritance with great simplicity.

#### Proposal C

- It captures most of the gain of identity-plus-instances while staying much
  lighter than Proposal A.

### Weakest Aspect Of Each Proposal

#### Proposal A

- It is the most expensive and most editorially demanding migration.

#### Proposal B

- It still leaves too much of the hard domain logic as derived convention.

#### Proposal C

- It still treats runs as less important than the requirements suggest they
  really are.

### Where The Decision Really Is

Proposal B is no longer the serious frontrunner.

The real choice is:

- **Proposal A**
  if you believe the visible run is a canonical fact that deserves stable
  identity and metadata

- **Proposal C**
  if you believe the visible run should remain a disciplined derived view over
  a simpler canonical identity model

I think the requirements now favor the first answer.

### Recommendation

My recommendation is:

1. retire Proposal B as a historical stepping stone
2. treat Proposal C as the best simplification-oriented alternative
3. prefer Proposal A if the repo truly wants to get ahead of future service
   backfill and anchor/link complexity instead of revisiting them later

So my current vote is **Proposal A**.

Not because it is prettier.
It is not.

Because it is the only one that seems to me to take the discovered service
pressure seriously enough to be done with this problem rather than merely
improve it.
