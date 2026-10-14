# Lua API evidence

Project Version: 0.7.0-dev.1
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

[UNKNOWN / RUNTIME GATE] Actual MP timed-action acknowledgement, command arrival,
derived ChanceToFall ownership/synchronization, save/reconnect behavior, material
consumption recovery and tooltip UI scales/controllers remain untested. G7 remains
BLOCKED / NOT TESTED and stable G8 BLOCKED. No custom Java runtime is used.
