# Validation and release gates

Project Version: 0.14.0-dev.1

## Current 0.14 material/reinforcement iteration

[TESTED: offline Windows Python 3.12 / Lupa Lua 5.1, 2026-10-16]
`python -B scripts/check_versions.py` and `python -B scripts/validate_release.py`
pass. Production preflight covers 196 runtime files, 15 Lua syntax compilations,
seven native clothing registrations, three ground models and twelve worn meshes,
case-correct requires, localization and asset provenance. Original ten-point tie
and crafted-retainer definitions remain intact; three LayeredTie types reuse the
same clothing assets and declare a fixed 100 native condition ceiling.

External regression command from the project root:
`python -B "$env:TEMP/eyewear-014-work/reinforcement_regression.py"`
passes 694 assertions against actual modules with offline doubles. It exercises
all fourteen materials, exact whole/drainable payment, all reinforcement limits,
condition-deficit conservation, stale/replayed/forged/foreign requests, tool
validation/invalidation, rollback/notification failures, legacy paid migration,
configuration snapshots, read-only live tooltips, menus, crafting and one-route
timed actions. The harness stays outside Git and runtime source. Installed source
inspection verifies the native APIs/FullTypes; no proprietary source is copied.

[RUNTIME GATE] Current G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable
G8 BLOCKED. Prior user-reported 0.13.1 acceptance applies only to that published
package, not this new gameplay. See TIE_REINFORCEMENT.md for dedicated acceptance scenarios and
save/downgrade limits. No game/server launch, package, deployment or upload.

## Current clothing synchronization patch

[TESTED: offline, 2026-10-15, 0.13.1-dev.1] `python -B scripts/check_versions.py`,
`python -B scripts/validate_release.py` and `git diff --check` pass. The production
preflight covers 195 runtime files, all 14 Lua syntax compilations, seven native
clothing GUID registrations, retained art provenance, localization and path case.
Disposable `python -B "$env:TEMP/B47ANCEDEyewear-lua-durability-audit/clothing_sync_regression.py"`
passes 126 assertions against actual modules with doubles. The same scenario fails
against the old module. This audit stays outside source; no test suite/debug code
was restored. CLOTHING_SYNC_FIX.md records root cause, mutation probes and exact
remaining native acceptance. G6 native/SP NOT TESTED; G7 BLOCKED / NOT TESTED;
stable G8 BLOCKED. No packaging, deployment or publication.

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

## Native durability source milestone, before authorized packaging

[TESTED: offline, 2026-10-14, 0.10.0-dev.1] Production source/version checks
passed for 169 runtime files, compiling all 14 Lua files without engine execution.
JSON/XML, localization keys/placeholders, require case, icons, native finite-item
properties, rare-item damage exemption and generated-item recipe exclusions pass.
`git diff --check` is the separate whitespace gate. No package existed at this source milestone.

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
launched. G7 BLOCKED / NOT TESTED; stable G8 BLOCKED. This source milestone did
not package, deploy or upload. See DURABILITY.md.

## Authorized Workshop development distribution

The user subsequently requested publication of 0.10.0-dev.1 as a development
build on 2026-10-14. Source/version checks run again before packaging; the
established Build-Workshop.ps1 and Publish-Workshop.ps1 preflights check ZIP CRC,
inventory, path/case safety, source/staging parity, commit/version provenance,
VDF identity/public visibility and canonical paragraph preservation. Exact
commands, commit, package/text hashes, upload verification and Steam desktop
restart outcome belong to generated publication-0.10.0-dev.1.json. Prior source
audit results above are retained as offline evidence, not upgraded to runtime
proof. This distribution remains MP testing only; G7/stable G8 remain blocked.

## Ground model source milestone

[TESTED: offline, 2026-10-14, 0.11.0-dev.1] Commands run from the project root:

```powershell
& 'C:/Users/willi/.cache/b47anced-tools/python311-blender/python.exe' scripts/build_retainer_ground_models.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --check -- . ':!AGENTS.md'
```

