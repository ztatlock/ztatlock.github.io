Good. Now I have a thorough picture of the actual code, schema, corpus, and consumers. Here's the review.

---

## Second-Pass Skeptical Review: Hidden Mismatches, Migration Traps, and Scoping Errors

### 1. Hidden requirement mismatches or blind spots in Proposal A

**A1. `venue_short` does not address the `<Programming>` problem honestly.**
The audit notes exactly one venue — `<Programming>` — that doesn't follow the `Full Name (ACRONYM)` pattern. Proposal A says `venue_short` is "an independent authored fact." But it doesn't explain what to do when `venue == venue_short`. The example record shows `"venue_short": "<Programming>"` which is identical to `"venue": "<Programming>"`. That looks fine for one case, but it also means `venue_short` provides zero new information for that record and doesn't help tooling distinguish "genuinely compact" from "just happens to be the same string." If the backfill hits more venues where full == short (e.g., `Nature`, `Science`, one-word journals), this becomes a noisier authored field with no semantic gain. A should say what `venue_short` actually means when the venue has no natural short form.

**A2. `pub_type` is optional, but the requirements say classification must support current grouping *and* future refinement.**
Proposal A adds `pub_type` as optional. But the actual code (`page_projection.py:470-477`, `publication_index.py:72-77`) renders both `/pubs/` and the CV purely from `listing_group`. If `pub_type` stays optional and `listing_group` stays the real driver, there's no mechanism forcing them into coherence. After backfill, you'll have 100+ bundles where `listing_group` says "main" but `pub_type` is absent — and the promised "future projection by kind" can't actually work until someone backtracks and fills in `pub_type` for everything. The field is dead weight until it's mandatory, but making it mandatory contradicts "gradual backfill." A doesn't resolve this tension.

**A3. The `primary_link` field disappears from discussion.**
The current schema has `primary_link` as a critical routing field for thin bundles (`publication_record.py:115-118`). The Proposal A record example still has it, but the proposal text never names it, never explains its relationship to `local_page`, and never addresses whether it stays at the top level or gets cleaned up. This is a real consumer-facing field — the homepage renderer uses it indirectly through `publication_index_title_url()`. A should explicitly state that `primary_link` survives unchanged.

**A4. Year extraction still happens from slugs in real code.**
`publication_year()` in `publication_record.py:121-125` extracts year from the slug. The homepage renderer (`page_projection.py:482`) calls `publication_year(record.slug)` to build the venue-year display line. The CV renderer (`page_projection.py:474`) does the same. Proposal A adds `pub_year` but doesn't address whether these consumers switch to `pub_year` or keep parsing slugs. If they keep parsing slugs, `pub_year` is decorative. If they switch, that's a consumer rewrite A doesn't account for in its "smallest migration" claim.

**A5. `person_key` adds a third identity mechanism without retiring anything.**
The current code only allows `name` and `ref` in person entries (`publication_record.py:217`). Adding `person_key` means the loader's `unknown_fields` check must be updated. More importantly, `ref` is currently the *only* mechanism for Djot link rendering (`_person_djot()` at line 512-514). A adds `person_key` but never explains which code path would use it or how it interacts with the existing collaborator derivation pipeline. It risks being a field nobody reads.

### 2. Hidden requirement mismatches or blind spots in Proposal B

**B1. `venue.series` has no honest semantics for workshops.**
11 of 69 bundles are `listing_group: workshop`. Workshop venues are typically one-off or loosely recurring. What is the `series` for `NSV`? Is it the same `series` as `NSV 2018` vs `NSV 2016`? Xavier's system handled this via BibTeX entry types and booktitle fields, not by inventing a series label for workshops. B's `venue.series` is designed for stable conference families (PLDI, ASPLOS) but becomes a forced authoring question for workshop bundles where the answer is genuinely ambiguous. The proposal doesn't acknowledge this.

