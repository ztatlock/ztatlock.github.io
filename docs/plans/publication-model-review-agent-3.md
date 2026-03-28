# Publication Model Review: Agent 3

Status: independent review draft

Inputs reviewed:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-requirements-review-synthesis.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements-review-synthesis.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)
- [publication-model-xavier-leroy-lessons.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-xavier-leroy-lessons.md)
- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-proposal-b-semantic-objects.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-b-semantic-objects.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)
- [publication-model-proposals-patch-list.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-patch-list.md)
- [publication-model-proposals-claude-review-1.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-1.md)
- [publication-model-proposals-claude-review-2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposals-claude-review-2.md)

Optional code grounding reviewed:

- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- [publication_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_index.py)
- [page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)

## Overall Judgment

I do **not** think Proposal A should win by default just because it is closer
to the current model.

After reading the requirements, corpus notes, prior reviews, and the actual
current loader/renderers, my current judgment is:

- **Proposal B is the better long-horizon direction**, but only if it stays
  disciplined and does **not** keep drifting toward a speculative ontology.
- **Proposal A is the safer near-term migration**, but it looks increasingly
  like a deliberately temporary refinement rather than the model I would want
  to keep for the next several years of publication growth.

So if the question is:

“Which proposal better positions the repo for future books / chapters /
proceedings / analysis / derived views?”

my answer is:

- **B is more promising**

If the question is:

“Which proposal minimizes immediate migration pain while fixing the strongest
current seams?”

my answer is:

- **A is more pragmatic**

Because the user explicitly asked to **downweight inertia** and **upweight
future simplicity and failure modes**, I currently favor **Proposal B**, with
targeted simplifications.

## 1. Findings On Proposal A

### A is strong where the current seams are concrete and immediate

Proposal A is a good direct response to the current audit.

It squarely fixes the five clearest real problems:

- explicit canonical year instead of slug-year / `pub_date` confusion
- explicit compact venue label instead of overloading `venue`
- clearer local-page readiness naming
- explicit identifiers
- explicit `pub_type` beside `listing_group`

That is not trivial.
Those are the actual seams that the repo is feeling today.

### A is especially good for migration honesty

Against the real current code, A is much less invasive than B.

Current code is very flat:

- `PublicationRecord` is a flat dataclass
- `publication_index.py` sorts directly on `record.pub_date`
- `page_projection.py` renders directly from `record.venue`,
  `publication_year(record.slug)`, `record.listing_group`
- `build_pub_inventory.py` relies directly on `record.detail_page`

Proposal A still requires real work:

- dataclass changes
- loader whitelist changes
- validation changes
- consumer rewrites for `pub_year` and `local_page`
- corpus-wide venue cleanup

But it does **not** require a new access pattern everywhere.
It keeps the authored record mentally flat.

### A fits the current corpus well

The corpus reality check strongly supports A’s main field additions:

- full/compact venue split is justified by `68/69` venue strings ending with a
  compact parenthetical
- explicit canonical year is justified by the `3/69` slug-year vs `pub_date`
  mismatch cases
- a small `pub_type` vocabulary looks feasible

So Proposal A is not solving imaginary problems.
It is solving real ones with minimal new structure.

### A is weaker on the next wave of publication complexity

This is where my skepticism rises.

Proposal A’s basic move is:

- add a few more top-level fields
- keep the rest of the record shape intact

That works for this round of seams.
It does **not** really address the deeper question:

- what shape should the publication record have once the repo wants more
  derived views and more semantic distinctions?

The requirements explicitly point toward future pressures around:

- books
- book chapters
- proceedings
- venue identity across papers
- analysis pipelines
- BibTeX / DOI / identifier-aware derivations
- richer top-of-CV and research/collaborator consumers

Proposal A does not fail those outright.
But it mostly leaves them as future additive top-level fields.

That is the part I distrust.

### A’s flatness is becoming structural debt

Proposal A solves the current seam by adding:

- `pub_year`
- `venue_short`
- `pub_type`
- `local_page`
- `identifiers`

That is already a noticeable expansion.

And the likely next pressures are exactly the ones that would add still more:

- venue identity
- publication family/series
- proceedings/container information
- books vs chapters vs reports distinctions
- maybe selection/prominence later

The problem is not “flat fields are always bad.”
The problem is that A’s answer to nearly every future seam is “one more
field.”

That is manageable in the short term.
I do not think it is the cleanest long-term publication model.

### A leaves BibTeX/identifier strategy too under-articulated

The requirements explicitly asked for attention to identifier strategy and the
relation to BibTeX.

Proposal A improves identifiers by adding an `identifiers` object, which is
good.
But it still reads as if identifiers are an auxiliary bag rather than an
important semantic substrate.

