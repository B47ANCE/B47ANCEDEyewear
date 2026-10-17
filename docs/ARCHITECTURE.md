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
client command. The paid Tie transaction now creates one linked native tie item;
vanilla crafting does not also produce it. Completion rechecks current state and
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
Historical finite-catch transactions and all custom Java paths remain retired.
Current native condition wear and reciprocal item links are described in DURABILITY.md.

WearableRetainers.lua selects one actual worn item in the dedicated registered
b47ancedeyewear:retainer slot. ModRegistries loads media/registries.lua before item
scripts; shared initialization extends the vanilla Human body-location group.
Crafted items use distinct cloth/leather icons; the rare item uses the original
black icon. All use the empty-texture clothing asset, with no fitted mesh. They occupy no existing eyewear or necklace slot.
Native item ownership, worn mappings, crafting and persistence remain vanilla.
There is no item escrow, saved userdata or reconstructed eyewear. Direct ties now
add a linked native clothing item and an additive schema-1 migration; see below.

The first compatible pair without an active improvised tie in worn-slot order receives the server-configured
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


RareRetainerLoot.lua is a server-only native OnFillContainer listener, with an
explicit client guard and no custom networking/loot command. Exact room/container
allowlists bound its work to school lockers, optical-store containers and pharmacy
counter/shelves. It reads validated server sandbox settings at fill time, checks
space using the script item's actual weight, scans only that container for an
existing rare item and makes one percentage roll. Native AddItem creates a single
actual UnbreakableRetainer; normal world-container synchronization/persistence owns
it. No user save or distribution table is rewritten and no filled container is
retrofitted. Native fills/respawns may roll again, without duplicating an item
already present. RareRetainerLootChance is 0–5%, default 0.25%, precision 0.01%; zero
or disabled wearable retainers prevents new spawns. Existing items remain valid.

The rare item has no craft output and uses the original black cord inventory icon;
cloth and leather craft outputs have distinct icon exports. Native cosmetic,
no-hole and no-body-coverage properties avoid normal damage/condition loss. Its
unbreakability is not implemented with infinite numeric durability, repair loops
or prohibited catch interception. The separate finite-catch hook remains blocked.

## Native head/clothing durability — 0.10

TieDurability.lua creates one actual finite clothing item per paid Tie and validates
reciprocal target/tie native IDs, material, main-inventory ownership and worn state.
Eyes, Face and Hat slots permit supported concurrent ties without replacing gear.
Allocation and target changes roll back before material consumption; once a use
is observed consumed, notification failure does not grant a refund or duplicate.
Untie discards only the owned matching item. Trading one half suspends protection;
trading/wearing both preserves the same condition. Missing newer items never
trigger reconstruction. Existing paid legacy ties get a one-time finite item only
when worn with available space/slot; the legacy record itself stays preserved.

All finite tie/retainer definitions use native Head coverage, cosmetic/no-hole
properties and 10 condition points. Native BloodClothingType removes condition
only server/SP and sends ordinary item stats. Vanilla break/Unwear handles worn
removal, including a server OnClothingUpdated event for players. Core uses an
active link for protection and a stable worn snapshot during legacy migration.
Three server sandbox resistance denominators (defaults 1/2/4, integer 1–100)
configure lifetime without refilling condition or changing per-instance maxima.
Fixed condition scale preserves the existing native representation; IDs/schema,
slot mappings and capacity constraints are implementation details. The rare
retainer's no-coverage/no-wear definition is unchanged. No custom damage packet,
hit polling, health heuristic, native method override or Lua combat roll is used.

Native layering/damage order applies; this accepted alternative does not promise
to save eyewear on every breaking blow. Exact hidden-roll interception remains
unavailable. Tooltips show actual native condition, not guessed catches left.
See DURABILITY.md for persistence, downgrade limits and dedicated acceptance gates.

## Current 0.14 materials and reinforcement

Fourteen audited materials, same-material strands, adhesive/duct tape, material-
specific installed native condition and zip-tie cutting are implemented in Lua.
See TIE_REINFORCEMENT.md for balance, ownership/payment/replay checks, new item
identity, existing-save policy and current runtime gates. G7 for THIS gameplay
iteration is BLOCKED / NOT TESTED; earlier published acceptance remains historical.

New direct Tie allocates LayeredTieEyes/Face/Hat. Legacy pre-link migration still
allocates the original ten-point types. TieMaterials.lua centralizes verified
materials, installation contribution snapshots, exact whole-item payment and
cutting-tool checks. Core validates state snapshots for all command actions and
implements paid reinforcement with rollback only before observed consumption.
TieDurability.state validates installed scalar metadata and native condition.
No dynamic ConditionMax, damage packet or client-owned gameplay counter exists.
The prior "all finite definitions ten points" milestone above describes the
retained old definitions. Current reusable retainers still have ten points.

## Crafted-retainer tape — 0.15

Crafted cloth/leather retainers now accept ONE tape in their main-inventory
right-click menu, worn or unworn. Default native wear-resistance bonus is +1 for
adhesive/+2 for duct tape. Condition, maximum, identity and worn mapping stay
unchanged; no recraft is required. Server intent validation, observed-payment
rollback boundaries, persistence, settings and runtime gates are detailed in
CRAFTED_RETAINER_TAPE.md. Unbreakable retainers are excluded. This is source-only;
current G7 NOT TESTED / BLOCKED and stable G8 BLOCKED.

RetainerTape uses the existing actual item, with one scalar ModData record and
native wear resistance. Core.snapshot recognizes crafted-item tape revision;
Server resolves IDs and calls WearableRetainers.applyTape. The shared timed action
allows main-inventory unworn targets only for this operation. Native damage and
vanilla condition remain authoritative; no new condition counter or item type.