**B2. `local_page.mode` objects create an asymmetric JSON shape.**
When `mode == "thin"`, the object has `primary_link`. When `mode == "full"`, it doesn't. This means consumers must now check `local_page.mode` *and* conditionally access `local_page.primary_link`. In the current model, `primary_link` is top-level and guarded by the `detail_page` boolean. B's nesting moves validation complexity from the loader into every consumer. The current loader validates the `primary_link`/`detail_page` relationship centrally (`publication_record.py:396-426`); B would need a more complex validator for a nested conditional shape.

**B3. `classification` nesting solves a problem that doesn't exist in the authored data.**
The current confusion between `listing_group` and potential `pub_type` is conceptual, not structural. No current author or script has ever confused them because `pub_type` doesn't exist yet. The nesting into `classification: { listing_group, pub_type }` adds indirection without reducing any actual error mode. The real risk (mentioned in the requirements) is that `listing_group` stays the only field forever — and nesting it doesn't change that.

**B4. `time` object breaks the simple `pub_date` filter pattern.**
The current code filters and sorts by `record.pub_date` (`publication_index.py:34-36`, `page_projection.py:498-499`). B replaces this with `time.date` and `time.year`, which means every sorting/filtering consumer must switch from `record.pub_date` to `record.time.date`. That's a pure refactor with no semantic benefit — the `time` object doesn't add information that `pub_year` + `pub_date` at top level wouldn't provide. The cost is real; the clarity gain is negligible.

**B5. B doesn't address the homepage `publication_year(record.slug)` problem either.**
Same blind spot as A (see A4). Both proposals add canonical year metadata but neither acknowledges that the current homepage and CV renderers derive display year from slug parsing, not from the record. Both proposals' consumer stories silently assume this gets fixed but don't count it as migration work.

### 3. Migration traps in Proposal A

**Trap A1: Cleaning `venue` strings is not a simple find-replace.**
The audit says 68/69 venues end in `(ACRONYM)`. But the actual strings are like `"Programming Language Design and Implementation (PLDI)"`. Removing the parenthetical to get a clean `venue` requires touching 68 records *and* simultaneously authoring 68 correct `venue_short` values. That's not "add a field" — it's a coordinated two-field rewrite of the most visible public-facing string in the schema. If any venue is cleaned but its `venue_short` is wrong or missing, the homepage silently degrades. This needs to be atomic, not gradual.

**Trap A2: The `detail_page` → `local_page` rename touches the validation pipeline.**
`publication_record.py`'s loader explicitly checks for `detail_page` in the allowed field set (line 329), uses it in `_normalize_optional_true_boolean` (line 351-354), and validates it in `_validate_publication_record` (line 396-426). The inventory tool uses `record.detail_page` throughout. The rename isn't just a sed — it's a rename in the dataclass, the loader, the validator, the inventory tool, the route discovery code, and the page projection code. A understates this as "rename."

**Trap A3: Adding `identifiers` requires deciding the loader's unknown-fields policy.**
The current loader rejects any field not in its whitelist (lines 325-345). Adding `identifiers` means updating that whitelist. Fine. But `identifiers` is a nested object — the loader will need a new `_normalize_identifiers()` function. Same for `person_key` in author entries (the current `_normalize_person` rejects unknown fields at line 217). A says "gradual" but the loader change must be done all-at-once for the build to pass.

### 4. Migration traps in Proposal B

**Trap B1: Every consumer access pattern changes simultaneously.**
The current code accesses `record.venue`, `record.pub_date`, `record.detail_page`, `record.listing_group` directly. B changes all of these to `record.venue.full`, `record.time.date`, `record.local_page.mode`, `record.classification.listing_group`. That's *every consumer* — the index renderer, the CV renderer, the homepage renderer, the page renderer, the collaborators pipeline, the inventory tool — all broken at once. There's no incremental path. You can't migrate `venue` to an object while `pub_date` is still flat; the loader would need to handle both shapes during transition.

**Trap B2: The `PublicationRecord` dataclass becomes nested dataclasses.**
The current `PublicationRecord` is a flat frozen dataclass. B requires new frozen dataclasses for `Time`, `Venue`, `Classification`, `LocalPage` — each with their own normalizers and validators. The `_normalize` functions in `publication_record.py` are ~300 lines of careful validation logic. B roughly doubles that.

