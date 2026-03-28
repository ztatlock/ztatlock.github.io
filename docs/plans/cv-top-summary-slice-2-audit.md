# CV Top Summary Slice 2 Audit

Status: implemented audit checkpoint

It builds on:

- [cv-top-summary-executive-block-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-executive-block-plan.md)
- [../policy/cv-top-summary.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/cv-top-summary.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)

## Goal

Audit trustworthy summary inputs and candidate summary statistics across the
current canonical domains before drafting concrete top-of-CV rewrite shapes.

The purpose of this slice is not to rewrite the CV.
It is to answer:

- what truths the repo can already support honestly
- which of those truths are strong enough for executive-summary use
- which are better treated as editorial signal sources rather than summary
  statistics
- how the top-of-CV summary should relate to the existing homepage top summary

## Current Surface Audit

### Homepage Top Summary

The homepage top summary in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
already does some important work well:

- it states a clear teaching/research mission
- it foregrounds students
- it explains the "formal verification of compilers" core
- it frames the broader cross-domain work as branching out from that core
- it already has a strong authored voice

What it does **not** currently do:

- summarize career scale
- surface recent momentum directly in the prose
- capture leadership/recognition explicitly
- provide any summary statistics

That suggests the CV top should not simply copy the homepage prose.
It should probably retain some of that identity/mission framing while adding:

- career-scale context
- recent high-signal momentum
- a small amount of honest summarization that would be out of place on the
  homepage

### Current Top-of-CV Block

