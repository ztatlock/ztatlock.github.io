## Proposal Comparison

### 1. Strongest advantages of A

- **Migration cost is genuinely small.** Every change is additive — new fields alongside existing ones, a rename, gradual backfill. No consumer rewrites required. With 69 bundles and a large backfill ahead, this matters a lot.
- **Preserves the current authoring mental model.** The record stays flat and scannable. A human editing `publication.json` by hand (or with agent help) doesn't need to think about which sub-object a field belongs to.
- **`venue` + `venue_short` directly solves the strongest real seam.** The audit shows 68/69 bundles carry embedded acronyms in `venue`. A flat split is the minimal fix that fully satisfies the homepage compact-display requirement (Req: Full vs Compact Display §3–§5) without heuristics.
- **Tolerates partial backfill naturally.** `pub_type`, `person_key`, and `identifiers` are all optional and independently backfillable — no structural dependency between them.

### 2. Strongest advantages of B

- **Groups correlated facts, preventing future flat-field sprawl.** The requirements doc lists 9+ consumer types and anticipates topic tags, prominence signals, and richer classification. A already acknowledges its own weakness here ("crowded flat schema over time"). B addresses this preemptively.
- **`venue.series` is a genuinely new capability.** Neither the current model nor Proposal A can answer "which papers were published at the same venue?" without string-matching display labels. B's optional `series` field gives lightweight venue identity that directly serves Req: Classification §4 (venue identity across papers) — a pressure A punts on entirely.
- **`local_page.mode` communicates intent better than a boolean.** The audit notes the conceptual awkwardness of `detail_page`. A renames it but keeps the same binary. B's `"thin"` / `"full"` vocabulary is more self-documenting and leaves room for a mid-curation state the requirements explicitly flag (Req: Local Bundle Readiness §6).
- **`classification` object cleanly separates page-grouping from semantic typing.** A introduces `listing_group` + `pub_type` as parallel top-level fields. B nests them together, making the intentional split visible in the data shape itself.

### 3. Biggest risks in A

- **The flat schema will keep growing.** A adds at least 4 new top-level fields (`pub_year`, `venue_short`, `pub_type`, `local_page`) plus a nested `identifiers` object. Future pressures (topic tags, venue identity, selection signals, prominence) will each add another top-level field. The record will become a checklist that's hard to scan, and A has no structural answer for when to stop.
- **Dodges venue identity.** The requirements explicitly call out "venue identity across papers" as a distinct pressure from venue display (Req: Classification §4). A provides no mechanism for this at all. If that need becomes real post-backfill, retrofitting it means touching every bundle again.
- **Two parallel classification fields with no grouping.** `listing_group` and `pub_type` sitting side-by-side at the top level will confuse future editors about which to use for what. The split is semantic but the representation doesn't signal that.

### 4. Biggest risks in B

- **Migration cost is concretely higher with unclear payoff today.** Every existing consumer (the `/pubs/` builder, CV renderer, homepage renderer, `build_pub_inventory.py`) must be rewritten to dereference nested objects. The audit shows current consumers don't actually need `venue.series`, `classification` nesting, or `local_page.mode` — the structure is speculative capacity.
- **Nesting makes diffs noisier and hand-editing harder.** The requirements explicitly value "reviewable, diff-friendly, and reasonable to edit with human help from agents" (Req: Backfill and Editability §5). Moving from `"pub_year": 2025` to `"time": { "year": 2025 }` doubles the line count and indentation depth for the same fact. At 69+ bundles, that's real friction.
- **`venue.series` risks premature modeling.** The requirements say "The model should allow later refinement without forcing a full venue ontology immediately" (Req: Classification §3). B's `series` field sits right on the boundary — it's not a full ontology, but it invites authoring decisions (Is `<Programming>` a series? What about one-off workshops?) that the corpus can't yet answer consistently. Getting `series` wrong across 69 bundles is harder to fix than not having it.
- **Solving near-future needs before they're real** — B's own cost list says this explicitly. The requirements doc warns against premature over-modeling for future consumers (Req: Future Top-Of-CV §, Non-Requirements §).

### 5. Which is more believable right now

**A is more believable**, for three specific reasons:

1. **The gap between current consumer needs and A's solution is nearly zero.** The audit shows exactly one consumer (homepage) that needs something the current model can't provide, and that's compact venue display. A solves it with `venue_short`. B also solves it, but wraps it in structural reorganization that no current consumer asked for.

2. **The backfill timing argument favors A.** The audit's strongest recommendation is "improve the model now, before the next large backfill wave." A can land quickly and cheaply, meaning backfill can proceed on a cleaned-up model. B's heavier migration delays that — and if backfill happens on the current model while B is debated, the whole point is lost.

3. **A's acknowledged weakness is manageable.** Yes, the flat schema will grow. But A leaves a clean upgrade path to B-style grouping later, when real consumers actually demand `venue.series` or richer classification. Going A-now then selectively nesting later costs less total work than going B-now and discovering some of the nesting was premature.

The one scenario where B wins: if you're confident the large backfill will be 100+ bundles and you want to pay the structural cost once rather than twice. But the requirements doc itself repeatedly warns against solving future needs before they're real, and the service-redesign playbook this project follows emphasizes starting from concrete consumer pressure. Right now, that pressure points at A.