Blender 4.5.7 LTS produced and re-imported three FBX 7400 meshes, each as one
mesh with matching dimensions. The labelled offline preview was inspected.
Editable .blend, packed textures and per-file/export hashes are preserved.
Source preflight passes for 176 runtime files and compiles all 14 Lua files
without executing gameplay; exact-case model/item/FBX/texture bindings, PNG
integrity and original authoring hashes pass. Read-only comparison with the
published 0.10 source confirms every Lua file is byte-identical and item scripts
differ only by the three WorldStaticModel bindings. Prior gameplay audits remain
historical 0.10 results; they were not rerun or relabeled.

No package, live deployment, Workshop upload, game/server launch or in-game
validation occurred. PZ orientation, placement, scale, lighting and dropped-item
appearance remain NOT TESTED. G7 BLOCKED / NOT TESTED; stable G8 BLOCKED.
The previous published 0.10 files were preserved by a bounded move with matching
SHA-256 hashes, a preservation ledger and a read-only ZIP CRC check.

## Black-cord sizing correction

[TESTED: offline, 2026-10-14, 0.11.1-dev.1] Commands from the project root:

```powershell
& 'C:/Users/willi/.cache/b47anced-tools/python311-blender/python.exe' scripts/build_retainer_ground_models.py --only-unbreakable
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --cached --check
```

Blender 4.5.7 LTS re-import dimensions match all three source meshes. Rare cord
footprint is 0.1434 x 0.099825 m, matching the crafted mean to within 0.00001 m;
its original footprint was 0.1656 x 0.1882 m. The updated labelled Blender preview
was inspected. Production preflight checks this footprint contract, all asset
hashes/bindings and 176 runtime files, including syntax compilation of 14 Lua files.
A read-only comparison confirms cloth/leather FBX, runtime textures, item/model
bindings and all Lua gameplay files are unchanged from commit abc82a4.
Prior evidence remains tied to its actual version; no gameplay audit was rerun.
No test suite, package, deployment, upload or PZ/server launch. In-game importer,
placement, lighting and display remain NOT TESTED; G7/stable G8 remain BLOCKED.

## Authorized ground-model Workshop distribution

The user subsequently requested 0.11.1-dev.1 publication as a development build
on 2026-10-14. This authorizes packaging and the existing Workshop item upload;
prior source-only statements above describe their original milestones. Run the
production source/version checks, Build-Workshop.ps1, check_versions.py --release
and Publish-Workshop.ps1 preflight against the exact committed source. Generated
publication-0.11.1-dev.1.json records package/text hashes, release commit, exact
commands, SteamCMD/API verification and the Steam desktop restart outcome.
Preserve public visibility, original artwork and prior published provenance.
No game/server launch or local SP deployment is authorized. G7 BLOCKED / NOT
TESTED and stable G8 BLOCKED remain unchanged; distribution is not runtime proof.

## Worn retainer source milestone

[TESTED: offline, 2026-10-14, 0.12.0-dev.1] Commands from the project root:

```powershell
& 'C:/Users/willi/.cache/b47anced-tools/python311-blender/python.exe' scripts/build_retainer_worn_models.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --cached --check
```

Blender 4.5.7 LTS produced six original DirectX text meshes plus editable source,
packed original atlases and a schematic preview (visually inspected). Independent
Assimp import (assimp-py 1.1.0) accepts every file with one mesh, expected triangle/
vertex counts, finite coordinates, normals, UVs and appropriate head-local scale.
Production preflight passes for 185 runtime files, compiling the unchanged 14 Lua
files and verifying exact item/XML/head-bone/texture/path-case/hash contracts.
Original ground assets/textures, inventory art, all gameplay Lua and improvised
appearance definitions are unchanged. Item changes only select three new clothing
XMLs. Prior validation retains its actual version and environment.
No package, deployment, Workshop upload, test/debug runtime code or PZ/server
launch. Actual wear/display, fit, old-save refresh, animation, hair/hat/frame
clipping and remote visuals remain NOT TESTED. G7/stable G8 remain BLOCKED.

