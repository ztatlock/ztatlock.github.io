# Publication Model Redesign Retrospective And Playbook

Status: lessons-learned reference

This note records the publication-model redesign as both:

- a concrete retrospective on what happened
- a reusable process/playbook for future deep data-model work in this repo

It is meant to be read alongside:

- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

The service redesign was the first major case where this repo learned how to do
a deep structured-data redesign well.
The publication redesign was the second major case, and it confirmed several of
the same lessons under a different kind of pressure.

That makes it especially valuable.
It is not just another success story.
It is a second data point on which parts of the process were genuinely
reusable.

## Why This Matters

The publication domain looked healthier than service at the start:

- publication bundles already existed
- the `/pubs/` page already derived from local bundle truth
- the CV and homepage consumers already had clearer roots
- there was no equally severe identity crisis like service had around recurring
  runs

So the tempting mistake would have been:

- just patch `venue_short`
- maybe rename `detail_page`
- keep going

That would have missed the real issue.

The hard lesson is:

- even when the overall architecture is right, field semantics can still be
  wrong enough that a deeper model review is worth doing before large backfill

Publications was exactly that kind of problem.

## What Made The Publication Redesign Different

Compared with service, the publication redesign had a different shape.

Service had a deeper canonical-model problem.
Publications had a stronger bundle-local foundation already, but weaker field
semantics inside that foundation.

So the redesign pressure came less from:

- what is the canonical visible unit?

and more from:

- what facts are actually being represented?
- which fields are doing multiple jobs?
- which current consumer groupings are page-shaped rather than semantic truth?
- what belongs in authored JSON versus in a richer normalized loaded model?

That difference matters.

It means future redesigns should not assume that every slippery domain needs a
service-scale architectural reset.
Sometimes the right answer is:

- keep the architecture
- redesign the field contract
- and be much more explicit about authored representation versus loaded model

## The Core Publication Saga

Compressed version:

1. We tried to improve homepage recent-publication rendering.
2. That exposed the `venue` seam immediately.
3. We realized compact venue display could not be solved honestly with the
   current field contract.
4. That led to a broader publication-model audit rather than a renderer patch.
5. We wrote a real seams/requirements pass before committing to a schema.
6. We explicitly enumerated current and expected consumers:
   - `/pubs/`
   - publication pages
   - CV indexed publications
   - homepage recent publications
   - collaborators and future cross-domain consumers
   - tooling and analysis pipelines
7. We reviewed those requirements critically, including external review.
8. We drafted competing proposals instead of refining only one.
9. We reality-checked them against the actual corpus.
10. We learned that the real decision was mostly about authored JSON shape, not
    about whether richer internal semantics were useful.
11. We converged on Proposal A as the leading authored-schema direction.
12. We explicitly preserved the right to rehydrate richer in-memory publication
    objects after parse.
13. We then implemented the redesign in bounded slices and chose one
    coordinated cutover instead of a long compatibility bridge.
14. After cutover, we removed the transitional scaffolding quickly.

That arc matters.

The final design did not come from a clever one-shot schema.
It came from repeatedly refusing to treat a real semantic seam as only a
display annoyance.

## The Most Important Publication Design Lesson

The single biggest conceptual win in publications was:

- clearly separating the **authored schema** from the **loaded model**

This became decisive when comparing Proposal A and Proposal B.

At first, B looked cleaner because it grouped semantics explicitly in JSON:

- `time`
- `venue`
- `classification`
- `identifiers`

But the real breakthrough was realizing:

- that grouping mostly mattered in the loaded model, not necessarily in the
  authored source

Once that became explicit, the design got simpler:

- keep authored `publication.json` physically simple and reviewable
- keep semantic fields honest
- allow richer normalized in-memory structure after parse where it helps code

This is a direct cousin of the service redesign lesson:

- do not collapse authored representation and canonical semantic model into the
  same design question too early

That lesson is likely reusable across many domains.

## The Second Most Important Publication Lesson

Requirements-first design work paid off again.

This was one of the strongest confirmed lessons from service, and publications
repeated it very clearly.

The process improved once we separated:

- seam notes
- consumer needs
- actual requirements
- proposals

The requirements phase forced us to say explicitly:

