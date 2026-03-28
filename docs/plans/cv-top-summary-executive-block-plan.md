# CV Top Summary / Executive Block Plan

Status: plan latched; slices 1-3 implemented; slice 4 rewrite next

It builds on:

- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [news-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-campaign.md)
- [publication-model-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/publication-model-redesign-retrospective-and-playbook.md)
- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

## Purpose

Reframe the current top-of-CV `Selected Recent Highlights` block as a broader
top-of-CV executive-summary problem rather than only a small cleanup seam.

The main question is no longer:

- should this block be projected?

The main questions are:

- what should the top of the CV do for the reader?
- what belongs in an authored executive-summary layer before the rest of the
  CV becomes full detail?
- which parts should stay fully authored?
- which tiny summary facts, if any, should later be pulled from canonical
  domains?
- how should this top-of-CV summary relate to the authored summary at the top
  of the homepage?

## Main Conclusion So Far

The current top-of-CV block should probably remain authored.

But the more important realization is:

- it is not best understood as a “highlights list”
- it is better understood as an **executive summary layer** for the CV

That executive-summary layer should:

- give a reader a quick sense of who Zach is
- summarize the overall shape and scale of the career
- surface strong recent momentum signals
- point the reader into the detailed CV below

So the redesign target is not:

- a tiny projected recent-items block

It is:

- a better authored top-of-CV summary that may selectively incorporate a small
  amount of trustworthy derived summary information where it clearly helps

## Why This Deserves Its Own Plan

