# Service Redesign Proposal A3 Residual Issues

Status: draft

This note records the small remaining seams in
[service-redesign-proposal-a3.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-proposal-a3.md)
after the current design review.

These are not model-choice problems.
They are follow-up clarifications to address before implementation.

## 1. Top-Level Record-Key Uniqueness

A3 explicitly requires global canonical run-key uniqueness, but it should also
state explicitly that top-level `records[].key` values are unique across the
entire file.

Why this matters:

- every authored record needs a stable audit-friendly identity
- singleton keys and shorthand series keys also become canonical run keys
- validator behavior should not have to infer uniqueness rules indirectly

## 2. Role Normalization Contract

A3 now explains role ownership and inheritance well, but it still does not say
whether role validation/comparison is:

- exact-string based
- lightly normalized
- or explicitly deferred for a later cleanup pass

Why this matters:

- current data already has role-string drift such as `Co-chair` vs `Co-Chair`
- implementation needs to know whether that drift is merely tolerated or should
  be normalized/validated now

## 3. Rich `details` Validation Contract

A3 preserves `details` at the correct ownership levels, but it should restate
more explicitly that `details` remain rich authored content with the same
validation expectations as today.

That includes:

- Djot-bearing authored text
- links
- person references
- later validation hooks over those references

Why this matters:

- the redesign should not accidentally make `details` look like opaque strings
- implementation should preserve the current source-validation discipline

## Current Judgment

A3 is still strong enough to serve as the leading redesign direction.

These three issues should be addressed in the next refinement pass, but they do
not reopen the broader design choice.
