# Validation and release gates

Project Version: 0.10.0-dev.1

The user explicitly requested removal of all testing code. No test suites,
gameplay doubles, item-grant/debug commands or Java harnesses remain in active source.
Production preflight checks are retained to reject malformed or unsafe releases.
Old test reports retain their observed versions; they are not current proof.

Commands from the project root, using a Python interpreter with requirements-tools.txt:

```powershell
python -B scripts/check_versions.py
python -B scripts/validate_release.py
./Build-Workshop.ps1 -PythonExe <python-with-lupa>
python -B scripts/check_versions.py --release
./Publish-Workshop.ps1 -PrepareOnly -PythonExe <python-with-lupa>
```

The syntax parser compiles Lua without executing gameplay. Source preflight checks
Lua-only payloads, case-correct requires, JSON/key/placeholder coverage,
recipe-name/instruction localization, canonical
Workshop text and source URL. Package preflight verifies inventory, safe paths,
case collisions, ZIP CRC, source/staging hashes and version provenance. Upload
preparation compares VDF description/change-note text to canonical real paragraphs.
These checks are static/offline integrity, not behavior tests or Linux/runtime evidence.

[VERIFIED: source] The crafting adapter uses installed vanilla OnTest/OnCreate,
IsWorn and keep semantics. Payment stays in the existing server/SP tie transaction;
clients submit the vanilla crafting action. No gameplay test suite was restored.
Recipe labels/instructions use English fallback in the 29 supported language
folders, matching the existing localization policy; key presence is not proof of
native-language translation quality.

[TESTED: offline, 2026-10-14] `python -B scripts/check_versions.py` passed for
0.7.0-dev.1. `python -B scripts/validate_release.py` passed for 128 runtime files,
including compilation of all nine Lua files without execution and translation
key/instruction coverage. A read-only identity audit matched all 47 recipe input
IDs against the installed generated item definitions. `git diff --check` passed.
Package results, source hashes and commit are recorded in generated provenance;
they do not replace the untested gameplay gates below.

[TESTED: offline, 2026-10-14, 0.8.0-dev.1] Run from the project root using the
bundled Python with Lupa 2.6:

```powershell
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --check
```

All passed: 165 runtime files; all 12 Lua files compile without execution; JSON,
XML, localization and exact original icon checks pass. A separate read-only
source audit matched all 49 referenced vanilla types and both defined custom
outputs. Native registry and clothing/equipment source paths were inspected, not
executed in PZ. No test suite was restored. No current 0.8 package was generated;
the prior provenance in dist/current remains a historical 0.7.0-dev.1 record.
See RETAINER_ITEMS.md for the exact durability hook blocker and current manual
runtime scenarios. Dedicated G7 and stable G8 remain blocked.

[RUNTIME GATE] SP behavior and dedicated MP have not been validated for this iteration.
[TESTED: offline, 2026-10-14, 0.9.0-dev.1] The same exact Python/version/source
commands above and `git diff --check` pass for 168 runtime files, including all 13
Lua files compiled without gameplay execution. Source review confirms three
distinct icon/item bindings, no crafting output for UnbreakableRetainer, and the
native cosmetic/no-hole/no-coverage properties. Installed world-fill event,
capacity and item-creation APIs and core school/optical/pharmacy room keys were
checked. Both new generated masters and all 64x64 runtime icons are true RGBA
with transparent borders; source/export/runtime hashes match. Original black
icon and model master hashes remain unchanged. No test suite was restored.
New loot appearances, native wear/damage, transfers, synchronization and saves
remain NOT TESTED. No 0.9 package, live deployment or Workshop upload was run.

G7 BLOCKED / NOT TESTED; G8 BLOCKED. Stable release requires current-commit dedicated evidence and gates. Under the
2026-10-14 Workshop MP testing policy, an explicit publish request may distribute
this labelled test build before G7, after all source/authority/security/package checks.
Preparation does not
launch a game/server, deploy live mods, connect via SFTP or contact SteamCMD.

## Current native durability source iteration

[TESTED: offline, 2026-10-14, 0.10.0-dev.1] Production source/version checks
passed for 169 runtime files, compiling all 14 Lua files without engine execution.
JSON/XML, localization keys/placeholders, require case, icons, native finite-item
properties, rare-item damage exemption and generated-item recipe exclusions pass.
`git diff --check` is the separate whitespace gate. No current package exists.

A disposable offline audit outside the repository executes the actual Core,
Retention, TieDurability, WearableRetainers and RetainerPresentation modules with
Lua doubles through bundled Python/Lupa lua51. Command from the project root:

```powershell
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B "$env:TEMP/B47ANCEDEyewear-lua-durability-audit/durability_logic_audit.py"
```

92 assertions PASS: all six material payments, duplicate requests, unpaid rollback,
paid notification failure, allocation notification failure, native-order break
reconciliation (modeled only), concurrent Eyes/Face/Hat slots, occupied/full/dead
rejection, one-time legacy migration, untouched historical data, missing-link
non-recreation, both-item transfer, previous-owner rejection, reciprocal ID
mismatch, stale worn-map/changed-owner rejection, dead-owner rejection, crafted break, live native condition projection, validated sandbox
resistance without repair, unbreakable exemption and client mutation rejection.
The injected failure messages are expected. The temporary audit is not shipped,
installed in the mod or restored as a repository test suite. This is offline Lua
logic evidence with doubles, NOT an actual native combat/save/network test.

[VERIFIED: preserved artifact] Published 0.9 ZIP/checksum/provenance retain their
SHA-256 hashes under dist/historical/0.9.0-dev.1-published; ZIP CRC is checked
read-only. The preservation ledger records all three files; nothing was deleted.

[RUNTIME GATE] Actual headwear layering, native damage eligibility/ordering and
condition packets, migration through real saves, both-item transfer, join/rejoin,
restart, UI and concurrency require SP/dedicated evidence. No game/server was
launched. G7 BLOCKED / NOT TESTED; stable G8 BLOCKED. No 0.10 package, deployment
or Workshop upload was performed or authorized. See DURABILITY.md.
