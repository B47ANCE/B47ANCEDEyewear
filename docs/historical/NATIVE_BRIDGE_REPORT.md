# Native catch / authority bridge report

Project Version: 0.3.0-dev.1

Recorded 2026-10-04. Architectural recommendation: **REVISE**.
The exact interception is buildable and loads in an isolated JVM. Actual PZ
combat and multiplayer conservation have not been demonstrated. Full retainer
gameplay remains blocked. This is an original development spike outside runtime
source, not a native readiness or release certificate.

## Exact native path

[VERIFIED source] Current installed Core initializes `GameVersion(42,21,"")`.
SHA-256 of original `zombie/characters/IsoGameCharacter.class`:
`29040e19c3e420499f73bc0ea0d5b86d7f7d38655acdc13d0107df736eb54c0b`.
Core.class SHA-256:
`8f5c69740c8bf2181123a831ab68d1dfb047453687cca6dc62c77816d76ab360`.
Agent pins both, not a general 42.x range. Research copies and decompiler output
are under `research/retainers/native/`; they never enter the agent/runtime package.

`native/tests/.../Trace.java` parsed the entire installed game JAR without class
initialization. Its 19 direct call sites and exact caller/callee descriptors are
retained in `research/retainers/native/call-sites.tsv`. No installed Lua reference
to helmetFall/fallenOnKnees was found with the command recorded below.

| Origin / caller | Route into decision | Authority and qualification |
| --- | --- | --- |
| AttackState.triggerPlayerReaction; FakeDeadAttackState.animEvent; AttackVehicleState.animEvent | BodyDamage.AddRandomDamageFromZombie(IsoZombie,String,int)Z -> helmetFall(Z)Z | Local attack/damage entry points; any client call to helmetFall returns false. Scratch/laceration/bite branch calls helmetFall with Head/Neck flag. Not every attempted attack reaches it. |
| ZombieHitPlayerPacket.process | Bite.process(IsoZombie,IsoGameCharacter)V -> AddRandomDamageFromZombie -> helmetFall | Bite explicitly calls damage only on GameServer.server. Server chooses the real native fall roll. Clients process presentation portions, not this fall roll. |
| CombatManager.attackCollisionCheck | hitCharacter.helmetFall(hitHead > 0) | SP invokes; local MP attacker also calls but helmetFall's client guard returns before roll. Client-provided helmetFall flag for zombie targets is not used as authority for player catch. |
| PlayerHitPlayerPacket.process -> processHits; WeaponHit.process(IsoGameCharacter,IsoGameCharacter,HandWeapon)V | target.helmetFall(isHitHead()) | WeaponHit invokes helmetFall under GameServer.server, after hit processing. Preceding OnWeaponHitXp is before fall RNG and is not a cancelable removal hook. |
| IsoGameCharacter.DoLand(F)V -> IsoPlayer.handleLandingImpact(FallDamage)V -> base handleLandingImpact | Light damaging fall -> helmetFall(false); more-than-light -> fallenOnKnees(true) -> helmetFall(true) | IsoPlayer landing override returns on clients. Exact scheduling/replication of remote falls remains a runtime gate. |
| BumpedState.exit / processOnExit; ClimbOverFenceState.OnAnimEvent_FallenOnKnees / OnAnimEvent_VaultSprintFallLanded | fallenOnKnees()V -> fallenOnKnees(Z)V -> helmetFall | fallenOnKnees rejects clients and god mode. Native animation/state event scheduling on dedicated server remains untested. |
| IsoGameCharacter.loadChange(ADD_RANDOM_DAMAGE_FROM_ZOMBIE) | AddRandomDamageFromZombie -> helmetFall | Client damage path can reach method, but helmetFall refuses before RNG. No second client fall roll. |
| IsoZombie.handleLandingImpact and zombie visuals branch | helmetFall / helmetFallFromVisuals | Zombie-specific outcomes remain vanilla; bridge refuses non-player characters. Visual-only zombie clothing is outside this actual player InventoryItem hook. |

[VERIFIED source] `IsoGameCharacter.helmetFall(Z)Z` first rejects GameClient.client.
For actual worn items it invokes private `helmetFallFromWornItems(Z)Z`.
That method uses the live WornItem/InventoryItem objects. Original bytecode:

| Bytecode offset | Operation |
| --- | --- |
| 44–49 | WornItem.getItem -> local 5, original InventoryItem |
| 66–85 | Clothing.getChanceToFall; +40 if hitHead; original chance <=0 skips roll |
| 88–95 | Rand.Next(100), comparison; IF_ICMPGT ->141 skips removal |
| 98 | Successful-roll fall-through, operand stack empty: interception window |
| 99–104 | getInventory().Remove(original) |
| 107–125 | getWornItems().remove; resetModelNextFrame; onWornItemsChanged; removed=true |
| 126–129 | createFallingItem(original) |
| 132–138 | Server breaks after first successful removal |
| 141 /147 | Next item / method exit |

The exact roll succeeds when `Rand.Next(100) <= chanceToFall`, provided original
chance >0. The bridge does not recompute probability, invoke RNG, or change chance.
It injects immediately after the branch at95. ALLOW follows original bytecode;
CATCH goes to141 in SP or147 on the server, preserving the server's one-successful-
decision budget. It leaves `removed` unchanged. Other unprotected items can still
fall in SP's original loop; no blanket suppression of all clothing occurs.

[VERIFIED source] `createFallingItem(InventoryItem)V` on server first calls
IsoGridSquare.AddWorldInventoryItem, then sends ZombieHelmetFalling relative to
coordinates. Despite its name, that packet has an isZombie flag and player ID.
It serializes the actual item with saveWithSize; clients loadItem(...,249), create
falling clothing and remove a worn player item by type, not stable item ID.
Local wearer sends SyncClothing and triggers OnClothingUpdated after removal.
This native type-based match is a material untested risk for duplicate same-type
items when ALLOW occurs. We preserve vanilla behavior; we do not rewrite packets.

In SP, createFallingItem creates IsoFallingClothing with the original item. In
both cases CATCH bypasses that entire call, equipment mutation, and its packet.
The outer helmetFall emits local OnClothingUpdated and fallen-hat state only when
something actually was removed. No suitable Lua event/listener/cancel callback
exists in the verified post-roll/pre-removal window. The method is private;
overriding it is not an existing exposed Java extension point.

Authority answers: the server rolls, unequips, removes and creates the world
item; clients receive the removal packet and mutate their local replica. The
server can veto before any of those operations through this injected branch.
[INFERRED] With a catch there should be no removal replication to undo. [UNKNOWN]
Dedicated event scheduling, competing equipment updates, packet delivery and
two-client visibility still require actual runtime observations.

## Bridge / loader / failure

Original `native/src/b47ance/bridge/{Agent,Patch,Bridge}.java`; generated Version
comes exclusively from VERSION. Java 25 public Class-File API, no library/loader
dependency. Premain registers an Instrumentation transformer for one exact class.
Helper visibility, Core hash, target hash, method signature, unique roll branch,
loop exit, RNG invocation and inventory-removal invocation are checked before
returning transformed bytes; ClassFile.verify checks the output. No redefinition
or retransformation. Already altered/mismatched bytecode returns null and logs
vanilla fallback. Exact hashes protect hard-coded local slots and structural
assumptions. Instrumentation changes an in-memory definition only.