The current top-of-CV block in
[site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
is mixed in a revealing way:

- `Leadership` is genuinely curated
- `Community Participation` is a one-off authored participation signal
- `Invited Talks` currently matches the complete 2024-2026 talk set
- `Selected Publications (2024-2025)` currently matches the complete 2024-2025
  indexed-publication set

So the current block is partly:

- a true executive-summary/editorial surface

and partly:

- a thin recent-window consumer disguised as "selected"

That strengthens the case for a redesign:

- keep the top layer authored
- stop pretending the current talks/publications subsections are especially
  curated
- make the block more honestly about summarizing Zach rather than listing all
  recent items from a few domains

## Canonical Domain Audit

### Students

Canonical source:

- [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)

Current trustworthy counts:

- `8` current students / postdocs
- `12` graduated PhD students
- `54` total graduated students across PhD, masters, and bachelors
- `69` total records across all student sections, including current students,
  completed postdoctoral mentoring, graduates, and visitors

Assessment:

- this is one of the strongest domains for top-summary statistics
- `current students` is immediately understandable and current
- `graduated PhD students` is also strong and high-signal
- the full `69` total is real but semantically broader; it mixes visitors,
  postdoctoral mentoring, and undergraduate/masters advising, so it is less
  obviously the right headline number

Best candidate stats from this domain:

- current students
- graduated PhD students

Secondary candidate:

- total mentored/advised people, if the final wording makes the breadth clear

### Publications

Canonical source:

- [site/pubs/](/Users/ztatlock/www/ztatlock.github.io/site/pubs/)

Current trustworthy counts:

- `69` indexed non-draft publication bundles
- `49` `conference`
- `7` `journal`
- `13` `workshop`
- `4` publication bundles with award/distinction badges
- `5` publications in `2024-2025`
- `11` publications in the homepage recent-publications window `2023-2025`

Assessment:

- this is another strong domain for top-summary statistics
- total indexed publications is honest and easy to understand
- award-paper count is meaningful and much stronger than raw workshop/main
  breakdowns
- recent-publication counts are real, but the current 3-year homepage window
  is too editorial and time-sensitive to be a durable CV-top headline by
  itself

Best candidate stats from this domain:

- indexed publications
- award papers

Useful signal sources from this domain:

- especially strong recent papers
- recent publication momentum

### Talks

Canonical source:

- [site/talks/](/Users/ztatlock/www/ztatlock.github.io/site/talks/)

Current trustworthy counts:

- `25` canonical invited/public talk bundles
- `12` talks since `2020`
- `3` talks since `2024`

Assessment:

- the domain is trustworthy enough for counts
- but talk counts are weaker top-summary statistics than student/publication
  counts
- the current recent-talk set is small enough that it is better treated as a
  recent-signal source than as a headline statistic

Best use:

- signal source for recent momentum

Possible secondary stat:

- total invited/public talks, if a final shape wants one more compact metric

### Service

Canonical source:

- [site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json)

Current trustworthy counts:

- `63` top-level service records
- `65` canonical service runs
- view-group membership counts:
  - `14` organizing
  - `32` reviewing
  - `8` mentoring
  - `12` department
- `7` runs currently selected by the homepage recent-service policy

Assessment:

- canonical service is trustworthy as a signal source
- it is weak as a top-summary statistics source
- raw service counts are not very meaningful to a reader
- the real value here is not "how much service" but "what kind of leadership
  and community roles are currently salient"

Best use:

- source of current leadership / community signals

Not recommended as headline stats:

- total service runs
- counts by service view group

### Teaching

Canonical source:

- [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)

Current trustworthy counts:

- `12` top-level teaching records across all groups
- `28` instructor-led offerings outside the historical `teaching_assistant`
  group
- `39` total offerings/entries if the historical TA group is included

Assessment:

- the domain is trustworthy, but the counts are noisy for executive-summary
  use
- the semantics are heterogeneous:
  - UW courses
  - special topics
  - summer schools
  - historical teaching-assistant work
- this makes raw counts much less informative than they first appear

Best use:

- source of selected authored teaching signals

Not recommended as headline stats:

- total teaching records
- total offerings

### Funding

Canonical source:

- [site/data/funding.json](/Users/ztatlock/www/ztatlock.github.io/site/data/funding.json)

Current trustworthy counts:

- `10` canonical funding records
- `2` PI-led grants
- `8` Co-PI grants
- `$15,072,893` total recorded funding volume
- `0` currently active/open records reaching `2026`

Assessment:

- the domain is trustworthy
- but the obvious headline stats are semantically tricky
- total dollars are especially dangerous because they mix PI and Co-PI roles
  and encourage readers to over-interpret shared grant totals
- the lack of currently active funding in the canonical set also weakens the
  case for a "current funding momentum" stat

Best use:

- selective authored evidence if a final narrative wants to mention funding

Not recommended as headline stats:

- total dollars
- total grant count by itself

### News

Canonical source:

- [site/data/news.json](/Users/ztatlock/www/ztatlock.github.io/site/data/news.json)

Current trustworthy counts:

- `23` canonical news records
- `7` records since `2024`

Assessment:

- canonical news is useful as a cross-domain signal inventory
- it is poor as a statistics source
- the value of news is qualitative: it captures recent talks, recognition,
  community participation, and releases in one place

Best use:

- inventory of recent high-signal items
- support for Dagstuhl-like participation and other authored top-summary
  signals

Not recommended as headline stats:

- news item counts

## Authored-Only Inputs Still Worth Using

Some strong executive-summary material is still authored rather than canonical:

- the homepage top-summary prose
- the CV `Experience` and `Education` sections
- the CV `Awards` section

This is not a problem.
The top-of-CV executive summary is itself an authored layer, so slice 3 should
be willing to use these authored inputs directly rather than trying to force
everything through canonical-domain counters.

Important examples:

- current rank / role framing
- research identity and mission
- selected awards and recognition

## Recommended Candidate Statistics

### Strong Shortlist

These currently look strongest for possible top-of-CV summary use:

- current students: `8`
- graduated PhD students: `12`
- indexed publications: `69`
- award papers: `4`

Why these lead:

- they are honest
- they are easy to explain
- they say something real about scale or distinction
- they are less semantically noisy than teaching, funding, or service counts

### Plausible But Secondary

- total invited/public talks: `25`
- total mentored/advised people: `69`

These are real, but they need more careful wording to avoid sounding broader
or more precise than they really are.

### Probably Avoid

- service totals
- teaching totals
- funding dollars
- raw news counts
- narrow recent-window counts as enduring top-of-CV stats

## Implications For Slice 3

The likely shape proposals should assume:

1. The top-of-CV block remains authored.
2. The homepage top summary remains a useful identity/mission reference point,
   not a template to copy.
3. The strongest derived stat candidates are:
   - current students
   - graduated PhD students
   - indexed publications
   - award papers
4. Service, news, and Dagstuhl-like participation matter more as signal
   sources than as counts.
5. Teaching and funding should probably influence authored prose more than a
   visible stats row.

That suggests the most promising shape candidates are things like:

- a short identity paragraph plus a small stat row plus recent-signal bullets
- a short identity paragraph plus a flatter mixed-content signal list
- a short narrative profile where only the most honest summary counts appear

## Main Conclusion

The audit supports a clear direction:

- the top of the CV should become more like an authored executive summary
- a small number of derived statistics can help
- but the stats need to be chosen very selectively
- the strongest current sources of honest scale are students and publications
- the strongest current sources of recent momentum are talks, service,
  publications, news, and authored participation/recognition items

So slice 3 should focus on authored shape proposals, not on building more
automation first.
