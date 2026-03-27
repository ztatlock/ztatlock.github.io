# Service Redesign Review: Agent B

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

1. pass 1: Proposal B
2. pass 2: Proposal C
3. pass 3: Proposal A

The standard used here is the latched requirements brief, especially the
long-horizon requirements around:

- stable anchors under backfill and multi-view rendering
- explicit recurring identity
- non-contiguous runs
- same-year multiplicity
- title drift
- rich details and link ownership
- deterministic ordering
- partial/uncertain historical knowledge
- future consumers beyond the current `/service/` page

## Executive View

My current ranking is:

1. **Proposal C**: best balance of simplicity and explicitness
2. **Proposal A**: strongest on robustness, but too canonically heavy
3. **Proposal B**: elegant but underpowered

My current recommendation is:

- if the redesign goal is genuinely to improve long-horizon clarity without
  overfitting the schema to current renderers, **Proposal C** is the strongest
  candidate
- **Proposal A** is defensible, but it over-corrects and risks baking present
  rendering policy into canonical data
- **Proposal B** helped surface the right direction, but it no longer matches
  the strengthened requirements closely enough

I am deliberately giving more weight to:

- future editability
- reduction of schema bulk
- avoiding canonicalization of consumer policy

and somewhat less weight to:

- making every currently annoying derived concept explicit in JSON

That weighting explains why I prefer Proposal C over Proposal A.

## Pass 1: Proposal B

### Summary Judgment

Proposal B is the most elegant-looking of the three on first read.

It has one powerful central move:

- make recurring identity structural by replacing flat per-year records with
  identity records that contain `instances`

That is a real improvement over the current `series_key`-plus-reaggregation
story. It also fits the repo’s existing taste:

- one canonical source
- explicit structure
- hand-editable JSON
- teaching-style identity plus instances

But after the requirements were strengthened, Proposal B now looks too
optimistic. It is simpler because it leaves several hard problems derived or
underspecified, not because it fully resolves them.

### What Proposal B Gets Right

#### 1. It fixes the current worst smell: implicit identity

This is Proposal B’s biggest contribution.

The current service model has:

- flat records
- optional `series_key`
- recurring identity only as an inferred grouping relation

Proposal B replaces that with:

- a stable identity object
- nested year instances
- explicit inheritance

That is a huge improvement for:

- editability
- validation
- reader comprehension
- duplication reduction

On this point, Proposal B is plainly better than the current model.

#### 2. One shape is genuinely pleasant

The “singletons and series use the same structure” idea is attractive for good
reasons:

- one validation path
- one authoring rhythm
- one reader expectation
- no top-level branching between singleton records and series records

This likely would make the file pleasant to scan and edit.

It would also reduce pointless repetition for uniform long-running service such
as:

- `UW Faculty Skit`
- `PACMPL Advisory Board`
- `PLDI Steering Committee`

#### 3. The inheritance model is clean

Identity-level defaults with instance overrides is the right base pattern for
this domain.

Proposal B is strong on:

- `role`
- `url`
- `details`

as inherited defaults with per-instance overrides.

That would sharply reduce canonical boilerplate and would make future editing
materially easier.

#### 4. It aligns well with teaching

This matters more than aesthetics.

The repo already understands:

- stable outer identity
- nested instances
- per-instance overrides

Proposal B uses the same mental model for service.

That consistency is valuable.

### What Proposal B Complicates Or Misses

#### 1. It conflates recurring identity with the visible grouped unit

This is the biggest weakness.

The requirements now make a clear distinction between:

- recurring identity
- contiguous run
- visible anchorable unit

Proposal B only models:

- identity
- instance

Runs are entirely derived.

That would be fine if runs were a minor renderer convenience. But the current
requirements show they are not:

- homepage wants to link to visible grouped entries
- service page wants stable grouped anchors
- future backfill will create more non-contiguous returns
- multi-view rendering complicates anchor identity

Proposal B still leaves too much of the real semantic load in derived code.

#### 2. Anchor stability is weaker than it first appears

Proposal B’s derived anchor story is clever, but not actually very strong.

The weak points are:

- single-run series anchor as bare `key`
- multi-run anchors as `key--START-END`
- section-prefixed anchors for multi-view cases

This means anchors still depend on:

- how runs are partitioned
- what years have been backfilled
- whether one identity has one run or multiple
- how many sections it appears in

That is exactly the kind of drift-sensitive logic the requirements are warning
about.

Proposal B argues that anchor change under run-boundary change is acceptable.
I am not persuaded. The requirements are more conservative than that.

#### 3. It assumes one identity-level `view_groups` default is usually enough

Proposal B does allow instance-level `view_groups` override, which is good.
But its center of gravity is still:

