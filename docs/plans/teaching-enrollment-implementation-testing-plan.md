# Teaching Enrollment Implementation / Testing Plan

Status: slices 1-3 implemented; slices 4-5 replanned as later follow-on work

It builds on:

- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [teaching-enrollment-policy-note.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-enrollment-policy-note.md)
- [teaching-domain-audit-before-enrollment.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-domain-audit-before-enrollment.md)
- the verified external handoff:
  `/Users/ztatlock/Dropbox/UW Lecture Recordings/ASSISTANT/work/handoff-enrollment-verified-to-website-agent.md`

## Purpose

This note switches teaching-enrollment work from policy discussion into
implementation and testing planning.

The main design choices are now narrow enough:

- the website teaching ledger remains canonical for site consumers
- the course/archive agent remains the deeper research authority
- enrollment should use a lightweight audited offering-level object
- Spring 2026 `CSE P590` belongs under the `uw-cse-507` / CARS family
- Spring 2026 enrollment should wait until the quarter is over

So the next job is not to redesign the teaching domain.
It is to land enrollment carefully without overloading the website repo or
accidentally perturbing existing teaching consumers.

## Goal

Implement first-pass teaching enrollment in a way that:

- preserves the current canonical teaching ledger shape and course-family
  semantics
- keeps the site build/check path trustworthy throughout the change
- adds Spring 2026 `CSE P590` to the canonical teaching ledger now
- backfills enrollment only for settled historical instructor-led UW
  offerings
- treats missing enrollment on current-quarter offerings as normal
- and treats any later stats helper or public enrollment-derived consumer as a
  separate explicit follow-on decision

## Main Execution Principle

Treat this as a **narrow teaching-ledger extension plus enrichment** problem,
not as a redesign of the teaching domain.

That means:

- first make optional enrollment executable in the loader/validator on focused
  fixtures
- then extend the canonical teaching ledger with the one verified new offering
  and the settled historical enrollment facts
- then review current consumers explicitly for visible downstream diffs, even
  if they do not render enrollment yet
- only after that decide whether the data should support:
  - an authorship-support scale-stats helper
  - a real public teaching-page consumer

Important scope control:

- first-pass enrollment applies only to instructor-led UW offerings:
  - `uw_courses`
  - `special_topics`
- it does **not** apply to:
  - `summer_school`
  - `teaching_assistant`

Important current-quarter rule:

- offerings may exist without enrollment
- missing enrollment on Spring 2026 `CSE P590` is expected and should not be
  treated as a warning condition

## Recommended Slice Order

### Slice 1. Loader / Validator Foundation

Extend the teaching schema and tests so offering-level enrollment is an
explicit optional canonical fact.

This slice is now implemented in:

- [teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/teaching_record.py)
- [test_teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_teaching_record.py)

Scope:

- extend [scripts/teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/teaching_record.py)
  so offerings may include:

```json
"enrollment": {
  "students": 160,
  "evidence_url": "https://www.washington.edu/students/timeschd/WIN2024/cse.html"
}
```

- keep `enrollment` optional
- require `students` to be a positive integer
- require `evidence_url` to be a non-empty string
- reject unknown enrollment fields
- add focused tests in
  [tests/test_teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_teaching_record.py)
  for:
  - valid offering-level enrollment objects
  - missing required enrollment subfields
  - invalid `students`
  - invalid `evidence_url`
  - unknown enrollment subfields
  - offerings with no enrollment still remaining valid
- do **not** change live canonical teaching data yet
- do **not** change public renderers yet

Why first:

- it turns the policy into executable contract
- it isolates schema mistakes from data-import mistakes
- it proves the domain can represent partial enrollment coverage honestly

Implemented outcome:

- offering-level enrollment is a supported optional canonical fact
- the teaching loader/validator and focused tests enforce its shape
- the live site data and rendered output are still unchanged

### Slice 2. Canonical Data Extension And Historical Enrollment Backfill

Update the canonical teaching ledger with the one verified new offering and
the settled historical enrollment facts.