In particular:

- DOI and publisher link remain parallel authored facts
- no stronger stance is taken on which is canonical for tooling
- no explicit thought is given to proceedings/container semantics where BibTeX
  fields often matter

This is not a blocker for A.
It is a sign that A is more “patch the current schema” than “clarify the
semantic core of the publication model.”

### A undershoots future derived views

The Xavier Leroy lesson matters here.

Xavier’s system is powerful not because it has one pretty bibliography record,
but because the data is organized enough to support multiple honest projections:

- by year
- by kind
- by topic
- by venue family

Proposal A helps with “by kind” a bit through `pub_type`.
But it does not make grouped semantic views especially natural.

You can build them.
But the model itself is still mostly a page-oriented bibliographic bundle plus
extra scalar fields.

## 2. Findings On Proposal B

### B is the only proposal that really tries to improve the semantic shape

Proposal B is not just “more nested A.”

Its core argument is:

- the current pressure points are not independent fields
- they are semantic clusters
- the model should make those clusters explicit now

I think this is the right long-horizon instinct.

The most convincing grouped objects are:

- `time`
- `venue`
- `classification`
- `identifiers`

Those are real semantic units.
They are not arbitrary nesting for its own sake.

### B gives the repo a better substrate for future publication work

This is the strongest point in B’s favor.

The requirements do not just ask to fix today’s homepage seam.
They ask for a model that can remain useful as the repo grows into:

- books
- book chapters
- proceedings
- future analysis features
- richer cross-domain consumers

B’s grouped shape is much better prepared for that future because it cleanly
separates:

- time semantics
- venue semantics
- classification semantics
- local-page readiness semantics
- identifier semantics

That gives later proposal work a better place to land.

For example:

- adding publication-series/container semantics fits more naturally near
  `venue` or `classification`
- adding DOI-aware derivation logic fits naturally under `identifiers`
- adding books/chapters/proceedings distinctions fits naturally under
  `classification`

In A, each of these would likely become another top-level patch.

### B is better aligned with the stated long-horizon review philosophy

The instruction to downweight inertia matters here.

If I ignore current code shape and ask:

“What record shape would I rather keep extending for five more years?”

I prefer B.

Why:

- the semantic clusters are clearer
- the authored data communicates intent better
- future consumers have cleaner inputs
- the record is less likely to become a growing checklist of unrelated fields

### B still keeps the right architectural boundary

This is important.

B does **not** propose a service-style reset.
It keeps:

- one bundle per publication
- one `publication.json` per bundle
- current local-assets model

So B is not radical architecture.
It is a schema improvement inside the current architecture.

That makes it much more credible than a more ambitious publication redesign
would be.

### B’s costs are real, not imaginary

Proposal B absolutely has higher migration cost.

Against the current code, it means:

- nested dataclasses or equivalent normalized structures
- loader/validator rewrite
- every consumer access path changing
- more complex JSON normalization
- more nested diffs and slightly heavier authoring

This is real.
It should not be hand-waved away.

### B is strongest if kept disciplined, weakest if it drifts further

My support for B is conditional.

I do **not** think B should grow into:

- venue registry
- venue family ontology
- author identity overhaul
- topic-tag system
- citation graph

If it starts trying to solve those now, it becomes over-scoped.

But the current draft of B is still relatively disciplined.
It groups the obvious semantic clusters without trying to build a giant graph.

That is why I think it remains viable.

### B still has one real ambiguity: does nesting buy enough?

This is the most important criticism against B.

For some of its objects, the benefit is obvious:

- `venue.full` / `venue.short`
- `time.year` / `time.date`
- `identifiers`

For others, it is more debatable:

- `classification`
- `local_page`

I think `classification` is justified.
I am less convinced `local_page` needs to be an object yet.

`local_page.mode` is semantically cleaner than a boolean, but it may be a more
ornate representation of a seam that is still effectively binary today.

So B is promising, but some of its grouping should perhaps be selectively
pruned rather than accepted wholesale.

## 3. Strongest Pros/Cons Of Each

### Proposal A

Strongest pros:

- smallest migration among serious options
- directly solves the strongest current seams
- fits the current corpus and current code with less upheaval
- easiest to backfill quickly before larger publication expansion
- lowest risk of getting bogged down in model work

Strongest cons:

- likely to continue flat-field sprawl
- weaker long-term semantic shape
- treats future semantic growth as additive patches
- under-prepares the repo for books/chapters/proceedings-style expansion
- weaker foundation for richer derived views and identifier-driven tooling

### Proposal B

Strongest pros:

- cleaner semantic clustering
- better long-term extensibility
- better substrate for later analysis and richer projections
- more future-proof for books/chapters/proceedings distinctions
- better separation of “what kind of fact this is” from page-specific
  rendering concerns