- one identity
- one default set of sections

That is weaker than the requirements document, which explicitly warns that
higher-level groupings should not assume stable shared section membership over
time.

This may not break often.
But the point of the redesign is to stop being surprised later.

#### 4. It does not give details a run-level home

This is a real omission.

Proposal B has:

- identity-level `details`
- instance-level `details`

But the requirements explicitly call out pressure at three levels:

- recurring identity
- contiguous run
- exact instance

There are realistic future cases where:

- something is true of one run, but not all runs
- the right place is neither the whole recurring identity nor a single year

Proposal B would force awkward duplication or over-hoisting there.

#### 5. It is weaker on title drift than it should be

Proposal B’s single-shape identity model assumes identity-level title is
stable enough.

That may be true now.
But the requirements explicitly ask for tolerance of:

- renamed programs
- title drift
- recurring lanes with evolving public labels

Proposal B does not really have a satisfying answer beyond “the identity title
is the title.”

### Hidden Seams And Likely Future Pain

#### A. Same-year multiplicity is not modeled confidently enough

Proposal B permits same-year multiplicity by array position.

I do not think that is enough.

The requirements are pointing toward:

- same-year multiplicity as a plausible future fact pattern
- anchors and consumer logic that may need to distinguish those instances

Array position is not a convincing canonical identity story.

#### B. Partial historical knowledge remains awkward

Proposal B does not say much about incomplete knowledge.

That matters because older service backfill may involve:

- uncertain runs
- fuzzy boundaries
- incomplete URLs
- incomplete role distinctions

Proposal B is neat when the author already understands the identity cleanly.
It is less convincing as a schema for exploratory historical cleanup.

#### C. It may underplay section duplication and anchor semantics

Proposal B treats section-prefixed anchors as an implementation detail.
I think that is a warning sign.

If anchor identity depends on section rendering, the model has not really
solved the “what is the stable visible unit?” question.

### Migration And Validation Implications

Migration would be straightforward:

- group flat records by `series_key`
- hoist shared fields
- inline `instances`

Validation would also improve:

- non-empty instances
- identity key uniqueness
- inheritance sanity
- repeated default detection

That is Proposal B’s real strength.

The problem is that the hard parts do not disappear.
They move into:

- run derivation
- anchor policy
- consumer logic

So migration is simpler than Proposal A, but conceptual cleanup is less
complete.

### Bottom Line On Proposal B

Proposal B is a meaningful improvement over the current model.

But against the strengthened requirements, it is now best understood as:

- a strong simplification move
- not yet a full design solution

I would not choose it if the goal is to stop revisiting service-model seams for
years.

## Pass 2: Proposal C

### Summary Judgment

Proposal C is the strongest design overall if the goal is:

- real simplification
- structural explicitness where it matters
- but no unnecessary canonical layer for every derived concept

It takes the best idea from Proposal B:

- make recurring identity structural

and then fixes several of Proposal B’s weak points:

- keep singletons simple
- allow instance-level `view_groups`
- add an explicit derived view layer with runs
- speak more directly to anchor rules and consumer usage

It still leaves some important seams.
But unlike Proposal B, those seams now look manageable rather than fundamental.

### What Proposal C Gets Right

#### 1. Two shapes is actually the right compromise

Proposal C’s two-shape model is better than Proposal B’s one-shape model.

Why:

- true singletons should not have to pretend to be recurring identities
- recurring series benefit from defaults and nested instances
- the schema is still small enough to understand

This is the place where Proposal C feels most aligned with the repo’s
“simple, explicit, narrow” design taste.

It avoids both extremes:

- Proposal B’s overly uniform shape
- Proposal A’s three-level canonical hierarchy

#### 2. It makes recurring identity explicit without over-canonicalizing runs

This is why I currently prefer it.

Runs are undeniably important.
But Proposal C keeps them in the derived-view layer rather than putting them in
canonical JSON.

That seems right to me because a run is partly:

- an actual temporal pattern
- and partly a consumer-facing grouping choice

Canonicalizing runs risks turning a useful summary concept into schema
obligation. Proposal C resists that.

#### 3. It has the cleanest relationship to the existing repo

Proposal C feels the most “native” to this codebase:

- singleton records resemble the current flat shape
- series records resemble teaching’s outer records
- the derived Python view layer is a normal repo pattern

That makes it easier to believe the redesign could land cleanly and be
maintained by future humans.

#### 4. It acknowledges multi-view and same-year stress better than Proposal B

Proposal C at least explicitly provides:

- instance-level `view_groups` override
- same-year multiplicity support
- explicit derived run views

Those moves show it has actually internalized the later requirements, not just
the original simpler brief.

#### 5. It keeps field ownership reasonably clear

