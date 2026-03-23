# State

This directory is for local generated/runtime state that is useful to keep next
to the repo but should not normally be committed.

Examples:

- script run-state such as last-submitted timestamps
- local logs from helper scripts
- repo-local generated snapshots such as `state/inventory/`

This is distinct from:

- `docs/`, which holds human-authored documentation
- `scripts/`, which holds executable helpers
- `~/Desktop/WEBFILES/`, which holds larger archival state and backups that
  live outside the repo
