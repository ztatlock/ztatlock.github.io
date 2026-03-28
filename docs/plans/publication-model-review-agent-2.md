# Publication Model Review: Agent 2

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

Optional code grounding used:

- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- [publication_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_index.py)
- [page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)

## Executive Judgment

I favor Proposal A today, but for narrower reasons than "it is closer to the
current code."

My read is:

- Proposal A is the better next move for this repo because it fixes the real
  seams directly, keeps authoring and backfill realistic, and does not create
  a larger migration surface than the current publication domain has earned.
- Proposal B is cleaner in the abstract, but too much of its extra structure is
  packaging rather than genuinely new semantic leverage.
- If the repo later accumulates stronger venue-identity, topic, or richer
  analysis consumers, a later move toward B-like grouping may become justified.
  I do not think the current corpus and current consumers justify paying that
  cost now.

That said, Proposal A should not be accepted unmodified.
It still needs a tighter treatment of:

- `pub_type`
- `primary_link`
- slug-year retirement
- the honest limitation that venue identity remains future work

## 1. Findings On Proposal A

Proposal A is the "conservative refinement" option:

- keep one bundle per publication
- keep one flat-ish `publication.json`
- add explicit fields for the seams that are now clearly real

### What A Gets Right

The strongest point in A's favor is that its new fields correspond almost one
for one with real pressure already visible in the requirements and in the
current consumers.

Those are:

- canonical publication year distinct from exact date
- compact venue display distinct from full bibliography display
- a clearer local-page-readiness name
- explicit identifiers
- a lighter semantic classification axis beyond `listing_group`

That is not cosmetic cleanup.
Those are the actual seams surfaced by:

- the homepage compact publication consumer
- the current slug-year vs `pub_date` mismatch cases
- DOI/arXiv pressure
- the boundary between thin and rich bundles

A therefore has a strong "semantic proportionality" advantage:

- it adds new semantics where the repo genuinely needs them
- it avoids changing the overall physical shape of every publication record
  just to achieve a cleaner conceptual grouping

### Migration Complexity

A is still a real migration.
It is not "almost free."

The current loader and consumers are tightly coupled to the old fields:

- `publication_index.py` sorts directly on `record.pub_date`
- `page_projection.py` renders venue-plus-year using `record.venue` and
  `publication_year(record.slug)`
- `build_pub_inventory.py` uses `record.detail_page` throughout
- `publication_record.py` whitelists allowed fields and author subfields

So A still requires:

- loader whitelist changes
- validator updates
- consumer rewrites for year rendering
- all-at-once rename of `detail_page`
- venue cleanup across the full indexed corpus

But A's migration is still materially smaller than B's because it preserves
the access pattern shape:

- top-level field stays a top-level field
- bundle authoring stays visually familiar
- existing code can be patched rather than conceptually rewritten

This matters because the repo is explicitly expecting substantial future
backfill.
The design should minimize the amount of structural churn that every future
bundle authoring pass must internalize.

### Backfill Practicality

This is where A is strongest.

Backfill under A remains easy to reason about:

- add `pub_year`
- clean `venue`
- add `venue_short`
- add `identifiers` where known
- add `pub_type` if required

Each of those changes is local to a single record.
Each is also visible in small diffs.

That matters more than usual here because:

- there are currently `69` indexed bundles
- the audit explicitly expects heavy future backfill
- older bundles are still mixed in richness

A's flatter shape is therefore not just inertia.
It is a genuine operational benefit for future corpus growth.

### Authoring And Diff Ergonomics

A is clearly better on diff ergonomics.

The physical record stays very close to today's mental model:

- title
- authors
- venue
- date/year
- links
- readiness

Adding a new value does not require remembering where a small nested object
lives.
That is not a trivial aesthetic point.
It directly affects:

- agent-assisted edits
- human review speed
- the chance of inconsistent backfill quality over dozens of bundles

### Validator / Loader Complexity

A raises complexity, but modestly.

The loader needs new normalizers for:

- `pub_year`
- `venue_short`
- `identifiers`
- possibly `pub_type`

But the current `PublicationRecord` remains mostly flat.
That means:

- fewer new nested dataclasses
- fewer nested validation branches
- simpler migration fallback logic if temporary dual-shape support were ever
  needed

This is a real advantage because `publication_record.py` is already the core
contract for several downstream consumers.

### Long-Horizon Failure Modes

A's biggest long-horizon risk is not immediate migration pain.
It is future flat-field sprawl.

The concern is real:

- `pub_year`
- `venue_short`
- `pub_type`
- `local_page`
- `identifiers`

already widen the record.

If the repo later adds:

- venue identity
- topic tags
- prominence or curation signals
- richer readiness states

then A could become a crowded field checklist.

That is A's real weakness.
It does not create much cleanup work now, but it may create another cleanup
point later if the publication model gains more semantic axes than currently
expected.

### Where A Still Feels Soft

The main unresolved places in A are:

#### `pub_type`

A currently wants to keep `listing_group` and add `pub_type`.
That is directionally right, but operationally unresolved.

If `pub_type` is optional:

- it risks becoming dead metadata
- future by-kind consumers will still not be trustworthy

