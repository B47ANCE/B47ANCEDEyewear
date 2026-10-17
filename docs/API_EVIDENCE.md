# Lua API evidence

Project Version: 0.15.0-dev.1

## Crafted-retainer tape — 0.15

Crafted cloth/leather retainers now accept ONE tape in their main-inventory
right-click menu, worn or unworn. Default native wear-resistance bonus is +1 for
adhesive/+2 for duct tape. Condition, maximum, identity and worn mapping stay
unchanged; no recraft is required. Server intent validation, observed-payment
rollback boundaries, persistence, settings and runtime gates are detailed in
CRAFTED_RETAINER_TAPE.md. Unbreakable retainers are excluded. This is source-only;
current G7 NOT TESTED / BLOCKED and stable G8 BLOCKED.


## Current 0.14 materials and reinforcement

Fourteen audited materials, same-material strands, adhesive/duct tape, material-
specific installed native condition and zip-tie cutting are implemented in Lua.
See TIE_REINFORCEMENT.md for balance, ownership/payment/replay checks, new item
identity, existing-save policy and current runtime gates. G7 for THIS gameplay
iteration is BLOCKED / NOT TESTED; earlier published acceptance remains historical.

[VERIFIED: source, 2026-10-16] Installed Steam app108600 build 25485521, Core.class
SHA-256 8f5c69740c8bf2181123a831ab68d1dfb047453687cca6dc62c77816d76ab360,
InventoryItem.class 48f01be16d1ef1b76e37638fac6e25ca4eb285ad38ab2f462caa5597318c7f9d
remain unchanged. All sixteen material/tape FullTypes were freshly read from
installed generated items. RippedSheets, DenimStrips and LeatherStrips have dirty
ReplaceOnUse variants; whole-item native Remove/sendRemoveItemFromContainer avoids
byproducts. Drainable inputs consume one UseAndSync script use. CraftRecipeData's
kept ItemCount path passes forced use plus keep to ItemUser, preventing replacements
and duplicate consumption after the Lua transaction.

InventoryItem.setConditionNoSound(int), hasSharpness(), isDull(), hasHeadCondition()
and getHeadCondition() are public and not HiddenFromLua. LuaManager.Exposer
registers InventoryItem and LuaJavaClassExposer exposes its public non-hidden
members. This establishes source exposure, not runtime invocation. Exposer.class
SHA-256 9727656efbc06d7772661775f7a6885c7976b9e09472d7b128a3d5638ea68efa;
LuaJavaClassExposer.class 4c8dc24c94de2cb814741f135d7d9baf8bc09062dd821d3c56cc4b09f322c0bd.
InputScript.doesItemPassSharpnessStatusTests implements the native IsNotDull rule
hasSharpness && isDull => reject. Additional positive tool general/head condition
and vanilla sharpknife/scissors tags are validated on server-owned instances.
InputScript.class SHA-256 4af3459b2358f5363825f6eb1efc8edfac6833779bb26011efa326050b913e9c.

syncItemFields(IsoPlayer,InventoryItem) in GlobalObject routes server packets to
the owning player; SyncItemFieldsPacket writes and applies actual condition. Its
class SHA-256 is 957430c8397cf76728fe376435d70db84f756aa897d2e753f971e396cb1c1a5c.
Native item ModData/condition serialization, inventory transfers and SyncClothing
carry their established data. No all-peer or late-join acceptance is inferred
from an owner notification. Packet arrival/order/rejoin still require dedicated
runtime evidence. InventoryItem saves omit full condition; dynamic conditionMax
is not established as serialized/synchronized. New fixed-max item types therefore
preserve old script maxima and never convert full old saves to a larger default.
Source inspection: 2026-10-14. Target Build 42.21.

Current patch audit (2026-10-15): CLOTHING_SYNC_FIX.md records the missing native
file GUID table cause, original installed class fingerprints, verified vanilla
getVisual call form, unready-asset rejection and remaining dedicated gate. Older
milestones below retain their observed versions and evidence.

The installed Steam app108600 build 25485521 uses the original JAR Core.class hash
8f5c69740c8bf2181123a831ab68d1dfb047453687cca6dc62c77816d76ab360,
matching the prior42.21 audit. InventoryItem.class hash:
48f01be16d1ef1b76e37638fac6e25ca4eb285ad38ab2f462caa5597318c7f9d.
This is binary/source provenance, not actual game execution.

[VERIFIED: source] Installed shared/TimedActions/ISBaseTimedAction.lua defines
perform() and delegates client queue completion through ISTimedActionQueue.
Installed shared/Entity/TimedActions/ISHandcraftAction.lua calls luaCallOnCreate
then processDestroyAndUsedItems. Server complete() invokes performRecipe(); client
perform() does not, while SP perform() does. No-output modification recipes are
present in installed scripts/generated/recipes/recipes_gasmasks.txt. Those recipes
use OnTest, OnCreate, kept inputs and AllowBatchCraft=false.

