---
title: 'Phase 02 Versioning Integration Branch'
type: 'chore'
created: '2026-05-17 07:38:42 -03'
status: 'done'
baseline_commit: '956198ca52bb3342b73567f76f5981950286f8d8'
context:
  - '../README.md'
  - '../02-integration-branch.md'
  - '../handoff-log.md'
  - '../TODO.md'
---

<frozen-after-approval reason="human-owned intent - do not modify unless human renegotiates">

## Intent

**Problem:** The versioning plan needs an Automator-owned integration branch that combines current `automator/main` with PR #3 Codex runtime support before preview tagging or consumer verification can proceed.

**Approach:** Re-fetch the live base and PR refs, create `next/codex-runtime-support` from `automator/main`, apply PR #3 commits, preserve module installability and official Automator metadata, add custom-source marketplace skill discovery, bump preview-facing versions to `1.15.0-next.0`, verify locally, and record the handoff.

## Boundaries & Constraints

**Always:** Preserve `skills/module.yaml`, `skills/module-help.csv`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`; keep npm identity as `bmad-story-automator`; keep marketplace/plugin identity as `bmad-automator`; preserve exact SHAs, commands, conflicts, and review results in the handoff log.

**Ask First:** Remote pushes, tag creation, npm publish, retagging, changing official BMAD-METHOD installer behavior, or editing official marketplace registry state. The current request pre-approves local branch switching, local commits, and applying the recommended local implementation path.

**Never:** Drop PR #3 runtime changes, drop `skills/module.yaml`, overwrite tracked files from another branch without preserving their contents, present unqualified `--modules baut` as stable, or perform destructive git cleanup.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Clean PR application | Fresh `automator/main` plus PR #3 commits | `next/codex-runtime-support` contains PR #3 runtime changes and current module files | Record exact applied commits in handoff |
| Metadata regression | PR changes leave package or plugin metadata pointing at a fork or old version | Official marketplace-facing identity restored and preview versions set to `1.15.0-next.0` | Fix metadata locally and capture changed files outside PR diff |
| Module manifest policy | Automator `skills/module.yaml` currently tracks release version while BMB precedent does not | Decide whether to bump `module_version` and document rationale | If left unchanged, explain why in handoff |
| Local verification failure | Tests, packaging, smoke, or diff checks fail | Capture exact command output and leave phase blocked with next action | Do not push or tag |

</frozen-after-approval>

## Code Map

- `package.json` -- npm package identity, scripts, and preview version.
- `.claude-plugin/plugin.json` -- Codex plugin metadata and preview version.
- `.claude-plugin/marketplace.json` -- marketplace plugin entry requiring `source: "./"`, preview `version`, and plugin-level `skills`.
- `skills/module.yaml` -- BMad module manifest whose `module_version` policy must be decided.
- `skills/bmad-story-automator/pyproject.toml` -- Python helper package version.
- `skills/bmad-story-automator/src/story_automator/__init__.py` -- runtime helper version if intentionally tied to release version.
- `docs/plans/versioning/TODO.md` -- Phase 02 checklist state.
- `docs/plans/versioning/handoff-log.md` -- clean-context continuity record.

## Tasks & Acceptance

**Execution:**
- [x] Git refs -- fetch `automator/main` and PR #3 head -- ensure Phase 02 starts from current live inputs.
- [x] `next/codex-runtime-support` -- create from `automator/main` and apply PR #3 commits -- produce the integration branch.
- [x] Required module/plugin files -- inspect and preserve after PR application -- prevent custom-source install regressions.
- [x] Metadata/version files -- restore official Automator identity, add marketplace `skills`, and bump preview versions -- make branch installable as `1.15.0-next.0`.
- [x] `skills/module.yaml` -- decide and record `module_version` handling -- preserve Automator semantics intentionally.
- [x] `docs/plans/versioning/TODO.md` and `docs/plans/versioning/handoff-log.md` -- mark Phase 02 complete and append exact handoff facts -- preserve clean-context continuity.

**Acceptance Criteria:**
- Given `automator/main` and PR #3 refs, when Phase 02 completes locally, then `next/codex-runtime-support` has a local commit containing PR #3 runtime support plus the planned metadata/version changes.
- Given a custom-source install reads `.claude-plugin/marketplace.json`, when it inspects the plugin entry, then it sees `source: "./"`, `version: "1.15.0-next.0"`, and both Automator skill paths.
- Given later agents read the versioning plan, when they inspect `TODO.md` and `handoff-log.md`, then Phase 02 status, HEAD SHA, changed files, verification, and next Phase 03 command are recorded.

## Spec Change Log

## Verification

**Commands:**
- `git fetch automator main '+refs/pull/3/head:refs/remotes/automator/pr/3' --no-tags` -- expected: fetch succeeds.
- `npm run verify` -- expected: Python tests, dry-run pack, and smoke test pass.
- `git diff --check` -- expected: no whitespace or patch-format errors.
- `git diff --name-status automator/main...HEAD` -- expected: PR #3 runtime files plus metadata/version and plan artifact updates only.

## Suggested Review Order

**Branch Preview Metadata**

- Custom-source shape, preview semver, and skill discovery live here.
  [`marketplace.json:11`](../../../../.claude-plugin/marketplace.json#L11)

- npm preview version and generated artifact exclusion share one package boundary.
  [`package.json:3`](../../../../package.json#L3)

- Python package uses PEP 440 preview metadata intentionally.
  [`pyproject.toml:7`](../../../../skills/bmad-story-automator/pyproject.toml#L7)

**Stop Hook Review Fixes**

- Hook command generation now canonicalizes executable paths.
  [`basic.py:43`](../../../../skills/bmad-story-automator/src/story_automator/commands/basic.py#L43)

- Existing env-wrapped hooks normalize instead of duplicating.
  [`stop_hooks.py:269`](../../../../skills/bmad-story-automator/src/story_automator/core/stop_hooks.py#L269)

**Continuity And Tests**

- Phase 02 handoff records refs, verification, decisions, and next command.
  [`handoff-log.md:109`](../handoff-log.md#L109)

- Regression test covers env-wrapped stop-hook normalization.
  [`test_stop_hooks.py:238`](../../../../tests/test_stop_hooks.py#L238)
