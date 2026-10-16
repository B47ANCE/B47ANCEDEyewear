# Rare unbreakable retainer

Project Version: 0.14.0-dev.1
Source audit: 2026-10-14; installed Project Zomboid 42.21 / Steam build 25485521.

## Item and artwork

B47ANCEDEyewear.UnbreakableRetainer is a separate, loot-only Unbreakable Eyewear
Retainer. No recipe produces it. The two existing crafted items remain distinct.
It uses the original black adjustable-cord icon unchanged; the original mesh and
model texture now also supply its static ground asset. A distinct male/female head-attached worn mesh is now included; actual fit is untested.
Crafted cloth and leather items now have separate original generated icons.

The item uses the existing retainer equipment slot and actual vanilla item
identity. Wear/Take Off, transfer and persistence retain that same object. The
server-controlled wearable enable/fall settings apply. One compatible untied,
unbroken, non-monocle pair is protected; hats retain the Tie/Untie flow.

Its native item definition is cosmetic, CanHaveHoles=false, RemoveOnBroken=false,
ChanceToFall=0 and has no BloodLocation/armor coverage. Native clothing damage
selects covered body parts; the uncovered retainer is not a damage layer. Native
Clothing.update does not decrement its condition. No wear/catch durability code
or automatic repair/condition-restoration timer is installed. This is unbreakable
in ordinary retainer use, rather than a large finite counter. Deliberate item
destruction/world cleanup or administrator edits are outside that durability claim.
This does not resolve the separate finite-retainer knock-off callback limitation.

## Loot ownership and configuration

RareRetainerLoot.lua runs in server Lua and guards isClient(). Vanilla's
OnFillContainer(roomName, containerType, itemContainer) invokes it synchronously
after native contents are generated. It adds at most one new actual item, only
if the eligible container has room and does not already contain this retainer.
It never overwrites loot tables, traverses nested inventories/world cells or
handles a custom client spawn request. Native container persistence/synchronization
owns the result. Opening an already populated container does not perform a new
mod roll; legitimate later native fill/respawn events can roll again.

| Room type | Eligible containers | Installed evidence |
| --- | --- | --- |
| elementaryschool, secondaryhall | locker | Distributions.lua: SchoolLockers / SchoolLockersBad |
| glassesstore | counter, displaycase, desk, other | Distributions.lua explicitly labels this room for optometrists |
| optometrist, opthroom | counter, displaycase, desk, other | Vanilla KeyNamer optometrist room and SuburbsDistributions legacy opthroom alias |
| pharmacy | counter, shelves | Distributions.lua includes PharmacyGlasses on pharmacy shelves |

RareRetainerLootChance is a percentage per eligible native fill with room for the
item: default 0.25%, bounds 0–5%, precision 0.01%. A server/SP ZombRand(10000) call is
compared with the rounded percentage in basis points. Zero disables new spawns;
disabling wearable retainers also prevents them. Existing items are preserved.
This explicit additional chance is independent of weighted vanilla loot rarity.
Changing it affects future eligible fills, including unexplored containers in
existing saves, and does not populate or reroll already filled containers.

The callback reads current authoritative SandboxVars at fill time. It does not
depend on initialization-time distribution weights: installed IsoWorld invokes
OnPreDistributionMerge before a later SandboxOptions.load/ItemPickerJava.Parse.
The installed fillContainerInternal exits for GameClient.client and passes the
actual container to OnFillContainer. ItemContainer.hasRoomFor(character,float),
ScriptManager.FindItem, Item.getActualWeight and ItemContainer.AddItem(String)
are exposed native interfaces verified in the installed game.

## Validation

[VERIFIED: source] Room/container definitions, event timing, input signatures,
native no-coverage damage selection and original icon SHA-256 were checked.
[TESTED: offline] Production preflight compiles Lua, validates metadata/assets,
and refuses a crafting output for the loot-only FullType. Generated master PNGs
have real alpha; runtime icons are 64x64 RGBA with transparent borders. High-resolution
masters, prompts, export details and hashes are retained in assets/retainers.

[RUNTIME GATE] Actual rare appearances, capacity behavior, network replication,
dedicated joins/rejoins, transfers, saves/restarts and wear/damage behavior remain
NOT TESTED. No game/server, package, deployment or upload was run for this iteration.
G7 BLOCKED / NOT TESTED; stable G8 BLOCKED.

## Ground presentation

All three retainer items now bind distinct static FBX/texture pairs through
WorldStaticModel. See GROUND_MODELS.md for authoring, exact native evidence and
offline validation. Ground assets and gameplay properties remain unchanged.
Worn presentation is added separately; see WORN_MODELS.md.
PZ import, placement, scale and lighting remain NOT TESTED.
