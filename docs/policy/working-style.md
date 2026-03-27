# Working Style

This repo is being improved through a long-running structured-content
redesign.

The goal is not to make the site more abstract or more automated for its own
sake.
The goal is to make it cleaner, simpler, more coherent, and easier to
maintain while preserving hand-authored prose and page-level editorial
control.

For the most detailed retrospective/process lesson currently available in this
repo, see
[../lessons/service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md).
Future deep model/redesign work should use that note when the problem starts to
look structural rather than like an isolated renderer tweak.

## Mission

The medium-term mission is:

- move repeated factual content into small canonical structured sources
- keep prose, framing, and editorial voice hand-authored
- make ownership of truth obvious
- reduce duplicated maintenance
- keep the architecture explicit and easy to reason about

## Planning Hierarchy

Work in this repo should be understood at three levels:

1. Vision / medium-term mission
   Clean up the repo and make the website architecture more coherent.
2. Campaigns
   One major factual domain at a time, for example:
   talks, publications, students, teaching, service, then CV consumers.
3. Slices
   Small, reviewable steps inside a campaign.
   Each slice should establish one clear invariant and then stop.

## Core Design Philosophy

Simple and clean matter a lot here.

Strong preferences:

- narrow, explicit code
- small schemas
- obvious single sources of truth
- explicit renderer policy per consumer when needed
- thin wrappers
- focused validation
- small tests around real invariants

Avoid:

- speculative generalization
- giant shared schemas
- framework-like abstractions that have not clearly earned their keep
- adding fields “for later” without a present need
- preserving historical formatting quirks when cleaner generated output would
  be better and still faithful

If a design feels too smart, it is probably wrong.

If a domain repeatedly produces vague discomfort, awkward grouping rules,
implicit identity, or renderer code that keeps inventing structure, treat that
as a sign to step back and use the service-redesign lessons/process rather than
continuing with local fixes by inertia.

## Architectural Patterns

The repo currently uses three main patterns:

1. Bundle-root domains
   Use when records may want local assets or detail pages.
   Examples: talks, publications.
2. Shared-data domains
   Use when facts are reused across pages but do not need per-record pages.
   Examples: students, teaching, service.
3. Cross-domain consumer wrappers
   Use when a page consumes multiple canonical domains.
   Example: the CV.

The CV is a consumer wrapper, not its own canonical data domain.
Do not create `site/data/cv.json`.

## Standard Rhythm

The normal collaboration rhythm is:

1. Review / orient
   Page in the relevant docs and code before changing anything.
2. Plan
   Define the next slice clearly.
   State what invariant it will establish.
3. Reflect
   Ask whether this is really the right next slice and whether it can be made
   narrower or simpler.
4. Implement
   Make the smallest real change that lands the invariant.
5. Verify
   Add focused tests, run targeted checks first, then full checks.
6. Sober review
   Audit for drift, stale docs, awkward scaffolding, hidden second sources of
   truth, or unnecessary complexity.
7. Align docs and backlog
   Make sure the repo records the truth.
8. Stop and reassess
   Do not automatically broaden scope at the end of a slice.

This rhythm is intentional:

- review
- plan
- reflect
- implement
- verify
- sober review
- align docs
- stop and reassess

## Slice Strategy

A good slice:

- has one clear goal
- establishes one clear invariant
- is easy to test
- leaves the repo cleaner than before
- does not quietly pull in unrelated design decisions

Each slice should make it easy to answer:

- what became canonical?
- what duplication was removed?
- what remains hand-authored?
- what was intentionally deferred?
- how is the new invariant verified?

## Consumer-Renderer Policy

Do not assume a consumer must render the same as the public wrapper for a
domain.

For example, the CV may legitimately use a more compressed renderer than a
public domain page.
Those differences should be explicit renderer policy, not hidden drift in
duplicated text.

## Format Changes

The current hand-authored presentation is not sacred line-for-line.

If a new structured renderer gives a cleaner result while preserving or
improving the underlying information, that is allowed.
But visible format changes must be:

- intentional
- explained as policy
- reviewed through old/new rendered output diffs when the slice is delicate

## Current Posture

The repo has already landed canonical or wrapper checkpoints for:

- talks
- publications
- students
- teaching
- service
- CV route cutover
- CV students projection

The next planned cross-domain consumer slice is teaching inside the CV.

## What Success Looks Like

Success here does not look like maximum automation.
It looks like:

- cleaner ownership of truth
- fewer duplicated facts
- simpler maintenance
- explicit design decisions
- readable code
- trustworthy docs