This slice is now implemented in:

- [teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- [test_teaching_record.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_teaching_record.py)

Scope:

- add Spring 2026 `CSE P590` under the existing
  `uw-cse-507` / `Computer-Aided Reasoning for Software` family
- do **not** add Spring 2026 enrollment yet
- backfill offering-level enrollment for settled historical instructor-led UW
  offerings in:
  - `uw_courses`
  - `special_topics`
- preserve the current record-level course-family model:
  - do not introduce a separate `CSE P590` family record
  - do not add per-offering catalog-designation machinery yet
- keep the teaching-assistant and summer-school groups unchanged

Data-shape expectation after slice 2:

- historical offerings in scope have `enrollment.students` and
  `enrollment.evidence_url`
- Spring 2026 `CSE P590` exists without `enrollment`

Testing and review targets:

- canonical-data validation still passes
- the current teaching ledger count of instructor-led UW offerings moves from
  `28` to `29`
- the known verified historical ledger remains unchanged apart from the new
  Spring 2026 addition and the new enrollment subobjects

Implemented outcome:

- the canonical teaching ledger includes the verified Spring 2026 offering
- settled historical instructor-led UW enrollment is canonical
- current-quarter missing enrollment remains an ordinary supported state

### Slice 3. Current Consumer Integrity Review

Review and test the existing consumers against the now-enriched teaching
ledger, even though they do not yet render enrollment publicly.

This slice is now implemented in:

- [teaching-enrollment-slice-3-consumer-review.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-enrollment-slice-3-consumer-review.md)
- [test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)

Why this deserves its own slice:

- adding Spring 2026 `CSE P590` is not visually neutral
- the homepage recent-teaching block uses a latest-year trailing window
- current consumers should be reviewed explicitly rather than relying on “no
  renderer code changed” as a proxy for safety

Scope:

- verify the public teaching page still renders the `uw-cse-507` family
  coherently with the added Spring 2026 offering
- verify the CV teaching section still reads cleanly with the added Spring
  2026 offering
- verify the homepage recent-teaching block updates honestly:
  - it will likely move from a `2023-2025` window to a `2024-2026` window
  - Autumn 2023 `CSE 507` will likely fall out
  - Spring 2026 `CSE P590` will likely appear under the umbrella family label
- explicitly review whether that homepage diff is acceptable
- keep enrollment itself unrendered in public consumers for now

Testing targets:

- focused projection tests in
  [tests/test_page_projection.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_page_projection.py)
  updated only where the canonical teaching ledger change produces an
  intentional visible diff
- no new public projection should fail merely because an offering lacks
  `enrollment`

Implemented outcome:

- all current teaching consumers still render cleanly over the enriched ledger
- missing enrollment on Spring 2026 is exercised as a real supported case
- the repo has explicit tests for the intended homepage teaching-window diff

### Slice 4. General Scale-Stats Helper For Authorship Support

Do **not** turn the top-of-CV `Overview` into a projection consumer.

Instead, the next useful follow-on should be a small general helper that
computes trustworthy scale-summary facts from canonical site data and makes
them easy to consult while authoring or revising editorial summary surfaces.

Important boundary:

- this helper should be **general**, not teaching-specific
- it should support authored summary work on the CV, homepage, and similar
  surfaces
- it should not automatically inject numbers into those authored blocks

Initial helper goals:

- compute compact, defensible scale facts from canonical site data
- surface those facts in a form humans and future agents can quickly consult
- make scope/exclusion boundaries explicit, especially where some data is
  intentionally incomplete
- remain extensible if later summary work wants additional metrics such as
  citation-derived facts

Initial facts worth computing in v1:

- current advisees total plus category breakdown
  - for example: PhD, postdoc, BS
- graduated advisees total plus category breakdown
  - for example: PhD, masters, bachelors
- completed postdoctoral mentoring count
- visiting students count
- indexed publications
- completed UW instructor-led offerings with enrollment present
- total UW students taught across offerings with enrollment present

Important v1 exclusions:

- no service-derived stats
- no citation-derived metrics yet
- no non-canonical or externally refreshed metrics

Important first-pass teaching rule:

- while Spring 2026 `CSE P590` lacks enrollment, teaching-scale totals should
  be explicit that they are computed only from offerings with enrollment
  present or through a closed historical boundary

Recommended output shape:

- a small script that prints a human-readable report to standard output
- no generated Markdown file yet
- no generated JSON file yet
- readable enough for direct human use
- deterministic enough for future agents to rely on during drafting support

Recommended report shape:

- a short `Core scale facts` section for the strongest summary-support facts
- a short `Additional context` section for useful supporting counts and caveats
- an explicit teaching note when current-quarter offerings are excluded from
  enrollment totals

Recommended usage pattern:

- run the helper while revising authored summary surfaces such as:
  - [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
  - [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- use the output as drafting support and factual grounding
- keep final prose decisions authored and reviewable
- allow the helper to expose more facts than any one current consumer uses,
  because future summary work may want different subsets
- treat the report as a drafting aid, not as a list of numbers that must all
  appear in any one summary surface

What this slice should **not** do:

- no macro or projection insertion into [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
- no automatic homepage top-summary insertion
- no teaching-page visual redesign yet

### Slice 5. Optional Teaching-Page Consumer Exploration

Only consider this after slice 4 clarifies whether the new teaching-scale
facts are actually useful in practice.

If a real built-site consumer still looks worthwhile, the first place to try
it is the bottom of the public teaching page rather than the top of the CV.

Candidate directions worth exploring later:

- one compact bottom-of-page teaching-scale summary sentence or paragraph
- a small factual stats block if it earns its keep editorially
- a quarter-by-quarter enrollment graph
- a distribution view such as a histogram or CDF of students taught across
  offerings

Important scope caution:

- do not commit to any of these yet
- revisit only after:
  - the scale-stats helper exists
  - Spring 2026 enrollment has landed
  - the public teaching page still seems like the right place for a real
    data-driven consumer

If slice 5 happens later, it should start from explicit user-facing value,
not from the mere existence of enrollment data.

## Testing Strategy

The first implementation should be tested in layers.

### Schema / Validation Tests

Add focused tests for:

- valid offering-level enrollment object
- invalid or missing enrollment subfields
- unknown enrollment subfields
- coexistence of enrollment with existing offering staffing fields
- offerings without enrollment remaining valid

### Canonical Data Tests

Add focused tests proving:

- the canonical teaching ledger still loads
- Spring 2026 `CSE P590` exists under the `uw-cse-507` family
- historical instructor-led UW offerings in scope carry enrollment
- `summer_school` and `teaching_assistant` remain enrollment-free unless a
  later separate design decision changes that

### Consumer Regression Tests

Review or extend tests for:

- public teaching-page rendering
- CV teaching rendering
- homepage recent-teaching rendering

The key question is not “does enrollment render?”
It is:

- do current consumers remain correct and coherent over the enriched ledger?

## Recommended First Implementation Boundary

The first implementation slice should **not** try to do all possible teaching
enrollment work.

It should do only this:

1. teach the loader/validator about optional offering-level enrollment
2. add Spring 2026 `CSE P590` under `uw-cse-507`
3. backfill enrollment for settled historical instructor-led UW offerings
4. review and test the public teaching, CV teaching, and homepage recent
   teaching diffs

It should explicitly defer:

- public enrollment rendering
- enrollment-derived stats on the homepage or CV
- summer-school audience modeling
- teaching-assistant enrollment analogues
- richer per-offering catalog-designation machinery

## Recommended Next Planning Truth Updates

Once this plan is accepted, the active repo truth should say:

- teaching-enrollment work is now an explicit follow-on slice for the teaching
  domain
- the first slice is a narrow canonical-data enrichment, not a redesign
- Spring 2026 `CSE P590` should be added now, but without enrollment until the
  quarter ends
