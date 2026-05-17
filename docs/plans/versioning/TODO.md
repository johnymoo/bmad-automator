# Versioning TODO

<!-- markdownlint-disable MD013 -->

## Phase 01 - Baseline

- [x] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [x] Fetch current `automator/main`.
- [x] Fetch PR #3 head.
- [x] Confirm `skills/module.yaml` exists on `main`.
- [x] Confirm PR #3 diff still applies cleanly.
- [x] Record current latest stable tag.
- [x] Append Phase 01 notes to `handoff-log.md`.

## Phase 02 - Integration Branch

- [x] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [x] Create `next/codex-runtime-support` from current `main`.
- [x] Apply PR #3 commits.
- [x] Resolve conflicts without dropping `skills/module.yaml`.
- [x] Restore official `bmad-code-org/bmad-automator` metadata.
- [x] Add marketplace `skills` entries for custom-source discovery.
- [x] Bump preview versions to `1.15.0-next.0`.
- [x] Record whether `skills/module.yaml` `module_version` tracks release tags for Automator.
- [x] Append Phase 02 notes to `handoff-log.md`.

## Phase 03 - Preview Tag

- [ ] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [ ] Run local verification.
- [ ] Push integration branch.
- [ ] Create annotated `v1.15.0-next.0` tag.
- [ ] Push preview tag.
- [ ] Optional: publish npm package with `--tag next`.
- [ ] Append Phase 03 notes to `handoff-log.md`.

## Phase 04 - Consumer Docs

- [ ] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [ ] Add stable install command.
- [ ] Add preview pin install command.
- [ ] Add branch custom-source install command.
- [ ] Add rollback command.
- [ ] Warn that `--modules baut` and `--next baut` track `main` while registry `default_channel: next` remains.
- [ ] Append Phase 04 notes to `handoff-log.md`.

## Phase 05 - Verification

- [ ] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [ ] Verify stable pin install in temp project.
- [ ] Verify preview pin install in temp project.
- [ ] Verify custom-source branch install in temp project.
- [ ] Verify all-stable does not select prerelease.
- [ ] Capture command output for any failure.
- [ ] Append Phase 05 notes to `handoff-log.md`.

## Phase 06 - Stable Promotion

- [ ] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [ ] Merge PR/integration into `main`.
- [ ] Bump stable version to `1.15.0`.
- [ ] Run `npm run verify`.
- [ ] Tag `v1.15.0`.
- [ ] Optional: `npm publish`.
- [ ] Update docs from preview to stable.
- [ ] Append Phase 06 notes to `handoff-log.md`.

## Phase 07 - Rollback

- [ ] Read `README.md`, assigned phase doc, and `handoff-log.md`.
- [ ] If preview breaks, cut `v1.15.0-next.1`.
- [ ] If stable breaks, cut patch tag after revert/fix.
- [ ] Keep install support notes updated.
- [ ] Append Phase 07 notes to `handoff-log.md`.