- what compact display means
- what canonical publication year means
- how `pub_date` differs from `pub_year`
- what local-page readiness means
- how identifiers and links relate
- what future consumers might need
- which boundary questions were real but deliberately deferred

That made later proposal comparison dramatically better.

Without the requirements pass, the proposal phase would have been much noisier
and much more likely to drift into accidental schema taste wars.

## Why The Process Worked

### 1. We Treated A Renderer Seam As A Model Question

The original trigger was small:

- homepage recent publications wanted `ASPLOS 2025`, not a long venue string

The useful move was not to patch that consumer heuristically.
The useful move was to ask:

- why does the model not have an honest compact venue fact already?

This is a reusable diagnostic:

- when a consumer wants a compact or curated view and the only available answer
  is “parse the display string,” the model is probably missing a semantic fact

### 2. We Stayed Grounded In The Real Corpus

The corpus check mattered a lot.

It told us:

- most venues already had an obvious full/compact split
- the awkward cases were real but narrow
- `listing_group` should not be trusted as semantic truth
- `pub_year` and `pub_date` already had real mismatch cases
- a small required `pub_type` vocabulary was actually feasible

That changed the discussion from:

- what seems elegant?

to:

- what does the real corpus justify right now?

### 3. We Used Requirements To Separate Truth From Legacy Projection

One of the most valuable publication-specific realizations was:

- `listing_group` is useful, but it is not canonical publication semantics

That could easily have been blurred away.

Instead, the requirements and corpus pass made the distinction explicit:

- `listing_group`
  retained current-consumer grouping field
- `pub_type`
  semantic classification

That kind of separation is important.
Many redesigns get stuck because a legacy projection field is treated as if it
were domain truth simply because it already exists.

### 4. We Used Competing Proposals Correctly

The A versus B comparison was valuable for the same reason competing service
proposals were valuable:

- it clarified tradeoffs sharply

Proposal A taught:

- how far disciplined flatness could go

Proposal B taught:

- what semantic groupings would be most valuable if the model grew further

The best result was not picking a winner immediately.
It was learning:

- which semantics both proposals agreed on
- which differences were mostly about physical authored shape
- which parts of B were better as loaded-model pressure than as authored JSON

That is a very reusable pattern.

### 5. We Used External Review As Pressure, Not Authority

Again, this repeated the service lesson.

The external reviews were most useful when they helped us:

- tighten requirements
- expose hidden assumptions
- force honesty about migration cost
- reality-check year semantics, venue cleanup, and `primary_link`

The right response was still:

- accept
- adjust
- reject

That preserved momentum without turning the process into opinion averaging.

### 6. We Preserved The Arc

Keeping:

- seam notes
- audit notes
- requirements
- review prompts
- review synthesis
- competing proposals
- patch lists
- corpus reality checks
- implementation plans

turned out to be just as useful here as it was in service.

This matters especially because publication work is unlikely to be over
forever.

There is a large future backfill backlog, and more publication-model review may
be needed later.
Preserving the arc means a future review can start from accumulated thought
instead of from foggy memory.

### 7. We Knew When To Stop Redesigning

Once the remaining questions were mostly:

- Proposal A versus Proposal B as authored shape
- required `pub_type`
- year semantics
- `primary_link`
- whether richer grouping belonged in authored JSON or only in memory

the design had become narrow enough.

At that point the right move was to:

- choose the leading authored direction
- implement it
- and stop churning on the schema

That is another confirmed lesson from service:

- redesign should stop when remaining disagreements are narrow, concrete, and
  testable

## What The Publication Campaign Adds To The Service Playbook

The publication redesign did not just repeat the service lessons.
It added several useful refinements.

### 1. Not Every Deep Redesign Needs A New Canonical Architecture

Service needed a much stronger semantic reset.
Publications did not.

So a future redesign should ask early:

- is the main problem canonical architecture?
- or are the main problems field semantics inside an already-good structure?

Those are different campaigns.

### 2. “Legacy Field” And “Semantic Field” Can Coexist Temporarily

Publications gave a clearer example of this than service did.

The right answer was not:

- immediately delete `listing_group`

The right answer was:

- keep `listing_group` for current projections
- add `pub_type` as the real semantic field
- let the distinction be explicit

This is a useful migration pattern for other domains.

