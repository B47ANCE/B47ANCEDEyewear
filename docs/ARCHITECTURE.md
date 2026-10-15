# Architecture

The authoritative Lua runtime is src/B47ANCEDEyewear/42. Core.lua owns schema-1
legacy tie state; Retention.lua provides the item profiles and validated server
sandbox interpretation. Clients send Tie/Untie intent with native inventory IDs.
Server.lua resolves items only in the sender's inventory and rechecks ownership,
worn state, usable material, current tie state and sandbox eligibility. SP actions
commit locally; MP timed-action completion does not also commit through a second channel.

Crafting.lua connects the vanilla TieGlasses CraftRecipe to the same transaction.
Vanilla OnTest(item, character) filters inputs; characterless UI previews use
item-only eligibility, while actual crafting requires worn headwear and material
in the player's main inventory. Input flags enforce worn/usable items and permit
favorites. Both inputs use mode:keep, so vanilla never charges a second material
use. OnCreate(recipeData, character) takes only the two selected input instances,
rejects ambiguous inputs and calls S.tie on the server/SP side. It sends no custom
client command and creates no output item. Completion rechecks current state and
server sandbox configuration. Invalidated work consumes nothing. Batch crafting
is disabled; recipe time 16 matches the existing action duration 80 after vanilla's
fivefold conversion. Recipe identifiers list installed Base types only; optional
modded eyewear retains context-menu support without a recipe dependency.

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
Finite-retainer transactions and all custom Java paths remain retired.

WearableRetainers.lua selects one actual worn item in the dedicated registered
b47ancedeyewear:retainer slot. ModRegistries loads media/registries.lua before item
scripts; shared initialization extends the vanilla Human body-location group.
Both clothing types use the original inventory icon and an empty-texture clothing
asset, with no fitted mesh. They occupy no existing eyewear or necklace slot.
Native item ownership, worn mappings, crafting and persistence remain vanilla.
There is no item escrow, saved userdata, generated replacement or schema migration.

The first compatible untied pair in worn-slot order receives the server-configured
retained fall value. Unequipping, disabling, breaking or transferring the retainer
restores the ordinary profile on the next authoritative refresh. WearableActions.lua
chains vanilla Wear/Take Off complete() and preserves its return value, then refreshes
on server/SP. A dedicated OnTick fallback runs every 30 ticks for connected players;
it scans worn slots only, uses direct container ownership, and never traverses world
or inventory contents. OnPlayerUpdate remains presentation/reconciliation coverage.
Changed fields reuse vanilla synchronization; no catch/damage client command exists.
The two ordinary output recipes let vanilla validate, consume inputs and create one
retainer. Needles/scissors are kept; material use is not repeated in Lua callbacks.

Sandbox defaults: TyingEnabled=true, EyewearFallMultiplier=1 (0.25–5),
StrappedHeadwearFallChance=0 (0–100). Server configuration is shared gameplay authority.
Changes to the multiplier/headwear value apply when worn items refresh; existing
ties remain zero-fall and can be untied even when new tying is disabled. Old unused
retainer sandbox fields have no effect. Schema IDs, inventory-ID bounds, tooltip
padding and the presentation condition thresholds remain internal technical constants.

[VERIFIED: source] Vanilla synchronization and inventory APIs are reused.
[RUNTIME GATE] Dedicated authority, timing, replication, join/reconnect, saves/restarts,
consumption error recovery and actual UI behavior remain untested. G7/G8 are blocked.