[VERIFIED: source] Original-JAR CraftRecipe.OnTestItem calls the Lua hook with
(item, character) and interprets its boolean result. CraftRecipeData.luaCallOnCreate
passes (recipeData, character). getAllInputItems includes both kept selections;
ISHandcraftAction.lua:108–125 explicitly documents manual input population.
CraftRecipeManager matches inputs using OnTest before built-in item flags.
Characterless preview calls exist in deprecated ISCraftInputItems.lua:43, so the
adapter allows structural preview checks while completion revalidates ownership.
InputFlag.IsWorn checks native worn state. ItemCount selects one physical input.

[VERIFIED: source] CraftRecipeData.processDestroyAndUsedItems passes isKeep to
ItemUser.UseItem; the keep path skips current-use decrement. The recipe keeps both
inputs and lets S.tie perform the single payment. The six selected material
definitions have no replacement-on-use/depletion, and ItemUser.RemoveItem safely
handles an already removed material after its last use. All 41 Base eyewear/hat
types and six materials exist in installed generated item scripts. Optional mod
types are omitted from the crafting definition to avoid unresolved dependencies.
ISCraftRecipeInfoBox.lua:104–105 translates Tooltip through ordinary getText;
Recipes.json uses bare recipe names. Installed getDuration multiplies recipe time
by five. These are source conclusions, not executed crafting evidence.

[VERIFIED: source] InventoryItem's exposed inventory/container, name/custom-name,
ModData, ID, current-use and UseAndSync interfaces support the retained context-menu
path. UseAndSync may consume before a synchronization exception; consumption must
be observed before retaining a paid tie. Existing syncItemModData/syncItemFields
remain vanilla synchronization, not a replacement networking implementation.

The inventory tooltip delegates to item:DoTooltip. The companion renderer chains
ISToolTipInv.render without replacing its vanilla measurement/drawing logic.

[VERIFIED: source, rechecked 2026-10-14] Original-JAR ModRegistries.init loads
<version-dir>/media/registries.lua (common fallback) through LuaManager.RunLua.
Both GameWindow and dedicated GameServer call ModRegistries.init before
ScriptManager.Load, so the custom location exists before item definitions resolve.
ItemBodyLocation exposes get(ResourceLocation) and register(String); the custom
namespace is accepted by RegistryReset.createLocation. BodyLocationGroup accepts
the resulting registered object in getOrCreateLocation. Installed NPCs/BodyLocations
uses this API, and ISWearClothing.complete / ISUnequipAction.complete mutate the
actual worn item on authoritative completion. Existing emptytexture clothing XML
(e.g. AthleticCup.xml) supplies a no-model convention. ItemName.json uses bare
FullType keys; custom slot labels use UI_ClothingType_ plus translation name.
InventoryItem.getEquipParent supports read-only tooltip selection.

The installed IsoGameCharacter.class SHA-256 is still
29040e19c3e420499f73bc0ea0d5b86d7f7d38655acdc13d0107df736eb54c0b,
byte-identical to the privately retained, previously audited native method.
helmetFallFromWornItems performs native RNG and immediate inventory/worn removal
and falling-item creation with no intervening Lua callback. Public helmetFall
emits OnClothingUpdated only afterward for a local player. OnPlayerGetDamage is
not evidence of that native successful roll. Exact -1-per-knock-off durability
remains BLOCKED in Lua under the current exposed API; no approximation is enabled.

[UNKNOWN / RUNTIME GATE] Actual MP timed-action acknowledgement, command arrival,
derived ChanceToFall ownership/synchronization, save/reconnect behavior, material
consumption recovery and tooltip UI scales/controllers remain untested. G7 remains
BLOCKED / NOT TESTED and stable G8 BLOCKED. No custom Java runtime is used.


[VERIFIED: source, 0.9.0-dev.1] ItemPickerJava.fillContainerInternal returns on
GameClient.client and emits OnFillContainer with room name, actual container type
and actual ItemContainer after native fill. The server hook reads current sandbox
values then; it does not use OnPreDistributionMerge (which occurs before a later
SandboxOptions.load in IsoWorld). Installed Distributions/KeyNamer/legacy aliases
verify school lockers, optical stores and pharmacy containers. ItemContainer's
hasRoomFor(character,float), AddItem(String), and script Item.getActualWeight are
available. The extra rare loot roll is server/SP-owned and changes no client state
or vanilla distribution table. Native container serialization persists the item.

