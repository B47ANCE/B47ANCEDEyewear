# Rename validation

Project Version: 0.3.0-dev.1

Date/environment: 2026-10-03, Windows offline, Python/lupa. No PZ runtime,
server, deployment or publication was performed. Full acceptance remains blocked.

| Check | Status | Evidence / limit |
| --- | --- | --- |
| Lua/static validation | PASS | Six Lua files parse; 38 offline tests; both PowerShell scripts parse. |
| Metadata consistency | PASS | One canonical Mod ID; exact translation parity across 29 locales; Workshop ID preserved. |
| Version consistency | PASS | Development checker validates all declared current mirrors. |
| Linux case sensitivity | NOT TESTED | Exact-case internal require/file audit PASS on Windows; vanilla dependencies exist. No Linux runtime used. |
| Single-player runtime | NOT TESTED | Human-operated PZ client required. |
| Existing-save migration | NOT TESTED | Migration mocks PASS; actual save activation/migration untested. |
| Dedicated server | NOT TESTED | G7 BLOCKED; no native dedicated evidence. |
| Two-client multiplayer | NOT TESTED | Command/ownership and separate-peer mocks PASS only. |
| Save/reload | NOT TESTED | State restoration mocks PASS only. |
| Sandbox settings | NOT TESTED | No baseline project SandboxVars/options; no namespace to migrate. Existing configurability gap remains. |
| Eyewear mechanics | NOT TESTED | Established offline regressions PASS; Retention.lua unchanged after identity substitutions. Native combat untested. |
| Release packaging | BLOCKED | Missing replacement thumbnail; no current ZIP. G8 also requires G7 PASS. |

[TESTED Windows offline] Baseline 0.2.0 passed 31 tests before editing. Current
version passes 38, including migration copy/precedence, malformed-state rejection,
client write refusal, monocle retirement, kit marker carryover, old-channel
rejection and exact requires/translation-key consistency. These are not native proof.

Exact commands from the workspace root:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B -m unittest discover -s ./B47ANCEDEyewear/tests -v
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear --json
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear --release --json
```

First two checks PASS. --release returns exit 1: no current package matches
dist/current/*.zip (expected BLOCKED). The baseline framework checker failed
because no version inventory existed; canonical controls were added from the
verified source version rather than guessed from archive filenames.

Both scripts were parsed using
System.Management.Automation.Language.Parser.ParseFile with zero errors.
`./B47ANCEDEyewear/Build-Workshop.ps1 -WorkshopRoot (Join-Path (Get-Location) '.tmp-eyewear-isolated-workshop')`
ran version/tests, then rejected missing replacement artwork before creating staging.
`Test-Path -LiteralPath './.tmp-eyewear-isolated-workshop'` returned False.
No live trees were altered.

Final case-insensitive search:

```powershell
rg -i -n 'Glasses Stay Put|GlassesStayPut|Glasses_Stay_Put|StayPutGlasses|\bGSP\b' B47ANCEDEyewear -g '!**/historical/**' -g '!*.pyc' -g '!check_versions.py'
```

Remaining hits are classified as follows:

- Core.lua: two deliberate legacy ModData reads; no old state-write namespace.
- TestKit.lua: deliberate legacy grant-marker read; no old command alias.
- tests/test_glasses.py: migration fixtures and old-channel rejection.
- CHANGELOG.md, WORKSHOP_DESCRIPTION.txt, IDENTITY_MIGRATION.md: historical
  identity, formerly/upgrade notice, and explicit migration instructions.
- This report: audit queries and historical classifications.
- historical/**: original packages, VDFs, backups, archived source, artwork,
  test cache, dated publication/preparation records, hashes and before/after diff.
  These are excluded from current source/build input.
- Workspace Caught Pants Down/docs/API_EVIDENCE.md: historical API-use observation.
- B47ANCEDBuildableFences/docs/evidence/pre-dev5-console-20261003T070602Z.txt:
  immutable captured console output; not rewritten as current proof.
- .tmp-stayput-api and old temporary/generated snapshots: historical research,
  not current project source or active packaging paths.
- No project-owned GSP or Glasses_Stay_Put identifier was found; generic unrelated
  occurrences were not renamed.

The baseline archive matches all 83 SHA-256 entries. A temporary Python audit
confirmed Retention.lua byte parity after identity substitution, six unique Lua
paths, one canonical mod.info, and no stale runtime filenames. Source diff:
historical/rename-source-diff.patch. No Git repository was initialized.

[RUNTIME GATE] G6 NOT TESTED; G7 BLOCKED / NOT TESTED; G8 BLOCKED. Test fresh SP,
upgraded save selection, dedicated Linux loading, two-client join/reconnect,
forged requests/material consumption, native timed-action untie, item probabilities,
secured/tied behavior, monocles, save/reload and transfer. Supply replacement
branding before Workshop packaging. Save compatibility remains inferred, not
certified. No current package or release readiness is claimed.
