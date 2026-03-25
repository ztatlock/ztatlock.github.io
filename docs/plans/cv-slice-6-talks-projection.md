# CV Slice 6: Talks Projection

Implemented.

## Goal

Replace only the duplicated `## Invited Talks` body in the CV with projection
from canonical talk bundles under `site/talks/`, while keeping the `## Invited
Talks` heading hand-authored in `site/cv/index.dj`.

## Why Talks Next

Talks is now the cleanest remaining CV consumer slice because:

- canonical talk truth already exists in bundle-local records under
  `site/talks/<slug>/talk.json`
- the public talks wrapper at `site/talks/index.dj` is already a thin
  placeholder-based consumer over that canonical bundle set
- the full CV `Invited Talks` section still duplicates the same `25` invited
  / public talk entries in one hand-maintained block
- that literal CV block already shows concrete drift from canonical talk
  bundle truth, for example:
  - the May 2023 UIUC entry currently differs in title and host text from the
    canonical bundle
  - the September 2019 / May 2019 order differs from canonical reverse
    chronological ordering
  - the FPBench entry in August 2017 currently omits the canonical title link

This is therefore a real cross-domain consumer cleanup slice, not a speculative
new schema campaign.

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Invited Talks` heading hand-authored.
3. Replace only the repeated `Invited Talks` body with a placeholder.
4. Add an explicit CV-specific talks renderer over canonical talk bundles
   discovered from `site/talks/`.
5. Add source validation for the placeholder-based CV talks section.

Likely placeholder:

- `__CV_TALKS_LIST__`

## Important Rendering Principle

This slice should not blindly reuse the public talks page renderer just because
the current public and CV views are similar.

Instead:

- reuse canonical talk ordering, date rendering, and title/segment link truth
  from the talk bundles
- keep the CV renderer explicit so any CV-specific formatting policy remains
  reviewable

Recommended first-slice CV talks policy:

- preserve the current one-entry-per-bullet structure
- keep titles linked when the canonical talk bundle has a `url`
- keep linked host/series segments when canonical talk bundles include a
  segment `url`
- preserve canonical reverse-chronological ordering
- preserve canonical month / season date rendering
- accept canonical corrections where talk bundle truth differs from the old CV

This policy stays close to the current CV while still making the consumer
honest.

## Important Boundary Decision

This slice should consume only the canonical invited/public talks bundles under
`site/talks/`.

It should not absorb:

- publication-local `"talks"` arrays in `site/pubs/<slug>/publication.json`
- service entries such as `FPTalks` organization
- the top-of-CV `Selected Recent Highlights -> Invited Talks` block
- talk detail-page expansion decisions for `extra.dj` bundles

The full `Invited Talks` section is the clean narrow slice.
The highlights block is a separate curated consumer and should remain a later
decision.

## Out Of Scope

- no `Selected Recent Highlights` projection here
- no `Leadership` or `Selected Publications` highlights projection
- no talk-schema expansion
- no talk detail-page route changes
- no homepage talks/highlights cleanup
- no new `site/data/talks.json`
- no `site/data/cv.json`

## Expected Invariants After This Slice

- the full CV `Invited Talks` section derives from canonical talk bundles
- the public talks page and the CV now share one canonical invited/public
  talks source while keeping separate consumer renderers
- no literal duplicated talk-entry block remains in the full CV `Invited
  Talks` section
- visible changes in that section are explainable as either:
  - explicit CV renderer policy
  - canonical correction from talk bundle truth
- the `Selected Recent Highlights -> Invited Talks` block remains authored by
  explicit policy for now

## Expected Visible Changes

The old/new rendered diff for this slice should likely include a small number
of intentional changes in the `Invited Talks` section, including:

- the May 2023 UIUC talk entry switching to the canonical title, canonical
  host text, and canonical linked seminar segment
- the September 2019 talk moving ahead of the May 2019 talk under canonical
  reverse-chronological ordering
- the August 2017 FPBench entry gaining its canonical title link and canonical
  same-month ordering

Those changes are acceptable because they improve agreement with canonical
bundle truth rather than introducing a new presentation policy by accident.

## Verification Targets

- focused renderer/projection tests for the CV talks view:
  - reverse-chronological ordering
  - title-link policy from canonical `url`
  - linked host/series-segment policy from canonical segment `url`
  - month and season date rendering
- validation that the required CV talks placeholder is present
- validation that literal duplicated talk-entry blocks are rejected in the
  projected CV `Invited Talks` section
- compare old and new rendered CV HTML with attention to the `## Invited
  Talks` section specifically:
  - only the intended `Invited Talks` body should change
  - surrounding sections should remain stable
  - visible differences should be explainable by explicit renderer policy or
    canonical correction
- `make test`
- `make build`
- `make check`

## Stop Point

Stop after the full CV `Invited Talks` projection and reassess.

The likely next talks-related question should then be deliberate:

- keep the `Selected Recent Highlights -> Invited Talks` block authored longer
- or plan a separate tiny highlights-consumer slice if projecting that
  three-entry subset clearly earns its keep

Do not automatically broaden from this slice into a larger highlights campaign
or into publication-local talk unification.
