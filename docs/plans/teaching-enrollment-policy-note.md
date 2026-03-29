# Teaching Enrollment Policy Note

Status: pre-implementation checkpoint

## Purpose

Capture the agreed boundary and policy for teaching-enrollment integration
before any schema or data changes land in the website repo.

This note is intentionally short.
It is not an implementation plan yet.

## Source Material

External handoff reviewed:

- `/Users/ztatlock/Library/CloudStorage/Dropbox/UW Lecture Recordings/ASSISTANT/work/handoff-enrollment-to-website-agent.md`
- `/Users/ztatlock/Library/CloudStorage/Dropbox/UW Lecture Recordings/ASSISTANT/knowledge/enrollment/enrollment-canonical.csv`

Current site-facing canonical teaching ledger:

- [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)

## Agreed Policy

### 1. Website Teaching Ledger

`site/data/teaching.json` is the website's canonical public teaching ledger.

That means:

- it should represent the instructor-led teaching offerings the site and CV
  publicly stand behind
- it does not need to import the full research/archive machinery of the course
  agent
- but it should stay consistent with the best verified offering history we have

### 2. Relationship To The Course Agent

The course agent remains the deeper research and reconciliation authority for
historical enrollment and offering evidence.

The website repo is a consumer of vetted facts, not the final research
authority on course history.

That means the site should not try to reproduce:

- multi-source harvesting logic
- archival preservation details
- long reconciliation notes
- the full external analysis apparatus

### 3. Enrollment Shape In Website Canonical Data

If teaching enrollment is imported into `site/data/teaching.json`, it should
use a lightweight audited object on each offering:

```json
"enrollment": {
  "students": 160,
  "evidence_url": "https://www.washington.edu/students/timeschd/WIN2024/cse.html"
}
```

This is preferred over:

- a bare integer with no traceability
- a much richer inline object carrying full source-analysis detail

### 4. Narrow Evidence Posture

The website repo should keep:

- `students`
- `evidence_url`

The website repo should not feel responsible for carrying the full external
analysis or archival provenance.

### 5. Current And Upcoming Offerings

Offerings and enrollment are distinct facts.

So:

- a new offering can appear in the canonical teaching ledger before enrollment
  is filled in
- enrollment may be added later once a public number is worth recording
- no additional provisional-state machinery is required unless a real consumer
  later needs it

## Immediate Integrity Questions Before Implementation

The reviewed handoff suggests this is not purely an enrichment slice.
It likely also requires a small ledger reconciliation pass with the course
agent.

Current examples to verify before implementation:

- whether the existing `uw-cse-331` Winter 2017 offering on the site is
  correct, since the reviewed enrollment handoff points instead to Winter 2016
- whether Spring 2026 PMP `CSE P590` should be represented in the site's
  canonical teaching ledger under the `uw-cse-507` family

Those ledger questions should be settled before enrollment import work begins.

## Implications For Future Consumers

If enrollment lands under this policy, the likely future uses are:

- better public teaching scale on the teaching page
- future CV executive-summary teaching scale if it clearly earns its keep
- later teaching-related analysis without overloading the website repo with
  research-agent responsibilities

The exact teaching stat shown on the CV or homepage should still be a later
editorial decision, not an automatic consequence of importing enrollment.