If `pub_type` is required:

- the backfill burden becomes real immediately

The corpus note suggests a small required vocabulary is feasible.
I think A needs to commit one way or the other.
My own recommendation is:

- make `pub_type` required for indexed bundles
- keep the first vocabulary deliberately small

#### `primary_link`

A keeps it in examples but under-explains it in prose.
That is a mistake because `primary_link` is central to the thin-bundle path and
already lives in current code.

It should remain explicit in the proposal and in the final schema.

#### Slug-year coexistence

A correctly introduces canonical year semantics, but it needs to say plainly:

- display consumers should stop using `publication_year(record.slug)`
- slug year remains a path convention and validation check only

Without that, `pub_year` risks becoming nominal rather than canonical.

## 2. Findings On Proposal B

Proposal B keeps the same one-bundle-per-publication architecture, but groups
related facts into nested semantic objects:

- `time`
- `venue`
- `classification`
- `local_page`
- `identifiers`

### What B Gets Right

B's strongest virtue is conceptual hygiene.

It sees a real danger in A:

- the record can become a growing flat checklist

And B tries to solve that now rather than later.

The clearest wins in B are:

- `venue.full` and `venue.short` make their relationship explicit
- `time.year` and `time.date` clearly separate display year from exact date
- `classification` makes page grouping vs semantic type visibly distinct
- `identifiers` has a natural stable home

This is not fake cleanliness.
These groupings do line up with real semantic clusters in the requirements.

B is also better than A if the repo expects richer long-term projection and
analysis over publications.
Once grouped objects exist, later extension is more structured:

- add more identifier types
- add more classification axes
- maybe later add venue-family semantics

So B is not merely "fancy JSON."
It is a bid to reduce future schema entropy.

### Migration Complexity

B is materially heavier than A.

This is not just because it is nested.
It is because the current code assumes a flat record almost everywhere.

Current direct-field access is pervasive:

- `record.pub_date`
- `record.venue`
- `record.listing_group`
- `record.detail_page`
- `record.primary_link`

B would rewrite all of those access paths:

- `record.time.date`
- `record.venue.full`
- `record.classification.listing_group`
- `record.local_page.mode`
- `record.local_page.primary_link`

That means a coordinated rewrite for:

- loader
- validator
- `/pubs/`
- CV publication projection
- homepage recent publications
- inventory tooling

This is the biggest argument against B.
It is not that the structure is wrong.
It is that the repo would pay a lot of migration cost now for structure that
current consumers do not yet fully require.

### Backfill Practicality

B is worse for backfill, and this matters.

The near-future publication workload is not "maintain a stable small schema."
It is "keep adding and refining many bundles."

Under B, even simple edits become a little more ceremonious:

- date fields live in `time`
- venue fields live in `venue`
- readiness semantics live in `local_page`
- classification questions live in `classification`

That is not catastrophic.
But it is more typing, more indentation, and more opportunities for partial
shape mistakes.

Because backfill is a first-class concern in the requirements, this is not a
mere preference issue.
It is a real design cost.

### Authoring And Diff Ergonomics

B is noticeably worse than A here.

The proposal adds nested objects without adding proportionate expressive power
in every case.

For example:

- `time.year` and `time.date` are semantically clean, but they do not give
  the author much more than `pub_year` and `pub_date`
- `local_page.mode` is more self-describing than a boolean, but it also makes
  the common case more verbose

I think B underestimates how much diff noise this creates when repeated across
dozens of bundles.

### Validator / Loader Complexity

B is clearly heavier here.

It needs nested object normalization for:

- `time`
- `venue`
- `classification`
- `local_page`
- `identifiers`

That implies:

- more nested dataclasses or equivalent shapes
- more object-level validation code
- more branching in consumer logic

And critically, some of the nesting does not eliminate semantic questions.
It only relocates them.

Example:

- `classification` still does not decide whether `pub_type` is required
- `local_page.mode` still does not decide whether the repo truly needs more
  than a binary readiness distinction

So B increases validation complexity before the underlying semantic choices are
fully settled.

### Long-Horizon Failure Modes

B's long-horizon failure mode is subtler than A's.

It is not field sprawl.
It is over-scoped structure that may age into busywork.

The biggest risk is that B solves packaging more than it solves semantics.

Examples:

#### `classification`

This object is tidy, but it does not actually resolve the hardest
classification question:

- is `pub_type` required and trusted?

Without that decision, nesting does not buy much.

#### `local_page`

This object may be the clearest overreach in B.

The current domain pressure is:

- distinguish thin from full local pages
- keep `primary_link` explicit

That does not obviously require an object.
It may simply require a clearer field name.

So `local_page.mode` risks becoming a permanent layer of structural noise for a
binary concept.

#### Future cleanup risk

If the repo later decides some of this grouping was not worth it, un-nesting is
its own migration.
That is a real cost.
B therefore creates more risk of future cleanup work if its additional
structure turns out to be only modestly useful in practice.

### Where B Still Feels Soft

B also has some under-specified areas:

#### `venue` grouping is strong, but venue identity is still not really solved

