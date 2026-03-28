# CV Top Summary Slice 3 Shape Proposals

Status: implemented proposal checkpoint

It builds on:

- [cv-top-summary-executive-block-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-executive-block-plan.md)
- [cv-top-summary-slice-2-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-slice-2-audit.md)
- [../policy/cv-top-summary.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/cv-top-summary.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)

## Goal

Compare a few concrete authored top-of-CV shapes before editing the live CV.

This slice is about visible structure and authoring posture, not exact final
wording.
The question is:

- what kind of top block should the CV have now that the current mixed
  "Selected Recent Highlights" format is understood as an executive-summary
  problem rather than a projection seam?

## Shared Constraints

All reasonable proposals should honor the same baseline:

- the top-of-CV layer remains authored
- the homepage top summary remains a related but distinct identity surface
- the block should stop pretending it is just a recent-items list
- if derived statistics appear, they should stay few and very trustworthy
- Dagstuhl-like participation remains allowed as an authored signal
- current category headings like `Leadership`, `Invited Talks`, and
  `Selected Publications` do not need to survive by default

The strongest currently-audited candidate statistics are still:

- `8` current students / postdocs
- `12` graduated PhD students
- `69` indexed publications
- `4` award papers

One important future note:

- a later teaching-enrichment slice with enrollment numbers may create better
  teaching-related executive-summary stats
- that is not a blocker for the current redesign
- it does mean the chosen shape should leave room for a later small stat tweak
  if that future data really earns it

## Proposal A: Narrative + Small Stat Row + Mixed Signals

### Shape

- title becomes something like `Executive Summary`
- one short narrative paragraph
- one compact stat line or stat mini-block
- one flat mixed list of `4-6` recent/editorial signals with no domain
  subheadings

Example rough structure:

1. short paragraph on identity, research style, and current role
2. compact stats such as:
   - `8 current students`
   - `12 graduated PhD students`
   - `69 publications`
   - `4 award papers`
3. mixed bullets for current momentum:
   - PLDI Steering Committee / PACMPL Advisory Board
   - 2025 PLDI Program Chair
   - recent invited talk
   - especially notable recent paper or recognition
   - Dagstuhl-like participation if still judged worth surfacing

### Strengths

- best quick-scan structure
- clearly distinct from the homepage without being redundant with it
- balances identity, scale, and momentum
- avoids fake domain completeness
- keeps the block short and high-signal
- gives the CV a strong top-level "why read this?" layer

### Risks

- easiest shape to make too productized or dashboard-like
- stat wording will need care so the line reads as summary, not brag-sheet
- the mixed bullet list needs disciplined pruning to avoid growing back into a
  mini-dump

### Maintenance Burden

Moderate.

- stats should change rarely
- the mixed bullets will need real editorial judgment
- but the shape itself is stable

## Proposal B: Narrative Profile + Mixed Highlights, No Stats

### Shape

- title becomes something like `Profile and Recent Highlights`
- one or two short narrative paragraphs
- one flatter mixed set of recent/editorial bullets
- no explicit summary statistics

Example rough structure:

1. short narrative on identity, research style, and current role
2. short paragraph on trajectory/current momentum
3. `4-6` mixed bullets covering leadership, selected publications, talks,
   recognition, and participation

### Strengths

- most literary and least mechanical
- easiest to keep fully authored
- lowest risk of noisy or misleading statistics
- likely the easiest bridge from the current homepage prose style

### Risks

- may not feel different enough from the homepage top summary
- risks underserving evaluative readers who want fast scale signals
- without stats, the block may still feel like "nice prose plus some bullets"
  rather than a genuinely stronger executive-summary layer

### Maintenance Burden

Moderate to high.

- everything depends on prose quality and ongoing editorial discipline
- less help from stable derived anchors

## Proposal C: Stats-Forward At-A-Glance Block

### Shape

- title becomes something like `At a Glance`
- compact stat panel first
- then a short profile paragraph
- then a few recent/editorial bullets

Example rough structure:

1. visible stat row first
2. short paragraph on identity / research style
3. short bullet list of recent momentum signals

### Strengths

- highest immediate scanability
- strongest sense of scale for hurried readers
- easiest place to incorporate future teaching-enrollment stats if those later
  become strong enough

### Risks

- most likely to feel too dashboard-like
- weakest fit for the repo's authored/editorial philosophy
- easiest to make visually busy or résumé-ish in the wrong way
- makes the stats feel like the point, when they should be supporting context

### Maintenance Burden

Low to moderate operationally, but high conceptually.

- the shape is easy to update
- but the repo would need stronger ongoing discipline to keep it from turning
  into metric accumulation

## Comparison

### Distinctness From Homepage

- `A` is strong: it borrows the homepage's identity function, but adds scale
  and momentum more explicitly
- `B` is weaker: it risks feeling like a homepage-summary cousin
- `C` is strongest on difference, but in a way that may be too abrupt

### Executive-Summary Feel

- `A` feels most like a real executive summary
- `B` feels most like refined authored prose
- `C` feels most like a quick dashboard

### Fit With Current Audit

- `A` best uses the slice-2 audit
- `B` underuses the strong candidate stats
- `C` overweights the stats relative to the editorial layer

### Maintenance Risk

- `A` seems healthiest if the stats stay few
- `B` risks drift back into vaguely-structured prose plus bullets
- `C` risks metric creep

## Recommendation

Proposal A should be the leading direction.

Why:

- it best matches the actual purpose of the block
- it makes room for a few honest scale signals without turning the CV top into
  a dashboard
- it stays clearly more executive-summary-like than the current block
- it remains distinct from the homepage top summary
- it still keeps the recent/editorial signals authored and mixed rather than
  mechanically grouped by domain

The strongest version of A is disciplined:

- one short paragraph, not two long ones
- a very small stat row, not a data panel
- a flat mixed signal list, not current domain subheadings
- no year range in the heading

## What This Implies For Slice 4

The live rewrite should probably target something close to:

1. a new heading that reads as executive summary, not `Selected Recent Highlights`
2. one compact authored narrative paragraph
3. a tiny row or sentence-level cluster of `3-4` stable summary statistics
4. a short mixed list of recent/editorial signals

Likely things to drop from the current live block:

- the explicit year range in the heading
- `Leadership` / `Invited Talks` / `Selected Publications` as standing
  subheadings
- the implicit claim that the talk/publication bullets are "selected" when
  they are currently just complete recent windows

Likely things to preserve in spirit:

- strong leadership/community signals
- room for Dagstuhl-like participation
- especially notable recent publications or talks
- the fact that the top of the CV should feel energetic and current, not only
  archival

## Main Conclusion

The shape comparison suggests that the right next move is no longer another
abstract policy discussion.

The repo now has a leading structural idea for the live rewrite:

- Proposal A
- narrative + tiny stat row + mixed editorial recent signals

So slice 4 should be a real authored rewrite of the top of
[site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj),
not another round of broad top-summary theory.
