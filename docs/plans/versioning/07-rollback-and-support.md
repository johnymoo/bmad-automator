# Phase 07 - Rollback And Support

<!-- markdownlint-disable MD013 -->

## Clean Context Start

Before doing this phase, read [README.md](./README.md), [handoff-log.md](./handoff-log.md), [TODO.md](./TODO.md), and the latest Phase 05 or Phase 06 handoff. Use the actual shipped tag and known risks recorded there.

## Goal

Keep a clean escape path for preview and stable users.

## Preview Rollback

If `v1.15.0-next.0` is bad:

1. Do not move or delete the tag.
2. Cut a fixed preview:

```bash
git tag -a v1.15.0-next.1 -m "v1.15.0-next.1"
git push automator v1.15.0-next.1
```

1. Tell testers to reinstall:

```bash
npx bmad-method install --modules baut --pin baut=v1.15.0-next.1 --tools codex --yes
```

1. If no fix is ready, tell testers to return to stable:

```bash
npx bmad-method install --modules baut --pin baut=v1.14.2 --tools claude-code --yes
```

## Stable Rollback

If `v1.15.0` ships and must be rolled back:

1. Do not move `v1.15.0`.
2. Cut a patch release from the last good stable base or from a revert commit:

```text
v1.15.1
```

1. Document the issue and fix in changelog.
2. Publish npm patch if npm stable was published.

## Support Notes

When collecting bug reports, ask for:

- install command used
- installed tag or branch
- `_bmad/install-manifest.csv`
- target tool: `claude-code`, `codex`, or both
- exact stderr/stdout from failed installer command
- whether install was official `--modules baut`, pinned, or `--custom-source`

## Known Confusion To Avoid

`--next baut` means `main` HEAD. It does not mean:

- open PR head
- `next/codex-runtime-support` branch
- prerelease npm dist-tag
- prerelease semver git tag

For PR preview, use `--pin baut=v1.15.0-next.N` or `--custom-source ...@next/codex-runtime-support`.

While the official registry keeps `baut` on `default_channel: next`, unqualified `--modules baut` also means `main` HEAD. Use `--all-stable` or `--pin baut=<stable-tag>` for stable rollback.

## Handoff Requirements

Append a Phase 07 entry to [handoff-log.md](./handoff-log.md) with:

- rollback commands validated
- support docs or issue templates changed
- known active incidents or confirmation none exist
- final stable and preview tags users should install
- any follow-up work outside this versioning plan
