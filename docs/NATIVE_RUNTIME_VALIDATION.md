# Native bridge runtime validation attempt

Project Version: 0.3.0-dev.1

2026-10-04. Recommendation: **REVISE**. User subsequently instructed that
in-game testing is unnecessary; testing stopped. No additional client/server
launch is authorized by this report. No gameplay catch evidence was obtained.

## Environment and preserved evidence

Windows; installed game JAR source identifies Build42.21; installed Azul Java
25.0.1; agent/project0.3.0-dev.1. Standard direct Java launch with the existing
agent=fixture, -debug, -nosteam, separate workspace cachedir and4GB heap.
Exact arguments: `native/runtime/sp-launch-arguments.txt`.
stdout/stderr: `native/runtime/sp-stdout.log`, `sp-stderr.log`.
Isolated engine log: `native/runtime/sp-cache/console.txt`.
Temporary source copy: `native/runtime/sp-cache/mods/B47ANCEDEyewear`.
No installed game files, production saves, production server, live mods or
Workshop content were modified. The temporary mod was not enabled in gameplay.

[TESTED Windows actual client startup] Agent registered. The first attempt used
the stock batch classpath `./;projectzomboid.jar`, while omitting the installed
JSON launcher's unrelated NPC agent. Existing loose classes under the installed
game directory still took precedence over JAR classes. Startup output includes
`[pzopt] loaded override` messages. Installed loose IsoGameCharacter.class hash:
`216f7621a3d66626b1dd1b9e7b02d4230114246e04f32e8c6b2021e630209b18`.
Audited original JAR class hash:
`29040e19c3e420499f73bc0ea0d5b86d7f7d38655acdc13d0107df736eb54c0b`.

The bridge logged `INCOMPATIBLE OR TRANSFORM FAILED; vanilla fallback;
IllegalArgumentException: class SHA-256 mismatch`, then startup terminated:
`LinkageError: loader 'app' attempted duplicate abstract class definition for
zombie.characters.IsoGameCharacter`, from DebugLog initialization through
MainScreenState.main. No game window/world/player was created. Process4852 exited.

Build mismatch refusal is expected; startup safety failed in this environment.
[UNKNOWN] The cause of the duplicate definition and the bridge's contribution
require a focused class-loading investigation. Do not attribute it solely to
the loose override or claim fallback is safe in real startup. The earlier
isolated Class.forName(...,false) PASS does not cover this startup order.

## SP matrix

| Test | Status |
| --- | --- |
| Vanilla control | BLOCKED |
| Real catch | BLOCKED |
| Same item | NOT TESTED |
| No inventory duplicate | NOT TESTED |
| No world duplicate | NOT TESTED |
| Repeated catches | NOT TESTED |
| Catch disabled -> normal removal | NOT TESTED |
| Real zombie-hit route | NOT TESTED |
| Secondary fall/knockdown route | NOT TESTED |
| Same-FullType collision | NOT TESTED |
| Callback failure fallback | NOT TESTED |
| Agent-absent control | NOT TESTED |

Separate startup results: agent registration PASS; incompatible bytecode refusal
PASS; client startup FAIL; safe startup fallback FAIL for this observed launch.
These are startup outcomes, not successful gameplay tests.

## MP matrix

| Test | Status |
| --- | --- |
| Dedicated server | BLOCKED |
| Server authority | NOT TESTED |
| Client A catch state | NOT TESTED |
| Client B catch state | NOT TESTED |
| No world duplicate | NOT TESTED |
| No inventory duplicate | NOT TESTED |
| ALLOW replication | NOT TESTED |
| Same-FullType collision | NOT TESTED |
| Reconnect | NOT TESTED |
| Server restart | NOT TESTED |

SP catch did not pass; no dedicated-server attempt was made. User then stopped
in-game testing. G7 remains BLOCKED / NOT TESTED; G8 BLOCKED.

## Linux

| Test | Status |
| --- | --- |
| Native agent loading | NOT TESTED |
| Transformation | NOT TESTED |
| Runtime catch | NOT TESTED |
| Safe fallback | NOT TESTED |

## Transaction protocol

Detailed production protocol design is deferred under the handoff's prerequisite
that runtime interception first be proven. The minimum boundary remains:
read authoritative state; validate revision/ownership; calculate an immutable
proposal without mutation; validate it; commit state and latch CATCH as one
native-controlled operation. Before commit, failure must perform no writes and
return ALLOW. After commit, optional diagnostics/replication must not change the
latched CATCH. Durability reaching0 on the breaking hit still returns CATCH;
next event returns ALLOW. Arbitrary Lua mutation followed by a fallible return
is unacceptable. The current read-only fixture does not implement that protocol.

Actual permanent-item conservation remains separate: exclusive loose/attached
ownership of the same native item, verified serialization and recovery. No
FullType-only reconstruction or actual-item escrow is implemented here.

## Remaining blockers and decision

Bridge blockers: startup-order duplicate-class failure; environment classpath
isolation; no real catch/conservation/MP proof; no bounded commit adapter.
Feature blockers: durability transaction, actual-item escrow, materials and
configuration remain unimplemented. Release blockers: dedicated gate, current
package/branding gates and native compatibility/failure behavior remain open.

**REVISE.** Smallest next technical investigation, without launching the game:
reproduce the helper/target class-loading order in an isolated JVM, including
an incompatible target and a logging-first entry point. Establish whether eager
helper type resolution creates a duplicate definition; retain failure logs
before changing code. Verify a JAR-only classpath independently of installed
loose overrides. No architecture rewrite, probability change, retainer content,
version promotion or release packaging was performed.