### 3. Corpus Manifests Can Be A Very Good Middle Slice

The checked-in migration manifest was a strong move.

It let us:

- make corpus decisions explicitly
- review them visibly
- test them directly
- and avoid ad hoc migration drift

That is more specific than the service playbook, and worth repeating for
domains where:

- there are many concrete record-level assignments to make
- but not enough complexity to justify a longer compatibility bridge

### 4. Compatibility Bridges Are Not Always Worth It

Service benefited from a temporary bridge at one stage.
Publications did not.

The publication redesign confirmed a more nuanced rule:

- preserve compatibility when it materially reduces migration risk
- do not preserve it when it mostly prolongs dead semantics and confusion

For publications, a coordinated cutover was the better move.

### 5. Physical JSON Simplicity Can Be A Positive Goal

Publications clarified that “keep authored JSON simple” is not just a
convenience.
It can be a principled design goal when:

- the semantic facts are still honest
- the loaded model can still be richer
- the corpus is hand-edited
- and future backfill volume will be large

That should matter in future domains too.

## What We Would Repeat

For a future domain that feels structurally slippery, the publication campaign
suggests repeating this sequence:

1. start from the consumer seam, but ask whether it points upstream
2. do an explicit seam audit before patching heuristically
3. write requirements separately from proposals
4. enumerate current and expected consumers explicitly
5. compare competing proposals instead of polishing one in isolation
6. reality-check them against the actual corpus
7. ask whether the disagreement is really about authored JSON, loaded model,
   or both
8. choose a leading direction only after that distinction is clear
9. use a manifest-based migration slice when many corpus decisions need to be
   visible and testable
10. cut over directly when compatibility shims would mostly preserve dead
    semantics
11. remove transitional scaffolding quickly after cutover

## What We Would Do Earlier Next Time

### 1. Name “Authored Shape Versus Loaded Model” Earlier

This became one of the clearest publication lessons, but it took a while to say
plainly.

Next time, once proposals start disagreeing about grouping or nesting, ask
early:

- does this grouping need to live in authored JSON?
- or does it only need to live in the normalized loaded model?

That question could shorten future proposal debates substantially.

### 2. Use A Corpus Reality Check Sooner

The corpus reality check was very helpful:

- venue cleanup
- year mismatches
- `listing_group` divergence
- feasible `pub_type`

Next time, it should probably happen a bit earlier, once the requirements are
good enough to know what facts to inspect.

### 3. Distinguish Legacy Projection Fields From Semantic Fields Earlier

The `listing_group` lesson was valuable.
It would have been even better to say sooner:

- a current consumer field may still be necessary
- without being canonical domain truth

That distinction is likely to recur in future redesigns.

## Publication-Specific Design Lessons Worth Remembering

These are narrower than the process lessons, but still important:

- `pub_year` and `pub_date` are different facts
- compact venue display is a real semantic requirement, not a string-formatting
  trick
- `primary_link` and identifiers are different kinds of fact
- local-page readiness should be explicit and honest
- publication-local talks should not be silently merged with the invited/public
  talks domain
- future backfill pressure is a strong reason to improve the model before large
  corpus expansion, not after

## How This Should Influence Future Work

For future structured-data redesigns in this repo:

- read the service retrospective first
- read this publication retrospective second
- use both to decide whether the domain looks more like:
  - service
  - publications
  - or some hybrid

Rough heuristic:

- if the problem is identity, grouping, stable anchors, or canonical visible
  units, it is probably more service-like
- if the architecture is mostly right but important facts are overloaded into
  the wrong fields, it is probably more publication-like

Either way, the repeated lesson is:

- requirements first
- competing proposals
- corpus pressure
- explicit distinction between authored representation and loaded model
- deliberate migration
- quick cleanup after cutover

## Bottom Line

The publication redesign confirmed that the service process was not a fluke.

It taught the same major lessons again:

- requirements before proposals
- real corpus pressure
- external review used carefully
- preserve the design arc
- stop redesigning once the remaining seams are narrow and testable

And it added an especially important refinement:

- the physical authored JSON and the richer rehydrated in-memory model are
  separate design surfaces, and keeping that distinction explicit can make the
  final design much simpler and better

That is a hard-won lesson worth keeping close for future domains.