Strongest cons:

- heavier migration across loader, validators, and all consumers
- more nested JSON and noisier diffs
- some objects may be more structured than current consumers strictly need
- risks drifting into speculative modeling if not kept disciplined

## 4. Where Each Proposal Is Under- Or Over-Scoped

### Proposal A is under-scoped in the long-horizon semantic sense

Under-scoped areas:

- venue identity / container semantics
- future by-kind / by-venue / by-analysis projections
- identifier strategy beyond “store some IDs”
- publication-type growth beyond the smallest current indexed distinction
- relation to possible future books / book chapters / proceedings features

Over-scoped areas:

- `pub_type` may be a bit over-eager if the repo is not ready to make it
  required immediately
- the conservative story is occasionally sold as “small” in a way that
  understates the real corpus-wide venue cleanup and consumer rewrites

### Proposal B is slightly over-scoped in structure, but less under-scoped

Under-scoped areas:

- it still does not really solve venue identity or proceedings/container
  semantics, it only prepares for them better
- it still defers stronger author identity questions
- it still leaves BibTeX authority and DOI-derived-link policy somewhat open

Over-scoped areas:

- `local_page` object may be more structure than needed in v1
- if `classification` later tries to absorb too many unrelated semantic axes,
  it will become muddy
- any temptation to add `venue.series` or a venue registry now would likely be
  premature

## 5. Which Proposal I Favor Now, If Any, And Why

I currently favor **Proposal B**, with refinement.

### Why not A?

Because when I discount inertia and focus on long-horizon maintainability, A
looks like the better patch set, not the better model.

I believe A would land cleanly.
I also believe the repo would revisit publication-model shape sooner than it
wants, because:

- the record would keep widening
- later books/chapters/proceedings pressure would not have a very natural home
- future semantic projections would still have to work around a page-leaning
  flat schema

### Why B?

Because B seems to hit the right middle ground:

- not a service-style reset
- still bundle-local
- still one `publication.json` per bundle
- but clearly more semantic and more extensible

That means B preserves the good architectural decisions already in place while
giving the schema a better long-term spine.

### What would make me change my mind back toward A?

Two things:

1. If the repo’s real constraint is “we must finish a large backfill very soon,
   and schema migration friction is the dominant risk.”
2. If a disciplined corpus test showed that most of B’s grouped objects buy
   very little in practice compared with A’s flatter additions.

Absent those two, I think B is the more convincing model.

## 6. Concrete Refinement Suggestions

### Refine A if it remains in contention

1. Make the “flat but growing” tradeoff explicit.
   Do not present A as merely cleaner.
   Say honestly that it prioritizes migration speed over deeper semantic
   restructuring.

2. Tighten the identifier stance.
   Explain more clearly whether DOI is expected to become the canonical
   machine-useful identifier and whether publisher URLs may later be derived
   from it.

3. Clarify what happens when the publication domain grows beyond
   `conference|journal|workshop`.
   Right now A hints that `pub_type` can expand, but it does not explain how
   this avoids becoming a flat metadata sprawl.

4. Add a limitation note about books/proceedings/container semantics.
   Be explicit that A does not solve those elegantly and would likely need a
   later structural pass.

### Refine B if it becomes the leading proposal

1. Keep `time`, `venue`, `classification`, and `identifiers`.
   Those are the most justified semantic objects.

2. Reconsider whether `local_page` needs to be an object in v1.
   A flatter `local_page` / `primary_link` pairing may be sufficient if the
   mode really is still binary in practice.

3. Be explicit that B is **not** introducing a venue registry or venue-family
   ontology now.
   It should prepare for later venue-related features without forcing those
   decisions early.

4. Add an explicit BibTeX/identifier note.
   The proposal should say whether identifiers are meant to become the
   machine-authoritative layer from which some links or derived exports can be
   produced.

5. Add a books/chapters/proceedings paragraph.
   B’s biggest strategic advantage is that it can grow into those better.
   It should say that explicitly and honestly.

6. Keep author identity conservative.
   Do not let B grow a people/collaborator schema in this pass.

## Final Recommendation

If the repo wants the **least disruptive** improvement now, choose A.

If the repo wants the **better publication model** for the next several years,
choose B, but keep it disciplined and resist speculative extra ontology.

My current vote is:

- **Favor Proposal B**
- but trim or simplify any parts of B that are nested without strong semantic
  payoff

That is the option I think best balances:

- current corpus reality
- future extensibility
- identifier-aware tooling
- later books/chapters/proceedings pressure
- richer derived views beyond current consumers

Changed file:

- `/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-3.md`
