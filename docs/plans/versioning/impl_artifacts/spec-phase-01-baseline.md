---
title: 'Phase 01 Versioning Baseline'
type: 'chore'
created: '2026-05-17 07:15:50 -03'
status: 'done'
baseline_commit: 'deaf297f3a420ca3787c00dcb1a70888940f3b07'
context:
  - '../README.md'
  - '../01-baseline-and-constraints.md'
  - '../handoff-log.md'
  - '../TODO.md'
---

<frozen-after-approval reason="human-owned intent - do not modify unless human renegotiates">

## Intent

**Problem:** The versioning plan needs a current Phase 01 baseline before any integration branch, preview tag, or release work proceeds.

**Approach:** Refresh live Automator and PR #3 facts, then record the results in the plan handoff log and mark only Phase 01 TODO items complete.

## Boundaries & Constraints

**Always:** Use the existing `automator` remote, preserve exact SHAs and command results, and keep this phase limited to baseline documentation.

**Ask First:** Remote pushes, branch switches, release tags, npm publishing, or changes outside the Phase 01 documentation scope.

**Never:** Change BMAD-METHOD installer code, edit the official marketplace registry, create preview refs, apply PR #3, or retag an existing release.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Phase 01 baseline refresh | Current `automator/main`, PR #3, official registry, and local plan docs | `TODO.md` Phase 01 items checked and `handoff-log.md` appended with exact facts | Capture exact failed command output in the handoff log |
| PR manifest mismatch | PR #3 lacks `skills/module.yaml` while `automator/main` has it | Handoff warns Phase 02 must preserve or restore `skills/module.yaml` | Do not patch product code in Phase 01 |

</frozen-after-approval>

## Code Map

- `../README.md` -- channel model and clean-context phase protocol.
- `../01-baseline-and-constraints.md` -- Phase 01 source requirements.
- `../TODO.md` -- phase checklist state.
- `../handoff-log.md` -- continuity record for later agents.

## Tasks & Acceptance

**Execution:**
- [x] `../TODO.md` -- mark only Phase 01 items complete -- reflect completed baseline work without advancing later phases.
- [x] `../handoff-log.md` -- append a dated Phase 01 entry -- preserve SHAs, tag, PR, registry, and merge-tree facts for Phase 02.

**Acceptance Criteria:**
- Given current remote refs, when Phase 02 starts, then the handoff log identifies the exact `automator/main` base SHA and PR #3 head SHA to re-fetch or compare.
- Given PR #3 still lacks `skills/module.yaml`, when Phase 02 applies PR #3, then the handoff log warns that the manifest must be preserved or restored.
- Given the official registry still sets `default_channel: next`, when consumer docs are updated later, then they do not present unqualified `--modules baut` as stable.

## Spec Change Log

## Verification

**Commands:**
- `git fetch automator main '+refs/pull/3/head:refs/remotes/automator/pr/3' --no-tags` -- expected: fetch succeeds.
- `git merge-tree --write-tree automator/main automator/pr/3` -- expected: exit `0`.
- `git diff --check` -- expected: no whitespace or patch-format errors.
