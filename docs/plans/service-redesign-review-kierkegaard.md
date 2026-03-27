# Service Redesign Review - Kierkegaard

Status: draft review

Scope:

- Proposal A: `docs/plans/service-redesign-proposal.md`
- Proposal B: `/Users/ztatlock/Downloads/foo/service-model-proposal-claude.md`
- Proposal C: `/Users/ztatlock/Downloads/service-model-proposal-claude.md`

Rotation order for this review:

1. Proposal A
2. Proposal B
3. Proposal C

## Pass 1 - Proposal A

Proposal A is the only design here that makes the service domain's three
important granularities explicit in the canonical model itself: `series`,
`runs`, and `instances`. That is a real strength because the hardest current
requirements are not about storage efficiency; they are about making visible
units, stable anchors, and multi-view rendering first-class instead of inferred
from flat records. The explicit `run` layer is especially strong for the public
`/service/` page and homepage consumers, because it gives the model a natural
anchorable rendering unit instead of forcing those consumers to reconstruct one
from scattered facts.

The `primary_view_group` idea is also a good fit for the requirements. It
solves the multi-view membership problem without pretending that a record has
only one home. That is a real design advantage over the current model, and it
is more honest than section-specific duplication. In the same vein, the
explicit field ownership rules are a strong step toward keeping authoring
predictable: if a fact belongs to the run, it lives on the run; if it varies by
instance, it lives on the instance. That is the right instinct for long-horizon
maintainability.

The main weakness is that Proposal A may be over-modeling the canonical data
relative to the requirements. The requirements ask for three granularities to
be supported, but not necessarily all encoded as top-level authored structures.
Making both `series` and `runs` explicit in the JSON increases the amount of
schema surface the repo has to validate, keep in sync, and teach to future
contributors. The design is clean conceptually, but it is also the heaviest
proposal to migrate and the most likely to accumulate cross-field drift if
validation ever becomes incomplete.

There is also a hidden seam in the way the proposal splits ownership across
`series`, `run`, and `instance` for `title`, `role`, `url`, and `details`. That
split is principled, but it creates more places where future backfill can go
wrong. A later maintainer will have to decide whether a new fact belongs to the
series, the run, or the instance, and that choice will matter for every
consumer. The model is more explicit, but it is not free. It trades inference
cost for authoring cost.

The biggest practical concern is role duplication across runs. Proposal A
deliberately omits a default `series.role`, which keeps roles tied to the
visible unit, but it also means a uniform role that really belongs to a long
recurring identity has to be repeated on every run. That is not fatal, but it
does mean the schema does not fully exploit the compression opportunity that
the requirements leave open. In the same category, the `details_djot` naming
leaks implementation format into the data model more than seems necessary.

Validation complexity is high here, but at least it is explicit. The model
needs to enforce series/run consistency, view-group placement, anchor
uniqueness, and the hand-authored field ownership rules. That is a lot, but it
is the right kind of work if the goal is to stop hidden derivation from
silently shaping consumer output. The proposal is strongest when judged by the
requirements around stable anchors, multi-view membership, and consumer-facing
run identity.

## Pass 2 - Proposal B

Proposal B is the most conservative of the three. It keeps the canonical shape
close to the current flat model while introducing just enough structure to make
recurring service identities explicit. That makes it attractive as a migration
story: one identity block with nested instances is easy to scan, easy to hand
edit, and easy to backfill mechanically from the existing corpus. It also fits
the repo's broader preference for identity-plus-instances patterns, which is a
real advantage for contributor comprehension.

Its best feature is simplicity of the authored data. Compared with Proposal A,
there is much less schema to explain. Compared with Proposal C, it is still
fairly direct about the canonical JSON shape and the inheritance contract. The
model clearly separates singleton facts from recurring series, and it gives
shared fields a sensible home at the identity level. That reduces duplication,
which is important for long-running service lanes with stable titles or URLs.