[VERIFIED: source] Native BloodClothingType.addHole and
IsoGameCharacter.addHoleFromZombieAttacks select damage layers from BloodLocation
coverage. The unbreakable item defines none, disallows holes, is cosmetic and has
zero fall chance; Clothing.update has no condition decrement. No condition-restoring
timer or hit callback is used. Actual native wear/damage remains a runtime gate.

[VERIFIED: installed source, 0.10.0-dev.1] BloodClothingType.addHole's no-hole
clothing branch applies Rand.NextBool(ConditionLowerChance) and subtracts exactly
one native condition point. Its private setConditionAndSync returns on clients
and calls Clothing.setCondition plus GameServer.sendItemStats on server/SP.
Clothing.setCondition(0) uses native Unwear(true); Unwear emits OnClothingUpdated
for any IsoPlayer, including a dedicated remote player. This differs from the
local-player-only event after helmetFall. Native equipment removal and condition
synchronization provide a safe authority path for the user-approved head/clothing
wear alternative, not an exposed successful knock-off callback.

InventoryItem's existing conditionMax scale is 10; condition is serialized as a
byte, while dynamic per-instance maxima are not established as synchronized. The
feature keeps that scale and configures Clothing.setConditionLowerChance on the
server. Native setWornItem sends SyncClothing, and installed shared timed actions
verify AddItem/sendAddItemToContainer and Remove/sendRemoveItemFromContainer.
Actual items and scalar reciprocal IDs persist through vanilla serialization.
Hook.WeaponHitCharacter can cancel the entire weapon hit, not one clothing drop;
OnBeingHitByZombie has only its event registration string in this installed JAR,
so it is not adopted as an invented server notification. See DURABILITY.md.

[INFERRED / RUNTIME GATE] Native layering/order and synchronized item-ID links
should preserve finite protection through ordinary equipment and save flows,
but dedicated transfer/reconnect/restart and actual combat acceptance are not
proven by source/bytecode inspection or Lua doubles. G7/stable G8 stay blocked.

[VERIFIED: source] ZombieHitPlayerPacket.process delegates to Bite.process, whose
GameServer.server branch calls BodyDamage.AddRandomDamageFromZombie. Its head
clothing-damage paths call addHoleFromZombieAttacks, reaching the authoritative
condition helper above. Both script Item and InventoryItem constructors default
conditionMax to 10, confirming unchanged crafted-item condition resolution.

## Ground presentation (0.11 source addition)

[VERIFIED: source] Installed Build 42.21 generated item/model definitions and
ItemModelRenderer.hasModel/init support WorldStaticModel -> qualified model
script -> static FBX mesh/texture. See GROUND_MODELS.md for exact installed
paths and acceptance limits. Blender 4.5.7 LTS roundtrip verifies export
structure and dimensions only; PZ import/display remains NOT TESTED.
No Lua gameplay, authority, persistence or synchronization paths changed.

## Worn retainer source addition

0.12.0-dev.1 adds original head-attached static clothing meshes through the
existing native worn slot, three new XML definitions and six male/female files.
See WORN_MODELS.md for installed 42.21 source evidence, authoring provenance,
authority/configuration assessment and remaining fit/MP gates. Existing items
resolve current clothing definitions through native ItemVisual.getClothingItem.
No Lua gameplay, persistence, IDs or custom synchronization changed. No package,
deployment, publication or PZ/server launch is part of this source iteration.
Published 0.11.1 ZIP/checksum/provenance were preserved unchanged with hashes,
a preservation ledger and a read-only ZIP CRC check. No artifacts were deleted.

## Improvised-tie worn presentation source addition

0.13.0-dev.1 uses the existing native head-attachment route for the three existing
improvised tie item types. Separate Eyes/Face/Hat XMLs and six original body-
specific meshes share the original cloth atlas for all six materials. Source
inspection confirms the slots, linked-item authority and native SyncClothing
already exist; all gameplay Lua remains unchanged. See IMPROVISED_TIE_MODELS.md
for current installed 42.21 evidence, asset provenance, configuration assessment,
independent import checks and explicit runtime gates. No client-owned gameplay,
new state, item types, schema or networking was introduced. Current iteration is
source only; no packaging, deployment, upload or game/server launch. Published
0.12.0 ZIP/checksum/provenance were preserved with matching hashes, a bounded
preservation ledger and ZIP CRC. No artifact deletion occurred.

[VERIFIED: source reuse, 0.15] Crafted tape reuses the previously inspected
Clothing.get/setConditionLowerChance, InventoryItem ModData/ID/condition and
syncItemModData/syncItemFields routes, plus exact whole-item Remove/sendRemove and
drainable UseAndSync payment. No new native methods/events, condition maxima,
serialized userdata or model bindings are introduced. Public Lua exposure/build
fingerprints remain those documented for installed 42.21 / Steam 25485521. Actual
packet arrival, native wear, persistence/rejoin/restart remain NOT TESTED.
