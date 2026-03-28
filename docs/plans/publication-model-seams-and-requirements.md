# Publication Model Seams And Requirements

Status: pre-redesign seam/requirements checkpoint

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-slice-5-recent-publications.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-5-recent-publications.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

## Why This Note Exists

The homepage recent-publications consumer exposed a real publication-model seam:
the current canonical `venue` field is doing two different jobs at once.

Today it serves as:

- the full bibliography-facing venue label used on `/pubs/` and in the CV
- the only available venue label for compact consumers such as the homepage

That is why the homepage currently renders:

- `Title (Architectural Support for Programming Languages and Operating Systems (ASPLOS) 2025)`

when what we actually want is closer to:

- `Title (ASPLOS 2025)`

That specific problem is small, but it is not isolated.
The current publication bundle model now has enough real consumers and enough
anticipated backfill pressure that it deserves a more deliberate review before
we make piecemeal field additions.

This note is therefore not the redesign itself.
It is the publication-domain equivalent of the service seam/requirements pass:

- name the seams we can already see
- state the current and likely future consumers
- make explicit what those consumers need
- decide whether publications needs only a small schema tweak or a deeper
  design review

## Current Context

The current canonical publication bundle model lives in:

- [scripts/publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- `site/pubs/<slug>/publication.json`

Current observed facts:

- all indexed publications now have canonical local bundles under `site/pubs/`
- the current indexed corpus contains `69` non-draft publication bundles
- `48` of those bundles are currently thinner `detail_page: false` records
- the same publication bundle truth now feeds:
  - `/pubs/`
  - the CV indexed-publication sections
  - the homepage recent-publications consumer
- further large publication backfill is expected
- the long-term intent is that all publications eventually have full,
  complete local bundles

That last point matters a lot.
This is probably not the last publication-model review the repo will ever do.
But it is still worth improving the design now, before dozens of additional
backfills accumulate on top of seams we already know about.

## Current And Anticipated Consumers

### Current Consumers

1. Publication detail pages under `site/pubs/<slug>/`
   Need full bibliographic display, local assets, links, metadata text, and
   publication-local extras such as videos/talk embeds.

2. Publications index at `/pubs/`
   Needs stable ordering, bibliography-style title/authors/venue/badges, and a
   canonical title link for every indexed publication.

3. CV indexed-publication sections
   Need compressed bibliography-style rendering over the indexed publication
   subset.

4. Homepage recent-publications
   Needs a much more compact renderer and a much smaller recent-selection
   policy than `/pubs/` or the CV.

### Anticipated Near-Term Consumers

1. Top-of-CV `Selected Publications` / `Selected Recent Highlights`
   May later want publication-aware rendering, but with stronger editorial
   compression than the current indexed-publication CV sections.

2. Collaborator and research-adjacent views
   Already depend on publication truth indirectly and may later want richer
   publication metadata.

3. Future honors/awards or “sticky publication” policies
   If publication density grows, the homepage or other consumers may want to
   treat award papers or especially important papers differently.

### Important Boundary Clarification

Publication-local `talks` are **not** the same domain as the invited/public
talks bundles under `site/talks/`.

Publication-local talks are usually:

- student talks
- conference presentations
- videos attached to a specific publication

The talks domain is instead for:

- invited/public talks that belong on the talks page

That distinction is already documented in
[talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md),
and the publication review should preserve it rather than accidentally
collapsing the domains.

## Current Model Seams

### 1. `venue` currently conflates full and short display semantics

This is the seam that surfaced immediately on the homepage.

Examples in the current corpus:

- `Programming Language Design and Implementation (PLDI)`
- `Architectural Support for Programming Languages and Operating Systems (ASPLOS)`
- `ACM Transactions on Graphics (TOG)`

The canonical field currently bakes the acronym into the full venue string.
That means the model cannot cleanly support both:

- full bibliography display
- short compact display

without either:

- string heuristics
- or duplicated punctuation in canonical data

This strongly suggests a future split such as:

- `venue`
- `venue_short`

with canonical data cleaned so `venue` no longer ends in
`(...ACRONYM...)` just to support compact consumers.

### 2. `detail_page` is doing real work, but its semantics are awkward

Today `detail_page` mainly means:

- whether a publication has a full local publication page with required assets
  and metadata

But this field is easy to misread as:

- whether the publication “really exists” canonically

That is not what it means.
Every indexed publication already has a canonical local bundle.

So the seam is not that `detail_page` is useless.
The seam is that its meaning is partly architectural and partly presentational,
and that distinction may deserve clearer naming or surrounding structure.

Questions this raises:

- is `detail_page` still the right name?
- is the local-page-readiness distinction the right abstraction?
- should canonical title-link policy continue to depend on this field
  implicitly?

### 3. `listing_group` is intentionally coarse and page-shaped

Today the model only supports:

- `main`
- `workshop`

That was a good earlier decision for the first `/pubs/` projection slices.
But it is now clearly a page-shape classification, not a strong publication
ontology.

This is not automatically wrong.
But it does raise the question:

- should the field stay a rendering-oriented grouping?
- should it be renamed to something more honest such as `pub_type`?
- or should there be both:
  - a coarse site-facing group
  - and a more semantic publication type or venue kind later

We do **not** need a grand venue ontology immediately.
But the model should stop pretending that `main` vs `workshop` is the only
interesting classification pressure publications will ever face.

### 4. `badges` are currently untyped strings

That is fine for current page rendering.
But if future selection policies ever want to prefer:

- award papers
- distinguished papers
- artifact-awarded papers

then raw string badges may stop being enough.

This does not necessarily mean badges need a rich schema now.
It does mean the publication review should explicitly decide whether:

- free-form badge strings are sufficient long-term
- or whether some light structure is likely to be needed later

### 5. Canonical destination is still mixed between local and external

Today the canonical title destination for a publication bundle is:

- local `/pubs/<slug>/` when `detail_page: true`
- otherwise `record.links[record.primary_link]`

That is honest given the current bundle model.
But it means compact consumers such as the homepage do not have one stable
rule like “always link locally.”

This is not necessarily a bug.
It is a design seam about what it means for a local publication bundle to be
canonical if some bundles still canonically send the reader elsewhere.

### 6. Publication-local identifiers are thin

The current model has:

- `title`
- `authors`
- `venue`
- `pub_date`
- links

But it does not currently have explicit fields such as:

- `doi`
- `arxiv_id`
- `isbn`

Instead some of those identifiers appear indirectly in:

- publisher links
- arXiv links
- BibTeX

This is likely too weak for the longer term.
In particular, a canonical `doi` field would be broadly useful.

At the same time, we do **not** want to turn publication bundles into a
BibTeX-reimplementation project.

So the real requirement here is:

- explicit canonical identifiers where they materially help downstream use
- while still allowing some intentional duplication between `publication.json`
  and `.bib`

### 7. The BibTeX relationship is underspecified

The current repo already has canonical `.bib` files in publication bundles.

The design question is not “should `publication.json` eliminate the BibTeX?”
The answer is no.

The real question is:

- which facts should intentionally live in `publication.json`
- which facts can remain BibTeX-only
- and where duplication is acceptable because the alternative would require
  writing and maintaining a complicated BibTeX normalization pipeline

This is a major design requirement for the next publication pass.

The current best direction is:

- allow some duplication explicitly
- avoid building a perfect BibTeX parser/writer pipeline
- still expose a small number of high-value identifiers such as DOI directly
  in canonical publication JSON

### 8. `Book Chapters` and possibly `Books` remain outside the boundary

Right now the CV `Book Chapters` section is authored by explicit policy.
That has been the correct short-term move.

But the longer-term publication boundary question remains:

- should book chapters eventually become publication bundles too?
- should books be considered at the same time?
- or should the publication bundle domain remain intentionally scoped to the
  indexed publications collection and leave books/chapters elsewhere

This is not just a CV formatting question.
It is part of the publication-domain boundary.

### 9. Future complete backfill will almost certainly surface more cases

This is not an abstract warning.
It is a design constraint.

The repo expects many more publication backfills, and those will likely
surface:

- unusual venue shapes
- additional identifier needs
- publication kinds not well-described by `main|workshop`
- richer external-link cases
- more cases where local pages exist in different states of completeness

So the publication model should be improved now with future backfill in mind,
not just patched for today’s homepage renderer.

## Requirements For The Next Publication Model Pass

Any improved publication model should satisfy these requirements.

### Consumer Requirements

1. Support both full bibliography-style venue display and compact short venue
   display without heuristics over one overloaded string field.
2. Preserve the current distinction between:
   - full local publication pages
   - thinner canonical bundles without full local pages
3. Keep publication-local talks/videos distinct from the invited/public talks
   domain.
4. Continue to support different renderers for:
   - `/pubs/`
   - `/cv/`
   - homepage recent publications
5. Avoid forcing homepage or CV consumers to reverse-engineer semantics out of
   display strings.

### Canonical-Data Requirements

1. Canonical publication JSON should stay easier to maintain than BibTeX
   tooling.
2. Some intentional duplication between `publication.json` and `.bib` is
   acceptable.
3. High-value identifiers such as DOI should likely exist directly in
   canonical JSON.
4. Canonical full-display fields should not carry compact-display punctuation
   just to support homepage-style consumers.
5. The model should stay friendly to large future backfill rather than
   requiring mass rewrites each time a new consumer appears.

### Boundary Requirements

1. Publication-local talk metadata should stay publication-local.
2. The model should explicitly decide what happens with:
   - book chapters
   - books
3. The model should not automatically broaden the publication boundary merely
   because a CV section exists.

## Questions The Design Review Should Answer

1. Should the model add `venue_short`, and if so, should `venue` be cleaned up
   to remove embedded acronyms?
2. Is `detail_page` the right long-term field name and abstraction?
3. Should `listing_group` remain page-shaped, be renamed, or be complemented
   by a stronger semantic field?
4. Should `badges` stay free-form strings?
5. Which identifiers should live directly in `publication.json`:
   - DOI?
   - arXiv identifier?
   - ISBN later for books/chapters?
6. What is the long-term boundary between:
   - indexed publications
   - book chapters
   - books
7. Should every publication eventually have a local page, or should “thin but
   canonical bundle with external destination” remain a stable long-term mode?

## Recommendation

This deserves a deeper design review, not just a one-field tactical fix.

But it probably does **not** need a service-scale architectural rewrite.

My current recommendation is:

- do a serious publication-model design review pass now
- keep it narrower than the service redesign
- focus on field semantics and bundle-boundary questions
- avoid immediate mass schema churn until that review is complete

In other words:

- publications likely needs a focused redesign/refinement exercise
- not a panic rewrite
- not just a quick `venue_short` patch either

## Suggested Next Process

1. Start with this seam/requirements checkpoint.
2. Audit the current publication bundle corpus against the seams above.
3. Draft one or more publication-model refinement proposals.
4. Compare those proposals critically against the requirements.
5. Only then migrate schema and backfill bundles.

This should happen **before** large further publication backfill or any attempt
to further canonicalize top-of-CV publication/highlights surfaces.

## Deferred External Inspiration

Before finalizing the next publication-model proposal, it would be reasonable
to study at least one mature external bibliography system for inspiration.

A specifically noted future reference is Xavier Leroy’s bibliography system:

- [Xavier Leroy bibliography](https://xavierleroy.org/bibrefs/leroy_bib.html#Courant-Leroy-convertibility)

That review should happen **after** the repo has made its own initial
conclusions, so outside inspiration helps sharpen the design rather than
replace local thinking.