B is better positioned than A for future venue identity, but the proposal does
not actually solve it now.
That is fine.
But it means some of B's extra cost is being paid in anticipation of a future
semantic axis rather than current necessity.

#### `local_page.mode` does not prove it earns its keep

This is B's weakest field cluster.
It is more structured than A's binary approach, but the repo does not yet have
a demonstrated third state or richer readiness consumer that requires it.

#### Migration payoff is still too implicit

B says it may age better.
That may be true.
But the proposal still does not fully prove that the extra nesting buys enough
real leverage before the next big backfill wave.

## 3. Strongest Pros And Cons Of Each

### Proposal A

Strongest pros:

- best backfill ergonomics
- smallest realistic migration
- easiest diffs and hand-editing
- directly fixes the currently visible seams
- keeps the publication bundle model narrow and explicit

Strongest cons:

- risk of long-term flat-field sprawl
- weak explicit home for future venue identity or richer classification axes
- unresolved `pub_type` policy
- can look cleaner than it is if migration cost is understated

### Proposal B

Strongest pros:

- cleaner semantic grouping
- better defense against future flat-schema sprawl
- stronger long-term shape for analysis and extension
- venue/time/classification distinctions become visibly first-class

Strongest cons:

- highest migration surface
- heavier authoring and noisier diffs
- some extra structure does not yet buy enough concrete value
- highest risk of "we paid for cleanup early, then had to clean it up again"
  if parts like `local_page.mode` turn out to be overbuilt

## 4. Where Each Proposal Is Under- Or Over-Scoped

### Proposal A Is Under-Scoped In These Areas

- venue identity remains explicitly future work
- `pub_type` policy is still not sharp enough
- `primary_link` treatment is not prominent enough
- slug-year retirement is not explicit enough

### Proposal A Is Over-Scoped In These Areas

A is not badly over-scoped.
Its main overreach risk is simply that it may add `pub_type` before the repo
has truly settled whether that field will be required and maintained well.

### Proposal B Is Under-Scoped In These Areas

- it still does not prove which nested structures are actually required now
- it does not settle the `pub_type` trust question
- it does not give a convincing semantic reason for `local_page.mode` beyond
  readability

### Proposal B Is Over-Scoped In These Areas

- `local_page` object
- early grouping of every semantic cluster before current consumers demand it
- migration size relative to current publication consumer pressure

This is why B feels simultaneously cleaner and less convincing.
It is more structured, but not all of that structure is earning immediate
value.

## 5. Which Proposal I Favor Now, If Any

I favor Proposal A now.

That is not because A is closer to the current code.
It is because A is the better trade under the actual pressures the repo has:

- real but still modest publication semantic expansion
- heavy near-future backfill
- strong preference for hand-editable records
- multiple consumers, but all still over one fundamentally flat publication
  object

If I aggressively downweight inertia and upweight long-term shape, B becomes
more interesting, but I still do not think it wins yet.

Why not:

1. B mostly reorganizes semantics that are already understandable in a flatter
   form.
2. The biggest future publication questions are still unresolved even under B:
   - venue identity
   - richer classification axes
   - author identity
3. The migration and authoring cost is immediate and certain, while much of
   B's advantage is contingent on future consumers that are not yet real.

So my recommendation is:

- choose A as the next real schema move
- but patch A before adoption so it is more honest about what it does not
  solve

## 6. Concrete Refinement Suggestions

### For Proposal A

1. Make `pub_type` required for indexed bundles, with a deliberately small
   first-pass vocabulary.

2. State plainly that display consumers switch from slug-year parsing to
   canonical year metadata.

3. Keep `primary_link` explicit and make its place in the model a first-class
   part of the proposal text.

4. Add an explicit limitation note that A does not solve venue identity in the
   first pass.

5. Treat venue cleanup as an atomic corpus migration, not casual incremental
   drift.

6. Defer any stronger author identity field such as `person_key`.

### For Proposal B

1. Either justify `local_page.mode` much more strongly or simplify it back
   toward A's binary approach.

2. Sharpen the argument that grouped semantic objects buy enough real value now
   to offset the migration cost.

3. Keep the strongest grouped object idea, `venue`, but be more skeptical
   about whether every other cluster needs the same treatment yet.

4. Be explicit that B requires an all-at-once consumer rewrite and why that is
   still worth it.

5. If B remains alive as a contender, consider whether a hybridized version
   with:
   - `venue` object
   - `identifiers` object
   - flatter time/readiness fields
   would actually capture most of B's value with less migration burden.

## Final Bottom Line

Proposal A is the better proposal for this repo at this moment.

Proposal B is the more structured proposal, but not yet the more convincing
one.
Its extra nesting is not worthless, but it is ahead of the current consumer
reality and creates more migration and future-cleanup risk than I think the
publication domain should pay before the next large backfill wave.

The best next step is not "pick A unchanged."
It is:

1. tighten A around `pub_type`, `primary_link`, and slug-year retirement
2. keep B's best long-horizon warning in mind, namely that venue/time/type
   semantics should not become endless flat accretion
3. then land the smaller, more credible migration first

## Changed File

- `/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-2.md`
