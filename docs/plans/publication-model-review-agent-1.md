# Publication Model Review - Agent 1

Status: independent review

Scope:

- Requirements: `docs/plans/publication-model-requirements.md`
- Synthesis: `docs/plans/publication-model-requirements-review-synthesis.md`
- Audit notes: `docs/plans/publication-model-audit-notes.md`
- Xavier lessons: `docs/plans/publication-model-xavier-leroy-lessons.md`
- Proposal A: `docs/plans/publication-model-proposal-a-conservative-refinement.md`
- Proposal B: `docs/plans/publication-model-proposal-b-semantic-objects.md`
- Corpus check: `docs/plans/publication-model-corpus-reality-check.md`
- Patch list: `docs/plans/publication-model-proposals-patch-list.md`
- Prior reviews: `docs/plans/publication-model-proposals-claude-review-1.md`, `docs/plans/publication-model-proposals-claude-review-2.md`

The current publication code path is small but real:

- `scripts/publication_record.py` still owns flat record parsing, `detail_page`,
  `listing_group`, `primary_link`, and slug-year validation.
- `scripts/publication_index.py` still sorts by `pub_date`.
- `scripts/sitebuild/page_projection.py` still renders homepage and CV
  publication lines from `publication_year(record.slug)` and `record.pub_date`.
- `scripts/build_pub_inventory.py` still treats `detail_page` as the local-page
  readiness bit.

That matters because the proposal choice is not only a schema choice. It is a
consumer rewrite choice, a migration choice, and a long-term semantic choice.

## 1. Findings On Proposal A

Proposal A is the lower-risk and easier-to-migrate proposal. It keeps the
current bundle-local architecture, stays mostly flat, and fixes the obvious
surface seams with additive fields. That is a legitimate virtue, and it should
not be understated. Given the current code shape, A is the least disruptive
path to getting canonical year, compact venue display, and an explicit local
page readiness field into the model.

The strongest thing A does is separate the homepage problem from the
bibliography problem without forcing a large restructuring. The current corpus
really does need a canonical display year that is not just slug parsing. The
corpus reality check shows `3/69` bundles where slug year and `pub_date.year`
diverge, and `68/69` venue strings already embed a compact acronym-like suffix.
So A is not inventing problems. It is responding to real corpus pressure with
small, direct fields.

The weakness is that A is still essentially a crowded flat checklist. It fixes
the current seams, but it does not give the publication domain a cleaner
semantic structure. `venue`, `venue_short`, `listing_group`, `pub_type`,
`local_page`, `primary_link`, `identifiers`, and canonical year all live side
by side. That is workable, but it leaves the data model vulnerable to future
field sprawl and makes the schema look like a patch stack rather than a
semantic decomposition.

More importantly, A still under-scopes venue identity across papers. The
requirements and the Xavier lesson note both make clear that venue identity is a
real semantic axis, not just display decoration. A does not create a home for
that axis. It treats compact display as the whole venue problem, which is not
enough if the repo later wants venue-family queries, by-kind analysis, or more
honest provenance for repeated venues. In other words, A fixes full-vs-compact
display, but it does not finish the venue model.

The other A weakness is that it preserves the current consumer split almost too
faithfully. It still needs explicit migration for `publication_year(slug)` in
`page_projection.py`, for `pub_date` sorting in `publication_index.py`, and for
`detail_page` handling in `build_pub_inventory.py`. That is not a reason to
reject A, but it means A is not actually "small" in code terms if the consumer
rewrites are done honestly. It is small in schema delta, not necessarily small
in total work.

## 2. Findings On Proposal B

Proposal B is the stronger long-term semantic design. It is the only proposal
that really tries to separate publication concerns into explicit semantic
objects instead of flattening them into one record-shaped checklist. That is a
meaningful improvement for long-term correctness. It gives `time`, `venue`,
`classification`, `local_page`, and `identifiers` their own places, which is a
better match for the requirements around canonical year, compact venue display,
publication type, and local-bundle readiness.

B is also better aligned with the corpus than it first looks. The corpus reality
check shows that compact venue labels are not a hypothetical homepage quirk:
`68/69` venue strings already end in an acronym-like suffix, and repeated
compact labels like `PLDI`, `POPL`, `OOPSLA`, and `ASPLOS` are common enough to
be a real semantic signal. A dedicated `venue` object with full and short forms
matches that reality better than a flat `venue`/`venue_short` split, because it
makes the difference between full display and compact display explicit rather
than incidental.

The same is true for `classification`. The corpus can clearly support a small
required `pub_type` vocabulary, and the requirements explicitly say the model
should not assume `listing_group` is the only meaningful classification forever.
B answers that requirement directly. A only hints at it. B gives the repo a
clean home for page grouping and publication type instead of leaving both in the
top level as parallel notions.

The main weakness in B is migration cost, and it is real. Every current consumer
that reads `publication_record.py` fields directly would need to be rewritten to
dereference nested objects. That includes the `/pubs/` renderer, the homepage
recent-publications block, the CV renderer, and inventory tooling. So B is not a
cheap refactor. It is a deliberate schema rewrite. That is acceptable only if
the team is actually optimizing for the long horizon rather than for the next
small patch.

The other weakness is that B still leaves some of the hardest boundary questions
slightly under-specified. In particular, it postpones venue identity across
papers by making `venue.series` optional later work rather than part of the
first-pass leading shape. I understand why it does that, because workshops and
one-off venues are genuinely awkward. But the requirements and corpus evidence
say venue identity is already a real pressure, not a theoretical one. B is
better than A on this axis, but it still does not fully close the seam.