Standard loader API reference: [ClassFileTransformer](https://docs.oracle.com/en/java/javase/25/docs/api/java.instrument/java/lang/instrument/ClassFileTransformer.html).
Public transform/build API: [CodeBuilder](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/classfile/CodeBuilder.html).
These specify the JVM mechanism; they do not certify PZ launcher integration.

Development callback, only when agent argument is exactly fixture:
`B47ANCEDEyewearNativeCatchFixture(character, originalItem, nativeBodyLocation,
hitHead, "SERVER"|"SP") -> "ALLOW"|"CATCH"`.
Result must be successful pcall with exactly one return value equal to CATCH.
Clients, non-player characters, absent callback, invalid ownership, malformed
result and reentrant call allow vanilla. Callback errors log once, disable catch
for the session and allow removal. The supplied fixture is read-only. Bridge
also checks original WornItem reference, worn membership and inventory owner
before and after callback. It never adds, removes, clones, drops or equips items.
Debug output is fixture-only and capped at32 events, including character/item
identity, FullType, body location, authority, head flag and ALLOW/CATCH.

[TESTED Windows offline] The standard loader registered under both JDK25.0.4.1
and the installed game Azul25.0.1 JRE. Actual original game class was transformed
and defined with Class.forName(...,false) and -Xverify:all in an isolated JVM;
engine was not initialized. This establishes bytecode loading, not a real fall.
Build wrappers are Windows-only; Linux JVM loading remains NOT TESTED.

Safe failure has limits: missing/invalid -javaagent files or an unsupported JVM
can abort JVM startup before premain runs. Launcher-side preflight/removing the
startup option is required; this spike does not claim to catch those errors.
Other agents modifying this class afterward and load-order interactions are
untested. Loader failure cannot silently imply a granted catch.

The supplied read-only Lua fixture accepts only the explicitly selected Base.Glasses
pair. It refuses all hats, monocles and other items; the Java bridge has no general
compatibility policy or production catch registration API yet.

## Identity / conservation / future state

| Property | Windows offline original fixture | Actual PZ runtime |
| --- | --- | --- |
| Same InventoryItem reference and native ID | PASS | NOT TESTED |
| No world duplication | PASS (zero drop calls) | NOT TESTED |
| No inventory duplication | PASS (one original object) | NOT TESTED |
| Ownership unchanged | PASS (same container/worn entry) | NOT TESTED |

InventoryItem reference `==` and getID are checked before/after catches. ID is
serialized by vanilla save/load; JVM identityHashCode is diagnostic only and is
never persisted. The callback receives the same object, not a lookup/replacement.
Twenty repeated catches have no drift; disabling fixture then permits ordinary
removal and drops the original object. Zero chance, failed rolls, head bonus,
client refusal, server roll budget, callback error and failure latch are tested.
These doubles cannot prove actual world inventories or peer conservation.

The callback's CATCH result is separate from remaining durability. A future
breaking-hit transaction can return CATCH after decrementing to zero; next hit
returns ALLOW. However no durable transaction/persistence proof exists here.
Arbitrary mutating Lua callbacks can fail after partial writes; the bridge cannot
roll back arbitrary script side effects. STOP production catch/durability until
a bounded authoritative commit/failure protocol is implemented and proven.

No permanent retainer object is created or escrowed. Passing the original eyewear
does not require deleting/recreating a retainer, and imposes no FullType-only
storage. Actual-item attachment escrow, mutually exclusive ownership, full-item
serialization, recovery and transfer remain a separate blocker. Saving userdata
is not an accepted persistence design. Re-equip-after-drop is explicitly rejected.

## Runtime matrix / gates

| Required runtime test | Status |
| --- | --- |
| Single-player vanilla control | NOT TESTED |
| Single-player catch | NOT TESTED |
| Same-item identity | NOT TESTED |
| No world duplicate | NOT TESTED |
| No inventory duplicate | NOT TESTED |
| Repeated catch | NOT TESTED |
| Catch disabled -> vanilla removal | NOT TESTED |
| Dedicated server | BLOCKED |
| Two-client visual synchronization | BLOCKED |
| Reconnect | NOT TESTED |
| Server restart | NOT TESTED |
| Linux native loading | NOT TESTED |

[RUNTIME GATE] Launching PZ/server and live deployment require explicit authority
under workspace AGENTS.md and JAVA_DEVELOPMENT_POLICY.md. None was performed.
The required two-client and Linux environments have not been established.
G6 runtime NOT TESTED; G7 BLOCKED / NOT TESTED; G8 BLOCKED. No packaging, staging,
publication, installed-file edits, sandbox expansion or retainer gameplay.

## Validation commands and decision

Run from workspace; exact host paths used in this record:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
./B47ANCEDEyewear/native/Build.ps1 -JdkHome './Last Known Address/build/toolchain/jdk-25.0.4.1+1' -GameJar 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/projectzomboid.jar'
& $pzPython -B B47ANCEDEyewear/native/tests/run.py --jdk './Last Known Address/build/toolchain/jdk-25.0.4.1+1' --game-jar 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/projectzomboid.jar' --runtime-java 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/jre64/bin/java.exe'
& $pzPython -B -m unittest discover -s B47ANCEDEyewear/tests -v
& $pzPython -B B47ANCEDEyewear/scripts/check_versions.py --root B47ANCEDEyewear --json
rg -n 'helmetFall|fallenOnKnees' 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/lua' -g '*.lua'
```

Before-edit version check PASS. After-edit native offline suite PASS; existing
44-test suite PASS; version consistency PASS. Logs are under native/build/.
Missing Workshop branding and absent current ZIP remain prior release blockers.
Current version remains0.3.0-dev.1: this is a development-only architectural spike
within the current prerelease, with no new shipping gameplay/API/save schema.
Future retainer feature0.4.0-dev.1 remains a separate plan, not an active mirror.

**REVISE:** smallest next investigation is an explicitly authorized isolated SP
launch using this exact agent and read-only fixture, with real untied eyewear
and real zombie hits, recording control/catch/disable and object IDs. Then use
the same server-only fixture on dedicated server plus two clients, including
same-type inventory collisions, reconnect and restart. Establish Linux loading
and a bounded durability transaction failure protocol before adopting this as
the expansion foundation. Keep all material/loot/permanent-item work blocked.