## Authorized worn-model Workshop development distribution

The user subsequently requested 0.12.0-dev.1 publication as a development build
on 2026-10-14. This authorizes packaging and the existing public Workshop item
upload; source-only statements above describe their original milestones. Run
check_versions.py, validate_release.py, Build-Workshop.ps1, check_versions.py
--release and Publish-Workshop.ps1 preflight against the exact committed source.
Generated publication-0.12.0-dev.1.json records source commit, package/text hashes,
exact commands, SteamCMD/API verification and graceful Steam restart outcome.
Preserve prior package/provenance, item identity, visibility and custom artwork.
No game/server launch or local SP deployment. Worn fit/clipping/remote visuals
remain NOT TESTED; G7 BLOCKED / NOT TESTED and stable G8 BLOCKED remain unchanged.

## Improvised tie visual source milestone

[TESTED: offline, 2026-10-14, 0.13.0-dev.1] Commands from the project root:

```powershell
& 'C:/Users/willi/.cache/b47anced-tools/python311-blender/python.exe' scripts/build_improvised_tie_models.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --cached --check
```

Blender 4.5.7 LTS exports six original Eyes/Face/Hat models plus editable source,
packed original cloth atlas, a schematic preview and per-file/helper provenance.
The preview was inspected; it shows male examples, eyewear rear and hat front.
Assimp import (assimp-py 1.1.0) accepts all six as one mesh each with finite
coordinates/normals, UVs, matching counts and head-local dimensions. Production
preflight passes for 194 runtime files; all 14 Lua files compile without gameplay
execution. It checks item/XML/head-bone/texture/slot/hash/case contracts, native
finite/rare invariants, retained ground/worn assets and localization/require case.
Read-only comparison confirms gameplay Lua, original retainer/XML/ground/icon
bytes are unchanged; item definitions only select the three new clothing XMLs.
Old validations retain their original versions; no gameplay audit was rerun.
Published 0.12 package/checksum/provenance remain hash-preserved, with ZIP CRC.
No testing/debug runtime code, package, deployment, Workshop upload or game/server
launch. PZ fit, simultaneous layers, clipping, old-save refresh, take-off/break
visuals and dedicated remote rendering remain NOT TESTED; G7/stable G8 BLOCKED.

## Authorized clothing-sync Workshop MP test distribution

The user requested publication of 0.13.1-dev.1 on 2026-10-15. Canonical inputs
remain WORKSHOP_DESCRIPTION.txt and WORKSHOP_CHANGE_NOTE.txt. Build-Workshop.ps1
and Publish-Workshop.ps1 prepare and validate the existing public item 3799754736
for App ID 108600. The generated publication-0.13.1-dev.1.json binds actual
SteamCMD/API results, source commit, package/text hashes and Steam restart outcome.
Previous source-only statements describe their original milestones. Runtime
acceptance remains NOT TESTED; G7 and stable G8 remain BLOCKED. No local SP
deployment, game/server launch or server modification is authorized.

## Thumbnail artwork source milestone

[TESTED: offline, 2026-10-15, 0.13.2-dev.1] Root thumbnail.png is an exact copy
of the user-selected PNG: 1254x1254 RGB, SHA-256
10ac7ba24b2b0f784a3a0eb294b915088311d8a3924d7aad4af3de2cf9d86758.
Pillow image.verify/load and hash/dimension comparison pass. The previous custom
1024x1024 PNG is preserved with its original hash in assets/branding. Commands:

```powershell
python -B scripts/check_versions.py
python -B scripts/validate_release.py
git diff --cached --check
```

All runtime source/model/icon/registration bytes are unchanged except modversion;
all 14 Lua files compile without gameplay execution. No package or deployment,
Workshop upload or PZ/server launch. Prior runtime evidence keeps its original
version/package; pending user-owned test documentation is excluded from this
thumbnail commit. See THUMBNAIL.md for artwork/export provenance and limits.
