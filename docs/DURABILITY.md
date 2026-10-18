# Lua-only native durability

Project Version: 0.15.1-dev.1

## Crafted-retainer tape — 0.15

Crafted cloth/leather retainers now accept ONE tape in their main-inventory
right-click menu, worn or unworn. Default native wear-resistance bonus is +1 for
adhesive/+2 for duct tape. Condition, maximum, identity and worn mapping stay
unchanged; no recraft is required. Server intent validation, observed-payment
rollback boundaries, persistence, settings and runtime gates are detailed in
CRAFTED_RETAINER_TAPE.md. Unbreakable retainers are excluded. This is source-only;
current G7 NOT TESTED / BLOCKED and stable G8 BLOCKED.


## Current reinforcement rules

New 0.14 LayeredTieEyes/Face/Hat types have a fixed native 100-point ceiling and
snapshotted material-specific installed capacities. All fourteen materials use
native condition, not a parallel damage counter. Three thin-material strands and
one tape reinforcement preserve existing wear; zip ties require a usable tagged
cutter. Original ten-point tie definitions and paid legacy migration remain intact.
See TIE_REINFORCEMENT.md for current balance, configuration, UI, server transactions
and save/downgrade limits. The original ten-point details below describe retained
legacy ties and reusable crafted retainers unless explicitly stated otherwise.
No new SP/dedicated runtime proof exists; current G7 BLOCKED / NOT TESTED.
Design and source audit: 2026-10-14; installed Build 42.21 / Steam build 25485521.

0.13.1 patch: all existing clothing XMLs are registered with native file GUIDs.
New ties with an unresolved visual are rejected before link/equip/publication or
material consumption; paid legacy migration can retry without duplicates.
Condition and native damage rules below remain unchanged. See CLOTHING_SYNC_FIX.md.

## Accepted rule

The user approved head/clothing damage as the durability trigger, and explicitly
included ALL improvised material ties plus both crafted retainers. This replaces
the previous requirement to count only hidden successful knock-off rolls. The
rare Unbreakable Eyewear Retainer remains exempt. No custom Java, extra Lua hit
roll, client damage/catch command, eyewear replacement or post-drop re-equipping
is introduced. The native clothing-damage rule is not advertised as a catch count.

## Native wear and configuration

Existing finite items cover Head, are cosmetic with no armor bonus, cannot develop holes,
have zero ChanceToFall and use the existing native 10-point condition scale.
BloodClothingType.addHole's no-hole clothing branch uses Rand.NextBool with the
item's ConditionLowerChance and removes ONE condition point when selected. The
native setConditionAndSync returns immediately on clients, changes condition on
server/SP, then GameServer.sendItemStats synchronizes it. Native item save/load
and transfer preserve actual condition; there is no separate durability counter.
Head clothing layering and native damage eligibility still apply. This is not
wear on every attack or every hit anywhere on the body. Environmental clothing
damage to Head can also cause wear. A worn tie/retainer can wear even without its
eyewear, or while its protection setting is disabled, just like native clothing.

| Server sandbox option | Default | Bounds/step | Meaning |
| --- | ---: | --- | --- |
| ImprovisedTieWearResistance | 1 | integers 1–100 / 1 | one-in-N native condition-loss chance for all fourteen materials, old and new ties |
| ClothRetainerWearResistance | 2 | integers 1–100 / 1 | one-in-N native condition-loss chance for cloth retainers |
| LeatherRetainerWearResistance | 4 | integers 1–100 / 1 | one-in-N native condition-loss chance for leather retainers |

Larger N lasts longer; these are probabilities, not promised hit capacities.
Invalid/missing/non-finite/out-of-range values fall back to defaults server-side.
Settings apply on authoritative wear completion/reconciliation and do not refill
condition. The fixed 10-point scale preserves existing crafted-item native
condition/save representation; wear resistance configures lifetime without
unsynchronized per-instance ConditionMax changes. IDs, schema versions, slot
count and capacity checks are internal technical constraints, not balance knobs.
UnbreakableRetainer retains its unchanged no-coverage/no-wear definition.

Clothing.setCondition(0) marks the item broken and native Unwear(true) removes it
from worn equipment, emits OnClothingUpdated for an IsoPlayer on the server too,
and handles its ordinary broken-item drop. Protection then refreshes from the
actual remaining equipment. Native damage ordering applies: a weapon strike can
break a tie before its later fall roll; saving the glasses on every breaking blow
is NOT guaranteed by this approved alternative. No delayed repair or extra free
protection window is deliberately added.