**Trap B3: `local_page.mode` as a string enum is weaker than the current boolean.**
The current `detail_page: true/false` is validated by `_normalize_optional_true_boolean` and then guarded in `_validate_publication_record`. Replacing it with `local_page: { "mode": "thin" }` means the validation must now check an enum value inside a nested object, and the conditional `primary_link` validation (which currently lives cleanly at the top level) must reach into two different nesting levels. This is more complex validation for no additional expressiveness today.

### 5. Especially good ideas from Xavier's setup that neither proposal handles well

**Multiple honest projections from one corpus.**
Xavier's strongest lesson is that the same dataset supports by-year, by-topic, and by-kind views as first-class public pages. Both proposals acknowledge this in prose but neither actually gives the build system a mechanism for it. The current code hardcodes two projections: `/pubs/` (grouped by `listing_group`) and the CV (same grouping, different renderer). Neither proposal adds a by-kind or by-topic projection, and neither extends the route discovery code to support additional index views. The proposals add *data* that could support future projections but don't address the *consumer architecture* that would make them real. Xavier's system works because projection is a build-time concern, not a schema-time concern — and that architectural insight isn't landing in either proposal.

**Identifier-driven links as a build-time derivation, not a duplicated authoring burden.**
Xavier's system can derive publisher URLs from DOIs. The current repo requires independently authoring both `"doi": "10.1145/..."` in `identifiers` *and* `"publisher": "https://doi.org/10.1145/..."` in `links`. Neither proposal addresses whether `links.publisher` should become derivable from `identifiers.doi` at build time. The Proposal A example record shows this exact duplication: DOI `10.1145/3669940.3707277` alongside publisher URL `https://dl.acm.org/doi/10.1145/3669940.3707277`. A build-time DOI→URL derivation would eliminate a class of authoring errors and reduce backfill work. Neither proposal even mentions this.

### 6. Sober advice for what to refine before choosing

**First: Prototype the venue cleanup on the actual corpus, not in example records.**
Both proposals' examples use the two cleanest cases (ASPLOS and `<Programming>`). Before choosing, actually draft `venue` and `venue_short` (or `venue.full` and `venue.short`) values for all 69 bundles. This will immediately surface cases where the compact label isn't obvious (e.g., is `LATTE` a clear compact label for a workshop most readers won't recognize? What about `NSV`? `FHPC`?). The venue cleanup is the heaviest real work in either proposal and neither has been reality-tested against the full corpus.

**Second: Decide whether `publication_year()` slug parsing is retired or not.**
Both proposals add canonical year metadata but neither admits that three separate codepaths (`publication_year(slug)`, `record.pub_date.year`, and the new `pub_year`/`time.year`) will coexist after migration. The requirements say "canonical temporal semantics must not rely only on slug-embedded year text" — but the current code *does* rely on it for display. Pick one: retire `publication_year()` and always use the new field, or admit that slug-year stays and `pub_year` is just a parallel fact. This changes the consumer migration scope significantly.

**Third: Don't add `person_key` in this pass.**
Neither proposal has a consumer for it. The collaborator derivation already works through the existing mechanism. Adding a third author-identity field without a consumer that reads it is exactly the kind of speculative modeling both proposals warn against in other contexts. Defer it to a separate, smaller proposal when there's a real consumer.

**Fourth: Settle the `pub_type` mandate question before choosing.**
If `pub_type` stays optional, it won't get filled during backfill and will be useless. If it's required, it's a real authoring burden. The right answer might be: make `pub_type` required but allow a small, explicit vocabulary (`conference`, `journal`, `workshop`, `tech-report`) that covers the actual corpus. Check what the 69 bundles would actually get — if the answer is "58 conference, 11 workshop, done" then this is trivially backfillable and should just be required from the start.

**Fifth: The choice between A and B is less important than getting the venue cleanup and year semantics right.**
Both proposals solve the same real seams. The structural question (flat vs nested) is a taste decision that can be revisited. The semantic questions (what does `venue_short` mean for single-word venues? does `pub_year` actually replace slug-year in consumers? is `primary_link` still explicitly modeled?) are the ones that will bite during migration regardless of nesting strategy. Resolve those before committing to either shape.
