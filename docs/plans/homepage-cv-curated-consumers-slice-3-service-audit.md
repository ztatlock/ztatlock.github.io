# Homepage / CV Curated Consumers Slice 3: Service Data Audit

Status: in progress

It builds on:

- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Audit the canonical service model in
[site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json)
before attempting any homepage recent-service projection, so the later homepage
consumer policy is based on the right grouped/coalesced service facts rather
than on accidental quirks of the current term-level data.

This slice should:

- audit how well current service records collapse into stable public-facing
  service groups
- identify obvious normalization seams in the canonical service data
- reconsider whether the current service data model has the right long-term
  shape for recurring concepts versus yearly instances
- clarify which grouped service views are plausible sources for homepage
  `Recent Service / Leadership`
- support later simulation of homepage service selection policies

It should not:

- project the homepage recent-service block yet
- change the public `/service/` page design
- change the CV service section design
- add a homepage placeholder yet

## Why Audit First

The service domain differs from homepage students, teaching, and news in one
important way:

- homepage service selection should operate over **coalesced service groups**,
  not over raw per-year canonical term records

The repo already has a good base coalescing helper in
[scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py):

- `group_service_records_for_view(...)`
- `collapse_service_year_label(...)`

But the audit showed a real seam:

- some annual records are intentionally not collapsed because their URLs differ
  by year
- some recurring roles arguably should still collapse conceptually even when
  details like URLs vary
- some recurring service concepts may eventually want both:
  - a stable collapsed concept for summaries and recent-homepage selection
  - per-instance links for year-specific event pages, committees, or programs
- some current public-homepage assumptions, such as including
  `EGRAPHS Community Advisory Board` but not any analogous `FPBench` advisory
  role, need to be reviewed against the canonical data

So the immediate next need is not a homepage projection helper.
It is a careful audit of what the service groups really should be.

## Current Audit Findings

The current homepage block in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
is fully explainable from canonical service data, but that does **not** mean
the current service grouping semantics are already the right long-term shape.

Notable findings from the first audit pass:

- the current homepage block is composed entirely of items visible in the
  canonical `organizing` view
- future service years already exist in canonical data, such as:
  - `2026 - 2029 PLDI Steering Committee`
  - `2026 - 2029 PACMPL Advisory Board Member`
- ongoing multi-year series already collapse well, such as:
  - `2022 - Present EGRAPHS Community Advisory Board`
- some repeated annual entries, especially `FPTalks`, are still year-specific
  in the grouped view because their term records differ by year-local URL

That last point is the biggest seam to resolve before homepage projection
policy is finalized.

More broadly, this means the slice is not just a homepage-selection audit.
It is also a careful review of whether the current service data model and its
supporting grouping code are the right long-term foundation.

## Main Questions For This Slice

The audit should answer:

1. Which current service series should remain year-specific in grouped views?

Examples to review:

- `FPTalks`
- `PLDI Workshops`
- any future recurring event series with year-specific links

2. Which current service series should collapse across years even if some
record-local fields differ?

Examples to review:

- advisory-board roles
- recurring committee/leadership appointments
- other stable titles with minor year-local differences

2A. Do some recurring series need a better concept/instance split?

For example:

- a stable recurring service concept like `FPTalks`
- multiple year-specific service instances with different URLs
- later consumers that may want either:
  - one collapsed summary entry
  - or links to several specific instances

This slice does not need to design the final schema immediately, but it should
identify whether that split is important enough to justify a later service-model
follow-on.

3. What grouped service surfaces are plausible homepage candidates?

The homepage block might ultimately draw from:

- organizing only
- organizing plus some department leadership
- a new narrower derived subset over existing groups

This slice should not decide by taste alone.
It should review the actual grouped service population first.

4. What homepage-relevant service facts, if any, are missing or overly awkward
in the canonical model today?

For example:

- repeated event series that should perhaps share a better series key
- roles that should collapse but currently do not
- future-facing terms that complicate recency anchoring

## Deliverables

This slice should produce:

- a reviewed service-audit note
- a short list of canonical service-data cleanup recommendations, if needed
- a recommendation about whether the service data model needs a later
  concept/instance follow-on for recurring series with year-specific links
- if warranted, a requirements brief and redesign proposal capturing what a
  cleaner long-horizon service model should accomplish
- a recommendation for the later homepage source scope:
  - organizing only
  - organizing plus selected department leadership
  - or another clear grouped-source rule
- a recommendation for the later homepage recency anchor rule in the presence
  of future service years

That redesign follow-on is now materially complete enough to serve as the
leading design checkpoint:

- [service-redesign-proposal-a4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a4.md)

The next move after this audit is therefore implementation/testing planning
rather than more redesign iteration:

- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)

## Recommended Work

The audit should:

1. enumerate grouped service entries by current view:
   - `reviewing`
   - `organizing`
   - `mentoring`
   - `department`
2. identify recurring series that look over-split or under-collapsed
3. review whether recurring service concepts with year-specific links need a
   better concept/instance representation
4. compare the current homepage service bullets against the grouped canonical
   service views
5. simulate a few plausible homepage selection policies over the grouped data
6. recommend the narrowest principled policy for the later projection slice

## Invariant

After this slice:

- the repo has an explicit reviewed understanding of grouped service semantics
  as they matter for homepage selection
- the repo has an explicit reviewed understanding of whether recurring service
  concepts need a stronger concept/instance model for future projections and
  summaries
- any later homepage recent-service consumer can be designed against the right
  grouped/collapsed service facts
- if small canonical service cleanups are needed, they are identified before
  projection logic builds on shaky grouping behavior

## Likely Code / Doc Surfaces

Primary surfaces:

- [site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json)
- [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)
- [docs/plans/service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- this audit note itself

Possible outputs:

- a reviewed notes doc under `docs/plans/`
- possibly a small follow-on canonical service cleanup slice
- possibly a later service-model follow-on if recurring series need clearer
  concept-versus-instance support

## Follow-On Slice

Only after this audit, and after the repo begins implementing the latched A4
redesign direction, should we plan the homepage projection slice.

That later slice should cover:

- the homepage `## Recent Service / Leadership` placeholder
- the final source-scope decision
- the final recency-window / cap / optional stickiness policy
- the missing trailing link:
  `Please see my [service page](service/) for more.`