The major weakness is that Proposal B pushes the hardest part of the problem
back into code. Runs are not an authored concept here; they are something the
renderer must infer from a sorted instance list. That is exactly where the
current design pressure comes from, and the proposal does not fully remove it.
It reduces one class of hidden derivation, but it leaves the run boundary,
anchor construction, and section-grouping logic to consumer code. That is
acceptable as an implementation tactic, but it is not yet a complete answer to
the requirements.

The anchor scheme is the clearest mismatch with the requirements. Anchors that
depend on `key--START-END` are readable, but they are not truly stable under the
late backfill cases the requirements explicitly call out. If older years are
added later, the rendered run boundary can change, which changes the anchor.
That is a real regression risk for homepage links, internal references, and any
future consumer that assumes anchors are durable identifiers rather than
derived labels. The section-prefixed anchor workaround for multi-view records
also feels like special casing rather than a clean resolution.

Proposal B is also weaker on future-proof validation than it first appears. It
has the right instinct about inheritance and uniqueness, but it does not fully
solve role normalization, section membership semantics at more than one
granularity, or the exact shape of visible grouped units. It is a good
incremental bridge away from the flat model, but it still leaves too much policy
to consumer code to be the final long-horizon design.

## Pass 3 - Proposal C

Proposal C is the most operationally complete of the two-shape proposals. It
keeps the canonical data relatively simple, but it also makes the code-side
contract much clearer by spelling out derived `ServiceInstanceView`,
`ServiceRunView`, and `ServiceSeriesView` objects, plus ordering, validation,
and consumer usage rules. That is a real improvement over Proposal B because it
turns the design from a shape sketch into an implementation plan. The migration
path is also more honest: it says up front that the loader and renderer should
be updated in step with the new view layer.

This proposal is strongest where it admits that runs are derived and that the
canonical data should stay hand-editable. That is a good match for this repo.
It avoids the heavier authored schema of Proposal A while still giving the code
clear boundaries for homepage, service page, and CV consumers. The inclusion
of explicit run partitioning and ordering rules is useful because it makes the
behavior testable instead of leaving it to convention.

The primary weakness is the same one that affects Proposal B: anchors are still
derived from run boundaries. A `key--START-END` anchor is fine as a display
label, but it is not a satisfying answer to the requirement that anchors
survive future backfill. If the run boundary changes, the anchor changes. The
proposal is candid about that, but candor is not the same as solving the
requirement. Section-prefixed anchors for multi-view records also make the
anchor story more complicated than it should be.

Proposal C is also less decisive than Proposal A on role normalization and
field ownership. It explicitly defers role normalization to a later validation
rule, which keeps the proposal flexible but means it does not yet answer one of
the requirements directly. It is a strong architecture note, but it still
depends on future code choices for some of the thorniest semantic questions.
That makes it less complete than Proposal A on the hardest requirements, even
though it is more operationally polished than Proposal B.

## Overall Comparison

Proposal A is the strongest answer to the requirements that matter most for the
service redesign: stable visible units, multi-view membership, and durable
anchors. Its big cost is that it raises the canonical schema complexity and the
validation burden. In other words, it buys correctness and explicitness by
making the authored model heavier. That is a defensible trade if the goal is to
stop future backfill and rendering ambiguity from recurring.

Proposal C is the best of the two-shape, derived-run proposals. It is clearer
and more implementation-ready than Proposal B, and it gives the loader and
renderers a concrete view layer to target. But it still inherits the anchor
fragility of derived run boundaries, so it does not fully satisfy the
requirements as written.

Proposal B is the weakest final design. It is attractive as a migration bridge
because it is compact and hand-editable, but it leaves too much run logic and
anchor policy in consumer code. That means it simplifies the data file more
than it simplifies the long-horizon system.

## Final Ranking

1. Proposal A
2. Proposal C
3. Proposal B

Bottom line: if the anchor and multi-view requirements are truly hard
constraints, Proposal A is the only one that fully leans into them. If the team
decides to optimize for the smallest possible canonical schema instead, then
Proposal C is the safer compromise, but it still leaves a real backfill
problem unresolved. Proposal B is best treated as an intermediate step, not the
final redesign.
