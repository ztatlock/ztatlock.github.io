# Service Redesign Retrospective And Playbook

Status: lessons-learned reference

This note records the service redesign as both:

- a concrete retrospective on what happened
- a reusable process/playbook for future deep data-model work in this repo

It exists because the service redesign was unusually hard-won.
It took real iteration, real doubt, real outside review, and real contact with
the actual website before the final design became obvious and believable.

The point of preserving that process is not to celebrate the amount of work.
It is to make future deep design dives faster, cleaner, and more deliberate.

## Why This Matters

The service domain exposed a class of repo problem that other domains may also
have in milder form:

- the data model was "working" but uneasy
- the site had multiple consumers with subtly different needs
- recurring identity, grouping, linking, and rendering were entangled
- future backfill and future consumers would have amplified the weaknesses

The easy mistake would have been to treat those seams as local rendering bugs
or one-off projection quirks.

The hard lesson is:

- if a domain repeatedly makes renderer code invent structure, the real problem
  is usually upstream in the model

Service was the clearest case where that happened.

## What Made The Service Redesign Different

Several things happened together:

1. We did not trust vague discomfort.
   We kept trying to name it precisely.

2. We did not trust the first neat-looking design.
   We kept stress-testing it against real corpus examples and future backfill.

3. We did not mistake external review for authority.
   We used it as pressure, comparison, and idea generation.

4. We kept the real website in view.
   The design was never allowed to drift into abstract schema games detached
   from `/service/`, the homepage, the CV, anchors, URLs, and the actual
   maintenance burden.

5. We preserved the arc.
   Earlier proposals, patch notes, reviews, and revisions stayed on disk.
   That made it possible to think historically instead of repeatedly
   re-litigating from scratch.

This combination is what made the process unusually successful.

## The Core Service Saga

Compressed version:

1. We started by trying to plan homepage recent-service over the existing
   service model.
2. That exposed unresolved seams in coalescing, links, titles, roles, anchors,
   repeated yearly service, and non-contiguous runs.
3. We realized the homepage policy could not be trusted until the service model
   itself was better understood.
4. We shifted from consumer planning into a service audit.
5. The audit turned into a broader model question:
   - instance
   - recurring identity
   - visible grouped unit
   - anchor target
6. We wrote a real requirements doc instead of continuing to reason informally.
7. We compared multiple competing designs rather than refining only one.
8. We reviewed those designs critically, including independent and rotated
   outside reviews.
9. We converged on canonical runs as the key semantic win.
10. We then improved the authored JSON shape substantially without giving up
    the canonical model.
11. Only after the model felt believable did we switch to implementation and
    migration planning.
12. During implementation, we learned that preserving exact legacy formatting
    was too expensive and not actually the right goal.
13. We shifted to preserving facts, stability, and trustworthiness while
    allowing cleaner run-native rendering.
14. The final slices landed quickly once the real design was clear.

That arc is important.

The successful outcome did **not** come from having a brilliant first design.
It came from progressively forcing the problem into the open until the right
design became simpler than the alternatives.

## The Most Important Design Lesson

The single biggest conceptual win in service was:

- identifying the right **canonical visible unit**

For service, that unit turned out to be the **run**, not the raw yearly
instance and not only the higher-level recurring identity.

That matters beyond service.

Future domain work should ask early:

- what is the atomic fact?
- what is the recurring identity?
- what is the visible grouped unit that consumers actually want?
- which of those needs stable identity?

Many messy redesigns come from collapsing those into one layer too early or
letting code derive one of them ad hoc.

## Why The Process Worked

### 1. We Stayed Close To Real Data

We repeatedly checked the actual corpus, not just toy examples.

That mattered because real service had:

- recurring yearly events with changing URLs
- non-contiguous returns
- multi-view membership
- future appointments already present in canonical data
- academic-year shorthand
- uneven details and role patterns

Without real data pressure, it would have been easy to adopt a cleaner but
wrong model.

### 2. We Wrote Requirements Before Declaring Victory

The requirements phase was a turning point.

It forced us to distinguish:

- what the site must represent
- what current data merely happens to look like
- what future backfill is likely to introduce
- what is a true requirement versus a historical formatting artifact

This sharply improved later proposal quality.