## Direct Tie attachments

The original six materials and eight added in 0.14 are all finite. New ties
use material-specific native budgets; old ties retain ten points. Tie still consumes one use once and keeps the original glasses/hat,
condition, prescription, model and ID. It now creates one real improvised tie,
links it to that eyewear's native ID and equips it. Three registered slots
(Eyes, Face, Hat) let an eyewear tie and a supported hat tie coexist. Each slot
holds one tie; occupied slots and insufficient space refuse new tying. A 0.01
weight tie replaces the spent material use; it is a real player-visible item,
not a hidden damage sensor or debugger item. All reuse the existing cloth icon.

Target schema-1 tie data adds wearSchema=1 and tieId; the tie's own ModData key
B47ANCEDEyewearTie contains schema=1, targetId and material. Links contain IDs and
plain scalar metadata, never userdata, item snapshots or valuable reconstruction
recipes. Protection requires BOTH actual items in the character's main inventory
and worn together, plus matching reciprocal ID/material records and positive tie
condition. Transfer the eyewear AND its tie together. Taking off/dropping/trading
only one suspends the tie's protection; wearing both reactivates that same tie.
Unrelated proxy items, missing/corrupt links and missing material metadata grant
no tie protection. A worn reusable retainer may protect eyewear whose link is
inactive. Untie discards only the resolved owned matching tie; it refunds nothing.
Broken ties remain ordinary broken native items, never new material or retainers.

The server resolves only Tie/Untie intent and native inventory IDs. The client
cannot request condition loss, specify durability or claim a successful catch.
Allocation and field mutation happen before UseAndSync. Unpaid failures roll back
metadata, chance, name and the newly allocated tie. Once material consumption is
observed, its paid tie survives a notification exception. Replayed Tie commands
fail the existing tied-state check. Native AddItem/sendAddItemToContainer and
setWornItem/SyncClothing carry the actual item; no parallel item network exists.

## Existing saves and recovery

A worn valid paid legacy schema-1 tie with NEITHER wearSchema nor tieId receives
one finite native tie, without a second material charge. Legacy StayPutGlasses
state is first copied to the canonical key; its historical data is preserved.
Migration waits for a free slot and capacity. It never displaces existing gear.
A persisted newer wearSchema/tieId forbids recreation if its counterparty is
lost, transferred or malformed. Old unworn ties migrate only when equipped.
Schema-2 historical finite-retainer records remain inactive and read-only.
Existing crafted items keep their native condition and gain head wear through
the updated script definition. No real player save was opened or rewritten by
this task. Native save/restart acceptance remains a dedicated runtime gate.

The 0.9 published ZIP, checksum and provenance were preserved byte-for-byte under
ignored dist/historical/0.9.0-dev.1-published, with a preservation ledger. Reverting
the Workshop package alone is not a safe saved-world downgrade: older versions
lack the three new item types and ignore the new finite link contract. Keep a
world/player backup made before upgrade; no automatic downgrade is provided.

## Evidence and limits

[VERIFIED: installed source] BloodClothingType.addHole and setConditionAndSync;
Clothing.setCondition/Unwear; InventoryItem condition serialization; native
IsoGameCharacter.setWornItem (SyncClothing); vanilla shared ISWearClothing,
ISUnequipAction and sendAddItemToContainer/sendRemoveItemFromContainer usage.
IsoGameCharacter.class SHA-256 remains
29040e19c3e420499f73bc0ea0d5b86d7f7d38655acdc13d0107df736eb54c0b.
Official method/access reference:
https://projectzomboid.com/modding/zombie/characters/IsoGameCharacter.html.

The same source audit confirms helmetFallFromWornItems has no callback between
its RNG success and removal. Hook.WeaponHitCharacter can cancel the whole weapon
hit, not just clothing removal. OnBeingHitByZombie is registered but has no
native caller in this installed JAR; it is not used as an invented damage hook.

[RUNTIME GATE] SP/dedicated head damage, layering, native condition replication,
last-condition-point ordering, paid migration, simultaneous gear changes, both-
item transfers, loss recovery, save/restart, join/rejoin and UI/controller behavior
need actual validation. Offline Lua/structural checks cannot prove these. G7
BLOCKED / NOT TESTED; stable G8 BLOCKED. Deployment/publication requires an explicit request;
distribution evidence does not establish runtime acceptance.
