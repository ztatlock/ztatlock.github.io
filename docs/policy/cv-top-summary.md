# CV Top Summary Policy

This document defines the purpose and authoring contract for the top-of-CV
executive-summary layer.

It builds on:

- [../plans/cv-top-summary-executive-block-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-executive-block-plan.md)
- [../plans/cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [../plans/homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)

## Purpose

The top of the CV is an authored executive-summary layer, not merely a
"selected recent highlights" list.

Its job is to help a reader understand, quickly:

- who Zach is
- what kind of researcher, teacher, and academic leader he is
- the overall shape and scale of the career
- what the strongest recent momentum signals are
- why the detailed CV below is worth reading closely

The rest of the CV is increasingly a large canonical-domain-backed factual
record.
The top block exists to do something different:

- orient the reader
- summarize trajectory
- surface salience
- provide a strong first impression

## Primary Audience

The primary audience is broad evaluative academic readers, especially people
who need a fast, high-signal understanding before scanning the full document.

Examples:

- hiring readers
- promotion/tenure/evaluation readers
- awards/committee readers
- collaborators or visitors trying to quickly understand the overall profile

Secondary audiences may still benefit, but the block should be optimized first
for "I need to understand the person quickly" rather than for comprehensive
reference.

## Core Policy

### Keep This Layer Authored

The top-of-CV executive summary should remain authored.

It should not become:

- `site/data/cv.json`
- a mechanically generated "latest from each domain" dump
- a second publications/talks/service page compressed into a few lines

Canonical domains should inform this block, but they should not control it.

### Iterate With Zach Until Approval

Agents helping with the top-of-CV summary should treat authored wording as
iterative draft material, not as content to finalize unilaterally.

That means:

- propose concrete wording and structural edits
- explain the intended tradeoffs clearly
- revise in response to Zach's feedback
- keep iterating until Zach explicitly approves the authored content

Do not treat "the page builds" or "the shape is now correct" as sufficient
grounds to consider the prose finished.

This block is an editorial surface.
Its wording should be settled collaboratively, not silently locked in by an
agent.

### Treat It As Summary, Not Repetition

The block should summarize the full CV, not repeat it in miniature.

It should favor:

- identity
- trajectory
- scale
- recent momentum
- a few strongly chosen cross-domain signals

It should avoid:

- category-completion pressure
- one-item-from-each-domain symmetry for its own sake
- long enumerations already represented faithfully below
- mechanically listing everything recent just because it exists canonically

### Keep The Editorial Layer Honest

This block is allowed to mix:

- recent publications
- invited talks
- service / leadership
- funding
- mentoring / advising
- recognition / awards
- broader research-community participation, including Dagstuhl-like items

That cross-domain mix is not a bug.
It is the reason this layer exists.

## What Belongs Here

Material belongs in the top summary when it helps a reader quickly understand:

- current identity and research/teaching profile
- overall scale or trajectory
- recent momentum
- unusually important or revealing signals
- cross-domain synthesis that would be awkward if scattered across the full CV

Good examples:

- a concise narrative description of research area and style
- a few high-signal recent developments
- carefully chosen participation/recognition items that matter to the profile
- a small number of trustworthy summary statistics, if they truly help

When the block mentions a specific publication, link to the honest canonical
destination for that publication:

- the local publication page if one exists
- otherwise the publication's primary external destination

## What Should Stay Out

The top summary should usually avoid:

- full recent-publication lists
- full recent-talk lists
- full service dumps
- duplicate section bodies that already exist lower in the CV
- weak filler items added only to pad category balance
- brittle line items that will require constant maintenance without improving
  understanding

If a fact already has a clear, strong home later in the CV, it should only be
repeated here if it materially improves the reader's immediate understanding.

## Summary Statistics

Summary statistics are allowed, but they are not required.

They should only be used when they are:

- trustworthy
- easy to maintain or derive honestly
- genuinely helpful for orientation
- unlikely to create noisy yearly churn

The top summary should not accumulate statistics just because they can be
counted.

## Dagstuhl-Like Participation

Dagstuhl-like research/community-participation items are allowed here as
authored editorial signals.

They should not be forced back into canonical service just to make the top of
the CV easier to automate.

The important distinction is:

- canonical service should stay semantically honest
- the top-of-CV summary may still surface participation/recognition items that
  matter to the overall profile

## Relationship To The Homepage Top Summary

The homepage top summary and the CV top summary should be designed with
awareness of each other.

They serve related but not identical roles:

- the homepage introduces the public site
- the CV top summary introduces the full evaluative record

They may overlap in theme or facts, but they should not drift into awkward
redundancy by inertia.

The homepage does not need to become a second CV.
The CV top does not need to become homepage prose with extra bullets.

## Heading / Shape Guidance

The exact visible shape is allowed to evolve.

Open implementation questions such as:

- whether to keep a year range
- whether to keep current subsection headings
- whether to use a flatter mixed-content format
- whether to include a short identity paragraph

should be decided by the current campaign slices, not frozen here forever.

But this policy does impose one constraint:

- the visible shape should make the block read as an executive summary rather
  than as a mini-dump of recent entries

## Maintenance Guidance

Revisit the top summary when:

- major recent signals appear that change the picture a reader should get
- the block stops feeling like an honest overview
- the category mix starts looking mechanical
- new canonical coverage or trustworthy counters make better summary support
  feasible
- the homepage top summary changes enough that the two surfaces need
  coordination

Do not update it just because the calendar year changed.
Prefer editorial honesty over timestamp churn.

When a rewrite is in progress, prefer short iterative proposal cycles over
large one-shot rewrites.
Show candidate language, get review, and only then settle the live wording.

## Non-Goals

This policy does not require:

- a new canonical CV data model
- deriving every top-summary fact from structured data
- reopening publication/service/talks canonical models
- automatic category balancing
- permanent preservation of the current `Selected Recent Highlights` title or
  subsection structure

## Working Rule Of Thumb

When editing the top of the CV, ask:

- does this help a reader understand Zach faster?
- does this summarize the whole picture better rather than repeat details?
- is this here because it matters, or because it was easy to list?

If the answer is mostly "it was easy to list," it probably does not belong in
the executive summary.
