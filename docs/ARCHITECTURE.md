# Architecture

The authoritative Lua runtime is src/B47ANCEDEyewear/42. Core.lua owns schema-1
legacy tie state; Retention.lua provides the item profiles and validated server
sandbox interpretation. Clients send Tie/Untie intent with native inventory IDs.
Server.lua resolves items only in the sender's inventory and rechecks ownership,
worn state, usable material, current tie state and sandbox eligibility. SP actions
commit locally; MP timed-action completion does not also commit through a second channel.

A context-menu tie snapshots the original name/custom-name, fall value and prior
metadata, mutates the same item, then invokes one vanilla UseAndSync. A failure
before consumption restores the snapshot. An exception after consumption retains
the paid tie; item synchronization is a separate notification and logs failures.
Untying restores the original name and derives the current untied fall value.
No inventory item is reconstructed, no material is refunded and no save is deleted.
Legacy StayPutGlasses records migrate by copy and remain preserved. Malformed data
is not treated as a valid tie. No real player saves are used by preparation tooling.

RetainerState.lua is a read-only schema-2 compatibility reader. The tooltip shows
stored historical values as inactive, or displays material/secured status for an
actual legacy tie. It never changes gameplay state or initiates network actions.
Unavailable finite-retainer transactions and all custom Java paths have been retired.

Sandbox defaults: TyingEnabled=true, EyewearFallMultiplier=1 (0.25–5),
StrappedHeadwearFallChance=0 (0–100). Server configuration is shared gameplay authority.
Changes to the multiplier/headwear value apply when worn items refresh; existing
ties remain zero-fall and can be untied even when new tying is disabled. Old unused
retainer sandbox fields have no effect. Schema IDs, inventory-ID bounds, tooltip
padding and the presentation condition thresholds remain internal technical constants.

[VERIFIED: source] Vanilla synchronization and inventory APIs are reused.
[RUNTIME GATE] Dedicated authority, timing, replication, join/reconnect, saves/restarts,
consumption error recovery and actual UI behavior remain untested. G7/G8 are blocked.