## 3. Strongest Pros And Cons

### Proposal A

Pros:

- Lowest migration risk.
- Easy for humans to scan and edit.
- Preserves the current bundle-local mental model.
- Solves the immediate homepage compact-display problem with minimal churn.
- Lets the repo add canonical year and compact venue data without forcing a
  new publication graph.

Cons:

- Leaves the model as a crowded flat checklist.
- Does not give venue identity across papers a first-class home.
- Keeps `listing_group` and `pub_type` as parallel top-level notions.
- Still requires consumer rewrites for canonical year, `detail_page`, and
  title-link policy.
- Risks another redesign later when future semantic axes arrive.

### Proposal B

Pros:

- Better long-term semantic separation.
- Cleanly distinguishes time, venue, classification, readiness, and
  identifiers.
- Better foundation for future projections, analysis, and classification axes.
- More honest about the difference between full display and compact display.
- Better candidate for a real single-source-of-truth model across consumers.

Cons:

- Larger rewrite across consumers and validation.
- Nested objects increase authoring and loader complexity.
- Still leaves venue identity across papers partly deferred.
- Risk of over-modeling if the team only wants a tactical fix.
- More structural change means more up-front backfill discipline.

## 4. Where Each Proposal Is Under- Or Over-Scoped

### Proposal A

A is under-scoped on long-term semantic structure. It correctly names the
surface seams but does not give the publication model a strong enough home for
venue identity, publication-kind evolution, or future analysis axes. It also
under-scopes the consumer migration story by making the change look smaller than
it is once `publication_year(slug)`, `pub_date` sorting, and `detail_page`
handling are actually updated.

A is over-scoped only in the sense that it adds a lot of top-level fields
without changing the underlying shape. That is fine as a patch strategy, but it
is still a lot of surface area for one flat record. The result is not wrong; it
is just more checklist-like than semantic.

### Proposal B

B is under-scoped where it postpones venue identity across papers. That seam is
already real, and the corpus check shows enough repeated compact labels to make
it worth modeling now. B is also slightly under-scoped on its migration plan:
the proposal describes the new shape well, but it does not fully spell out the
codebase-wide consumer rewrite that follows from the nested objects.

B is over-scoped only if the repo is treating this as a near-term patch. If the
goal is long-horizon correctness, the extra structure is not overkill. It is the
right kind of explicitness.

## 5. Which Proposal I Favor Now

I favor Proposal B, narrowly.

That is not because it is cheaper. It is because the publication model
requirements are fundamentally semantic, not cosmetic. The repo needs a clean
distinction between temporal metadata, venue display, classification,
readiness, and identifiers. B is better aligned with that reality. It is also
better aligned with Xavier's lesson that identifiers, landing pages, and
publication kinds are different facts and should not be squeezed into one flat
field bag.

Proposal A is the safer implementation path, and if the team only wants the
smallest possible migration then A is defensible. But that would be a near-term
optimization, not the best long-term design. A keeps the current model looking
familiar. B makes the model more truthful.

The main reason I do not favor A is that it still looks like an evolved patch to
the current structure, not a clearer semantic model. If the repo wants to avoid
having the next publication redesign three years from now, B is the better bet.

## 6. Concrete Refinement Suggestions

### For Proposal A

- State explicitly whether `pub_type` is required or optional. If it is
  optional, it is likely dead weight. If it is required, say so plainly and
  commit to a small vocabulary.
- Say exactly what `venue_short` means when it is identical to `venue`. The
  corpus has at least one such case, and the semantics need to allow it.
- Explicitly preserve `primary_link` and explain how it interacts with
  `local_page`.
- State that consumers switch from slug-year rendering to canonical year
  metadata, because the current code still uses `publication_year(slug)`.
- Add an explicit limitation note that A does not model venue identity across
  papers, so that future maintainers do not mistake it for a complete venue
  design.

### For Proposal B

- Either bring venue identity into the first pass or add a very explicit note
  that B is deliberately postponing that seam and why.
- Tighten the migration story around `local_page.mode` and `classification`
  so the loader and all consumers have a concrete upgrade path.
- Spell out how `primary_link` survives the rewrite and where title-link policy
  lives after nesting.
- Make the consumer rewrite cost explicit instead of treating it as an
  implementation detail.
- Clarify the threshold for requiring `pub_type` and `time.year` so those
  objects do not become optional noise.

### For Both Proposals

- Treat canonical year as the display year in consumers and retire
  `publication_year(slug)` as the primary display source.
- Prototype the venue cleanup across the entire 69-bundle corpus, not just on
  the easy acronym cases.
- Keep author identity conservative for now. `name` and optional `ref` remain
  sufficient; `person_key` is not yet justified here.
- Be explicit about DOI vs publisher-link derivation. The current corpus and
  Xavier's bibliography both suggest that persistent identifiers deserve their
  own canonical treatment.
- Keep the publication boundary questions visible: indexed publications versus
  book chapters, books, and publication-adjacent records.

## Final Judgment

If the repo wants the smallest safe change, Proposal A wins.

If the repo wants the better long-term publication model, Proposal B wins.

I favor Proposal B because this review should weight semantic correctness and
future consumer clarity more heavily than current inertia. The rewrite cost is
real, but the current publication corpus is already large enough and regular
enough to justify paying that cost once instead of carrying a flat checklist
forward and revisiting the same seams later.

Changed file:

- `/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-review-agent-1.md`
