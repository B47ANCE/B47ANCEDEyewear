# Lua API evidence

Project Version: 0.11.0-dev.1
Source inspection: 2026-10-14. Target Build 42.21.

The installed Steam app108600 build25485521 uses the original JAR Core.class hash
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
