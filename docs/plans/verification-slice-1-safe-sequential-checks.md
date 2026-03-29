# Verification Slice 1: Safe Sequential Checks

Status: implemented

It builds on:

- [AGENTS.md](/Users/ztatlock/www/ztatlock.github.io/AGENTS.md)
- [ROADMAP.md](/Users/ztatlock/www/ztatlock.github.io/ROADMAP.md)
- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)

## Goal

Make the repo's preferred verification workflow explicit and safer by giving
agents and humans one obvious sequential pre-commit target.

This slice is operational hardening, not a structured-data campaign.

## Why This Slice Now

Recent teaching-staffing work reinforced an existing operational seam:

- `make test`, `make build`, and `make check` are safest when run
  sequentially
- `build/` is shared mutable state, so parallel verification can create noisy
  failures even when the repo is correct
- overlapping git actions can similarly create avoidable `.git/index.lock`
  churn

The upcoming teaching-assistant data import is a larger slice with broader
surface area, so this is a good point to tighten the workflow before that
work begins.

Later experience reinforced one more subtle lesson:

- a successful unittest phase inside `make verify` is not the same as the
  full verification target succeeding
- agents must wait for the wrapper command itself to exit before declaring
  verification green

## Invariant

After this slice:

- the repo has one explicit "safe verification" make target that runs the
  standard checks sequentially
- `AGENTS.md` and related guidance prefer that target over ad hoc parallel
  invocation of separate verification commands
- no site content, data, or rendering policy changes

## Scope

In scope:

- add a make target such as `make verify` that runs, in order:
  1. `make test`
  2. `make build`
  3. `make check`
- document that this target is the preferred pre-commit verification path
- update agent-facing guidance to avoid parallel verification and overlapping
  git actions
- add a small roadmap note if needed so the repo's operational policy stays
  explicit

Out of scope:

- changing the underlying `build`, `test`, or `check` behavior
- trying to prevent manual misuse of separate targets
- unrelated build-system refactors
- any teaching-staffing data changes

## Policy

Recommended policy:

- keep `make test`, `make build`, and `make check` available individually
- add one clearly named sequential wrapper target for the safe default path
- tell future agents to prefer the wrapper target, especially before commit
- keep git actions sequential in normal operation rather than trying to
  automate around `.git/index.lock`

This should stay simple and explicit.

## Likely File Surfaces

- `Makefile`
- `AGENTS.md`
- likely `ROADMAP.md`

## Tests And Verification

Verification for this slice should include:

- run the new safe target directly
- `make check`
- `git diff --check`

Rendered HTML diff review is not necessary here because the intended outcome
is operational only.

## Stop Point

Stop after the safe verification target and docs are landed.

The next move should then be the teaching-assistant canonicalization slice,
using the new sequential-safe verification path.
