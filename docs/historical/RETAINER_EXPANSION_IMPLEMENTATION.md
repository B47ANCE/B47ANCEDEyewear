# Retainer expansion implementation

Project Version: 0.4.0-dev.1
Date: 2026-10-05
Status: partial development implementation; permanent branch blocked.

## Implemented development candidate

- Server-owned, schema-2 finite makeshift state on the original eyewear.
- All 14 audited material contributions and caps, same-material layering with existing wear preserved, one tape reinforcement, rubber-band cap, zip-tie tape exclusion and sharp-tool removal.
- Revision-checked inventory intents: server resolves native item IDs and validates ownership, worn status, materials and sandbox configuration. Removal destroys makeshift material without refund.
- Read-only post-roll durability proposal. Native bridge replaces one state table before canceling native removal. The breaking hit is the final catch; subsequent falls proceed normally. No additional RNG, replacement eyewear or re-equipping.
- Native Lua-init capability registration, pure-Java agent registration to avoid premature engine-class loading, immutable installed-build fingerprints and vanilla fallback on incompatibility.
- Right-click retainer menus, current/maximum durability, material, layer and tape information. Complete English-fallback keys in all 29 language folders.
- Server sandbox durability and impact multipliers and makeshift enable switch. Permanent settings remain explicitly reserved/inactive.
- Known legacy ties migrate once to one finite strand when the native capability is available; no material refund. Without the bridge, existing Lua behavior remains available.

## Validation

[TESTED: offline Windows Python/Lupa] 54 tests pass, including 10 finite-retainer regression tests. Command:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B -m unittest discover -s B47ANCEDEyewear/tests
```

[TESTED: offline Windows JDK 25] Native compilation, actual installed classfile transformation/verifier, 12 isolated fixture scenarios, production table-commit scenarios, immutable-field/stale-revision refusal and mismatched-build vanilla fallback pass:

```powershell
& ./B47ANCEDEyewear/native/Build.ps1 -JdkHome './Last Known Address/build/toolchain/jdk-25.0.4.1+1' -GameJar 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/projectzomboid.jar'
& $pzPython -B B47ANCEDEyewear/native/tests/run.py --jdk './Last Known Address/build/toolchain/jdk-25.0.4.1+1' --game-jar 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/projectzomboid.jar'
& $pzPython B47ANCEDEyewear/scripts/check_versions.py
```

Logs: native/build/expansion-lua-tests.log and native/build/expansion-native-tests.log. These are isolated engine doubles and classfile checks, not gameplay. The production commit harness runs on the build JDK; earlier fixture/load checks also ran on the installed game JRE. Version consistency passes; no current release package exists.

## Remaining blockers

[UNKNOWN] The actual reusable permanent item needs mutually exclusive loose/attached ownership, complete native-item persistence, transfer/reconnect recovery and return of the same item. InventoryItem exposes saveWithSize/loadItem; this alone does not establish an atomic attachment transaction. Generic attachment slot/model properties do not prove nested valuable-item persistence. No userdata persistence or FullType-only replacement has been substituted.

The repository invariant says: "STOP affected gameplay implementation and document the blocker if a safe authority model cannot be established." Consequently permanent attachment/removal, permanent catch, extremely rare loot registration and worn-model binding remain disabled. Original sprite and mesh preparation are retained; they are not a functioning wearable item. Asset export and visual replication remain unfinished.

[RUNTIME GATE] Native startup after the loader change, actual post-roll catches, item consumption/save recovery, timed-action serialization, remote-client synchronization, join/reconnect, dedicated-server authority and Linux loading are not tested. The historical failed startup report is preserved. G7 BLOCKED / NOT TESTED; G8 BLOCKED. No PZ/server launch or new Workshop deployment occurred. The published Workshop item remains 0.3.0-dev.1.
