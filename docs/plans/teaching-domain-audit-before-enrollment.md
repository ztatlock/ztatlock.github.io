# Teaching Domain Audit Before Enrollment

Status: pre-implementation audit

## Purpose

Capture the current state of the teaching domain before any enrollment
integration work begins.

This note is meant to inform:

- future teaching-enrollment slice design
- future summary-stat decisions for the CV or homepage
- future course-family representation questions such as `CSE 507` vs `CSE P590`

## Current Canonical Teaching Domain

The teaching domain is now mature enough that the main canonical ledger shape
is clear and stable:

- canonical data lives in
  [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- the loader/validator lives in
  [scripts/teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/teaching_record.py)
- the main shared consumers live in
  [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)

Current canonical groups:

- `uw_courses`
- `special_topics`
- `summer_school`
- `teaching_assistant`

Current corpus size:

- `uw_courses`: `4` records, `25` offerings
- `special_topics`: `3` records, `3` offerings
- `summer_school`: `2` records, `2` events
- `teaching_assistant`: `3` records, `11` offerings
- instructor-led UW offerings currently represented on the site:
  `28`

The verified external handoff implies the next instructor-led UW total should
be `29`, once Spring 2026 `CSE P590` is added.

## What A Teaching Record Currently Means

The live teaching model is already closer to a **course family by content**
than to a strict registrar ledger of literal catalog numbers.

Evidence:

- the `uw-cse-505` record already includes Spring 2019, whose offering URL is
  `csep505/19sp/`
- the public teaching and CV renderers show one record-level `code` and
  `title`, then list offerings under that family
- homepage recent teaching also flattens one record-level `code` and `title`
  into each bullet

So the current domain is already making a semantic choice:

- “what course family did Zach teach?”
- not “what exact registrar catalog number existed each quarter?”

That existing choice is what makes treating Spring 2026 `CSE P590` as part of
the `uw-cse-507` / `Computer-Aided Reasoning for Software` family feel
coherent rather than exceptional.

## Current Consumers

### Public Teaching Page

[site/teaching/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/teaching/index.dj)
is now a thin authored wrapper over projected teaching content.

The public teaching page currently wants:

- stable course-family headings
- ordered offerings within each family
- staffing on instructor-led UW courses and special topics
- summer-school events
- a small amount of authored framing that remains outside canonical JSON

It does **not** currently want:

- aggregate teaching counts
- enrollment statistics
- per-offering registrar nuance in the visible labels

### CV Teaching Section

[site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
uses a deliberately compressed teaching view.

It wants:

- stable course-family identity
- ordered offering terms
- special-topics grouping
- summer-school history
- separate teaching-assistant history

It intentionally omits:

- most links
- staffing detail
- current-vs-historical registrar nuance
- summary teaching statistics

This means the CV teaching section is quite tolerant of the current
family-oriented model.

### Homepage Recent Teaching

The homepage recent-teaching block is a flattened teaser consumer over:

- `uw_courses`
- `special_topics`
- `summer_school`

It excludes:

- `teaching_assistant`

The current policy is:

- flatten all eligible offerings/events
- anchor a 3-year window to the latest teaching year
- order by year descending, then term/event month

This consumer is currently the most sensitive to any new teaching-ledger
backfill, because adding a newer offering can shift the visible 3-year window.

Important example:

- once Spring 2026 `CSE P590` is added, the homepage recent-teaching window
  will likely move from `2023-2025` to `2024-2026`
- that will naturally drop Autumn 2023 `CSE 507` from the homepage teaser

That is not obviously wrong, but it is a real downstream effect to review
explicitly during implementation.

### Collaborators

Teaching also now feeds the collaborators domain through canonical staffing
facts. That means teaching is no longer “just a page and CV” domain; it is now
a source of cross-domain relationship facts too.

Enrollment itself does not immediately change this, but it is a sign that the
teaching domain has become real shared infrastructure rather than a thin
presentation slice.

## What The Verified External Handoff Settled

The verified handoff at:

- `/Users/ztatlock/Dropbox/UW Lecture Recordings/ASSISTANT/work/handoff-enrollment-verified-to-website-agent.md`

materially simplified the situation.

It settled that:

- the current site teaching ledger is correct for all already-listed
  instructor-led UW offerings
- the earlier `uw-cse-331` Winter 2017 mismatch was a gap in the external CSV,
  not an error in the site ledger
- the one new offering that belongs in the site ledger is Spring 2026
  `CSE P590`

So the next teaching-enrollment work should be treated as:

- one small ledger extension
- plus enrollment enrichment

not as a large historical reconciliation campaign.

## Main Seams Exposed By The Audit

### 1. Family Identity vs Literal Catalog Number

The biggest live seam is now explicit:

- the teaching model behaves like a course-family model
- but its visible top-level fields are still a single `code` and `title`

That is fine for current consumers, but it means the model does not yet have a
first-class way to say:

- “this family is usually known as `UW CSE 507`”
- “this specific offering was taught as `CSE P590`”

Current judgment:

- this is acceptable for now
- the repo can implicitly treat `uw-cse-507` as the broader CARS family
- but this is the first place future multi-designation pressure will surface

### 2. One Offering Per Family Per Term

Within a record, offerings are currently unique by `(year, term)`.

That means the model assumes:

- at most one family-level offering per term

This matches the corpus today.
It also matches how Spring 2019 `CSEP 505` is currently represented.

But it is worth noting explicitly:

- if a future teaching family needed two genuinely distinct offerings in the
  same term under one family, the current shape would not represent that
  cleanly

This is not a present blocker, just a visible future seam.

### 3. Enrollment Scope

The current verified external handoff is about instructor-led UW offerings.

So the natural first enrollment scope is:

- `uw_courses`
- `special_topics`

and not:

- `summer_school`
- `teaching_assistant`

That scope matches the policy we already want for future summary stats too:

- if the site later says “more than 1,700 UW students taught,” that should be
  grounded in instructor-led UW course offerings, not teaching-assistant work
  or summer-school audiences

### 4. Homepage Window Sensitivity

Because the homepage recent-teaching block uses a moving latest-year window,
teaching backfill is not purely additive from a visible-render perspective.

Adding Spring 2026 `CSE P590` will likely:

- add a new homepage recent-teaching item
- shift the visible window forward
- remove Autumn 2023 `CSE 507` from that teaser

That is probably acceptable, but the implementation slice should treat it as
an intentional reviewed diff rather than a surprise.

### 5. Policy Note Drift

The current
[teaching-enrollment-policy-note.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-enrollment-policy-note.md)
still reflects the pre-verification state and therefore still mentions the old
`uw-cse-331` integrity question.

That note is still directionally correct on policy, but it should be refreshed
once implementation planning begins so the integrity section reflects the now
verified handoff.

## Audit Conclusions

The teaching domain is in good shape for a modest enrollment slice.

The main conclusions are:

- the canonical teaching ledger is already structurally strong
- the verified external handoff validates the existing ledger for current
  instructor-led UW offerings
- Spring 2026 `CSE P590` is a small real extension, not evidence of a broken
  teaching history
- the current site model is already implicitly family-oriented enough to absorb
  `CSE P590` under `uw-cse-507` for now
- the next implementation slice should stay narrow and avoid reopening the
  whole teaching model

## Recommended Pre-Implementation Stance

Before touching implementation, assume:

- `uw-cse-507` can continue to act as the CARS family for now
- enrollment should remain a lightweight audited object on offerings
- first-pass enrollment scope should be instructor-led UW offerings only
- homepage recent-teaching diffs caused by Spring 2026 backfill should be
  reviewed deliberately
- broader multi-designation or per-offering catalog-label machinery should stay
  deferred unless a real consumer clearly needs it