The current `Selected Recent Highlights` block in
[site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
mixes:

- service / leadership
- community participation
- invited talks
- selected publications

That mix is real and useful.
It is also exactly why the block has resisted simple projection.

The block exists because the rest of the CV is increasingly a detailed,
structured, domain-backed factual record.
The top needs to do something different:

- orient the reader
- summarize trajectory
- surface salience
- provide a strong first impression

That is a legitimate authored role.

## Guiding Principles

### 1. Keep This Layer Authored

The top-of-CV executive summary should remain authored unless a tiny derived
subcomponent clearly earns its keep.

Why:

- it is cross-domain
- it is selective
- it is narrative
- it may include things that intentionally do not belong in any one canonical
  domain, such as Dagstuhl-like research/community participation

This should **not** become `site/data/cv.json`.

### 2. Distinguish Summary From Dump

The purpose of the top block is not to repeat the detailed CV in miniature.

It should:

- summarize identity
- summarize trajectory
- summarize scale
- highlight recent momentum

It should not:

- become a second bibliography
- become a second talks list
- become a second service page
- become a mechanically generated “latest from each domain” dump

### 3. Prefer Authoring Guidance Over Premature Automation

If the block will remain authored, the main near-term need is:

- a clear statement of purpose
- guidance for what belongs
- guidance for what should stay out
- rough maintenance expectations

Only after those are clear should we consider tiny derived helpers.

### 4. Use Canonical Domains To Inform, Not To Control

Canonical domain data should inform the executive summary:

- recent publications
- recent talks
- recent service / leadership
- current students
- funding
- news

But that does not mean those domains should directly generate the top block.

The executive summary is a downstream editorial consumer of many truths, not a
thin projection of one truth.

### 5. Coordinate With The Homepage Top Summary

The authored summary at the top of the homepage and the top-of-CV executive
summary should be reviewed together.

Why:

- both are top-level identity surfaces
- both summarize research/teaching/profile for an evaluator or visitor
- both may need to avoid awkward redundancy
- summary statistics or current-momentum framing may want to align loosely

This does **not** require them to be the same.
It does mean the two surfaces should be designed with awareness of each other.

## Open Design Questions

These questions should be answered deliberately before rewriting the block:

1. Primary audience

- Who is this for first?
  - promotion/tenure/evaluation readers?
  - hiring readers?
  - general academic visitors?
  - collaborators/students?

2. Main purpose

- Is the top block mainly:
  - identity summary?
  - career-scale summary?
  - recent momentum summary?
  - or an intentional blend?

3. Block shape

- Should the top of the CV include:
  - a short narrative paragraph?
  - summary statistics?
  - a smaller “recent signals” list?
  - category headings?
  - or a flatter mixed editorial list?

4. Summary statistics

- Which statistics would actually help?
- Which are trustworthy enough to derive?
- Which would become noisy or brittle?
- Which belong on the CV top but not the homepage top?

5. Recency versus importance

- Should an older but major signal remain in the executive summary?
- How quickly should recent items roll off?

6. Category balance

- Should the block intentionally mix:
  - publications
  - talks
  - service / leadership
  - community participation
  - students / mentoring
  - awards / recognition
  - funding
  - teaching
- or should it simply surface the strongest signals regardless of category?

7. Dagstuhl-like items

- How should non-service research/community-participation items interact with
  the top summary?
- Should they remain authored bullets?
- Should they be framed as participation, recognition, or something else?

8. Heading semantics

- Should the explicit year range stay?
- Should the phrase `Selected Recent Highlights` stay?
- Should the block use a title that better conveys “executive summary”?

9. Maintenance policy

- How often should this block be revisited?
- What kinds of new events should trigger updates?
- What counts as “worth surfacing” here?

## Non-Goals

This plan should not silently expand into:

- a new canonical CV data model
- a new homepage/CV joint registry
- projecting the entire top block from existing domains
- a demand that every summary fact be derived
- forcing Dagstuhl-like items back into service
- reopening the canonical publication, talks, or service models

## Recommended Slice Order

### Slice 1. Purpose / Requirements / Guidance

First write down what this top-of-CV layer is for.

Scope:

- state the purpose of the top-of-CV executive summary
- identify the primary audience and secondary audiences
- define what kinds of things belong there
- define what kinds of things should not be duplicated there
- define whether the block is expected to remain authored indefinitely
- define the relationship to the homepage top summary
- decide whether summary statistics are in scope at all

Likely outputs:

- this plan refined
- a stable guidance note under `docs/policy/`

Invariant after slice 1:

- future edits to the top-of-CV block have a clear editorial contract
- the repo no longer treats the block as merely an annoying projection seam

Implemented outputs:

- [../policy/cv-top-summary.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/cv-top-summary.md)
- updates to [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md),
  [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md),
  and [ROADMAP.md](/Users/ztatlock/www/ztatlock.github.io/ROADMAP.md)

### Slice 2. Source Audit And Candidate Inventory

Before rewriting the block, audit what trustworthy inputs already exist.

Scope:

- review current candidate signals from:
  - publications
  - talks
  - service
  - news
  - students
  - funding
  - awards
- identify candidate summary statistics across canonical domains
- identify which candidates are stable enough to derive
- identify which candidates are better left authored
- review the authored homepage summary at the top of `site/pages/index.dj`
  alongside the CV top block

Invariant after slice 2:

- the repo knows which facts are available
- the rewrite is informed by real canonical coverage, not guesswork

Implemented outputs:

- [cv-top-summary-slice-2-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-slice-2-audit.md)
- updates to [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md),
  [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md),
  and [ROADMAP.md](/Users/ztatlock/www/ztatlock.github.io/ROADMAP.md)

### Slice 3. Executive-Summary Shape Proposals

Draft a few authored top-of-CV alternatives before editing the live CV.

Possible shapes:

1. short identity paragraph + compact recent-signal list
2. short identity paragraph + a few summary stats + compact recent-signal list
3. short narrative profile + flatter mixed bullets with no current
   subheadings

Scope:

- compare a few candidate block shapes
- evaluate their tone, density, and maintenance burden
- review whether current headings like `Leadership`, `Invited Talks`, and
  `Selected Publications` still make sense
- decide whether a year range in the heading is helpful or brittle

Invariant after slice 3:

- the repo chooses a clear authored top-of-CV summary shape deliberately

Implemented outputs:

- [cv-top-summary-slice-3-shape-proposals.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-slice-3-shape-proposals.md)
- updates to [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md),
  [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md),
  and [ROADMAP.md](/Users/ztatlock/www/ztatlock.github.io/ROADMAP.md)

### Slice 4. CV Executive-Summary Rewrite

Once the shape is chosen, rewrite the top-of-CV block itself.

Scope:

- edit `site/cv/index.dj`
- keep the result authored
- make the block more honest as a summary of Zach rather than a mini-dump of
  recent entries
- preserve or improve Dagstuhl-like participation treatment
- update guidance comments or nearby documentation for future maintenance

Invariant after slice 4:

- the top of the CV clearly reads as an executive summary layer
- the remaining detailed CV below remains the canonical full record

### Slice 5. Homepage Top-Summary Reassessment

After the CV top summary is redesigned, reassess the authored summary at the
top of the homepage.

Scope:

- compare overlap and redundancy between homepage top prose and the CV top
  executive summary
- decide whether the homepage top should stay as-is
- or whether it should be lightly retuned in tone, emphasis, or summary
  statistics
- keep the homepage a homepage, not a second CV

Invariant after slice 5:

- homepage and CV top summaries feel coordinated rather than redundant

### Slice 6. Tiny Derived Helpers Only If They Clearly Earn It

Only after the authored summary shape is stable should the repo consider any
small derived helpers.

Possible examples:

- a trustworthy summary-stat helper
- a tiny recent-signal helper that informs authorship
- a reusable counter over canonical domains

This slice should only happen if:

- the same summary fact keeps being maintained manually
- the derived version is clearly more trustworthy
- the helper does not flatten the editorial nature of the block

Invariant after slice 6:

- any tiny automation supports authorship instead of replacing it

## Current Recommendation

The current best next step is slice 4, a live but still fully authored CV
rewrite.

Why:

- the block's purpose and maintenance contract are now explicit
- the summary-source audit is done
- the repo now has a leading shape direction for the live rewrite
- another proposal pass is less useful than testing that direction on the real
  CV

Only after that should we rewrite the block itself.

## Expected Long-Term Outcome

The likely end state is:

- the top of the CV remains authored
- it becomes more like an executive summary and less like a mixed mini-dump
- it may use a few carefully chosen derived facts or summary statistics
- Dagstuhl-like participation remains expressible there without distorting
  canonical service
- the homepage top summary and CV top summary become better aligned in role,
  while still remaining different surfaces for different contexts