### 3. We Used Competing Proposals Well

The proposal comparison was valuable not because one model from another agent
was going to replace the repo proposal wholesale.

It was valuable because competing proposals surfaced tradeoffs cleanly:

- canonical run vs derived run
- lighter physical JSON vs explicit semantic layers
- authoring burden vs anchor stability
- co-location vs canonical visible-unit identity

The best outcome was not "pick a winner and stop thinking."
It was:

- learn what each proposal was right about
- steal the good physical-shape ideas
- keep the stronger semantic core

That is how Proposal A turned into A2/A3/A4.

### 4. We Used Outside Review As Pressure, Not Control

The external/independent reviews helped a lot.
But they helped because they were used correctly.

Good uses:

- identify missing requirements
- reveal hidden assumptions
- pressure-test stability claims
- force explicit inheritance/validation rules
- highlight where the physical JSON shape was still clumsy

Bad uses would have been:

- blindly averaging opinions
- letting reviews reopen settled architecture without new evidence
- mistaking verbosity or neatness for correctness

The right move was to translate review feedback into:

- accept
- adjust
- reject

That prevented churn while still letting the design improve.

### 5. We Preserved The Design Arc

Keeping:

- requirements
- proposals
- patch notes
- reviews
- refined proposals
- implementation plan

turned out to be useful, not just archival.

It let us:

- see what had actually changed
- avoid reliving the same vague unease
- distinguish structural disagreements from already-resolved issues
- reflect on process quality later

This is one of the main reasons a `docs/lessons/` note is worth writing now.

### 6. We Knew When To Stop Redesigning

Eventually the remaining A4 issues were:

- validation contract details
- key-uniqueness wording
- role-normalization stance
- rich-details contract wording

At that point the right move was to stop redesigning and implement.

This is crucial.

A redesign is ready when the remaining objections are:

- narrow
- local
- testable
- and no longer about the core semantic shape

If the remaining debate is mostly validator rules and wording, the design is
probably ready.

## What We Would Repeat

This is the most reusable part of the lesson.

For a future domain that feels genuinely slippery, the recommended process is:

### Stage 1. Admit That The Problem May Be Structural

Do this when:

- consumer policy keeps exposing upstream discomfort
- grouping rules feel arbitrary
- identity is implicit
- renderers keep inventing structure
- future backfill obviously threatens stability

Do **not** keep pretending it is only a renderer tweak.

### Stage 2. Audit The Real Corpus

Before proposing redesign:

- identify the real records that stress the model
- classify recurring patterns
- name the corner cases
- note current and likely future consumers

The goal is not to collect every possible fact.
It is to find the examples that actually pressure the model.

### Stage 3. Write Requirements

Do this before committing to a design.

The requirements doc should capture:

- what must be represented
- who uses it
- what needs stable identity
- what can vary by consumer
- what future backfill likely introduces
- all known corner cases and seams

This step is the boundary between vague discomfort and real design work.

### Stage 4. Write At Least Two Real Proposals

Do not iterate only one proposal against itself.

The point is not just variety.
The point is to expose the true tradeoffs.

At minimum compare:

- a lighter/derived option
- a more explicit/canonical option

Then decide whether the heavier semantics are actually earning their cost.

### Stage 5. Review Critically From Multiple Angles

The best review pattern from service was:

- evaluate each proposal on its own merits
- compare proposals directly
- rotate starting points so one proposal is not always treated as the default

The review prompt should explicitly ask for:

- hidden complexity
- validation pain
- migration burden
- long-horizon stability
- likely backfill problems
- physical JSON ergonomics
- whether the design is truly simpler or just more explicit

### Stage 6. Synthesize, Do Not Average

The job after review is:

- identify what feedback is structurally important
- identify what feedback is mostly about documentation
- identify what feedback is stale because the proposal already evolved

Then convert review output into:

- accept
- adjust
- reject

This is the step that turns review from noise into design progress.

### Stage 7. Preserve The Arc

Keep:

- the requirements
- the competing proposals
- the review corpus
- the patch notes
- the refined proposal sequence

This helps future reflection and prevents repeating solved arguments.

### Stage 8. Separate Semantic Model From Authored Representation

This was one of the highest-value service lessons.

The winning service result did **not** come from choosing between:

- explicit semantics
- ergonomic JSON

It came from realizing we could have:

- a richer canonical loaded model
- and a lighter authored shape that rehydrates into it

This is likely to matter again in future domains.

### Stage 9. Implement In Slices That Test The Proposal

Service implementation worked because it was staged:

1. executable loader/validator foundation
2. canonical data migration
3. current-consumer cutover
4. later consumer policy work

This let implementation validate the design instead of forcing one giant leap.

### Stage 10. Preserve Semantics, Not Historical Formatting

This was a major mid-course correction.

Trying to preserve exact old formatting made later slices worse.

The better rule is:

- preserve facts
- preserve stable links/anchors where they matter
- preserve trust in build/check/diffs
- but do **not** preserve awkward historical formatting if the new model wants
  a cleaner rendering

This is likely a general lesson, not just a service lesson.

### Stage 11. Stop Redesigning Once The Remaining Issues Are Narrow

Do not keep polishing proposals forever.

Switch to implementation when remaining issues are mostly:

- validation details
- naming policy
- migration notes
- test targets

That is late enough.

## What We Would Do Better Next Time

The service process worked, but it was not perfectly efficient.

Things to improve:

### 1. Write The Requirements Earlier

We spent a long time reasoning informally before writing the redesign
requirements.

Next time, write the requirements sooner once the discomfort is clearly
structural.

### 2. Name The Visible Unit Earlier

We should have asked sooner:

- what is the canonical visible unit?

That question unlocked a lot.

### 3. Distinguish "Policy Problem" From "Model Problem" Faster

We first approached homepage recent-service as a consumer-policy slice.
It turned out to be blocked on a model question.

Future work should ask earlier:

- is this really a consumer-policy problem, or is the consumer exposing a bad
  model?

### 4. Be More Explicit About Review Use

The accept/adjust/reject pattern worked well, but it emerged during the
process.

Next time that should be built into the review plan from the start.

### 5. Introduce A Lessons Doc Earlier

The service saga generated a lot of method knowledge that only became obvious
after the fact.

Future major redesigns should probably get a short running retrospective note
earlier, not only at the end.

## How To Recognize A Domain That Deserves This Treatment

Not every data model needs a service-level design odyssey.

A domain probably deserves a deep design dive when several of these are true:

- multiple consumers need materially different renderings
- identity/grouping feels implicit or fragile
- recurring entities and atomic facts are not the same thing
- external links vary across repeated appearances
- future backfill is likely
- anchors/internal links need to stay stable
- renderer code keeps compensating for data-shape weakness
- the domain causes repeated "this feels wrong" discussions that are hard to
  resolve locally

If only one or two of those are true, a narrower slice is probably better.

## Lightweight Version Of This Process

For a domain that seems moderately tricky but not service-level tricky:

1. audit real corpus
2. write a short requirements note
3. compare two proposals, not three
4. do one external review pass
5. refine once
6. move to implementation planning

The full service process is not the default.
It is the escalation path when the seams are deep enough to justify it.

## Suggested Future Checklist

If another domain seems to deserve this process, use this checklist.

1. Write a short "why this may be structural" note.
2. Audit the real corpus and identify the stress cases.
3. Write a requirements doc.
4. Draft at least two competing proposals.
5. Review them critically, ideally with multiple independent starting points.
6. Write explicit accept/adjust/reject patch notes from the reviews.
7. Preserve the proposal arc instead of overwriting history.
8. Refine toward one leading design.
9. Stop when remaining issues are narrow and testable.
10. Write an implementation/testing plan with slices and invariants.
11. During implementation, preserve semantics before formatting.
12. After landing, write or update a lessons-learned note.

## Bottom Line

The service redesign succeeded because we did all of the following together:

- trusted the discomfort enough to investigate it
- grounded the work in the real corpus and real site consumers
- wrote requirements before declaring victory
- compared competing designs
- used outside review without surrendering judgment
- preserved the design arc
- separated semantic model from authored representation
- staged implementation carefully
- and stopped redesigning when the remaining issues became narrow

That combination is repeatable.

The better future version is not "do less thinking."
It is:

- reach the right kind of thinking sooner
- structure it more intentionally
- and stop as soon as the design becomes genuinely believable