Like Proposal B, it uses explicit inheritance.

That is still right.

But because it separates singleton and series records, it avoids a lot of the
“one shape but special meaning depending on count” awkwardness of Proposal B.

### What Proposal C Complicates Or Leaves Exposed

#### 1. Anchor identity is still derived, and that is its weakest point

This is the main reason I do not think Proposal C is an easy slam dunk.

Proposal C’s anchor logic still depends on:

- derived run partitioning
- run boundaries
- `key--START-END` for multi-run series

The proposal explicitly accepts anchor churn if run boundaries change under
backfill.

I understand the argument.
I still think this is the shakiest part of Proposal C.

If the repo is very serious about stable internal link targets, Proposal A is
better.

#### 2. It still has no explicit run-level metadata home

Proposal C keeps:

- series-level defaults
- instance-level overrides

But not a canonical run-level metadata object.

That is elegant.
It is also a real limitation for:

- run-specific details
- run-specific URLs that are not uniform across the whole series
- run-specific time semantics
- run-local title shifts

Today this may not matter often.
The requirements are intentionally preparing for a future where it might.

#### 3. It is not strong enough on title drift

This is a subtler version of the same problem.

Proposal C uses:

- series-level title
- singleton title

but not clearly:

- instance-level or run-level title override

That means it still assumes more title stability than the requirements want.

#### 4. It still leans on “derived views will sort it out”

Proposal C is much better than the current flat model.
But it still trusts the Python view layer to resolve several semantically
important questions:

- run identity
- anchor identity
- uniformity detection
- section projection

That is acceptable if the derived layer stays small and disciplined.
It is a risk if it becomes another home for hidden policy.

### Hidden Seams And Likely Future Pain

#### A. Section-safe anchors are still not fully satisfying

Proposal C’s anchor story is section-independent.
That is cleaner than Proposal B’s section-prefixed fallback.

But it also means:

- one rendered service run can appear in more than one section
- only one visible copy can really be “the” anchor target

Proposal C does not have as explicit an answer here as Proposal A’s
`primary_view_group`.

That may be a feature rather than a bug.
But it leaves a decision for renderer policy that Proposal A resolves in data.

#### B. Partial or uncertain knowledge remains only partly addressed

Proposal C is better than Proposal B because series and singleton shapes are
structurally simpler and derived views are clearer.

But it still assumes the author usually knows:

- whether something is a series or singleton
- what belongs in the same series
- what the shared defaults are

That is still a modest pressure point for older historical backfill.

#### C. Same-year multiplicity without instance keys is workable but not ideal

Proposal C says array position can distinguish same-year duplicates.

That is workable.
I do not love it.

If same-year multiplicity becomes common, Proposal C may eventually want
instance keys anyway.

### Migration And Validation Implications

Migration is still quite manageable:

- group by `series_key`
- create singleton or series records
- hoist shared defaults
- preserve overrides

Validation could be very good:

- record-shape discrimination
- non-empty series instances
- year ordering
- inherited field sanity
- role normalization
- details validation

This is one of Proposal C’s strengths: it improves the current model a lot
without exploding the validator surface the way Proposal A does.

### Bottom Line On Proposal C

Proposal C is the best current candidate if the redesign wants to stay:

- explicit
- relatively small
- familiar to the repo
- and not overfit to today’s service-page rendering concerns

Its weaknesses are real, especially around anchors and run-level metadata.
But I currently judge those to be the right remaining seams, not fatal flaws.

## Pass 3: Proposal A

### Summary Judgment

Proposal A is the most complete and the most conservative from a correctness
perspective.

If the only question were:

- “Which proposal most fully resolves today’s identified service seams?”

the answer would probably be Proposal A.

But I do not think that is the only question.
The better question is:

- “Which design most improves long-horizon clarity without turning the schema
  into a mirror of current consumer structure?”

On that question, Proposal A becomes more mixed.

### What Proposal A Gets Right

#### 1. It takes stable visible units seriously

Proposal A’s best idea is:

- `run` is the visible, anchorable, consumer-facing unit

That is a real answer to a real problem.

Compared to Proposal B and C, Proposal A is strongest on:

- stable anchor home
- multi-view internal linking
- service/homepage shared grouped unit

#### 2. It models three levels directly

The requirements name pressure at:

- instance
- run
- series

Proposal A simply reflects that structure.

That makes several currently hard questions easier:

- where does run-level metadata live?
- where does anchor identity live?
- where does a multi-view visible entry live?

This is why Proposal A feels robust.

#### 3. It has the best answer to multi-view ambiguity

The explicit `primary_view_group` is ungainly, but useful.

Proposal A is strongest where the requirements are strictest:

- one canonical anchor home
- one canonical homepage target
- one canonical visible run record

### What Proposal A Complicates

#### 1. It turns derived grouping into canonical modeling

This is my biggest objection.

Proposal A promotes `run` into canonical JSON.

That means authors must now explicitly maintain:

- series records
- run records
- instance records

This is a lot more than the current repo usually asks of canonical shared data.

It also means the schema starts to encode:

- current grouping needs
- current linking needs
- current consumer concerns

That may be warranted.
But it is a very high bar.

#### 2. It makes the data model more complex than teaching

Proposal A cannot really claim the “same as teaching” advantage.

Teaching has:

- outer identity
- nested instances

Proposal A has:

- outer identity
- middle visible unit
- nested instances

That is a more elaborate structure than any current successful domain in the
repo.

I think that matters.

#### 3. `primary_view_group` still feels like a smell

I understand why it exists.
I still do not like it.

It feels like:

- section rendering policy
- internal link policy

have been pushed into canonical data because the proposal wants to solve them
once and for all.

Sometimes that is the right call.
Here I worry it is too eager.

#### 4. It increases migration and maintenance burden the most

Proposal A has the highest cost:

- more migration choices
- more identifiers
- more validator invariants
- more editorial modeling decisions

That extra burden only pays off if the repo really needs that structure soon.

I am not yet convinced it does.

### Hidden Seams And Likely Future Pain

#### A. Authors may disagree about what a run is

Proposal A assumes runs are canonical enough to encode.

But runs are partly:

- temporal fact
- interpretation
- rendering summary

If two humans disagree on whether something is one run or two, Proposal A turns
that disagreement into canonical schema friction.

Proposal C leaves more of that judgment to the derived layer, which I think is
often healthier.

#### B. Optional series plus required runs plus nested instances can become
fussy

Proposal A is robust partly because it gives every level a place.

But that also means:

- more sparse objects
- more optional fields
- more cross-level duplication opportunities
- more complicated migration scripts

That is real long-horizon maintenance cost.

#### C. It may still be weaker than it looks on partial knowledge

Proposal A has more places to put partial facts.
That is good.

But partial knowledge still has to be normalized into:

- a series
- a run
- one or more instances

That can encourage premature hardening of uncertain history.

### Migration And Validation Implications

Proposal A would require the most careful migration by far.

Validation burden rises significantly:

- series existence and integrity
- run existence and integrity
- run/series cross references
- run/instance consistency
- primary view-group sanity
- anchor identity invariants
- time-basis sanity

This is not a deal-breaker.
But it is a meaningful tax.

### Bottom Line On Proposal A

Proposal A is the most robust design if the repo wants to optimize for:

- explicit visible-unit semantics
- explicit anchor stability
- explicit multi-view resolution

I still think it is too much canonical machinery for a first redesign unless
the repo has already decided those problems must be solved in data rather than
in a thin derived layer.

## Overall Comparative Evaluation

### Strongest Aspect Of Each Proposal

#### Proposal A

- It takes stable visible-unit and anchor semantics most seriously.

#### Proposal B

- It most cleanly exposes recurring identity and inheritance with minimal
  conceptual machinery.

#### Proposal C

- It best balances structural explicitness with schema restraint.

### Weakest Aspect Of Each Proposal

#### Proposal A

- It canonizes too much consumer-shaped structure.

#### Proposal B

- It leaves too many requirements unresolved in derived code.

#### Proposal C

- Its derived run-anchor story is still weaker than the requirements ideally
  want.

### Where The Real Decision Lies

The central decision is not “three levels or two?”

It is:

- should **runs** be canonical data
- or should **runs** remain derived view objects over canonical identity plus
  instances?

Everything else follows from that.

If the answer is:

- “runs are canonical facts”

then Proposal A wins.

If the answer is:

- “runs are best treated as derived consumer-facing views over a cleaner
  canonical identity model”

then Proposal C wins.

I currently think the second answer is wiser.

### Recommendation

My recommendation is:

1. treat Proposal B as superseded
2. focus the real choice on Proposal A vs Proposal C
3. prefer Proposal C unless anchor stability and multi-view canonical-home
   semantics are judged strong enough to justify Proposal A’s extra weight

More concretely:

- If you want the cleanest **schema** with the fewest long-term moving parts,
  choose **Proposal C**
- If you want the most explicit **consumer contract** and are willing to pay
  more canonical complexity, choose **Proposal A**

My own vote is **Proposal C**, but not casually. It would still need one more
careful pass on:

- anchor semantics
- title drift
- run-level metadata pressure
- same-year multiplicity identity

If those cannot be resolved cleanly without accreting more derived complexity,
then Proposal A becomes the safer choice.
